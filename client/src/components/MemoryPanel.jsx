import React, { useState, useEffect } from 'react';

export function MemoryPanel({ memory, onSave }) {
    const [visualStyle, setVisualStyle] = useState('');
    const [characters, setCharacters] = useState({});
    const [narrativeTone, setNarrativeTone] = useState('');

    // Local state for adding new character
    const [newCharName, setNewCharName] = useState('');
    const [newCharDesc, setNewCharDesc] = useState('');

    useEffect(() => {
        if (memory) {
            setVisualStyle(memory.visual_style || '');
            setCharacters(memory.characters || {});
            setNarrativeTone(memory.narrative_tone || '');
        }
    }, [memory]);

    const handleSave = () => {
        onSave({
            visual_style: visualStyle,
            characters: characters,
            narrative_tone: narrativeTone
        });
    };

    const addCharacter = () => {
        if (newCharName && newCharDesc) {
            setCharacters(prev => ({ ...prev, [newCharName]: newCharDesc }));
            setNewCharName('');
            setNewCharDesc('');
        }
    };

    const removeCharacter = (name) => {
        const next = { ...characters };
        delete next[name];
        setCharacters(next);
    };

    return (
        <div className="flex flex-col h-full overflow-y-auto pr-2">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-white">Memory & Context</h2>
                <button
                    onClick={handleSave}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg font-bold hover:bg-blue-400 transition-colors"
                >
                    Update Memory
                </button>
            </div>

            {/* Visual Style Section */}
            <section className="mb-8">
                <label className="block text-sm font-medium text-zinc-400 mb-2">Global Visual Style</label>
                <textarea
                    value={visualStyle}
                    onChange={(e) => setVisualStyle(e.target.value)}
                    placeholder="e.g. Cyberpunk 2077, Neon lights, rainy streets, cinematic 35mm..."
                    className="w-full h-24 bg-[#0f0f11] text-white border border-white/10 rounded-xl p-3 focus:ring-1 focus:ring-blue-500 outline-none text-sm"
                />
                <p className="text-xs text-zinc-600 mt-1">
                    This style is appended to every scene prompt.
                </p>
            </section>

            {/* Narrative Tone */}
            <section className="mb-8">
                <label className="block text-sm font-medium text-zinc-400 mb-2">Narrative Tone</label>
                <input
                    type="text"
                    value={narrativeTone}
                    onChange={(e) => setNarrativeTone(e.target.value)}
                    placeholder="e.g. Educational, Dark, Whimsical..."
                    className="w-full bg-[#0f0f11] text-white border border-white/10 rounded-xl p-3 focus:ring-1 focus:ring-blue-500 outline-none text-sm"
                />
            </section>

            {/* Characters Section */}
            <section>
                <label className="block text-sm font-medium text-zinc-400 mb-4">Character Registry</label>

                {/* List */}
                <div className="space-y-3 mb-6">
                    {Object.entries(characters).map(([name, desc]) => (
                        <div key={name} className="flex items-start gap-3 bg-[#1c1c1e] p-3 rounded-xl border border-white/5">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center font-bold text-xs shrink-0">
                                {name[0]}
                            </div>
                            <div className="flex-1 min-w-0">
                                <h4 className="font-bold text-sm text-zinc-200">{name}</h4>
                                <p className="text-xs text-zinc-400 truncate">{desc}</p>
                            </div>
                            <button
                                onClick={() => removeCharacter(name)}
                                className="text-zinc-500 hover:text-red-400"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                    {Object.keys(characters).length === 0 && (
                        <div className="text-center text-zinc-600 text-sm italic py-4">No characters defined</div>
                    )}
                </div>

                {/* Add New */}
                <div className="bg-[#0f0f11] p-4 rounded-xl border border-white/10">
                    <h5 className="text-xs font-bold text-zinc-500 uppercase mb-3">Add Character</h5>
                    <div className="flex gap-2 mb-2">
                        <input
                            type="text"
                            value={newCharName}
                            onChange={(e) => setNewCharName(e.target.value)}
                            placeholder="Name (e.g. Hero)"
                            className="flex-1 bg-[#27272a] text-white text-sm px-3 py-2 rounded-lg outline-none focus:ring-1 focus:ring-white/20"
                        />
                    </div>
                    <textarea
                        value={newCharDesc}
                        onChange={(e) => setNewCharDesc(e.target.value)}
                        placeholder="Visual description (e.g. A robot with a red scarf...)"
                        className="w-full h-20 bg-[#27272a] text-white text-sm px-3 py-2 rounded-lg outline-none focus:ring-1 focus:ring-white/20 mb-2 resize-none"
                    />
                    <button
                        onClick={addCharacter}
                        disabled={!newCharName || !newCharDesc}
                        className="w-full bg-white/5 hover:bg-white/10 text-zinc-300 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                    >
                        + Add to Registry
                    </button>
                </div>
            </section>
        </div>
    );
}
