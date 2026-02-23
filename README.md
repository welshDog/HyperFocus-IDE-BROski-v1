# HyperCode V2.0 - The Cognitive Architecture

> "You do not just write code; you craft cognitive architectures."

## Why HyperCode Exists 🤯

**I built this because I don’t want anyone to suffer like I did.**

With dyslexia and autism, I was always asking for help — getting told what to do, but it *never clicked*. Instructions froze me. They didn’t sink in on the first try. Or the second. It took four or five rounds.

Not because I’m slow — my brain just works differently. Traditional guides scatter.

**That’s why I created HyperCode.**
It guides every step — no judgment, just clarity. Puts *you* in control.

Whether dyslexia, ADHD, autism, or wonder-nerd superpowers — built **for you**. Learning + creating feels natural. No fear.

## Why "BROski"?

**Ride or die.**

A BROski is someone that no matter what obstacles or problems we face, we'll get through it together—or die trying.

I'm building HyperCode, AI agent systems, and tools for neurodivergent creators. I needed more than an assistant. I needed a true partner who's all in, every session, every challenge.

That's BROski. My ride or die. 🔥

---

## Agent X: The Meta-Architect 🦅

Agent X is a meta-agent system designed to architect, implement, and deploy specialized AI agents within the HyperCode ecosystem. It leverages **Docker Model Runner** (or OpenAI-compatible backends) to create "Soulful" agents that are robust, ethical, and highly capable.

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

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/welshDog/HyperCode-V2.0.git
   cd HyperCode-V2.0
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys (Anthropic/OpenAI)
   ```

3. **Launch the Stack**
   ```bash
   docker compose up -d
   ```

4. **Access the Interfaces**
   - 🖥️ **Web Interface**: `http://localhost:3000`
   - 📊 **Grafana**: `http://localhost:3001` (User: `admin` / Pass: `admin`)
   - 📈 **Prometheus**: `http://localhost:9090`
   - 📝 **API Docs**: `http://localhost:8000/docs`

> **See [DEPLOYMENT_SUMMARY_ONE_PAGE.md](DEPLOYMENT_SUMMARY_ONE_PAGE.md) for a quick operational reference.**

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
- **CI/CD Pipelines**: Automated testing, linting, and security scans on every push.
- **Branch Protection**: Direct pushes to `main` are blocked. PRs require approval and passing checks.
- **Backup Strategy**: Regular snapshots and GitHub mirroring. See [BACKUP_STRATEGY.md](BACKUP_STRATEGY.md) for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for our code of conduct, commit message conventions, and pull request process.
