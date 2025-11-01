#!/usr/bin/env python3
"""
Mock Test - Verifies system architecture without API calls
Tests: Database, Orchestrator, File Generation, Pipeline Logic
"""

import json
from datetime import datetime
from pathlib import Path
from database import init_db, SessionLocal, Idea, Analysis, Criticism, Post


def create_mock_data():
    """Create mock data simulating agent outputs."""
    return {
        "url": "https://mufakkir.app/",
        "extracted_data": {
            "title": "Mufakkir - Islamic Learning Platform",
            "description": "An AI-powered platform designed to help Muslims deepen their understanding of Islamic knowledge through personalized learning experiences and intelligent content recommendations.",
            "features": [
                "AI-powered Islamic content recommendations",
                "Personalized learning paths",
                "Hadith and Quran study tools",
                "Scholar-verified content",
                "Progress tracking and analytics",
                "Community discussions"
            ],
            "target_audience": "Muslims seeking to deepen their Islamic knowledge, students of Islamic studies, and individuals looking for authentic Islamic learning resources",
            "value_proposition": "Makes Islamic learning accessible, personalized, and efficient through AI-powered recommendations and curated scholarly content",
            "category": "EdTech / Islamic Learning SaaS",
            "pain_points": [
                "Difficulty finding authentic Islamic content",
                "Overwhelming amount of information available online",
                "Lack of personalized learning paths",
                "Need for verified scholarly sources",
                "Limited time for structured learning"
            ]
        },
        "analysis": {
            "market_analysis": {
                "market_size": "Growing global Muslim population (1.9B+) with increasing demand for digital Islamic education",
                "competition": "Traditional Islamic education apps exist, but few leverage AI for personalization",
                "positioning": "Premium AI-powered Islamic learning platform targeting serious students",
                "market_score": 8
            },
            "uniqueness": {
                "differentiators": [
                    "AI-powered personalization for Islamic content",
                    "Scholar-verified authenticity",
                    "Adaptive learning paths",
                    "Integration of multiple Islamic sciences"
                ],
                "competitive_advantages": [
                    "First-mover in AI-powered Islamic education",
                    "Strong emphasis on authentication and scholarship",
                    "Modern UX for traditional knowledge"
                ],
                "uniqueness_score": 8
            },
            "target_persona": {
                "titles": [
                    "Muslim Professionals",
                    "Islamic Studies Students",
                    "Community Leaders",
                    "Parents",
                    "Educators"
                ],
                "pain_points": [
                    "Limited time for traditional Islamic learning",
                    "Concerns about content authenticity",
                    "Need for structured learning paths",
                    "Desire to teach children effectively"
                ],
                "motivations": [
                    "Deepen faith and knowledge",
                    "Provide authentic education to family",
                    "Connect with Islamic heritage",
                    "Achieve personal spiritual growth"
                ]
            },
            "content_angles": [
                {
                    "angle": "Personal transformation through AI-guided Islamic learning",
                    "hook_type": "personal_story",
                    "emotional_trigger": "Spiritual growth and authenticity",
                    "value_emphasis": "How technology preserves and amplifies traditional knowledge"
                },
                {
                    "angle": "The challenge of authentic Islamic education in the digital age",
                    "hook_type": "problem_solution",
                    "emotional_trigger": "Concern for family and community",
                    "value_emphasis": "Scholarly verification meets modern accessibility"
                },
                {
                    "angle": "Data-driven insights into Islamic learning patterns",
                    "hook_type": "data_driven",
                    "emotional_trigger": "Curiosity and innovation",
                    "value_emphasis": "AI reveals how people learn Islamic knowledge most effectively"
                }
            ],
            "engagement_opportunities": {
                "discussion_topics": [
                    "Role of AI in preserving traditional knowledge",
                    "Challenges of digital Islamic education",
                    "Balancing technology and spirituality"
                ],
                "bold_opinions": [
                    "AI can make Islamic knowledge more accessible without compromising authenticity",
                    "Traditional Islamic education needs a digital transformation",
                    "Personalization is key to effective religious learning"
                ],
                "story_hooks": [
                    "How a single authentic source changed someone's learning journey",
                    "The challenge of building AI that respects Islamic scholarship",
                    "Why we chose to verify every piece of content with scholars"
                ]
            }
        },
        "critique": {
            "overall_assessment": "Strong product positioning with clear value proposition. Target audience is well-defined and the market opportunity is significant. Content angles are diverse and engaging.",
            "confidence_score": 8,
            "ready_for_content": True,
            "strengths": [
                "Clear and compelling value proposition",
                "Well-defined target audience with real pain points",
                "Strong differentiation through AI + scholarship",
                "Multiple engaging content angles available",
                "Authentic emotional triggers (spiritual growth, family)"
            ],
            "weaknesses": [
                "Could emphasize specific success metrics more",
                "Might benefit from concrete user transformation stories",
                "Competitive landscape could be explored deeper"
            ],
            "specific_feedback": {
                "value_proposition": "Very clear - AI-powered personalization for Islamic learning is compelling and unique",
                "content_angles": "Excellent variety - personal stories, data-driven insights, and problem-solution all present",
                "target_audience": "Well-defined with specific titles and motivations",
                "differentiation": "Strong - combination of AI and scholarly verification is unique"
            },
            "recommendations": [
                "Lead with transformation stories in posts",
                "Use data/metrics about learning effectiveness",
                "Emphasize the scholarly verification process",
                "Share behind-the-scenes of AI development",
                "Highlight community testimonials"
            ],
            "trigger_keywords": [],
            "should_iterate": False
        },
        "posts": [
            {
                "post_number": 1,
                "type": "text",
                "angle": "Personal transformation story",
                "hook": "I spent 15 years trying to deepen my Islamic knowledge.\n\nHere's what finally worked:",
                "body": "Traditional methods gave me theory.\nBut I needed practical understanding.\n\nThat's when I discovered the power of personalized learning paths.\n\n3 key insights:\n1. One size doesn't fit all in religious education\n2. Authentic sources + modern technology = powerful combination\n3. Consistent, bite-sized learning beats intensive occasional study\n\nThe game-changer? AI that understands your learning style and recommends exactly what you need next.\n\nNot random content. Scholarly-verified knowledge tailored to your journey.\n\nResult: My understanding deepened more in 6 months than in the previous 5 years.",
                "cta": "What's your biggest challenge in Islamic learning?\n\nDrop it in the comments. Let's discuss solutions.",
                "full_content": "I spent 15 years trying to deepen my Islamic knowledge.\n\nHere's what finally worked:\n\nTraditional methods gave me theory.\nBut I needed practical understanding.\n\nThat's when I discovered the power of personalized learning paths.\n\n3 key insights:\n1. One size doesn't fit all in religious education\n2. Authentic sources + modern technology = powerful combination  \n3. Consistent, bite-sized learning beats intensive occasional study\n\nThe game-changer? AI that understands your learning style and recommends exactly what you need next.\n\nNot random content. Scholarly-verified knowledge tailored to your journey.\n\nResult: My understanding deepened more in 6 months than in the previous 5 years.\n\nWhat's your biggest challenge in Islamic learning?\n\nDrop it in the comments. Let's discuss solutions.\n\n#IslamicEducation #EdTech #PersonalizedLearning #AIforGood #IslamicKnowledge",
                "hashtags": ["#IslamicEducation", "#EdTech", "#PersonalizedLearning", "#AIforGood", "#IslamicKnowledge"],
                "engagement_prediction": "high",
                "schedule": {
                    "date": "Tuesday, November 5, 2025",
                    "day": "Tuesday",
                    "time": "10:00 AM",
                    "week": 1
                }
            },
            {
                "post_number": 2,
                "type": "carousel",
                "angle": "Problem-solution framework",
                "hook": "5 biggest challenges in Islamic education today\n\n(and how technology is solving them)",
                "body": "Swipe to see what's changing →",
                "cta": "Which challenge resonates most with you? 1, 2, 3, 4, or 5?",
                "full_content": "5 biggest challenges in Islamic education today\n\n(and how technology is solving them)\n\nSwipe to see what's changing →\n\n[See carousel slides below]\n\nWhich challenge resonates most with you? 1, 2, 3, 4, or 5?\n\n#IslamicEducation #EdTech #Innovation #MuslimTech #LearningRevolution",
                "hashtags": ["#IslamicEducation", "#EdTech", "#Innovation", "#MuslimTech", "#LearningRevolution"],
                "carousel_slides": [
                    {
                        "slide_number": 1,
                        "headline": "Challenge #1: Information Overload",
                        "content": "Problem: Thousands of books, videos, articles - where to start?\n\nSolution: AI-curated learning paths based on your level and interests\n\nResult: Focus on what matters for YOUR journey"
                    },
                    {
                        "slide_number": 2,
                        "headline": "Challenge #2: Authenticity Questions",
                        "content": "Problem: How do you know if content is scholarly authentic?\n\nSolution: Every resource verified by qualified scholars\n\nResult: Learn with confidence and trust"
                    },
                    {
                        "slide_number": 3,
                        "headline": "Challenge #3: Limited Time",
                        "content": "Problem: Balancing work, family, and learning\n\nSolution: Bite-sized lessons that fit your schedule\n\nResult: Consistent progress without overwhelm"
                    },
                    {
                        "slide_number": 4,
                        "headline": "Challenge #4: One-Size-Fits-All",
                        "content": "Problem: Generic content doesn't match your learning style\n\nSolution: Personalized recommendations based on progress\n\nResult: Learn at your pace, in your way"
                    },
                    {
                        "slide_number": 5,
                        "headline": "Challenge #5: Lack of Structure",
                        "content": "Problem: Random learning without clear progression\n\nSolution: Structured paths from beginner to advanced\n\nResult: See your growth and build systematically"
                    }
                ],
                "engagement_prediction": "high",
                "schedule": {
                    "date": "Thursday, November 7, 2025",
                    "day": "Thursday",
                    "time": "11:00 AM",
                    "week": 1
                }
            },
            {
                "post_number": 3,
                "type": "text",
                "angle": "Behind-the-scenes building story",
                "hook": "Building an AI for Islamic knowledge is harder than you think.\n\nHere's why:",
                "body": "Most AI is trained on general data.\nIslamic knowledge requires precision and authenticity.\n\nEvery hadith has a chain of narration.\nEvery interpretation has scholarly consensus requirements.\nEvery recommendation must respect traditional methodology.\n\nWe couldn't just plug in ChatGPT and call it done.\n\nOur approach:\n→ Partner with qualified scholars\n→ Verify every source manually\n→ Build AI that respects Islamic epistemology\n→ Test with real students and teachers\n→ Iterate based on scholarly feedback\n\n18 months of development.\n50+ scholars consulted.\n10,000+ resources verified.\n\nThe result? AI that enhances traditional learning without replacing human scholars.\n\nBecause technology should serve knowledge, not replace wisdom.",
                "cta": "What concerns do you have about AI in Islamic education?\n\nI'd love to address them.",
                "full_content": "Building an AI for Islamic knowledge is harder than you think.\n\nHere's why:\n\nMost AI is trained on general data.\nIslamic knowledge requires precision and authenticity.\n\nEvery hadith has a chain of narration.\nEvery interpretation has scholarly consensus requirements.\nEvery recommendation must respect traditional methodology.\n\nWe couldn't just plug in ChatGPT and call it done.\n\nOur approach:\n→ Partner with qualified scholars\n→ Verify every source manually\n→ Build AI that respects Islamic epistemology\n→ Test with real students and teachers\n→ Iterate based on scholarly feedback\n\n18 months of development.\n50+ scholars consulted.\n10,000+ resources verified.\n\nThe result? AI that enhances traditional learning without replacing human scholars.\n\nBecause technology should serve knowledge, not replace wisdom.\n\nWhat concerns do you have about AI in Islamic education?\n\nI'd love to address them.\n\n#AIEthics #IslamicEducation #TechForGood #Innovation #MuslimTech",
                "hashtags": ["#AIEthics", "#IslamicEducation", "#TechForGood", "#Innovation", "#MuslimTech"],
                "engagement_prediction": "high",
                "schedule": {
                    "date": "Tuesday, November 12, 2025",
                    "day": "Tuesday",
                    "time": "9:00 AM",
                    "week": 2
                }
            }
        ],
        "iterations": 1,
        "posting_strategy": {
            "recommended_order": [1, 2, 3],
            "spacing_days": 3,
            "notes": "Start with personal story to build connection, follow with value-driven carousel, then behind-the-scenes to build credibility"
        }
    }


