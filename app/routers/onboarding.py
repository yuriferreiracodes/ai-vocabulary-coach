import uuid
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.flashcard import ChatMessage
from app.services.onboarding_service import OnboardingService

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])
templates = Jinja2Templates(directory="templates")

SESSION_COOKIE = "vocab_session"


def get_session_id(request: Request) -> str:
    return request.cookies.get(SESSION_COOKIE) or str(uuid.uuid4())


@router.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    message: ChatMessage,
    db: Session = Depends(get_db),
):
    session_id = get_session_id(request)
    svc = OnboardingService(db)

    result = svc.send_message(session_id, message.content)

    response = templates.TemplateResponse(
        "onboarding/partials/message.html",
        {
            "request": request,
            "user_message": message.content,
            "ai_reply": result["reply"],
            "onboarding_complete": result["onboarding_complete"],
        },
    )
    response.set_cookie(SESSION_COOKIE, session_id, httponly=True, samesite="lax")
    return response
