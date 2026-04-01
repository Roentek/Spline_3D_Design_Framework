"""LLM client for routing natural language to Spline MCP tool calls via OpenRouter."""

import json
import httpx
from src.config import Config

SPLINE_SYSTEM_PROMPT = """\
You are a 3D design assistant that creates and manipulates 3D objects using the Spline API.
When the user describes a 3D object or scene they want, translate their request into concrete
Spline operations. Respond with a JSON object containing:

{
  "narration": "A friendly explanation of what you're creating/doing",
  "operations": [
    {
      "tool": "createObject",
      "params": {
        "sceneId": "<scene_id>",
        "type": "cube|sphere|cylinder|cone|torus|plane|text|light",
        "name": "ObjectName",
        "position": {"x": 0, "y": 0, "z": 0},
        "rotation": {"x": 0, "y": 0, "z": 0},
        "scale": {"x": 1, "y": 1, "z": 1},
        "color": "#hexcolor"
      }
    }
  ],
  "sceneDescription": "A brief summary of the current scene state after operations"
}

Available tools: createObject, updateObject, deleteObject, createMaterial, applyMaterial,
createLayeredMaterial, addMaterialLayer, addDirectionalLight, addCamera, configureFog,
configurePostProcessing, createState, createEvent, createAction, setVariable, configureApi.

Object types: cube, sphere, cylinder, cone, torus, plane, text, image, group, light.

Material types: standard, physical, basic, lambert, phong, toon, matcap, normal.
Material properties: color, roughness (0-1), metalness (0-1), opacity (0-1), transparent,
wireframe, emissive (hex), emissiveIntensity, side (front/back/double), flatShading.

Always respond with valid JSON. If the user asks something non-3D related, still use the
JSON format but set operations to an empty array and explain in the narration.

When no sceneId is provided, use "default" as the sceneId.
Compose multi-object scenes by issuing multiple createObject operations.
Choose realistic colors and proportions. Position objects so they don't overlap.
"""


async def chat_with_llm(
    message: str,
    history: list[dict],
    scene_id: str = "default",
    model: str | None = None,
) -> dict:
    """Send a message to the LLM and get structured Spline operations back."""
    cfg = Config()
    model = model or cfg.OPENROUTER_MODEL

    messages = [{"role": "system", "content": SPLINE_SYSTEM_PROMPT}]

    for entry in history[-20:]:
        messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({
        "role": "user",
        "content": f"[Active Scene ID: {scene_id}]\n\n{message}",
    })

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Spline 3D Design Framework",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4096,
                "response_format": {"type": "json_object"},
            },
        )
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "narration": content,
            "operations": [],
            "sceneDescription": "",
        }

    parsed["model"] = data.get("model", model)
    parsed["usage"] = {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }

    return parsed
