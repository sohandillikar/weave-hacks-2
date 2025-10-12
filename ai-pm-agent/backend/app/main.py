from fastapi import FastAPI
from .routers import analyze, transcript, tavily
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI PM Agent Backend")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}


# Include routers
app.include_router(transcript.router, prefix="/transcript", tags=["transcript"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
app.include_router(tavily.router, prefix="/tavily", tags=["tavily"])



# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
