import os
import shutil
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.engine import scriptor, artist, audio, director, veo, storage

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Storage
project_manager = storage.ProjectManager(base_dir="storage")

# Request Models
class CreateProjectRequest(BaseModel):
    name: str = "Untitled Project"
    topic: str
    mode: str = "text_to_video" # text_to_video, image_constrained, video_extension
    parent_project_id: Optional[str] = None

class UpdateScriptRequest(BaseModel):
    script: Dict[str, Any]

class UpdateMemoryRequest(BaseModel):
    memory: Dict[str, Any]

class GenerateRequest(BaseModel):
    mode: Optional[str] = None # Optional override

# --- Helper Functions ---

def run_project_generation(project_id: str):
    """
    Background task to execute generation based on project state.
    """
    project = project_manager.get_project(project_id)
    if not project:
        return

    # Update status
    project['status'] = 'running'
    project_manager.save_project(project_id, project)
    
    project_dir = project_manager._get_project_path(project_id)
    mode = project.get('mode', 'text_to_video')
    
    try:
        # 1. Scripting (if not present)
        if mode == 'text_to_video' and not project.get('script'):
            project['status'] = 'scripting'
            project_manager.save_project(project_id, project)
            
            script_data = scriptor.generate_script(project['topic'])
            project_manager.update_script(project_id, script_data)
            project = project_manager.get_project(project_id) # Reload

        # 2. Asset Generation
        project['status'] = 'generating_assets'
        project_manager.save_project(project_id, project)
        
        output_path = os.path.join(project_dir, "final.mp4")
        
        # Extract Memory
        project_memory = project.get('memory', {})
        
        if mode == "image_constrained":
             success = veo.generate_image_constrained_video(
                 project['topic'], 
                 output_path, 
                 log_prefix="[Image-Constrained] "
             )
        
        elif mode == "video_extension":
             # TODO: Handle parent video linking logic more robustly
             pass 
             success = False
             project['error'] = "Extension mode refactor in progress"
             
        else:
            # Text-to-Video / Script-based
            script = project.get('script')
            if not script:
                 raise Exception("No script found to generate from")
            
            total_scenes = len(script['scenes'])
            
            for idx, scene in enumerate(script['scenes']):
                s_id = scene['id']
                
                # Audio
                audio_path = os.path.join(project_dir, f"scene_{s_id}.mp3")
                if not os.path.exists(audio_path):
                     audio.generate_audio(scene['voiceover'], audio_path)
                
                # Visuals
                video_path = os.path.join(project_dir, f"scene_{s_id}.mp4")
                image_path = os.path.join(project_dir, f"scene_{s_id}.png")
                
                if not os.path.exists(video_path):
                    log_prefix = f"[Scene {idx+1}/{total_scenes}] "
                    veo_success = False
                    try:
                        # PASS MEMORY CONTEXT HERE
                        veo_success = veo.generate_veo_clip(
                            scene['visual_prompt'], 
                            video_path, 
                            context=project_memory,
                            log_prefix=log_prefix
                        )
                    except Exception as e:
                        print(f"Veo gen failed: {e}")
                    
                    if not veo_success:
                         print(f"Fallback to Imagen for Scene {s_id}")
                         artist.generate_image(scene['visual_prompt'], image_path)

            # 3. Rendering
            project['status'] = 'rendering'
            project_manager.save_project(project_id, project)
            
            success = director.render_video(script, project_dir, output_path)

        if success:
            project['status'] = 'completed'
            project['video_url'] = f"/static/{project_id}/final.mp4"
        else:
            project['status'] = 'failed'
            if not project.get('error'):
                project['error'] = "Generation/Rendering failed"

        project_manager.save_project(project_id, project)

    except Exception as e:
        print(f"Project Job failed: {e}")
        project['status'] = 'failed'
        project['error'] = str(e)
        project_manager.save_project(project_id, project)


# --- API Endpoints ---

@app.post("/api/projects")
async def create_project(request: CreateProjectRequest):
    """Create a new project container."""
    project = project_manager.create_project(
        name=request.name,
        topic=request.topic,
        mode=request.mode
    )
    return project

@app.get("/api/projects")
async def list_projects():
    """List all projects."""
    return project_manager.list_projects()

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get full project state."""
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/api/projects/{project_id}/script")
async def update_script(project_id: str, request: UpdateScriptRequest):
    """Update the script (Source of Truth)."""
    project = project_manager.update_script(project_id, request.script)
    if not project:
         raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/api/projects/{project_id}/memory")
async def update_memory(project_id: str, request: UpdateMemoryRequest):
    """Update the persistent memory (Style/Characters)."""
    project = project_manager.update_memory(project_id, request.memory)
    if not project:
         raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/api/projects/{project_id}/generate")
async def generate_project(project_id: str, background_tasks: BackgroundTasks):
    """Trigger the generation process for a project."""
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    background_tasks.add_task(run_project_generation, project_id)
    return {"status": "queued", "project_id": project_id}

# --- Legacy Support (Optional) ---
# Keeping the old endpoint temporarily if needed, or mapping it to new flow.
# For strict migration, we remove it. The user approved the plan which implied changes.
# But for the frontend to work immediately, we might need it.
# Let's map the old endpoint to the new flow for backward compatibility if possible,
# OR just break it as planned. Plan said "Breaking API Change". I will execute the break.

# Mount storage as static resources (videos)
os.makedirs("storage", exist_ok=True)
app.mount("/static", StaticFiles(directory="storage"), name="static")

# Mount Frontend (Static Files)
# We assume the frontend build is copied to 'app/static_ui' in the Docker image
frontend_dir = os.path.join(os.path.dirname(__file__), "static_ui")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="ui_assets")

    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        # Allow API calls to pass through
        if full_path.startswith("api/") or full_path.startswith("static/"):
             raise HTTPException(status_code=404, detail="Not Found")
        
        # Serve index.html for React Router
        return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/")
def read_root():
    # If frontend exists, serve it
    if os.path.exists(frontend_dir):
        return FileResponse(os.path.join(frontend_dir, "index.html"))
    return {"status": "ok", "message": "Creative Memory Layer API (v2) - Frontend not found"}


