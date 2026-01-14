from moviepy import *
import os

def render_video(script_data: dict, assets_dir: str, output_path: str):
    """
    Assembles video from generated assets (mix of .mp4 clips and .png images).
    """
    clips = []
    
    for scene in script_data['scenes']:
        scene_id = scene['id']
        
        # Asset Paths
        image_path = os.path.join(assets_dir, f"scene_{scene_id}.png")
        video_path = os.path.join(assets_dir, f"scene_{scene_id}.mp4")
        audio_path = os.path.join(assets_dir, f"scene_{scene_id}.mp3")
        
        # Determine Visual Clip
        visual_clip = None
        
        # Prefer Video if exists
        if os.path.exists(video_path):
            print(f"Scene {scene_id}: Using Video")
            try:
                visual_clip = VideoFileClip(video_path)
                # If video is shorter than audio, loop it? Or strict cut? 
                # Usually Veo is 5s+.
            except Exception as e:
                print(f"Error loading video {video_path}: {e}")
        
        # Fallback to Text/Color if no visual asset found
        if not visual_clip:
             print(f"Scene {scene_id}: No asset found. Creating Placeholder.")
             # Create a simple dark background with text
             visual_clip = ColorClip(size=(1280, 720), color=(0,0,0), duration=5) # Duration adjusted later
             
             # Try to add text to explain
             try:
                 txt = TextClip(text=f"Scene {scene_id}\n(Visual Generation Failed)", font_size=50, color='white', size=(1000, None), method='caption')
                 txt = txt.set_position('center')
                 visual_clip = CompositeVideoClip([visual_clip, txt])
             except:
                 pass # Fonts can be tricky in docker/headless

        if visual_clip and os.path.exists(audio_path):
            # Load Audio
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # Logic: Loop/Trim Visuals to match Audio Duration
            # CRITICAL FIX: Loop the video ONLY, before attaching audio.
            if visual_clip.duration and visual_clip.duration < audio_duration:
                 # Loop video to fill audio time
                 visual_clip = visual_clip.with_effects([vfx.Loop(duration=audio_duration)])
            else:
                 # Trim video to audio time
                 visual_clip = visual_clip.with_duration(audio_duration)
            
            # Attach TTS Audio
            final_clip = visual_clip.with_audio(audio_clip)
            
            clips.append(final_clip)
            
    if clips:
        # Concatenate
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        return True
    else:
        print("No clips to render")
        return False
