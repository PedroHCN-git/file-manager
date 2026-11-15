from backend.documents import doc_route
from backend.infra.session_manager import create_tables
from backend.users import user_route

from fastapi import FastAPI
import uvicorn

create_tables()

app = FastAPI(debug=True)
app.include_router(doc_route)
app.include_router(user_route)

if __name__ == '__main__':

    uvicorn.run(app=app, host='127.0.0.1' ,port=8080)