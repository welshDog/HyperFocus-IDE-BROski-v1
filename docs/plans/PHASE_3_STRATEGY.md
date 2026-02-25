# Phase 3 Strategy: Robustness & Accessibility

**Goal:** Transform the prototype into a hardened, accessible product that neurodivergent developers can rely on daily.

## 1. Executive Summary
Phase 2 successfully proved the architecture scales (2 replicas, <0.1% error rate). However, the "missed" latency target (2.56s vs 300ms) and the lack of test dependencies reveal a critical need for **robustness**. Simultaneously, the "Neurodivergent-First" promise requires us to move beyond "dark mode" into true **accessibility** (ARIA, keyboard nav, screen reader support).

## 2. Priority 1: Testing & Stability (The "Confidence" Layer)
*Rationale: We cannot ask users to trust an "exoskeleton for their brain" if it breaks silently.*

### Tasks
*   **Fix CI Pipeline:** The `ci-python.yml` and `test.yml` workflows need to be unified. The missing `pytest` dependency in `requirements.txt` was a critical catch.
*   **Expand Test Suite:**
    *   **Unit:** Increase coverage from ~0% (current) to >80% for `hypercode-core`.
    *   **Integration:** Add tests for the `Redis -> Celery -> Agent` pipeline.
*   **Performance Optimization:** Investigate the 2.56s latency.
    *   *Hypothesis:* Cold start of LLM clients or database connection pooling.
    *   *Action:* Implement `KeepAlive` for HTTP clients and tune SQLAlchemy pool size.

## 3. Priority 2: Frontend Accessibility (The "Neuro-Inclusive" Layer)
*Rationale: Accessibility is not a feature; it's our core value proposition.*

### Tasks
*   **ARIA Audit:** Ensure the `AgentGraph` and `Terminal` components are screen-reader friendly.
*   **Keyboard Navigation:** Users should be able to submit intents and navigate the graph without a mouse (critical for users with motor control issues).
*   **Reduced Motion:** Respect OS settings to disable "pulsing" animations for users with vestibular sensitivity.

## 4. Implementation Plan (2-Week Sprint)

| Week | Focus | Deliverable |
| :--- | :--- | :--- |
| **Week 1** | **Testing** | CI/CD Green, Coverage > 80%, P95 Latency < 1s |
| **Week 2** | **A11y** | WCAG 2.1 AA Compliance, Keyboard Nav Support |

## 5. Success Metrics
*   **Test Coverage:** > 80% (Verified by Codecov)
*   **CI Pass Rate:** 100% on `main`
*   **Lighthouse A11y Score:** 100/100
*   **P95 Latency:** < 800ms (Production Baseline)

---
**Status:** Approved for Execution
**Lead:** BROski
