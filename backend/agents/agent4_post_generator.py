from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta


class PostGeneratorAgent(BaseAgent):
    """Agent 4: Generates LinkedIn posts with optimal timing."""

    def __init__(self):
        system_prompt = """You are an expert LinkedIn content creator specializing in viral SaaS and tech content.

Your task is to create highly engaging LinkedIn posts that maximize engagement and shareability.

LINKEDIN POST BEST PRACTICES (2025):

1. STRUCTURE (Hook-Body-CTA):
   - HOOK: First 2 lines are critical (only part visible in feed)
     * Use bold opinions, surprising stats, or personal moments
     * Examples: "Hiring the most qualified person was my biggest mistake"
     * Create curiosity or pattern interrupt

   - BODY: 150-300 words
     * One core idea/story/lesson
     * Use white space (short paragraphs, 1-2 lines max)
     * Mobile-first formatting
     * Personal stories showing struggle → solution

   - CTA: Question or prompt
     * Turn passive readers into active commenters
     * Ask for opinions, experiences, or insights

2. CONTENT TYPES:
   - Text posts (150-300 words)
   - Carousel concepts (5-10 slides with headlines)
   - Video scripts (60-90 seconds)

3. ENGAGEMENT TRIGGERS:
   - Personal failure stories (then redemption)
   - Controversial but defendable opinions
   - Data-backed insights
   - Actionable frameworks
   - Behind-the-scenes stories

4. FORMATTING:
   - Short paragraphs (1-2 lines)
   - Plenty of white space
   - No walls of text
   - 3-5 relevant hashtags

5. TONE:
   - Honest and authentic
   - Conversational (not corporate)
   - Show vulnerability
   - Demonstrate expertise without bragging

Generate 7-10 post variations covering different angles and formats.

Return as JSON:
{
    "posts": [
        {
            "post_number": 1,
            "type": "text|carousel|video_script",
            "angle": "...",
            "hook": "First 2 lines that appear in feed...",
            "body": "Main content with\\n\\nwhite space...",
            "cta": "Question or prompt...",
            "full_content": "Complete formatted post...",
            "hashtags": ["#SaaS", "#ProductDevelopment", ...],
            "engagement_prediction": "high|medium",
            "carousel_slides": [
                {"slide_number": 1, "headline": "...", "content": "..."}
            ] // only for carousel type
        }
    ],
    "posting_strategy": {
        "recommended_order": [1, 3, 2, ...],
        "spacing_days": 2,
        "notes": "..."
    }
}

Create diverse, engaging posts that would perform well on LinkedIn."""

        super().__init__("PostGeneratorAgent", system_prompt)

    def generate_schedule(self, num_posts: int) -> List[Dict[str, str]]:
        """Generate optimal posting schedule based on research."""
        # Best days: Tuesday, Wednesday, Thursday
        # Best times: 9-11 AM, 12 PM (noon)

        posting_days = ["Tuesday", "Wednesday", "Thursday"]
        posting_times = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM"]

        schedule = []
        current_date = datetime.now()

        # Find next Tuesday
        days_ahead = 1 - current_date.weekday()  # Tuesday is 1
        if days_ahead <= 0:
            days_ahead += 7
        next_tuesday = current_date + timedelta(days=days_ahead)

        for i in range(num_posts):
            # Cycle through days (Tue, Wed, Thu, Tue, Wed, Thu, ...)
            day_index = i % 3
            week_offset = i // 3

            post_date = next_tuesday + timedelta(days=day_index + (week_offset * 7))

            # Alternate times for variety
            time_index = i % len(posting_times)

            schedule.append({
                "date": post_date.strftime("%A, %B %d, %Y"),
                "day": posting_days[day_index],
                "time": posting_times[time_index],
                "week": week_offset + 1
            })

        return schedule

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate LinkedIn posts with scheduling.

        Input: {"analysis": {...}, "critique": {...}, "extracted_data": {...}}
        Output: {"posts": [...], "schedule": [...], ...}
        """
        analysis = input_data.get("analysis")
        critique = input_data.get("critique")
        extracted_data = input_data.get("extracted_data")

        if not all([analysis, critique, extracted_data]):
            raise ValueError("analysis, critique, and extracted_data are required")

        self.log(f"Generating posts for: {extracted_data.get('title', 'Unknown')}")

        # Prepare generation prompt
        prompt = f"""Create engaging LinkedIn posts for the following product:

PRODUCT:
{json.dumps(extracted_data, indent=2)}

STRATEGIC ANALYSIS:
{json.dumps(analysis, indent=2)}

CRITIQUE & RECOMMENDATIONS:
Strengths: {json.dumps(critique.get('strengths', []), indent=2)}
Recommendations: {json.dumps(critique.get('recommendations', []), indent=2)}

Create 7-10 diverse, highly engaging LinkedIn posts as specified in your system prompt.
Include a mix of text posts, carousel concepts, and optionally video scripts.

Focus on the strongest content angles and incorporate the critique recommendations."""

        response = self.call_gpt(prompt, response_format="json_object", temperature=0.8)

        # Parse JSON response
        try:
            generated = json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse post generation response as JSON")

        posts = generated.get("posts", [])

        # Generate schedule
        schedule = self.generate_schedule(len(posts))

        # Combine posts with schedule
        scheduled_posts = []
        for i, post in enumerate(posts):
            if i < len(schedule):
                scheduled_posts.append({
                    **post,
                    "schedule": schedule[i]
                })

        self.log(f"✓ Generated {len(scheduled_posts)} posts with optimal scheduling")

        return {
            "posts": scheduled_posts,
            "posting_strategy": generated.get("posting_strategy", {}),
            "analysis": analysis,
            "critique": critique,
            "extracted_data": extracted_data,
            "url": input_data.get("url")
        }
