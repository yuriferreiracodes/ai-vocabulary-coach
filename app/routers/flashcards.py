import uuid
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.flashcard import ReviewResult
from app.services.flashcard_service import FlashcardService

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"])
templates = Jinja2Templates(directory="templates")


@router.post("/{flashcard_id}/review", response_class=HTMLResponse)
async def review_flashcard(
    flashcard_id: uuid.UUID,
    result: ReviewResult,
    request: Request,
    db: Session = Depends(get_db),
):
    svc = FlashcardService(db)
    card = svc.record_review(flashcard_id, result.quality)
    return templates.TemplateResponse(
        "decks/partials/flashcard.html",
        {"request": request, "card": card, "reviewed": True},
    )
