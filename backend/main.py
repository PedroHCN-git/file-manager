from backend.documents import doc_route
from backend.infra.session_manager import create_tables
from backend.auth.auth_route import auth_route
from backend.users.user_route import user_route

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

create_tables()

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?",
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
app.include_router(doc_route)
app.include_router(auth_route)
app.include_router(user_route)

if __name__ == '__main__':

    uvicorn.run(app=app, host='127.0.0.1' ,port=8080)