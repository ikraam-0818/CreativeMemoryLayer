import os
import json
import uuid
import shutil
from typing import Dict, Optional
from datetime import datetime

STORAGE_DIR = "storage"

class ProjectManager:
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_project_path(self, project_id: str) -> str:
        return os.path.join(self.base_dir, project_id)

    def _get_project_file(self, project_id: str) -> str:
        return os.path.join(self._get_project_path(project_id), "project.json")

    def create_project(self, name: str, topic: str = "", mode: str = "text_to_video") -> dict:
        project_id = str(uuid.uuid4())
        project_dir = self._get_project_path(project_id)
        os.makedirs(project_dir, exist_ok=True)

        project_data = {
            "id": project_id,
            "name": name,
            "topic": topic,
            "mode": mode,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "script": None,
            "memory": {
                "visual_style": "",
                "characters": {},
                "narrative_tone": ""
            },
            "assets": [], # List of asset file paths
            "video_url": None
        }

        self.save_project(project_id, project_data)
        return project_data

    def get_project(self, project_id: str) -> Optional[dict]:
        file_path = self._get_project_file(project_id)
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading project {project_id}: {e}")
            return None

    def save_project(self, project_id: str, data: dict):
        file_path = self._get_project_file(project_id)
        data['updated_at'] = datetime.now().isoformat()
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def update_script(self, project_id: str, script: dict) -> Optional[dict]:
        project = self.get_project(project_id)
        if not project:
            return None
        
        project['script'] = script
        project['status'] = 'script_ready'
        self.save_project(project_id, project)
        return project

    def update_memory(self, project_id: str, memory: dict) -> Optional[dict]:
        project = self.get_project(project_id)
        if not project:
            return None
        
        # Merge or replace? Let's replace for now to keep it simple
        # But ensure we don't lose keys if partial update? 
        # For now, client sends full memory object.
        project['memory'] = memory
        self.save_project(project_id, project)
        return project

    def list_projects(self) -> list:
        projects = []
        if not os.path.exists(self.base_dir):
            return []
            
        for pid in os.listdir(self.base_dir):
            p_path = os.path.join(self.base_dir, pid)
            if os.path.isdir(p_path):
                p_data = self.get_project(pid)
                if p_data:
                    projects.append(p_data)
        
        # Sort by updated_at desc
        return sorted(projects, key=lambda x: x.get('updated_at', ''), reverse=True)

# Global singleton or dependency
manager = ProjectManager()
