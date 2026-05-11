from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routes import auth, applications, resumes, ai, dashboard, users

app = FastAPI(
    title="HireTrack AI",
    description="Intelligent Job Application Management Platform",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(resumes.router)
app.include_router(ai.router)
app.include_router(dashboard.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to HireTrack AI", "version": "1.0.0"}