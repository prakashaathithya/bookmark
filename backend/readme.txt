docker run --name pg-local -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=bookmarks -p 5432:5432 -d postgres:16

cd C:\Users\Prakash\Documents\Python\bookmark

--python3 -m venv .venv #first time only
source .venv/bin/activate        # Windows: .venv\Scripts\activate(its working)
pip install -r requirements.txt

uvicorn main:app --reload --port 8000