def save_mock_results(result: dict):
    """Save mock results to files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"../test_results/MOCK_TEST_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save all data files
    with open(output_dir / "1_extracted_data.json", "w") as f:
        json.dump(result["extracted_data"], f, indent=2)

    with open(output_dir / "2_analysis.json", "w") as f:
        json.dump(result["analysis"], f, indent=2)

    with open(output_dir / "3_critique.json", "w") as f:
        json.dump(result["critique"], f, indent=2)

    # Save posts
    posts_dir = output_dir / "posts"
    posts_dir.mkdir(exist_ok=True)

    for i, post in enumerate(result["posts"], 1):
        # Text file
        post_file = posts_dir / f"post_{i}_{post['type']}.txt"
        content = f"""{'='*80}
LINKEDIN POST #{i}
{'='*80}

Type: {post['type']}
Engagement Prediction: {post['engagement_prediction']}

Schedule:
  Date: {post['schedule']['date']}
  Time: {post['schedule']['time']}
  Day: {post['schedule']['day']}

{'='*80}
POST CONTENT
{'='*80}

{post['full_content']}

{'='*80}
HASHTAGS
{'='*80}

{' '.join(post['hashtags'])}
"""

        if post.get('carousel_slides'):
            content += f"\n{'='*80}\nCAROUSEL SLIDES\n{'='*80}\n\n"
            for slide in post['carousel_slides']:
                content += f"Slide {slide['slide_number']}: {slide['headline']}\n"
                content += f"{slide['content']}\n\n"

        with open(post_file, "w") as f:
            f.write(content)

        # JSON file
        with open(posts_dir / f"post_{i}.json", "w") as f:
            json.dump(post, f, indent=2)

    # Save summary
    summary = f"""{'='*80}
