# UI/CLI Flow Design Specification: HyperCode Agent Control Center

## 1. Overview
This specification details the user interface and command-line flow for the HyperCode Agent Orchestrator. The goal is to provide a seamless, transparent, and actionable interface for users to define tasks, view strategic plans, monitor agent execution, and analyze results.

**Target Audience:** Developers (Neurodivergent-focused: clean, low-clutter, high-contrast options).
**Core Philosophy:** "Command & Control" - User sets intent, Agents execute, User reviews.

---

## 2. CLI Design (HyperFlow Terminal)

The CLI is the primary interface for rapid interaction. It uses a structured, interactive display (like `rich` or `ink` for React CLI).

### 2.1. Task Input Mode
**Command:** `hyper run` or `./broski-cli start`

**Interface:**
```text
┌───────────────────────────────────────────────────────────────┐
│  🚀 HyperCode Agent Crew v2.3                                 │
└───────────────────────────────────────────────────────────────┘
  
  What is your mission?
  > Build a habit tracker with React and Python_
  
  [Context Options (Use arrow keys)]:
  [x] High Priority
  [ ] MVP Scope
  [ ] Mobile Responsive
  
  [Press ENTER to Launch]
```

### 2.2. Strategist Plan Display
Once the task is submitted, the **Project Strategist** takes over.

**Interface:**
```text
┌── 🧠 Project Strategist ──────────────────────────────────────┐
│  Analyzing request... Done.                                   │
│                                                               │
│  🎯 Mission: Full-Stack Habit Tracker                         │
│  ⏱️  Est. Time: 160h  |  📊 Complexity: High                  │
│                                                               │
│  📋 Execution Plan:                                           │
│  1. [DevOps] Infrastructure Setup (Docker, CI/CD)             │
│  2. [Database] Schema Design (Users, Habits, Streaks)         │
│  3. [Backend] Auth & CRUD API (FastAPI)                       │
│  4. [Frontend] UI Implementation (React + Tailwind)           │
│  5. [QA] Testing & Verification                               │
│                                                               │
│  [y] Approve Plan   [n] Refine   [q] Quit                     │
└───────────────────────────────────────────────────────────────┘
```

### 2.3. Specialist Call Visualization (Real-Time)
As agents execute, the CLI updates in real-time using a split-pane or progress bars.

**Interface:**
```text
┌── ⚡ Active Agents ───────────────────────────────────────────┐
│                                                               │
│  🔹 Frontend Specialist   [==========  ] 65% | Generating UI  │
│     > Creating HabitCard.tsx...                               │
│     > Adding Tailwind classes...                              │
│                                                               │
│  🔸 Backend Specialist    [✓ Done      ] 100% | API Ready     │
│     > POST /habits endpoint created.                          │
│                                                               │
│  🔹 QA Engineer           [Pending     ] Waiting for FE...    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 2.4. Consolidated Results Panel
Final summary after all agents complete.

**Interface:**
```text
┌── ✅ Mission Accomplished ────────────────────────────────────┐
│                                                               │
│  📂 Artifacts Generated:                                      │
│  - /backend/app/routes/habits.py                              │
│  - /frontend/src/components/HabitCard.tsx                     │
│  - /database/migrations/001_initial.sql                       │
│                                                               │
│  📝 Summary:                                                  │
│  Successfully built MVP features. Frontend connects to API.   │
│  Database schema applied.                                     │
│                                                               │
│  [View Report]  [Open VS Code]  [Deploy]                      │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. Web UI Design (HyperFlow Dashboard)

The Web UI provides a richer, visual experience with drag-and-drop capabilities and detailed analytics.

### 3.1. Layout Structure
- **Sidebar:** Navigation (Mission Control, Agents, Settings, History).
- **Main Area:** Dynamic content based on state.
- **Status Bar:** Global system health (Redis, Core, API Latency).

### 3.2. Task Input (Mission Control)
- **Central Input Field:** Large, focus-mode text area.
- **Context Chips:** Clickable tags for constraints (e.g., "Next.js", "Python", "Secure").
- **Voice Input:** Microphone icon for dictation.

### 3.3. Execution View (The "Flow")
- **Visual Node Graph:**
    - **Strategist Node** (Top) -> Connected to Specialist Nodes.
    - **Active Nodes** pulse with color (Blue = Thinking, Green = Done, Red = Error).
- **Live Logs:** Collapsible side panel showing raw agent logs.
- **Artifact Preview:** Tabbed view to see code being generated in real-time.

### 3.4. Results & Review
- **Diff View:** Side-by-side comparison of generated code vs. existing.
- **Chat Interface:** "Ask a follow-up" input to refine specific parts of the result.
- **One-Click Actions:** "Commit to Git", "Run Tests", "Deploy to Preview".

---

## 4. Technical Specifications

### 4.1. Frontend Stack
- **Framework:** Next.js (React 18)
- **Styling:** Tailwind CSS + Framer Motion (animations)
- **State Management:** Zustand (local) + TanStack Query (server)
- **Icons:** Lucide React

### 4.2. Component Hierarchy
```
src/components/
├── mission/
│   ├── TaskInput.tsx         # Main entry point
│   ├── ContextSelector.tsx   # Chips/Options
│   └── PlanReview.tsx        # Strategist output display
├── monitoring/
│   ├── AgentStatusCard.tsx   # Individual agent state
│   ├── LiveLogViewer.tsx     # WebSocket stream renderer
│   └── ResourceUsage.tsx     # CPU/RAM metrics
├── results/
│   ├── ArtifactExplorer.tsx  # File tree of generated code
│   └── CodePreview.tsx       # Syntax highlighted viewer
└── layout/
    ├── Sidebar.tsx
    └── StatusBar.tsx
```

### 4.3. Data Flow
1. **User Input** -> `POST /hyperrun`
2. **Orchestrator** -> Broadcasts events via Redis Pub/Sub (`agent_events` channel).
3. **WebSocket Server** -> Pushes events to Frontend Client.
4. **Frontend Store** -> Updates Agent Status map (`{ "frontend": "working", ... }`).
5. **UI** -> Re-renders AgentStatusCard components.

### 4.4. Error Handling
- **Network Error:** Toast notification with "Retry" button.
- **Agent Failure:**
    - UI highlights the failed agent node in Red.
    - "Debug" button opens the raw log/traceback.
    - Option to "Retry Step" or "Skip".

---

## 5. Quality Assurance
- **Performance:**
    - Initial Load: < 1.5s (LCP)
    - Interaction Latency: < 100ms
- **Accessibility:**
    - ARIA labels on all interactive elements.
    - Keyboard navigation support (Tab flow).
    - High-contrast mode toggle.
- **Responsiveness:**
    - Desktop (1440px+): Full graph view.
    - Tablet (768px): Stacked view.
    - Mobile (375px): Simplified list view.
