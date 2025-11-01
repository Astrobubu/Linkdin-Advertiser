from agents import WebScraperAgent, IdeaAnalyzerAgent, CriticAgent, PostGeneratorAgent
from database import get_db, Idea, Analysis, Criticism, Post
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import json
from datetime import datetime


class PipelineOrchestrator:
    """Orchestrates the multi-agent pipeline with looping capability."""

    def __init__(self):
        self.agent1 = WebScraperAgent()
        self.agent2 = IdeaAnalyzerAgent()
        self.agent3 = CriticAgent()
        self.agent4 = PostGeneratorAgent()

    def log(self, message: str):
        """Log orchestrator activity."""
        print(f"[ORCHESTRATOR] {message}")

    def save_to_database(
        self,
        db: Session,
        url: str,
        extracted_data: Dict,
        analysis: Dict,
        critique: Dict,
        posts: list,
        iteration: int
    ) -> Idea:
        """Save all pipeline results to database."""
        # Create or update Idea
        idea = db.query(Idea).filter(Idea.url == url).first()

        if not idea:
            idea = Idea(
                url=url,
                title=extracted_data.get("title"),
                description=extracted_data.get("description"),
                extracted_features=json.dumps(extracted_data.get("features", [])),
                target_audience=extracted_data.get("target_audience"),
                status="posts_generated"
            )
            db.add(idea)
            db.commit()
            db.refresh(idea)
        else:
            idea.status = "posts_generated"
            db.commit()

        # Save Analysis
        analysis_record = Analysis(
            idea_id=idea.id,
            analysis_text=json.dumps(analysis),
            market_score=analysis.get("market_analysis", {}).get("market_score", 0),
            uniqueness_score=analysis.get("uniqueness", {}).get("uniqueness_score", 0),
            suggested_angles=json.dumps(analysis.get("content_angles", []))
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

        # Save Criticism
        criticism_record = Criticism(
            idea_id=idea.id,
            analysis_id=analysis_record.id,
            feedback=json.dumps(critique),
            strengths=json.dumps(critique.get("strengths", [])),
            weaknesses=json.dumps(critique.get("weaknesses", [])),
            loop_trigger=critique.get("should_iterate", False),
            keywords_found=json.dumps(critique.get("trigger_keywords", [])),
            iteration_count=iteration
        )
        db.add(criticism_record)
        db.commit()

        # Save Posts
        for post_data in posts:
            post = Post(
                idea_id=idea.id,
                content=post_data.get("full_content"),
                post_type=post_data.get("type"),
                scheduled_date=post_data.get("schedule", {}).get("date"),
                scheduled_time=post_data.get("schedule", {}).get("time"),
                engagement_prediction=post_data.get("engagement_prediction"),
                hashtags=json.dumps(post_data.get("hashtags", [])),
                hook=post_data.get("hook"),
                body=post_data.get("body"),
                cta=post_data.get("cta"),
                carousel_slides=json.dumps(post_data.get("carousel_slides")) if post_data.get("carousel_slides") else None
            )
            db.add(post)

        db.commit()
        return idea

    def run_pipeline(self, url: str, db: Session) -> Dict[str, Any]:
        """
        Run the complete multi-agent pipeline.

        Args:
            url: The URL to analyze
            db: Database session

        Returns:
            Complete pipeline results including generated posts
        """
        self.log(f"🚀 Starting pipeline for: {url}")
        self.log("=" * 80)

        # Agent 1: Scrape & Extract
        self.log("\n📥 AGENT 1: Web Scraper & Extractor")
        self.log("-" * 80)
        agent1_output = self.agent1.process({"url": url})
        extracted_data = agent1_output["extracted_data"]
        self.log(f"✓ Extracted: {extracted_data.get('title')}")

        # Agent 2 & 3 Loop
        iteration = 1
        should_loop = True
        analysis = None
        critique = None

        while should_loop and iteration <= 3:  # Max 3 iterations
            self.log(f"\n🔄 ITERATION {iteration}")
            self.log("-" * 80)

            # Agent 2: Analyze
            self.log("\n🧠 AGENT 2: Deep Analyzer")
            agent2_output = self.agent2.process({
                "extracted_data": extracted_data,
                "url": url,
                "previous_critique": critique if iteration > 1 else None
            })
            analysis = agent2_output["analysis"]
            self.log(f"✓ Market Score: {analysis.get('market_analysis', {}).get('market_score', 'N/A')}/10")
            self.log(f"✓ Uniqueness Score: {analysis.get('uniqueness', {}).get('uniqueness_score', 'N/A')}/10")

            # Agent 3: Critique
            self.log("\n🎯 AGENT 3: Critic & Refiner")
            agent3_output = self.agent3.process({
                "analysis": analysis,
                "extracted_data": extracted_data,
                "url": url,
                "iteration": iteration
            })
            critique = agent3_output["critique"]
            should_loop = agent3_output["should_loop"]

            if should_loop:
                self.log(f"⚠️  Loop triggered: {critique.get('trigger_keywords', [])}")
                self.log("   Re-analyzing with feedback...")
                iteration += 1
            else:
                self.log(f"✓ Analysis approved (Confidence: {critique.get('confidence_score', 'N/A')}/10)")

        # Agent 4: Generate Posts
        self.log("\n✍️  AGENT 4: Post Generator")
        self.log("-" * 80)
        agent4_output = self.agent4.process({
            "analysis": analysis,
            "critique": critique,
            "extracted_data": extracted_data,
            "url": url
        })
        posts = agent4_output["posts"]
        self.log(f"✓ Generated {len(posts)} LinkedIn posts")

        # Save to database
        self.log("\n💾 Saving results to database...")
        idea = self.save_to_database(
            db=db,
            url=url,
            extracted_data=extracted_data,
            analysis=analysis,
            critique=critique,
            posts=posts,
            iteration=iteration
        )
        self.log(f"✓ Saved to database (Idea ID: {idea.id})")

        # Final summary
        self.log("\n" + "=" * 80)
        self.log("🎉 PIPELINE COMPLETE!")
        self.log(f"   Product: {extracted_data.get('title')}")
        self.log(f"   Iterations: {iteration}")
        self.log(f"   Posts Generated: {len(posts)}")
        self.log(f"   Market Score: {analysis.get('market_analysis', {}).get('market_score', 'N/A')}/10")
        self.log(f"   Uniqueness Score: {analysis.get('uniqueness', {}).get('uniqueness_score', 'N/A')}/10")
        self.log("=" * 80)

        return {
            "idea_id": idea.id,
            "url": url,
            "extracted_data": extracted_data,
            "analysis": analysis,
            "critique": critique,
            "posts": posts,
            "iterations": iteration,
            "posting_strategy": agent4_output.get("posting_strategy", {})
        }
