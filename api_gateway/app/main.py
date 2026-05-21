from fastapi import FastAPI

from .routers.auth_proxy import router as auth_router
from .routers.library_proxy import router as library_router
from .routers.progress_proxy import router as progress_router
from .routers.tracker_proxy import router as tracker_router
from .routers.metadata_proxy import router as metadata_router
from .routers.recommendations_proxy import router as recommendations_router

app = FastAPI(
    title="API Gateway",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(library_router)
app.include_router(progress_router)
app.include_router(tracker_router)
app.include_router(metadata_router)
app.include_router(recommendations_router)


@app.get("/health")
def health_check():
    return {
        "service": "api_gateway",
        "status": "ok",
    }