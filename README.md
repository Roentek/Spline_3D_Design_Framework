# Spline 3D Design Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A plug-and-play framework for integrating interactive 3D scenes built in [Spline](https://spline.design) into websites and applications using the Spline API.

---

## What is Spline?

[Spline](https://spline.design) is a 3D design tool that lets you create interactive, real-time 3D scenes directly in the browser. It supports animations, physics, events, and variables — all exportable to the web with minimal setup.

The **Spline API** is a set of tools and SDKs that allow developers to embed those scenes into their own apps and control them programmatically — triggering animations, manipulating objects, reading and writing variables, and responding to 3D scene events using JavaScript or TypeScript.

---

## About This Project

This repository is a **starter template and framework** for working with the Spline API. It provides a structured foundation for:

- Embedding Spline scenes into web projects
- Interacting with 3D objects, animations, and variables via code
- Integrating Spline with AI tools, databases, and external services using MCP servers

Use this as a starting point when building apps that combine Spline's interactive 3D capabilities with backend services or AI workflows.

---

## Key Features

- **Spline API integration** — Load and control 3D scenes, trigger events, and read/write scene variables
- **MCP server support** — Pre-configured connections to Tavily, Supabase and OpenRouter
- **OpenRouter AI** — Flexible model routing for AI-powered interactions within 3D experiences
- **Supabase backend** — Database and edge functions ready for 3D app data persistence
- **Environment-based configuration** — All API keys managed via `.env` (never committed)

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Spline_3D_Design_Framework
```

### 2. Configure environment variables

Copy the example env file and fill in your API keys:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `SPLINE_API_KEY` | Spline API key — found in your Spline account settings under API Keys |
| `OPENROUTER_API_KEY` | OpenRouter key for AI model access |
| `SUPABASE_API_PAT` | Supabase personal access token (for MCP) |
| `SUPABASE_PROJECT_URL` | Your Supabase project URL |
| `SUPABASE_PROJECT_KEY` | Supabase anon or service role key |
| `TAVILY_API_KEY` | Tavily API key for web search |

### 3. Get your Spline API key

1. Sign in at [spline.design](https://spline.design)
2. Go to **Account Settings → API Keys**
3. Generate a new key and add it to your `.env` file

---

## Spline API Quick Reference

The Spline runtime lets you interact with your 3D scene after it loads:

```js
import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);

await app.load('https://prod.spline.design/your-scene-url/scene.splinecode');

// Trigger an event on a named object
app.emitEvent('mouseDown', 'Button');

// Read a variable
const value = app.getVariable('score');

// Set a variable
app.setVariable('score', 42);
```

---

## MCP Servers Configured

This project includes MCP (Model Context Protocol) server integrations for use with Claude Code:

| Server | Purpose |
| --- | --- |
| Spline | Access and control Spline scenes |
| Tavily | Web search and research |
| Supabase | Database operations and edge functions |
| OpenRouter | Multi-model AI inference |

---

## License

MIT License - Copyright (c) 2026 Roentek Designs

See [LICENSE](LICENSE) for details.
