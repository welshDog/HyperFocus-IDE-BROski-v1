# HyperCode V2.0 - The Cognitive Architecture

> "You do not just write code; you craft cognitive architectures."

![HyperCode Mission Control Dashboard](docs/assets/Screenshot%20of%20IDE%20TOP%202026-02-25.png)

## Why HyperCode Exists 🤯

**HyperCode is a cognitive prosthetic for your coding brain.**

Traditional IDEs demand rote memorization and endless context switching—the very things that paralyze neurodivergent minds. HyperCode replaces this friction with a collaborative **AI Agent Swarm (HyperSwarm)** that handles the executive function tax for you. Whether you have ADHD, dyslexia, or autism, HyperCode aligns with how you actually think: visually, creatively, and in bursts of hyperfocus.

It’s not just a tool. It’s a partner. Your "BROski"—ride or die.

**[Read the full manifesto & story →](docs/STORY.md)**

---

## ⚡ Quick Start

Get the entire ecosystem running in **under 2 minutes**.

## 🚀 Performance & Benchmarks

HyperCode V3.0 is optimized for high-concurrency environments:

- **100+ Concurrent Agents**
- **< 800ms Latency (P99)**
- **60 FPS Real-time Visualization**

See [PERFORMANCE.md](PERFORMANCE.md) for load testing details and results.

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- **Perplexity API Key** (for agent intelligence)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/welshDog/HyperCode-V2.0.git
   cd HyperCode-V2.0
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your PERPLEXITY_API_KEY
   ```

3. **Launch the Stack**
   ```bash
   docker compose up -d
   ```

4. **Access the Interfaces**
   - 🖥️ **Web Interface (Dashboard)**: `http://localhost:3000/dashboard`
   - 🧠 **Orchestrator API**: `http://localhost:8080/docs`
   - 📊 **Grafana**: `http://localhost:3001` (User: `admin` / Pass: `admin`)
   - 📈 **Prometheus**: `http://localhost:9090`

> **See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed instructions.**

---

## 🏗️ Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system design.

## 📂 Project Structure

- **THE HYPERCODE/**: Core application logic.
  - `hypercode-core`: FastAPI backend service.
  - `hyperflow-editor`: React/Vite frontend editor.
- **BROski Business Agents/**: Autonomous agent system configurations.
- **agents/**: Specialized AI agents (Frontend, Backend, QA, etc.).
- **docker/**: Docker configuration and build scripts.
- **docs/**: Comprehensive documentation.
- **.github/workflows/**: CI/CD pipelines.

## 🛡️ Development Workflow & Backup

We enforce strict development practices to ensure stability:
- **Technical Standards**: All code follows the [Hyper Dev Vibe Coder Technical Standards](HDVC-Technical.md).
- **CI/CD Pipelines**: Automated testing, linting, and security scans on every push.
- **Branch Protection**: Direct pushes to `main` are blocked. PRs require approval and passing checks.
- **Backup Strategy**: Regular snapshots and GitHub mirroring. See [BACKUP_STRATEGY.md](BACKUP_STRATEGY.md) for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for our code of conduct, commit message conventions, and pull request process.
