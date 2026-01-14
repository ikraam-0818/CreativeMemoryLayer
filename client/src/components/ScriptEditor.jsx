import React, { useState, useEffect } from 'react';

export function ScriptEditor({ script, onSave }) {
    const [localScript, setLocalScript] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        if (script) {
            setLocalScript(JSON.stringify(script, null, 2));
        }
    }, [script]);

    const handleSave = () => {
        try {
            const parsed = JSON.parse(localScript);
            setError(null);
            onSave(parsed);
        } catch (err) {
            setError("Invalid JSON: " + err.message);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-white">Script Editor</h2>
                <button
                    onClick={handleSave}
                    className="bg-white text-black px-4 py-2 rounded-lg font-bold hover:bg-zinc-200 transition-colors"
                >
                    Save Changes
                </button>
            </div>

            {error && (
                <div className="bg-red-500/10 text-red-400 p-3 rounded-lg mb-4 text-sm font-mono border border-red-500/20">
                    {error}
                </div>
            )}

            <div className="flex-1 relative">
                <textarea
                    value={localScript}
                    onChange={(e) => setLocalScript(e.target.value)}
                    className="w-full h-full bg-[#0f0f11] text-zinc-300 font-mono text-sm p-4 rounded-xl border border-white/10 focus:ring-2 focus:ring-purple-500 outline-none resize-none leading-relaxed"
                    spellCheck="false"
                />
            </div>

            <p className="text-xs text-zinc-600 mt-2">
                Edit the scenes, visual prompts, or voiceover text directly. Ensure JSON format is valid.
            </p>
        </div>
    );
}
