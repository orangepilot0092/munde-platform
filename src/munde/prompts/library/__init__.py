"""
Munde Prompt Library - Central registry of all agent prompts.
"""
from munde.prompts.base import PromptLibrary
from munde.prompts.library.jalsetu import register_jalsetu_prompts
from munde.prompts.library.krishisetu import register_krishisetu_prompts

# Initialize and populate the library
prompt_library = PromptLibrary()

# Register all agent prompts
register_jalsetu_prompts(prompt_library)
register_krishisetu_prompts(prompt_library)

# Future agents will be added here:
# register_nagarsetu_prompts(prompt_library)
# register_arogyasetu_prompts(prompt_library)
# etc.

__all__ = ["prompt_library", "PromptLibrary"]
