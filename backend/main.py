from backend.documents import doc_route

from fastapi import FastAPI
import uvicorn

app = FastAPI(debug=True)
app.include_router(doc_route)

if __name__ == '__main__':

    uvicorn.run(app=app, host='127.0.0.1' ,port=8080)