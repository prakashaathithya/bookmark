import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://app:app@localhost:5432/bookmarks"
)
engine = create_engine(DATABASE_URL)


class Bookmark(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    url: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # creates the table on startup
    yield


app = FastAPI(title="Bookmarks API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/bookmarks")
def list_bookmarks():
    with Session(engine) as session:
        return session.exec(select(Bookmark)).all()


@app.post("/api/bookmarks")
def create_bookmark(bookmark: Bookmark):
    with Session(engine) as session:
        session.add(bookmark)
        session.commit()
        session.refresh(bookmark)
        return bookmark


@app.delete("/api/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    with Session(engine) as session:
        bm = session.get(Bookmark, bookmark_id)
        if not bm:
            raise HTTPException(status_code=404, detail="Not found")
        session.delete(bm)
        session.commit()
        return {"deleted": bookmark_id}