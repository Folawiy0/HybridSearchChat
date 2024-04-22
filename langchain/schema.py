from pydantic import BaseModel, model_validator
from typing import Dict, Any

class ChatGeneration(BaseModel):
    text: str

    @model_validator(pre=False, skip_on_failure=True)
    def set_text(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "text" in values:
            pass
        return values
