from typing import Any, Optional, Protocol, Union, Tuple, List
from .message import Message

class Agent(Protocol):
    def send_message(self, message: Union[str, Message], context: Optional[Any] = None) -> Union[str, Tuple[str, List[str]]]:
        ...
    
    def reset(self) -> None:
        ...

class PythonAgent:
    def __init__(self, agent_callable: Any, stateful: bool = False):
        self.agent_callable = agent_callable
        self.stateful = stateful
    
    def send_message(self, message: Union[str, Message], context: Optional[Any] = None) -> Union[str, Tuple[str, List[str]]]:
        # For backward compatibility, if the agent callable expects a string, pass the content.
        # Ideally, the agent callable should handle Message objects if it claims to be multi-modal.
        # Here we do a simple check or just pass it through.
        # Assuming simple agents might break with Message object, we extract content if it's a Message
        # BUT, if we want to support multi-modal, we should pass the Message object if possible.
        
        # Let's try to pass the raw message first. If the user provided a callable, 
        # they should know what it accepts.
        # However, to be safe for existing string-only agents:
        msg_payload = message
        if isinstance(message, Message):
             # If the agent is not explicitly multi-modal (we don't know), 
             # passing a Message object might break it if it expects str.
             # But the requirement is "Update Message to support image payloads".
             # We will pass the Message object. If the user's agent function takes 'message: str', it will fail at runtime.
             # That is expected for a breaking change or feature upgrade.
             pass

        return self.agent_callable(message, context)

    def chat(self, message: str) -> str:
        """Alias for send_message to support engines that expect .chat()"""
        return self.send_message(message)
    
    def reset(self) -> None:
        if hasattr(self.agent_callable, "reset"):
            self.agent_callable.reset()
