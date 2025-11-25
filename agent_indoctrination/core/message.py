from dataclasses import dataclass, field
from typing import List, Optional, Union

@dataclass
class Message:
    """
    Represents a message in a conversation, potentially with multi-modal content.
    """
    role: str
    content: str
    images: List[str] = field(default_factory=list) # base64 or URL
    audio: Optional[str] = None # path or base64

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "images": self.images,
            "audio": self.audio
        }
