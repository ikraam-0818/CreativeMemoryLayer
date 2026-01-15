from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, JSON
from sqlalchemy import Column
import uuid

class Project(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    topic: str
    mode: str = "text_to_video"
    status: str = "created"
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Store complex objects as JSON
    script: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    memory: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    assets: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    
    video_url: Optional[str] = None
    error: Optional[str] = None
