from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator
from .utils.prompts import SYSTEM_PROMPT, USER_PROMPT


class Parser(BaseModel):
    system_prompt: str = Field(
        title="System Prompt",
        default=SYSTEM_PROMPT,
        extra={"type": "TextArea"},
    )
    user_prompt: str = Field(
        title="user Prompt",
        default=USER_PROMPT,
        extra={"type": "TextArea"},
    )
    open_ai_api_key: str = ""

    @field_validator("open_ai_api_key")
    @classmethod
    def open_ai_api_key_validator(cls, api_key):
        if not api_key or api_key.strip() == "":
            raise ValueError("The OpenAI API key cannot be empty")
        return api_key


@plugin
def settings_model():
    return Parser
