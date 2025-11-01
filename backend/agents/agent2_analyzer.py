from .base_agent import BaseAgent
from typing import Dict, Any
import json


class IdeaAnalyzerAgent(BaseAgent):
    """Agent 2: Performs deep analysis of the product/idea."""

    def __init__(self):
        system_prompt = """You are a senior product strategist and market analyst specializing in SaaS and web applications.

Your task is to perform a comprehensive analysis of a product/idea for LinkedIn marketing purposes.

Analyze the following dimensions:

1. MARKET ANALYSIS
   - Market size and opportunity
   - Competition landscape
   - Market positioning
   - Market Score (0-10)

2. UNIQUENESS & DIFFERENTIATION
   - What makes this unique?
   - Key differentiators
   - Competitive advantages
   - Uniqueness Score (0-10)

3. TARGET PERSONA
   - Detailed buyer persona
   - Job titles and roles
   - Pain points and motivations
   - Decision-making factors

4. LINKEDIN CONTENT ANGLES
   - What angles would resonate on LinkedIn?
   - Story hooks (personal, data-driven, problem/solution)
   - Emotional triggers
   - Value propositions to emphasize

5. ENGAGEMENT POTENTIAL
   - Topics that would spark discussion
   - Controversial/bold opinions to share
   - Storytelling opportunities
   - Call-to-action ideas

Return your analysis as a valid JSON object:
{
    "market_analysis": {
        "market_size": "...",
        "competition": "...",
        "positioning": "...",
        "market_score": 8
    },
    "uniqueness": {
        "differentiators": ["...", "..."],
        "competitive_advantages": ["...", "..."],
        "uniqueness_score": 7
    },
    "target_persona": {
        "titles": ["...", "..."],
        "pain_points": ["...", "..."],
        "motivations": ["...", "..."]
    },
    "content_angles": [
        {
            "angle": "...",
            "hook_type": "personal_story|data_driven|problem_solution",
            "emotional_trigger": "...",
            "value_emphasis": "..."
        }
    ],
    "engagement_opportunities": {
        "discussion_topics": ["...", "..."],
        "bold_opinions": ["...", "..."],
        "story_hooks": ["...", "..."]
    }
}

Be strategic and think from a LinkedIn content marketing perspective."""

        super().__init__("IdeaAnalyzerAgent", system_prompt)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the extracted product/idea data.

        Input: {"extracted_data": {...}, "url": "...", ...}
        Output: {"analysis": {...}, "extracted_data": {...}}
        """
        extracted_data = input_data.get("extracted_data")
        if not extracted_data:
            raise ValueError("extracted_data is required")

        self.log(f"Analyzing: {extracted_data.get('title', 'Unknown Product')}")

        # Prepare analysis prompt
        prompt = f"""Analyze the following product/idea for LinkedIn content marketing:

PRODUCT INFORMATION:
Title: {extracted_data.get('title')}
Description: {extracted_data.get('description')}
Features: {json.dumps(extracted_data.get('features', []), indent=2)}
Target Audience: {extracted_data.get('target_audience')}
Value Proposition: {extracted_data.get('value_proposition')}
Category: {extracted_data.get('category')}
Pain Points Addressed: {json.dumps(extracted_data.get('pain_points', []), indent=2)}

Provide a comprehensive strategic analysis as specified in your system prompt."""

        response = self.call_gpt(prompt, response_format="json_object")

        # Parse JSON response
        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse analysis response as JSON")

        self.log("Analysis complete")

        return {
            "analysis": analysis,
            "extracted_data": extracted_data,
            "url": input_data.get("url")
        }
