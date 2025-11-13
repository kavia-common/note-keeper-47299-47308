from typing import Dict, List, Optional
import uuid
from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Initialize FastAPI with metadata for better OpenAPI docs
app = FastAPI(
    title="Notes Backend API",
    description=(
        "A lightweight FastAPI backend providing health checks and in-memory CRUD stubs "
        "for a notes resource. This is a stub implementation intended for wiring and UI integration."
    ),
    version="0.1.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness endpoints."},
        {"name": "Notes", "description": "In-memory CRUD stubs for notes."},
        {"name": "Docs", "description": "Helper endpoints with usage information."},
    ],
)

# Keep CORS permissive to support preview environments and different origins
# We do not hardcode URLs; if needed, env vars can be used later for restriction.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permissive per requirement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database" for notes; simple dict keyed by note id
NOTES_STORE: Dict[str, Dict[str, str]] = {}


# Pydantic models

class NoteBase(BaseModel):
    """Base note fields shared by create/update models."""
    title: str = Field(..., description="Title of the note")
    content: str = Field("", description="Body/content of the note")


class NoteCreate(NoteBase):
    """Model for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Model for updating a note."""
    title: Optional[str] = Field(None, description="Updated title of the note")
    content: Optional[str] = Field(None, description="Updated content of the note")


class Note(NoteBase):
    """Full Note model returned by the API."""
    id: str = Field(..., description="Unique identifier (UUID4) for the note")


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns a simple JSON payload to indicate the service is healthy.",
    responses={200: {"description": "Healthy response with a message"}},
)
def health_check() -> Dict[str, str]:
    """Root health check endpoint."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/api",
    tags=["Docs"],
    summary="API usage notes",
    description="Provides helpful information for using the API and where to find the docs.",
    responses={200: {"description": "Informational usage response"}},
)
def api_usage() -> Dict[str, str]:
    """Helper endpoint pointing to docs and notes resource."""
    return {
        "docs": "/docs",
        "openapi": "/openapi.json",
        "notes_collection": "/api/notes",
        "health": "/",
        "message": "Explore the interactive Swagger UI at /docs. This backend exposes in-memory CRUD for /api/notes.",
    }


# NOTES ROUTES (in-memory stubs)

# PUBLIC_INTERFACE
@app.get(
    "/api/notes",
    tags=["Notes"],
    summary="List notes",
    description="Returns all notes currently stored in memory.",
    response_model=List[Note],
    responses={
        200: {"description": "List of notes"},
    },
)
def list_notes() -> List[Note]:
    """List all notes in the in-memory store."""
    return [Note(id=nid, title=ndata["title"], content=ndata.get("content", "")) for nid, ndata in NOTES_STORE.items()]


# PUBLIC_INTERFACE
@app.post(
    "/api/notes",
    tags=["Notes"],
    summary="Create note",
    description="Creates a new note and returns it.",
    response_model=Note,
    responses={201: {"description": "Note created"}},
    status_code=201,
)
def create_note(note: NoteCreate = Body(..., description="Payload to create a new note")) -> Note:
    """Create a new note with a generated UUID."""
    new_id = str(uuid.uuid4())
    NOTES_STORE[new_id] = {"title": note.title, "content": note.content}
    return Note(id=new_id, title=note.title, content=note.content)


# PUBLIC_INTERFACE
@app.get(
    "/api/notes/{note_id}",
    tags=["Notes"],
    summary="Get note by id",
    description="Retrieves a note by its id.",
    response_model=Note,
    responses={
        200: {"description": "Note found"},
        404: {"description": "Note not found"},
    },
)
def get_note(
    note_id: str = Path(..., description="UUID of the note"),
) -> Note:
    """Get a single note by id."""
    data = NOTES_STORE.get(note_id)
    if not data:
        raise HTTPException(status_code=404, detail="Note not found")
    return Note(id=note_id, title=data["title"], content=data.get("content", ""))


# PUBLIC_INTERFACE
@app.put(
    "/api/notes/{note_id}",
    tags=["Notes"],
    summary="Replace note",
    description="Replaces the title and content of a note.",
    response_model=Note,
    responses={
        200: {"description": "Note updated"},
        404: {"description": "Note not found"},
    },
)
def replace_note(
    note_id: str = Path(..., description="UUID of the note"),
    note: NoteCreate = Body(..., description="New data for the note"),
) -> Note:
    """Replace all fields of an existing note."""
    if note_id not in NOTES_STORE:
        raise HTTPException(status_code=404, detail="Note not found")
    NOTES_STORE[note_id] = {"title": note.title, "content": note.content}
    return Note(id=note_id, title=note.title, content=note.content)


# PUBLIC_INTERFACE
@app.patch(
    "/api/notes/{note_id}",
    tags=["Notes"],
    summary="Update note (partial)",
    description="Updates one or more fields of a note.",
    response_model=Note,
    responses={
        200: {"description": "Note updated"},
        404: {"description": "Note not found"},
    },
)
def update_note(
    note_id: str = Path(..., description="UUID of the note"),
    note: NoteUpdate = Body(..., description="Partial update payload"),
) -> Note:
    """Partially update a note's fields."""
    data = NOTES_STORE.get(note_id)
    if not data:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.title is not None:
        data["title"] = note.title
    if note.content is not None:
        data["content"] = note.content
    NOTES_STORE[note_id] = data
    return Note(id=note_id, title=data["title"], content=data.get("content", ""))


# PUBLIC_INTERFACE
@app.delete(
    "/api/notes/{note_id}",
    tags=["Notes"],
    summary="Delete note",
    description="Deletes a note by its id.",
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"},
    },
    status_code=204,
)
def delete_note(
    note_id: str = Path(..., description="UUID of the note"),
) -> None:
    """Delete a note from the store."""
    if note_id not in NOTES_STORE:
        raise HTTPException(status_code=404, detail="Note not found")
    del NOTES_STORE[note_id]
    # 204 No Content returns empty body by default
    return None
