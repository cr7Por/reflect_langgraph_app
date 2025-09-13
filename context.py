"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated


@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    generation_prompt: str = field(
        default="you are a helpful assistant, you can answer questions and help with tasks.",
        metadata={
            "description": "The prompt to use for the content generations. "
            "This prompt sets the context and behavior for the agent.",
        },
    )

    reflection_prompt: str = field(
        default="you are a thinker, you can reflect on the generated content and give advice on how to improve it.",
        metadata={
            "description": "The prompt to use for the reflections on content. "
            "This prompt sets the context and behavior for the reflect agent.",
        },
    )

      

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        import os
        from dataclasses import fields

        for f in fields(self):
            if not f.init:
                continue

            current_value = getattr(self, f.name)
            default_value = f.default
            env_var_name = f.name.upper()
            env_value = os.environ.get(env_var_name)

            # Only override with environment variable if current value equals default
            # This preserves explicit configuration from LangGraph configurable
            if current_value == default_value and env_value is not None:
                if isinstance(default_value, bool):
                    # Handle boolean environment variables
                    env_bool_value = env_value.lower() in ("true", "1", "yes", "on")
                    setattr(self, f.name, env_bool_value)
                else:
                    setattr(self, f.name, env_value)
