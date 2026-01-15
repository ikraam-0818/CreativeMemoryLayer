import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import Session, create_engine, select, SQLModel
from app.engine.models import Project

class DBProjectManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        # Create tables if they don't exist
        SQLModel.metadata.create_all(self.engine)
        
        # Ensure storage dir exists for assets even if using DB for metadata
        os.makedirs("storage", exist_ok=True)

    def _get_project_path(self, project_id: str) -> str:
        # We still keep local file storage for assets/videos for now
        # In a real cloud setup, this might point to S3
        path = os.path.join("storage", project_id)
        os.makedirs(path, exist_ok=True)
        return path

    def create_project(self, name: str, topic: str = "", mode: str = "text_to_video") -> dict:
        project = Project(
            name=name, 
            topic=topic, 
            mode=mode,
            memory={
                "visual_style": "",
                "characters": {},
                "narrative_tone": ""
            }
        )
        
        with Session(self.engine) as session:
            session.add(project)
            session.commit()
            session.refresh(project)
            
            # Ensure local asset folder exists
            self._get_project_path(project.id)
            
            return project.model_dump()

    def get_project(self, project_id: str) -> Optional[dict]:
        with Session(self.engine) as session:
            project = session.get(Project, project_id)
            if not project:
                return None
            return project.model_dump()

    def save_project(self, project_id: str, data: dict):
        # In SQLModel, we update the object.
        # This method signature mimics the file-based save_project which took a dict.
        with Session(self.engine) as session:
            project = session.get(Project, project_id)
            if not project:
                return
            
            # Update fields
            project.status = data.get('status', project.status)
            project.updated_at = datetime.now()
            
            # Complex JSON fields
            if 'script' in data:
                project.script = data['script']
            if 'memory' in data:
                project.memory = data['memory']
            if 'assets' in data:
                project.assets = data['assets']
            if 'video_url' in data:
                project.video_url = data['video_url']
            if 'error' in data:
                project.error = data['error']
                
            session.add(project)
            session.commit()

    def update_script(self, project_id: str, script: dict) -> Optional[dict]:
        with Session(self.engine) as session:
            project = session.get(Project, project_id)
            if not project:
                return None
            
            project.script = script
            project.status = 'script_ready'
            project.updated_at = datetime.now()
            
            session.add(project)
            session.commit()
            session.refresh(project)
            return project.model_dump()

    def update_memory(self, project_id: str, memory: dict) -> Optional[dict]:
        with Session(self.engine) as session:
            project = session.get(Project, project_id)
            if not project:
                return None
            
            project.memory = memory
            project.updated_at = datetime.now()
            
            session.add(project)
            session.commit()
            session.refresh(project)
            return project.model_dump()

    def list_projects(self) -> list:
        with Session(self.engine) as session:
            statement = select(Project).order_by(Project.updated_at.desc())
            results = session.exec(statement).all()
            return [p.model_dump() for p in results]
