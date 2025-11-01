from .base_agent import BaseAgent
from typing import Dict, Any
import json
from config import settings


class CriticAgent(BaseAgent):
    """Agent 3: Critically evaluates analysis and provides feedback."""

    def __init__(self):
        system_prompt = """You are a critical content strategist and senior marketer with expertise in LinkedIn engagement.

Your task is to critically evaluate the product analysis and provide constructive feedback.

EVALUATION CRITERIA:

1. CLARITY OF VALUE PROPOSITION
   - Is the value clear and compelling?
   - Would it resonate with the target audience?
   - Any gaps or confusing points?

2. CONTENT ANGLE STRENGTH
   - Are the proposed angles engaging?
   - Do they leverage LinkedIn best practices?
   - Are they differentiated from competitors?

3. AUTHENTICITY & CREDIBILITY
   - Can these angles be supported with real stories/data?
   - Are they authentic or too salesy?
   - Will they build trust?

4. VIRAL POTENTIAL
   - Which angles have highest engagement potential?
   - What's missing for viral content?
   - Any controversial/bold opinions to add?

CRITICAL ASSESSMENT:
Identify specific issues using these trigger keywords when major problems exist:
- "needs_refinement" - unclear or weak positioning
- "unclear_value_prop" - value proposition isn't compelling
- "iterate" - analysis needs another pass
- "needs_improvement" - specific aspects need work
- "weak_positioning" - market positioning unclear

Return your critique as a valid JSON object:
{
    "overall_assessment": "...",
    "strengths": [
        "Strength 1...",
        "Strength 2..."
    ],
    "weaknesses": [
        "Weakness 1...",
        "Weakness 2..."
    ],
    "specific_feedback": {
        "value_proposition": "...",
        "content_angles": "...",
        "target_audience": "...",
        "differentiation": "..."
    },
    "recommendations": [
        "Recommendation 1...",
        "Recommendation 2..."
    ],
    "trigger_keywords": ["needs_refinement", "..."],
    "should_iterate": false,
    "confidence_score": 8,
    "ready_for_content": true
}

Be brutally honest but constructive. Your feedback will improve the final content."""

        super().__init__("CriticAgent", system_prompt)

    def check_for_loop_triggers(self, critique: Dict[str, Any]) -> bool:
        """Check if critique contains keywords that trigger a loop."""
        trigger_keywords = critique.get("trigger_keywords", [])
        should_iterate = critique.get("should_iterate", False)

        # Check if any trigger keywords match our configured keywords
        has_triggers = any(
            keyword in settings.loop_keywords
            for keyword in trigger_keywords
        )

        return has_triggers or should_iterate

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Critically evaluate the analysis.

        Input: {"analysis": {...}, "extracted_data": {...}, "iteration": 1}
        Output: {"critique": {...}, "should_loop": bool, "analysis": {...}, ...}
        """
        analysis = input_data.get("analysis")
        extracted_data = input_data.get("extracted_data")
        iteration = input_data.get("iteration", 1)

        if not analysis:
            raise ValueError("analysis is required")

        self.log(f"Critiquing analysis (iteration {iteration})...")

        # Prepare critique prompt
        prompt = f"""Critically evaluate the following product analysis:

PRODUCT: {extracted_data.get('title', 'Unknown')}

ANALYSIS:
{json.dumps(analysis, indent=2)}

ITERATION: {iteration} of {settings.max_loop_iterations}

Provide a thorough critique as specified in your system prompt.

{"NOTE: This is iteration " + str(iteration) + ". Be extra critical if issues persist from previous iterations." if iteration > 1 else ""}
"""

        response = self.call_gpt(prompt, response_format="json_object")

        # Parse JSON response
        try:
            critique = json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse critique response as JSON")

        # Check if we should loop
        should_loop = self.check_for_loop_triggers(critique)

        # Don't loop if we've hit max iterations
        if iteration >= settings.max_loop_iterations:
            should_loop = False
            self.log(f"Max iterations ({settings.max_loop_iterations}) reached. Proceeding to post generation.")

        if should_loop:
            self.log(f"⚠️  Critique triggered loop. Keywords found: {critique.get('trigger_keywords', [])}")
        else:
            self.log(f"✓ Analysis approved. Confidence: {critique.get('confidence_score', 'N/A')}/10")

        return {
            "critique": critique,
            "should_loop": should_loop,
            "analysis": analysis,
            "extracted_data": extracted_data,
            "iteration": iteration,
            "url": input_data.get("url")
        }
