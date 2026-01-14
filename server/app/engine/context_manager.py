from typing import Dict, Optional

class ContextManager:
    """
    Handles certain logic to inject 'Memory' (styles, characters) into generation prompts.
    """
    
    @staticmethod
    def apply_context(prompt: str, memory: Optional[Dict] = None) -> str:
        """
        Rewrites a scene prompt to include visual styles and character descriptions
        defined in the Memory object.
        """
        if not memory:
            return prompt
            
        enhanced_prompt = prompt
        
        # 1. Inject Character Descriptions
        characters = memory.get('characters', {})
        for name, description in characters.items():
            # Simple check if character name is in prompt (case-insensitiveish)
            if name.lower() in prompt.lower():
                # Avoid double description if already present (naive check)
                if description not in enhanced_prompt:
                    # Append description: "Professor (an elderly owl...)"
                    # Using a simple append for now to be robust
                    enhanced_prompt += f" -- Character Detail: {name} is {description}."

        # 2. Inject Global Visual Style
        visual_style = memory.get('visual_style')
        if visual_style:
            enhanced_prompt += f" -- Visual Style: {visual_style}."
            
        return enhanced_prompt

    @staticmethod
    def get_default_memory() -> Dict:
        return {
            "visual_style": "",
            "characters": {},
            "narrative_tone": ""
        }
