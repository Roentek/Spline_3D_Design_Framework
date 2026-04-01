"""Spline 3D Design Framework — FastAPI server."""

import json
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from src.config import Config
from src.llm_client import chat_with_llm

# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
_config: Config | None = None
_sse_queues: list[asyncio.Queue] = []

# In-memory scene object registry (for the 3D preview)
_scene_objects: dict[str, list[dict]] = {}  # sceneId -> [objects]


def _broadcast(event: str, data: dict) -> None:
    for q in _sse_queues:
        q.put_nowait({"event": event, "data": json.dumps(data)})


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _config
    _config = Config()
    _broadcast("status", {"message": "Server ready", "type": "info"})
    yield


app = FastAPI(title="Spline 3D Design Framework", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES_DIR = Path(__file__).parent / "templates"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    return (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/config")
async def get_config():
    cfg = _config or Config()
    return {
        "defaultModel": cfg.OPENROUTER_MODEL,
        "hasSplineKey": bool(cfg.SPLINE_API_KEY),
    }


@app.get("/scene-events")
async def scene_events():
    """SSE stream for real-time scene update notifications."""
    queue: asyncio.Queue = asyncio.Queue()
    _sse_queues.append(queue)

    async def stream():
        try:
            while True:
                msg = await queue.get()
                yield f"event: {msg['event']}\ndata: {msg['data']}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            _sse_queues.remove(queue)

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "").strip()
    scene_id = body.get("sceneId", "default")
    history = body.get("history", [])
    model = body.get("model")

    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)

    try:
        result = await chat_with_llm(message, history, scene_id, model)
    except Exception as exc:
        return JSONResponse(
            {"error": _friendly_error(exc)},
            status_code=502,
        )

    # Register created objects in our in-memory store
    operations = result.get("operations", [])
    if scene_id not in _scene_objects:
        _scene_objects[scene_id] = []

    for op in operations:
        tool = op.get("tool", "")
        params = op.get("params", {})

        if tool == "createObject":
            obj = {
                "id": f"obj_{len(_scene_objects[scene_id])}",
                "type": params.get("type", "cube"),
                "name": params.get("name", "Untitled"),
                "position": params.get("position", {"x": 0, "y": 0, "z": 0}),
                "rotation": params.get("rotation", {"x": 0, "y": 0, "z": 0}),
                "scale": params.get("scale", {"x": 1, "y": 1, "z": 1}),
                "color": params.get("color", "#888888"),
            }
            _scene_objects[scene_id].append(obj)

        elif tool == "updateObject":
            target = params.get("name", "")
            for existing in _scene_objects[scene_id]:
                if existing["name"] == target:
                    if "position" in params:
                        existing["position"] = params["position"]
                    if "rotation" in params:
                        existing["rotation"] = params["rotation"]
                    if "scale" in params:
                        existing["scale"] = params["scale"]
                    if "color" in params:
                        existing["color"] = params["color"]

        elif tool == "deleteObject":
            target = params.get("name", "")
            _scene_objects[scene_id] = [
                o for o in _scene_objects[scene_id] if o["name"] != target
            ]

    # Broadcast scene update to all connected viewers
    _broadcast("scene-update", {
        "sceneId": scene_id,
        "objects": _scene_objects.get(scene_id, []),
        "operations": operations,
    })

    return {
        "narration": result.get("narration", ""),
        "operations": operations,
        "sceneDescription": result.get("sceneDescription", ""),
        "objects": _scene_objects.get(scene_id, []),
        "model": result.get("model", ""),
        "usage": result.get("usage", {}),
    }


@app.get("/scene/{scene_id}")
async def get_scene(scene_id: str):
    return {"sceneId": scene_id, "objects": _scene_objects.get(scene_id, [])}


@app.delete("/scene/{scene_id}")
async def clear_scene(scene_id: str):
    _scene_objects[scene_id] = []
    _broadcast("scene-update", {"sceneId": scene_id, "objects": []})
    return {"status": "cleared"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _friendly_error(exc: Exception) -> str:
    msg = str(exc).lower()
    if "401" in msg or "unauthorized" in msg:
        return "API key invalid or missing. Check your OPENROUTER_API_KEY in .env"
    if "429" in msg or "rate" in msg:
        return "Rate limited by the AI provider. Wait a moment and try again."
    if "timeout" in msg:
        return "Request timed out. The AI model may be overloaded — try again."
    return f"LLM request failed: {exc}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    cfg = Config()
    uvicorn.run(
        "server:app",
        host=cfg.SERVER_HOST,
        port=cfg.SERVER_PORT,
        reload=True,
    )
