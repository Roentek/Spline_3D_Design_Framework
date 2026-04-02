# Spline 3D Design Framework

## Project Overview

This is a framework for creating and controlling interactive 3D scenes using [Spline](https://spline.design) through AI-assisted natural language. It combines the **Spline MCP Server** with Claude Code to enable creating 3D objects, applying materials, setting up lighting, configuring events/animations, and generating embeddable code — all via conversational prompts.

Spline is a browser-based 3D design tool supporting real-time rendering, physics, animations, events, variables, and web/mobile export. The Spline API and `@splinetool/runtime` SDK allow programmatic control of scenes after export.

## MCP Servers

Configured in `.mcp.json`:

| Server | Purpose |
| -------- | --------- |
| **spline-mcp** | Create/manipulate 3D objects, scenes, materials, lighting, events, and generate runtime code |
| **tavily-mcp** | Web search and research |
| **openrouter-mcp** | Multi-model AI inference |

## Environment Variables

All keys are in `.env` (never committed). Required for Spline:

- `SPLINE_API_KEY` — from Spline Account Settings > API Keys

---

## Spline MCP Server Tools Reference

The `spline-mcp` server provides tools organized into these categories. All scene-modifying tools require a `sceneId` parameter.

### Scene Management

| Tool | Description |
| ------ | ------------- |
| `getScene` | Get scene details by ID |
| `getScenes` | List available scenes (supports `projectId`, `limit`, `offset`) |
| `exportSceneCode` | Generate code in `vanilla`, `react`, or `next` format |
| `generateEmbedCode` | Create HTML iframe embed code (`width`, `height`, `frameBorder`) |

### Object Creation & Manipulation

| Tool | Description |
| ------ | ------------- |
| `getObjects` | List all objects in a scene |
| `getObjectDetails` | Get details of a specific object |
| `createObject` | Create a 3D object with type, position, rotation, scale, color |
| `updateObject` | Modify position, rotation, scale, color, visibility of an object |
| `deleteObject` | Remove an object from the scene |
| `generateObjectCode` | Generate runtime code for object interactions |

**`createObject` types:** `cube`, `sphere`, `cylinder`, `cone`, `torus`, `plane`, `text`, `image`, `group`, `light`

**`createObject` parameters:**

- `type` (required) — object primitive type
- `name` (required) — object name
- `position` — `{x, y, z}` defaults to `{0, 0, 0}`
- `rotation` — `{x, y, z}` in degrees, defaults to `{0, 0, 0}`
- `scale` — `{x, y, z}` defaults to `{1, 1, 1}`
- `color` — hex string (e.g. `"#ff0000"`)
- `properties` — additional key-value properties

### Materials

| Tool | Description |
| ------ | ------------- |
| `getMaterials` | List all materials in a scene |
| `getMaterialDetails` | Get details of a specific material |
| `createMaterial` | Create a new material |
| `updateMaterial` | Modify material properties |
| `applyMaterial` | Assign a material to an object |

**Material types:** `standard`, `physical`, `basic`, `lambert`, `phong`, `toon`, `matcap`, `normal`

**Material properties:** `color`, `roughness` (0-1), `metalness` (0-1), `opacity` (0-1), `transparent`, `wireframe`, `emissive` (hex), `emissiveIntensity`, `side` (front/back/double), `flatShading`

### Advanced Materials (Layered)

| Tool | Description |
| ------ | ------------- |
| `createLayeredMaterial` | Create material with multiple composable layers |
| `addMaterialLayer` | Add a layer to an existing material |
| `configureColorLayer` | Set color and intensity |
| `configureImageLayer` | Apply texture with tiling, offset, rotation |
| `configureGradientLayer` | Create linear/radial/angular gradients |
| `configureNormalLayer` | Apply normal maps for surface detail |
| `configureFresnelLayer` | Edge-based reflectivity effects |
| `configureGlassLayer` | Transparent surfaces with refraction (tint, ior, roughness) |
| `configureMatcapLayer` | Pre-rendered material captures |
| `listMaterialLayers` | List all layers on a material |
| `deleteMaterialLayer` | Remove a layer |
| `reorderMaterialLayers` | Change layer stacking order |

**Spline material layer types available in the editor:** Color, Image, Video, Gradient, Noise, Fresnel, Rainbow, Toon, Outline, Glass, Matcap, Displace, Pattern, Normal, Depth/3D Gradient, Lighting

### Lighting & Camera

| Tool | Description |
| ------ | ------------- |
| `addDirectionalLight` | Add directional light (position, color, intensity, castShadow) |
| `addCamera` | Add camera (perspective/orthographic, position, target, fov 1-179) |
| `configureFog` | Set up atmospheric fog (color, density, near, far) |
| `configurePostProcessing` | Apply bloom and depth of field effects |

### States & Events

| Tool | Description |
| ------ | ------------- |
| `getStates` | List all states in a scene |
| `getStateDetails` | Get details of a specific state |
| `createState` | Create a state with property changes and transitions |
| `triggerState` | Activate a state |
| `getEvents` | List all events |
| `getEventDetails` | Get event details |
| `createEvent` | Create an event with type and actions |
| `triggerEvent` | Fire an event with optional data |
| `createComprehensiveEvent` | Create event with full configuration (23 event types) |
| `configureEventParameters` | Set event-specific parameters (key codes, distances, trigger areas, etc.) |
| `generateEventListenerCode` | Generate code for attaching event listeners |

**Event types:** `mouseDown`, `mouseUp`, `mouseOver`, `mouseOut`, `mouseMove`, `touchStart`, `touchEnd`, `touchMove`, `keyDown`, `keyUp`, `keyPress`, `scroll`, `collision`, `distance`, `triggerArea`, `lookAt`, `follow`, `stateChange`, `variableChange`, `start`, `dragAndDrop`, `aiAssistantTrigger`, `aiAssistantListener`, `custom`

### Actions

| Tool | Description |
| ------ | ------------- |
| `createAction` | Create an action attached to an event |
| `configureTransitionAction` | Set up state transitions with duration/easing |
| `configureSoundAction` | Audio playback (volume, loop, spatial 3D audio) |
| `configureAnimationAction` | Object animations (rotate, move, scale, fade) |
| `configureVariableAction` | Modify variables (set, increment, decrement, multiply, divide, toggle) |
| `configureConditionalAction` | Branch logic based on variable conditions |
| `configureApiRequestAction` | External API calls with response-to-variable mapping |
| `configureCameraAction` | Switch camera with transition |
| `listActions` | List all actions on an event |
| `deleteAction` | Remove an action |

**Action types:** `transition`, `sound`, `video`, `openLink`, `resetScene`, `switchCamera`, `createObject`, `destroyObject`, `sceneTransition`, `animation`, `particlesControl`, `variableControl`, `conditional`, `setVariable`, `clearLocalStorage`, `apiRequest`

### Variables

| Tool | Description |
| ------ | ------------- |
| `getVariable` | Read a scene variable |
| `setVariable` | Update a scene variable (string, number, or boolean) |
| `generateVariableCode` | Generate code for variable manipulation |

**Spline variable types:** Number, String, Boolean, Time (Clock/Timer/Stopwatch), Counter, Random

### API & Webhooks

| Tool | Description |
| ------ | ------------- |
| `configureApi` | Set up an API connection (method, URL, headers, body, variable mappings) |
| `getApis` | List all API connections |
| `deleteApi` | Remove an API connection |
| `createWebhook` | Create a webhook for scene events |
| `getWebhooks` | List webhooks |
| `deleteWebhook` | Remove a webhook |
| `triggerWebhook` | Manually invoke a webhook with data |
| `configureOpenAI` | Integrate OpenAI text generation into scenes |
| `generateTextWithOpenAI` | Generate AI text (prompt, model, maxTokens, temperature) |

### Code Generation & Runtime

| Tool | Description |
| ------ | ------------- |
| `getRuntimeSetup` | Get setup guidance for `@splinetool/runtime` integration |
| `generateComprehensiveExample` | Full code example for a scene |
| `generateAnimationCode` | Animation code (rotate/move/scale/color, duration, easing, loop) |
| `generateSceneInteractionCode` | Interaction code (explore, eventListeners, variables, camera, physics, custom) |
| `generateReactComponent` | React/TypeScript component wrapping a Spline scene |

### Design Tools (19 subcategories)

The server also registers tools for: Parametric Objects, Text, Particles, Physics, Boolean Operations, Cloner, Components, Extrusion, Gaussian Splatting, Hana, 3D Library, 3D Modeling, Multi-Scene, 3D Paths, Pen, 3D Sculpting, Shape Blend, UI Scenes, Version History.

---

## Spline Runtime SDK (`@splinetool/runtime`)

For client-side scene control after export. Install: `npm install @splinetool/runtime`

### Core Methods

```js
import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);
await app.load('https://prod.spline.design/<scene-url>/scene.splinecode');

// Object lookup
const obj = app.findObjectByName('MyCube');
const obj2 = app.findObjectById('uuid-here');
const all = app.getAllObjects();

// Object properties (read/write)
obj.position.x = 10;       // position {x, y, z}
obj.rotation.y = 45;       // rotation {x, y, z} in degrees
obj.scale.x = 2;           // scale {x, y, z}
obj.visible = false;        // visibility toggle
obj.intensity = 0.5;        // light intensity

// Events
app.emitEvent('mouseDown', 'ButtonName');
app.addEventListener('mouseDown', (e) => { /* handler */ });

// Variables
const val = app.getVariable('score');
app.setVariable('score', 42);

// Camera
app.setZoom(1.5);

// Playback
app.play();
app.stop();
```

### Supported Frameworks

- **Vanilla JS** — `@splinetool/runtime`
- **React** — `@splinetool/react-spline`
- **Next.js** — `@splinetool/react-spline/next`

---

## Spline AI Features (Require Pro/Team + AI Add-on)

These features are available in the Spline editor (not via MCP):

- **AI 3D Generation** — Text-to-3D, Image-to-3D, or Text+Image-to-3D. Best for single organic objects, generates 4 previews to choose from.
- **AI Textures** — Generate textures from text descriptions (grass, concrete, wood, etc.). Resolutions: 512x512, 1024x1024, 2048x2048.
- **AI Style Transfer** — Generate stylized images using 3D scenes as a base. Controls: seed, prompt, style presets, modifiers, precision, variance, mode (Outline/Edges/Shapes).
- **Spell AI 3D Worlds** — AI-generated 3D environments.

---

## Workflow Guidelines

### Creating a 3D Scene from Natural Language

1. **Get or create a scene** — Use `getScenes` to find existing scenes or work with a known `sceneId`
2. **Create objects** — Use `createObject` with primitive types (cube, sphere, cylinder, cone, torus, plane, text)
3. **Position objects** — Set `position`, `rotation`, `scale` on creation or via `updateObject`
4. **Apply materials** — Use `createMaterial` then `applyMaterial`, or use layered materials for complex surfaces
5. **Add lighting** — Use `addDirectionalLight`, configure intensity and shadows
6. **Set up camera** — Use `addCamera` with perspective/orthographic type and FOV
7. **Add interactivity** — Create events and actions for user interaction
8. **Add variables** — Use `setVariable` for dynamic state management
9. **Configure atmosphere** — Use `configureFog` and `configurePostProcessing` for visual polish
10. **Export** — Use `exportSceneCode` (vanilla/react/next) or `generateEmbedCode` for iframe embedding

### Best Practices

- Name all objects descriptively for easy reference in code
- Use hex colors consistently (e.g., `"#3498db"`)
- Set up variables before creating events that reference them
- Use layered materials for realistic surfaces (glass, metal, etc.)
- Test with `generateComprehensiveExample` to verify scene setup
- For complex scenes, build incrementally — create objects first, then materials, then events

### Export Formats Available in Spline

- **Web:** Public URLs, Spline Viewer, Code (Vanilla/React/Next.js), Self-hosted
- **Apple:** iOS embeds, visionOS Mirror, SwiftUI API
- **Android:** Native embeds, APK, AAB, Kotlin API
- **Files:** Images, Video, Image Sequences, GLTF/GLB, USDZ, STL (3D printing)

---

## Documentation Reference

- Spline Docs: <https://docs.spline.design/>
- Spline AI Docs index: <https://docs.spline.design/llms.txt>
- Spline MCP Server: <https://github.com/aydinfer/spline-mcp-server>
- Runtime NPM: <https://www.npmjs.com/package/@splinetool/runtime>
- React wrapper: <https://www.npmjs.com/package/@splinetool/react-spline>
