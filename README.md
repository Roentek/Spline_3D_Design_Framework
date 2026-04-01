# Spline 3D Design Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A framework for creating and controlling interactive 3D scenes using [Spline](https://spline.design) through AI-assisted natural language. Chat with an LLM to build 3D objects, apply materials, set up lighting, and see results in a live Three.js viewport — all from your browser.

---

## What is Spline?

[Spline](https://spline.design) is a 3D design tool that lets you create interactive, real-time 3D scenes directly in the browser. It supports animations, physics, events, and variables — all exportable to the web with minimal setup.

The **Spline API** is a set of tools and SDKs that allow developers to embed those scenes into their own apps and control them programmatically — triggering animations, manipulating objects, reading and writing variables, and responding to 3D scene events using JavaScript or TypeScript.

---

## About This Project

This repository provides a **local web application** for building 3D scenes with natural language. It includes:

- A **chat interface** where you describe objects, materials, and scenes in plain English
- A **live 3D viewport** (Three.js) that renders objects in real time as the AI creates them
- A **FastAPI backend** that routes your messages through OpenRouter to an LLM, which returns structured Spline operations
- **MCP server integrations** for Spline, Tavily, Supabase, and OpenRouter

---

## Key Features

- **Natural language 3D creation** — Describe what you want and watch it appear in the viewport
- **Live Three.js preview** — Orbit, zoom, pan, wireframe toggle, and camera presets
- **Scene object tracking** — Real-time object list with type icons and color swatches
- **Multi-model support** — Switch between Claude, GPT-4o, Gemini, or OpenRouter Auto
- **Spline MCP integration** — 70+ tools for objects, materials, lighting, events, animations, and code generation
- **SSE live updates** — Server-Sent Events push scene changes to all connected viewers
- **One-click VS Code launch** — F5 starts the server and opens your browser

---

## Project Structure

```text
Spline_3D_Design_Framework/
├── .vscode/
│   ├── launch.json             # Debug config — "Spline 3D Start Server"
│   └── tasks.json              # Auto-opens browser on launch
├── src/
│   ├── __init__.py
│   ├── config.py               # Environment variable loader
│   └── llm_client.py           # OpenRouter LLM client with Spline system prompt
├── templates/
│   └── index.html              # Frontend — chat panel + Three.js 3D viewport
├── static/                     # Static assets (favicon, images)
├── server.py                   # FastAPI server (chat, SSE, scene state)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .mcp.json                   # MCP server configuration
├── CLAUDE.md                   # Full Spline MCP tools reference for Claude Code
├── LICENSE                     # MIT license
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Spline_3D_Design_Framework
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Fill in your API keys:

| Variable | Required | Description |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | Yes | OpenRouter key for AI model access |
| `SPLINE_API_KEY` | For MCP | Spline API key — Account Settings > API Keys |
| `SUPABASE_API_PAT` | Optional | Supabase personal access token |
| `SUPABASE_PROJECT_URL` | Optional | Your Supabase project URL |
| `SUPABASE_PROJECT_KEY` | Optional | Supabase anon or service role key |
| `TAVILY_API_KEY` | Optional | Tavily API key for web search |
| `SERVER_HOST` | No | Defaults to `127.0.0.1` |
| `SERVER_PORT` | No | Defaults to `8080` |

### 4. Get your Spline API key

1. Sign in at [spline.design](https://spline.design)
2. Go to **Account Settings > API Keys**
3. Generate a new key and add it to your `.env` file

### 5. Launch the application

**Option A — VS Code (recommended):**

Press **F5** to start the debug configuration "Spline 3D Start Server". The browser opens automatically at `http://localhost:8080`.

**Option B — Terminal:**

```bash
python server.py
```

Then open `http://localhost:8080` in your browser.

---

## How It Works

```text
User types: "Create a red metallic sphere floating above a dark plane"
        │
        ▼
   FastAPI /chat endpoint
        │
        ▼
   OpenRouter LLM (Claude, GPT-4o, Gemini, etc.)
        │
        ▼
   Structured JSON response with Spline operations:
   [createObject sphere, createObject plane, ...]
        │
        ▼
   Server tracks scene state + broadcasts via SSE
        │
        ▼
   Frontend renders objects in Three.js viewport
```

The chat panel shows the AI's narration and a summary of operations executed. The 3D viewport updates in real time with orbit controls, wireframe mode, camera presets (Reset, Top, Front), and a live object list.

---

## Spline API Quick Reference

The Spline runtime lets you interact with exported 3D scenes:

```js
import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);

await app.load('https://prod.spline.design/your-scene-url/scene.splinecode');

// Find and manipulate objects
const obj = app.findObjectByName('MyCube');
obj.position.x = 5;
obj.rotation.y = 45;
obj.scale.set(2, 2, 2);

// Trigger events
app.emitEvent('mouseDown', 'Button');

// Variables
app.setVariable('score', 42);
const value = app.getVariable('score');
```

---

## MCP Servers Configured

This project includes MCP (Model Context Protocol) server integrations for use with Claude Code:

| Server | Purpose |
| --- | --- |
| **Spline** | Create/manipulate 3D objects, materials, lighting, events, and generate runtime code |
| **Tavily** | Web search and research |
| **Supabase** | Database operations and edge functions |
| **OpenRouter** | Multi-model AI inference |

See [CLAUDE.md](CLAUDE.md) for the complete Spline MCP tools reference (70+ tools across 10 categories).

---

## License

MIT License - Copyright (c) 2026 Roentek Designs

See [LICENSE](LICENSE) for details.
