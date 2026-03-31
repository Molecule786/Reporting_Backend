from fastapi import APIRouter
from pydantic import BaseModel
import re

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    action: str | None = None

def get_ai_response(user_message: str) -> tuple[str, str | None]:
    message = user_message.lower()
    
    # Simple rule-based logic to guide users
    if "report" in message or "submit" in message:
        return "You can submit a new report or view your existing reports from the Dashboard. Would you like me to take you there?", "navigate_dashboard"
    elif "leave" in message or "vacation" in message or "time off" in message:
        return "I can help you with leave requests. You can submit a leave request directly from the Employee Dashboard.", "navigate_dashboard"
    elif "task" in message or "todo" in message or "job" in message:
        return "You can view and manage your assigned tasks in the Dashboard area.", "navigate_dashboard"
    elif "profile" in message or "account" in message:
        return "You can edit your profile details or change your password from the Profile section.", "navigate_profile"
    elif "admin" in message and "leave" in message:
        return "Administrators can review and approve leave requests from the Admin Dashboard.", "navigate_admin"
    elif "admin" in message:
        return "The Admin Dashboard provides full overview of reports, users, and leave requests.", "navigate_admin"
    elif "hello" in message or "hi" in message or "hey" in message:
        return "Hello! I am your AI assistant for Molecule WorkFlow Pro. I can guide you through reports, tasks, and leave requests. How can I help you today?", None
    else:
        return "I'm not quite sure how to help with that yet, but you can find most features like reports, tasks, and leave management in you dashboard. What are you looking to do?", None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    response, action = get_ai_response(chat_message.message)
    return ChatResponse(response=response, action=action)
