import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export function ProjectList({ onSelectProject }) {
    const [projects, setProjects] = useState([]);
    const [newTopic, setNewTopic] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadProjects();
    }, []);

    const loadProjects = async () => {
        const data = await api.listProjects();
        setProjects(data);
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        if (!newTopic) return;

        setLoading(true);
        try {
            const project = await api.createProject(newTopic);
            await loadProjects();
            setNewTopic('');
            onSelectProject(project.id);
        } catch (err) {
            console.error(err);
            alert('Failed to create project');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6">
            <header className="mb-12 text-center">
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-2">
                    Creative Memory Layer
                </h1>
                <p className="text-zinc-500">Select a project or start a new vision.</p>
            </header>

            {/* Creator Bar */}
            <form onSubmit={handleCreate} className="mb-12 flex gap-4">
                <input
                    type="text"
                    value={newTopic}
                    onChange={(e) => setNewTopic(e.target.value)}
                    placeholder="Enter a topic needed (e.g. 'The Future of AI')..."
                    className="flex-1 bg-[#1c1c1e] text-white border border-white/10 rounded-xl px-6 py-4 focus:ring-2 focus:ring-purple-500 outline-none transition-all placeholder-zinc-600"
                />
                <button
                    disabled={loading || !newTopic}
                    className="bg-white text-black px-8 py-4 rounded-xl font-bold hover:bg-zinc-200 disabled:opacity-50 transition-colors"
                >
                    {loading ? 'Creating...' : 'Create Project'}
                </button>
            </form>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map(project => (
                    <div
                        key={project.id}
                        onClick={() => onSelectProject(project.id)}
                        className="group bg-[#0f0f11] border border-white/5 hover:border-purple-500/50 p-6 rounded-2xl cursor-pointer transition-all hover:-translate-y-1 relative overflow-hidden"
                    >
                        <div className="absolute top-0 right-0 p-4 opacity-50 text-xs font-mono text-zinc-500">
                            {new Date(project.updated_at).toLocaleDateString()}
                        </div>

                        <h3 className="text-xl font-bold text-white mb-2 line-clamp-2">
                            {project.topic}
                        </h3>

                        <div className="flex items-center gap-2 mt-4">
                            <span className={`px-2 py-1 rounded-md text-xs font-medium uppercase tracking-wider
                 ${project.status === 'completed' ? 'bg-green-500/10 text-green-400' :
                                    project.status === 'failed' ? 'bg-red-500/10 text-red-400' :
                                        'bg-blue-500/10 text-blue-400'}`}>
                                {project.status}
                            </span>
                            <span className="text-xs text-zinc-600 font-mono">
                                {project.mode}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            {projects.length === 0 && (
                <div className="text-center text-zinc-600 py-20">
                    No projects yet. Create one to begin.
                </div>
            )}
        </div>
    );
}
