
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.routes import node_routes , auth
from .core.database import _engine
from .db.migrations import run_db_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically check database changes and sync schemas on server start/restart
    run_db_migrations(_engine)
    yield


app = FastAPI(
    title = "NodePilot Control Plane",
    description = "LangGraph orchestration, MCP gateway, policies, approvals, node registry, and audit services",
    version = "0.0.1",
    lifespan = lifespan,
)

app.include_router(node_routes.route)

app.include_router(auth.route)


@app.get("/health")
async def health():
    return {"status" :  "ok"}

@app.get("/version")
async def version():
    return {"version" :  "0.0.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

