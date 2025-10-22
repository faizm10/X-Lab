from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(String(255), primary_key=True)  # Job listing ID from source
    company = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    team = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metadata
    first_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Tracking
    posted_date = Column(DateTime, nullable=True)
    scraped_count = Column(Integer, default=1)
    
    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "title": self.title,
            "team": self.team,
            "location": self.location,
            "url": self.url,
            "description": self.description,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "is_active": self.is_active,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "scraped_count": self.scraped_count,
        }

