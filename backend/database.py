from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import settings

Base = declarative_base()


class Idea(Base):
    """Stores product ideas extracted from URLs."""
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    extracted_features = Column(Text)  # JSON string
    target_audience = Column(Text)
    status = Column(String, default="extracted")  # extracted, analyzed, criticized, posts_generated
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="idea")
    criticisms = relationship("Criticism", back_populates="idea")
    posts = relationship("Post", back_populates="idea")


class Analysis(Base):
    """Stores deep analysis from Agent 2."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    analysis_text = Column(Text)
    market_score = Column(Float)
    uniqueness_score = Column(Float)
    suggested_angles = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    idea = relationship("Idea", back_populates="analyses")
    criticisms = relationship("Criticism", back_populates="analysis")


class Criticism(Base):
    """Stores criticism and feedback from Agent 3."""
    __tablename__ = "criticisms"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    feedback = Column(Text)
    strengths = Column(Text)  # JSON string
    weaknesses = Column(Text)  # JSON string
    loop_trigger = Column(Boolean, default=False)
    keywords_found = Column(Text)  # JSON string
    iteration_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    idea = relationship("Idea", back_populates="criticisms")
    analysis = relationship("Analysis", back_populates="criticisms")


class Post(Base):
    """Stores generated LinkedIn posts."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    content = Column(Text)
    post_type = Column(String)  # text, carousel, video_script
    scheduled_date = Column(String)  # e.g., "Tuesday, Nov 5"
    scheduled_time = Column(String)  # e.g., "10:00 AM"
    engagement_prediction = Column(String)
    hashtags = Column(Text)  # JSON string
    hook = Column(Text)
    body = Column(Text)
    cta = Column(Text)
    carousel_slides = Column(Text, nullable=True)  # JSON string for carousel posts
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    idea = relationship("Idea", back_populates="posts")


# Database setup
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
