import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ScriptEditor } from './ScriptEditor';
import { MemoryPanel } from './MemoryPanel';
import { VideoPanel } from './VideoPanel';

export function Studio({ projectId, onBack }) {
    const [project, setProject] = useState(null);
    const [activeTab, setActiveTab] = useState('script'); // script, memory, video

    useEffect(() => {
        loadProject();
    }, [projectId]);

    const loadProject = async () => {
        try {
            const data = await api.getProject(projectId);
            setProject(data);
            // If script is missing, staying on script tab is fine. 
            // If completed, maybe default to video? For now sticky to script or user choice.
        } catch (err) {
            console.error(err);
            alert('Failed to load project');
        }
    };

    const handleScriptSave = async (newScript) => {
        try {
            const updated = await api.updateScript(projectId, newScript);
            setProject(updated);
            alert('Script saved!');
        } catch (err) {
            alert('Failed to save script');
        }
    };

    const handleMemorySave = async (newMemory) => {
        try {
            const updated = await api.updateMemory(projectId, newMemory);
            setProject(updated);
            alert('Memory settings updated!');
        } catch (err) {
            alert('Failed to update memory');
        }
    };

    if (!project) return <div className="text-white p-10">Loading Studio...</div>;

    return (
        <div className="flex flex-col h-screen bg-black text-white font-sans selection:bg-purple-500 selection:text-white">
            {/* Top Bar */}
            <header className="h-16 border-b border-white/10 flex items-center px-6 justify-between bg-[#0f0f11]">
                <div className="flex items-center gap-4">
                    <button
                        onClick={onBack}
                        className="text-zinc-500 hover:text-white transition-colors"
                    >
                        ← Back
                    </button>
                    <div className="h-6 w-px bg-white/10" />
                    <h1 className="font-bold text-lg truncate max-w-md">{project.topic || project.name}</h1>
                </div>

                {/* Tabs */}
                <div className="hidden md:flex gap-1 bg-white/5 p-1 rounded-lg">
                    {['script', 'memory', 'video'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all capitalize
                 ${activeTab === tab ? 'bg-white text-black shadow-lg' : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}
                        >
                            {tab === 'video' && project.status === 'completed' ? '✨ Video' : tab}
                        </button>
                    ))}
                </div>

                <div className="w-20" /> {/* Spacer for balance */}
            </header>

            {/* Main Content */}
            <main className="flex-1 overflow-hidden p-6 relative">

                {/* Mobile Tab Switcher (Visible only on small screens) */}
                <div className="md:hidden flex mb-4 gap-2 overflow-x-auto pb-2">
                    {['script', 'memory', 'video'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-2 rounded-full text-sm font-bold border transition-colors capitalize shrink-0
                     ${activeTab === tab ? 'bg-white text-black border-white' : 'border-white/20 text-zinc-400'}`}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                <div className="h-full max-w-6xl mx-auto">
                    {activeTab === 'script' && (
                        <ScriptEditor
                            script={project.script}
                            onSave={handleScriptSave}
                        />
                    )}

                    {activeTab === 'memory' && (
                        <MemoryPanel
                            memory={project.memory}
                            onSave={handleMemorySave}
                        />
                    )}

                    {activeTab === 'video' && (
                        <VideoPanel
                            project={project}
                            onRefresh={setProject}
                        />
                    )}
                </div>
            </main>
        </div>
    );
}
