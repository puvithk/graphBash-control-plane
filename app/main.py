
from fastapi import FastAPI
from .api.routes import node_routes , auth


app = FastAPI(
    title = "NodePilot Control Plane",
    description = "LangGraph orchestration, MCP gateway, policies, approvals, node registry, and audit services",
    version = "0.0.1",
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
    uvicorn.run(app, host="[IP_ADDRESS]", port=8080)
