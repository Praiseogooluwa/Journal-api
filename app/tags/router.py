from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import get_current_user
from app.entries.models import Entry
from app.tags.models import Tag
from app.tags.schemas import TagCreate, TagResponse

router = APIRouter(tags=["tags"])

@router.post("/entries/{entry_id}/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def add_tag(entry_id: int, tag_data: TagCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    tag_name = tag_data.name.lower()
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)

    if tag in entry.tags:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists on this entry")

    entry.tags.append(tag)
    db.commit()
    return tag

@router.delete("/entries/{entry_id}/tags/{tag_name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag(entry_id: int, tag_name: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    tag = db.query(Tag).filter(Tag.name == tag_name.lower()).first()
    if not tag or tag not in entry.tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found on this entry")

    entry.tags.remove(tag)
    db.commit()
    return None

@router.get("/entries/filter", response_model=list[dict])
def filter_by_tag(tag: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tag_obj = db.query(Tag).filter(Tag.name == tag.lower()).first()
    if not tag_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    entries = db.query(Entry).filter(
        Entry.user_id == current_user.id,
        Entry.tags.any(Tag.name == tag.lower())
    ).all()

    return [{"id": e.id, "title": e.title, "date": str(e.date), "mood": e.mood} for e in entries]