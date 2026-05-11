import uuid
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.deck_service import DeckService
from app.services.onboarding_service import OnboardingService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SESSION_COOKIE = "vocab_session"


def get_session_id(request: Request) -> str:
    return request.cookies.get(SESSION_COOKIE) or str(uuid.uuid4())


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    svc = OnboardingService(db)
    user = svc.get_or_create_session(session_id)

    response = templates.TemplateResponse(
        "index.html", {"request": request, "user": user}
    )
    response.set_cookie(SESSION_COOKIE, session_id, httponly=True, samesite="lax")
    return response


@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    svc = OnboardingService(db)
    user = svc.get_or_create_session(session_id)
    conversation = svc.get_conversation_history(user)

    response = templates.TemplateResponse(
        "onboarding/chat.html",
        {"request": request, "user": user, "conversation": conversation},
    )
    response.set_cookie(SESSION_COOKIE, session_id, httponly=True, samesite="lax")
    return response


@router.get("/decks", response_class=HTMLResponse)
async def decks(request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    svc = DeckService(db)
    user_decks = svc.list_decks(session_id)
    onboarding_svc = OnboardingService(db)
    user = onboarding_svc.get_or_create_session(session_id)

    return templates.TemplateResponse(
        "decks/list.html",
        {"request": request, "decks": user_decks, "user": user},
    )


@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def deck_detail(deck_id: uuid.UUID, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    svc = DeckService(db)
    deck = svc.get_deck(session_id, deck_id)
    if not deck:
        return HTMLResponse("Deck not found", status_code=404)

    from app.services.flashcard_service import FlashcardService
    fc_svc = FlashcardService(db)
    due_cards = fc_svc.get_due_cards(deck_id)

    return templates.TemplateResponse(
        "decks/detail.html",
        {"request": request, "deck": deck, "due_cards": due_cards},
    )
