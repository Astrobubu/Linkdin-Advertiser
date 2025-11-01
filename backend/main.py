from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import init_db, get_db, Idea, Analysis, Criticism, Post
from orchestrator import PipelineOrchestrator
from typing import List, Optional
import json
import uvicorn


app = FastAPI(title="LinkedIn Advertiser API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✓ Database initialized")


# Pydantic models
class URLInput(BaseModel):
    url: HttpUrl


class IdeaResponse(BaseModel):
    id: int
    url: str
    title: Optional[str]
    description: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    content: Optional[str]
    post_type: Optional[str]
    scheduled_date: Optional[str]
    scheduled_time: Optional[str]
    hook: Optional[str]
    body: Optional[str]
    cta: Optional[str]
    hashtags: Optional[str]
    carousel_slides: Optional[str]
    engagement_prediction: Optional[str]

    class Config:
        from_attributes = True


class PipelineResult(BaseModel):
    idea_id: int
    url: str
    extracted_data: dict
    analysis: dict
    critique: dict
    posts: List[dict]
    iterations: int
    posting_strategy: dict


# API Routes
@app.get("/")
def read_root():
    return {
        "message": "LinkedIn Advertiser API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/analyze", response_model=PipelineResult)
async def analyze_url(url_input: URLInput, db: Session = Depends(get_db)):
    """
    Run the complete multi-agent pipeline on a URL.

    This endpoint:
    1. Scrapes the web page
    2. Extracts product/idea information
    3. Performs deep analysis
    4. Critically evaluates (with looping if needed)
    5. Generates LinkedIn posts with optimal timing
    """
    try:
        orchestrator = PipelineOrchestrator()
        result = orchestrator.run_pipeline(str(url_input.url), db)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@app.get("/api/ideas", response_model=List[IdeaResponse])
async def get_ideas(db: Session = Depends(get_db)):
    """Get all analyzed ideas."""
    ideas = db.query(Idea).order_by(Idea.created_at.desc()).all()
    return [
        IdeaResponse(
            id=idea.id,
            url=idea.url,
            title=idea.title,
            description=idea.description,
            status=idea.status,
            created_at=idea.created_at.isoformat() if idea.created_at else ""
        )
        for idea in ideas
    ]


@app.get("/api/ideas/{idea_id}")
async def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific idea."""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # Get related data
    analyses = db.query(Analysis).filter(Analysis.idea_id == idea_id).all()
    criticisms = db.query(Criticism).filter(Criticism.idea_id == idea_id).all()
    posts = db.query(Post).filter(Post.idea_id == idea_id).all()

    return {
        "idea": {
            "id": idea.id,
            "url": idea.url,
            "title": idea.title,
            "description": idea.description,
            "features": json.loads(idea.extracted_features) if idea.extracted_features else [],
            "target_audience": idea.target_audience,
            "status": idea.status,
            "created_at": idea.created_at.isoformat() if idea.created_at else ""
        },
        "analysis": json.loads(analyses[-1].analysis_text) if analyses else None,
        "critique": json.loads(criticisms[-1].feedback) if criticisms else None,
        "posts": [
            {
                "id": post.id,
                "type": post.post_type,
                "content": post.content,
                "hook": post.hook,
                "body": post.body,
                "cta": post.cta,
                "scheduled_date": post.scheduled_date,
                "scheduled_time": post.scheduled_time,
                "hashtags": json.loads(post.hashtags) if post.hashtags else [],
                "carousel_slides": json.loads(post.carousel_slides) if post.carousel_slides else None,
                "engagement_prediction": post.engagement_prediction
            }
            for post in posts
        ],
        "iterations": criticisms[-1].iteration_count if criticisms else 1
    }


@app.get("/api/posts/{idea_id}", response_model=List[PostResponse])
async def get_posts(idea_id: int, db: Session = Depends(get_db)):
    """Get all generated posts for a specific idea."""
    posts = db.query(Post).filter(Post.idea_id == idea_id).all()

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this idea")

    return posts


@app.delete("/api/ideas/{idea_id}")
async def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    """Delete an idea and all related data."""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # Delete related records (cascade should handle this, but being explicit)
    db.query(Post).filter(Post.idea_id == idea_id).delete()
    db.query(Criticism).filter(Criticism.idea_id == idea_id).delete()
    db.query(Analysis).filter(Analysis.idea_id == idea_id).delete()
    db.query(Idea).filter(Idea.id == idea_id).delete()

    db.commit()

    return {"message": "Idea deleted successfully"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "LinkedIn Advertiser API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
