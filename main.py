from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import coverletter, jd, linkedin, pitch, resume

app = FastAPI(title="cvDoctor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(jd.router)
app.include_router(coverletter.router)
app.include_router(linkedin.router)
app.include_router(pitch.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
