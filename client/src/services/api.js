const BASE_URL = import.meta.env.PROD ? '/api' : 'http://localhost:8000/api';

export const api = {
    // Projects
    createProject: async (topic, mode = 'text_to_video') => {
        const res = await fetch(`${BASE_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, mode })
        });
        return res.json();
    },

    listProjects: async () => {
        const res = await fetch(`${BASE_URL}/projects`);
        return res.json();
    },

    getProject: async (projectId) => {
        const res = await fetch(`${BASE_URL}/projects/${projectId}`);
        return res.json();
    },

    // Updates
    updateScript: async (projectId, script) => {
        const res = await fetch(`${BASE_URL}/projects/${projectId}/script`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ script })
        });
        return res.json();
    },

    updateMemory: async (projectId, memory) => {
        const res = await fetch(`${BASE_URL}/projects/${projectId}/memory`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ memory })
        });
        return res.json();
    },

    // Generation
    generateVideo: async (projectId) => {
        const res = await fetch(`${BASE_URL}/projects/${projectId}/generate`, {
            method: 'POST'
        });
        return res.json();
    }
};
