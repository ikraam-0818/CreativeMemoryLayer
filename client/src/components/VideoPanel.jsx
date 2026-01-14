import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export function VideoPanel({ project, onRefresh }) {
    const [generating, setGenerating] = useState(false);
    const [status, setStatus] = useState(project.status || 'idle');
    const [videoUrl, setVideoUrl] = useState(project.video_url);

    // Poll status while running
    useEffect(() => {
        if (project.status === 'running' || project.status === 'scripting' || project.status === 'generating_assets' || project.status === 'rendering') {
            const interval = setInterval(async () => {
                const p = await api.getProject(project.id);
                setStatus(p.status);
                if (p.status === 'completed' || p.status === 'failed') {
                    setVideoUrl(p.video_url);
                    onRefresh(p); // Update parent state
                    clearInterval(interval);
                }
            }, 2000);
            return () => clearInterval(interval);
        } else {
            setStatus(project.status);
            setVideoUrl(project.video_url);
        }
    }, [project]);

    const handleGenerate = async () => {
        try {
            setGenerating(true);
            await api.generateVideo(project.id);
            onRefresh(await api.getProject(project.id)); // Force reload to start polling
        } catch (err) {
            alert("Generation failed to start");
        } finally {
            setGenerating(false);
        }
    };

    const getStatusLabel = () => {
        switch (status) {
            case 'scripting': return 'Writing Script...';
            case 'generating_assets': return 'Creating Visuals (Veo)...';
            case 'rendering': return 'Rendering Audio & Video...';
            case 'completed': return 'Ready';
            case 'failed': return 'Generation Failed';
            default: return status;
        }
    };

    return (
        <div className="flex flex-col h-full justify-center items-center">
            {/* Video Player Main Stage */}
            <div className="w-full aspect-video bg-black rounded-2xl border border-white/5 shadow-2xl overflow-hidden relative group max-h-[60vh]">
                {videoUrl ? (
                    <video
                        src={`http://localhost:8000${videoUrl}`}
                        controls
                        className="w-full h-full object-contain"
                        autoPlay={status === 'completed'} // Autoplay if just finished
                    />
                ) : (
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center">
                        {status === 'created' || status === 'script_ready' ? (
                            <div className="text-zinc-500">
                                <p className="mb-4">Project is ready to generate.</p>
                                <p className="text-xs opacity-50">Review the Script and Memory tabs first.</p>
                            </div>
                        ) : (
                            <div className="flex flex-col items-center gap-4">
                                <div className="w-12 h-12 border-2 border-white/10 border-t-purple-500 rounded-full animate-spin"></div>
                                <p className="text-zinc-200 animate-pulse font-mono tracking-widest uppercase text-xs">
                                    {getStatusLabel()}
                                </p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Controls */}
            <div className="mt-8 flex gap-4 w-full max-w-lg justify-center">
                <button
                    onClick={handleGenerate}
                    disabled={status === 'running' || status === 'scripting' || status === 'generating_assets' || status === 'rendering'}
                    className="bg-white text-black px-8 py-3 rounded-full font-bold hover:bg-zinc-200 disabled:opacity-50 transition-all flex items-center gap-2"
                >
                    {status === 'completed' ? 'Regenerate Video' : 'Generate Video'}
                </button>

                {videoUrl && (
                    <a
                        href={`http://localhost:8000${videoUrl}`}
                        download={`video_${project.id}.mp4`}
                        className="bg-zinc-800 text-white px-6 py-3 rounded-full font-medium hover:bg-zinc-700 transition-all"
                    >
                        Download
                    </a>
                )}
            </div>

            {project.error && (
                <div className="mt-4 text-red-400 text-sm bg-red-500/10 px-4 py-2 rounded-lg border border-red-500/20">
                    Error: {project.error}
                </div>
            )}
        </div>
    );
}