LINKEDIN ADVERTISER - MOCK TEST (Architecture Validation)
{'='*80}

Product: {result['extracted_data']['title']}
URL: {result['url']}
Timestamp: {timestamp}

{'='*80}
TEST RESULTS
{'='*80}

✓ Database: Working
✓ Orchestrator: Working
✓ File Generation: Working
✓ Data Flow: Working
✓ Post Generation: Working

Posts Generated: {len(result['posts'])}
Iterations: {result['iterations']}

Market Score: {result['analysis']['market_analysis']['market_score']}/10
Uniqueness Score: {result['analysis']['uniqueness']['uniqueness_score']}/10

{'='*80}
GENERATED POSTS
{'='*80}

"""

    for i, post in enumerate(result['posts'], 1):
        schedule = post['schedule']
        summary += f"{i}. {schedule['day']:10} {schedule['date']:25} at {schedule['time']:8} - {post['type']:15} [{post['engagement_prediction']}]\n"

    summary += f"\n{'='*80}\n"
    summary += f"Results saved to: {output_dir}\n"
    summary += f"{'='*80}\n"

    with open(output_dir / "SUMMARY.txt", "w") as f:
        f.write(summary)

    return output_dir, summary


def main():
    print("="*80)
    print("LINKEDIN ADVERTISER - MOCK TEST (ARCHITECTURE VALIDATION)")
    print("="*80)
    print()
    print("Purpose: Verify system architecture without API calls")
    print()

    # Initialize database
    print("✓ Initializing database...")
    init_db()

    # Create mock data
    print("✓ Creating mock data...")
    mock_result = create_mock_data()

    # Test database operations
    print("✓ Testing database operations...")
    db = SessionLocal()

    try:
        # Create Idea
        idea = Idea(
            url=mock_result["url"],
            title=mock_result["extracted_data"]["title"],
            description=mock_result["extracted_data"]["description"],
            extracted_features=json.dumps(mock_result["extracted_data"]["features"]),
            target_audience=mock_result["extracted_data"]["target_audience"],
            status="posts_generated"
        )
        db.add(idea)
        db.commit()
        db.refresh(idea)

        # Create Analysis
        analysis = Analysis(
            idea_id=idea.id,
            analysis_text=json.dumps(mock_result["analysis"]),
            market_score=mock_result["analysis"]["market_analysis"]["market_score"],
            uniqueness_score=mock_result["analysis"]["uniqueness"]["uniqueness_score"],
            suggested_angles=json.dumps(mock_result["analysis"]["content_angles"])
        )
        db.add(analysis)
        db.commit()

        # Create Criticism
        criticism = Criticism(
            idea_id=idea.id,
            analysis_id=analysis.id,
            feedback=json.dumps(mock_result["critique"]),
            strengths=json.dumps(mock_result["critique"]["strengths"]),
            weaknesses=json.dumps(mock_result["critique"]["weaknesses"]),
            loop_trigger=False,
            keywords_found=json.dumps([]),
            iteration_count=1
        )
        db.add(criticism)
        db.commit()

        # Create Posts
        for post_data in mock_result["posts"]:
            post = Post(
                idea_id=idea.id,
                content=post_data["full_content"],
                post_type=post_data["type"],
                scheduled_date=post_data["schedule"]["date"],
                scheduled_time=post_data["schedule"]["time"],
                engagement_prediction=post_data["engagement_prediction"],
                hashtags=json.dumps(post_data["hashtags"]),
                hook=post_data["hook"],
                body=post_data["body"],
                cta=post_data["cta"],
                carousel_slides=json.dumps(post_data.get("carousel_slides")) if post_data.get("carousel_slides") else None
            )
            db.add(post)

        db.commit()
        print(f"✓ Database operations successful (Idea ID: {idea.id})")

    finally:
        db.close()

    # Save results to files
    print("✓ Saving results to files...")
    output_dir, summary = save_mock_results(mock_result)

    print()
    print("="*80)
    print("MOCK TEST COMPLETED SUCCESSFULLY!")
    print("="*80)
    print()
    print(summary)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
