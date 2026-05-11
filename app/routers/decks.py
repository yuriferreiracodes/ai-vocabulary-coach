import uuid
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.deck_service import DeckService

router = APIRouter(prefix="/api/decks", tags=["decks"])
templates = Jinja2Templates(directory="templates")

SESSION_COOKIE = "vocab_session"


def get_session_id(request: Request) -> str:
    return request.cookies.get(SESSION_COOKIE) or ""


@router.post("/generate", response_class=HTMLResponse)
async def generate_deck(
    request: Request,
    topic: str = Form(...),
    count: int = Form(default=10),
    db: Session = Depends(get_db),
):
    session_id = get_session_id(request)
    svc = DeckService(db)

    try:
        deck = svc.generate_deck(session_id, topic, count)
        return templates.TemplateResponse(
            "decks/partials/deck_card.html",
            {"request": request, "deck": deck, "new": True},
        )
    except ValueError as exc:
        return HTMLResponse(f'<div class="text-red-500 p-4">{exc}</div>', status_code=400)


@router.delete("/{deck_id}", response_class=HTMLResponse)
async def delete_deck(
    deck_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    session_id = get_session_id(request)
    svc = DeckService(db)
    svc.delete_deck(session_id, deck_id)
    return HTMLResponse("")
