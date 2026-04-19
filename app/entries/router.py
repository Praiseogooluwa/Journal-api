from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.entries.models import Entry
from app.entries.schemas import EntryCreate, EntryResponse, EntryUpdate
from app.auth.utils import get_current_user
from app.tags.models import Tag
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/entries", tags=["entries"])

@router.post("/", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_entry = Entry(
        title=entry.title,
        content=entry.content,
        mood=entry.mood,
        date=entry.date,
        user_id=current_user.id
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    for tag_name in entry.tags:
        tag_name = tag_name.lower()
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        if tag not in new_entry.tags:
            new_entry.tags.append(tag)

    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/entry", response_model=list[EntryResponse])
def get_entries(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entries = db.query(Entry).filter(Entry.user_id == current_user.id).all()
    return entries

@router.get("/summary", response_model=dict[str, str])
def get_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entries = db.query(Entry).filter(Entry.user_id == current_user.id).order_by(Entry.date.desc()).limit(7).all()
    if not entries:
        return {"summary": "No entries found for this week."}

    moods = [entry.mood for entry in entries]
    topics = [entry.title for entry in entries]

    summary = f"This week you made {len(entries)} entries. "
    summary += f"Your moods were: {', '.join(moods)}. "
    summary += f"You worked on: {', '.join(topics)}. "
    summary += "Keep up the consistency and try to go deeper on the topics you explored."

    return {"summary": summary}

@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return entry

@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: int, entry_data: EntryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    if entry_data.title is not None:
        entry.title = entry_data.title
    if entry_data.content is not None:
        entry.content = entry_data.content
    if entry_data.mood is not None:
        entry.mood = entry_data.mood
    if entry_data.date is not None:
        entry.date = entry_data.date
    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return None