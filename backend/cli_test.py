#!/usr/bin/env python3
"""
CLI Test Script for LinkedIn Advertiser
Tests the multi-agent pipeline and outputs results to files
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from database import init_db, SessionLocal
from orchestrator import PipelineOrchestrator


def save_results_to_files(result: dict, run_number: int):
    """Save pipeline results to organized files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"../test_results/run_{run_number}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save extracted data
    with open(output_dir / "1_extracted_data.json", "w") as f:
        json.dump(result["extracted_data"], f, indent=2)

    # Save analysis
    with open(output_dir / "2_analysis.json", "w") as f:
        json.dump(result["analysis"], f, indent=2)

    # Save critique
    with open(output_dir / "3_critique.json", "w") as f:
        json.dump(result["critique"], f, indent=2)

    # Save posts as individual files
    posts_dir = output_dir / "posts"
    posts_dir.mkdir(exist_ok=True)

    for i, post in enumerate(result["posts"], 1):
        # Save each post as text file
        post_file = posts_dir / f"post_{i}_{post.get('type', 'text')}.txt"

        content = f"""{'='*80}
LINKEDIN POST #{i}
{'='*80}

Type: {post.get('type', 'text')}
Engagement Prediction: {post.get('engagement_prediction', 'N/A')}

Schedule:
  Date: {post.get('schedule', {}).get('date', 'N/A')}
  Time: {post.get('schedule', {}).get('time', 'N/A')}
  Day: {post.get('schedule', {}).get('day', 'N/A')}

{'='*80}
POST CONTENT
{'='*80}

{post.get('full_content', post.get('content', 'N/A'))}

{'='*80}
HASHTAGS
{'='*80}

{' '.join(post.get('hashtags', []))}

"""

        # Add carousel slides if present
        if post.get('carousel_slides'):
            content += f"\n{'='*80}\nCAROUSEL SLIDES\n{'='*80}\n\n"
            for slide in post['carousel_slides']:
                content += f"Slide {slide['slide_number']}: {slide['headline']}\n"
                content += f"{slide['content']}\n\n"

        with open(post_file, "w") as f:
            f.write(content)

        # Also save as JSON
        with open(posts_dir / f"post_{i}.json", "w") as f:
            json.dump(post, f, indent=2)

    # Save summary
    summary = f"""{'='*80}
LINKEDIN ADVERTISER - TEST RUN #{run_number}
{'='*80}

Product: {result['extracted_data'].get('title', 'N/A')}
URL: {result['url']}
Timestamp: {timestamp}

{'='*80}
PIPELINE SUMMARY
{'='*80}

Iterations: {result['iterations']}
Posts Generated: {len(result['posts'])}

Market Score: {result['analysis'].get('market_analysis', {}).get('market_score', 'N/A')}/10
Uniqueness Score: {result['analysis'].get('uniqueness', {}).get('uniqueness_score', 'N/A')}/10

{'='*80}
PRODUCT INFORMATION
{'='*80}

Title: {result['extracted_data'].get('title')}
Description: {result['extracted_data'].get('description')}
Category: {result['extracted_data'].get('category')}
Target Audience: {result['extracted_data'].get('target_audience')}

Features:
{chr(10).join('  - ' + f for f in result['extracted_data'].get('features', []))}

Pain Points:
{chr(10).join('  - ' + p for p in result['extracted_data'].get('pain_points', []))}

{'='*80}
ANALYSIS SCORES
{'='*80}

Market Analysis:
  Market Size: {result['analysis'].get('market_analysis', {}).get('market_size', 'N/A')}
  Competition: {result['analysis'].get('market_analysis', {}).get('competition', 'N/A')}
  Positioning: {result['analysis'].get('market_analysis', {}).get('positioning', 'N/A')}
  Score: {result['analysis'].get('market_analysis', {}).get('market_score', 'N/A')}/10

Uniqueness:
  Score: {result['analysis'].get('uniqueness', {}).get('uniqueness_score', 'N/A')}/10
  Differentiators:
{chr(10).join('    - ' + d for d in result['analysis'].get('uniqueness', {}).get('differentiators', []))}

{'='*80}
CRITIQUE SUMMARY
{'='*80}

Overall Assessment: {result['critique'].get('overall_assessment', 'N/A')}
Confidence Score: {result['critique'].get('confidence_score', 'N/A')}/10
Ready for Content: {result['critique'].get('ready_for_content', 'N/A')}

Strengths:
{chr(10).join('  ✓ ' + s for s in result['critique'].get('strengths', []))}

Weaknesses:
{chr(10).join('  ✗ ' + w for w in result['critique'].get('weaknesses', []))}

Recommendations:
{chr(10).join('  → ' + r for r in result['critique'].get('recommendations', []))}

{'='*80}
POST SCHEDULE
{'='*80}

"""

    for i, post in enumerate(result['posts'], 1):
        schedule = post.get('schedule', {})
        summary += f"{i}. {schedule.get('day', 'N/A'):10} {schedule.get('date', 'N/A'):25} at {schedule.get('time', 'N/A'):8} - {post.get('type', 'text'):15} [{post.get('engagement_prediction', 'N/A')}]\n"

    summary += f"\n{'='*80}\n"
    summary += f"Results saved to: {output_dir}\n"
    summary += f"{'='*80}\n"

    with open(output_dir / "SUMMARY.txt", "w") as f:
        f.write(summary)

    return output_dir, summary


def main():
    print("="*80)
    print("LINKEDIN ADVERTISER - CLI TEST MODE")
    print("="*80)
    print()

    if len(sys.argv) < 2:
        print("Usage: python cli_test.py <url> [run_number]")
        print("Example: python cli_test.py https://mufakkir.app/ 1")
        sys.exit(1)

    url = sys.argv[1]
    run_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    print(f"Test Run: #{run_number}")
    print(f"URL: {url}")
    print()

    # Initialize database
    print("Initializing database...")
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Run pipeline
        print("Starting multi-agent pipeline...")
        print()

        orchestrator = PipelineOrchestrator()
        result = orchestrator.run_pipeline(url, db)

        print()
        print("="*80)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*80)
        print()

        # Save results to files
        print("Saving results to files...")
        output_dir, summary = save_results_to_files(result, run_number)

        print()
        print(summary)

        return 0

    except Exception as e:
        print()
        print("="*80)
        print("ERROR!")
        print("="*80)
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
