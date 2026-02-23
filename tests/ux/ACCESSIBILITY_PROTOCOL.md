# HyperSwarm Accessibility & Inclusion Test Protocol (Phase 2)

## 🎯 Objective
Validate that the HyperSwarm Control Center is fully accessible (WCAG 2.1 AA) and optimized for neurodivergent developers.

---

## 1. Automated Accessibility Checks (Pa11y / Axe)

Run these checks using the automated script: `tests/ux/a11y_check.js`

- [ ] **Contrast Ratio**: Ensure all text meets 4.5:1 (Normal) and 3:1 (Large).
- [ ] **ARIA Landmarks**: Verify `role="banner"`, `role="main"`, `role="region"`, `role="complementary"`.
- [ ] **Alt Text**: All meaningful images/icons have alt text.
- [ ] **Form Labels**: All inputs (intent box, sliders) have associated labels.
- [ ] **Focus Indicators**: All interactive elements show a visible outline on focus.

## 2. Screen Reader Validation (Manual)

**Tools:** NVDA (Windows) or VoiceOver (Mac).

### Scenario A: Navigation
1.  Navigate from the top of the page using only `Down Arrow`.
2.  **Pass Criteria**:
    - [ ] "HyperSwarm Control Center" is announced as Heading 1.
    - [ ] "Status: Operational" is announced (using `.sr-only` text).
    - [ ] "Visual Cortex" graph is announced with its accessible description.

### Scenario B: Interaction
1.  Tab to "Intent Box".
2.  Type "Test Intent".
3.  Tab to "Speed Slider".
4.  Use `Arrow Keys` to adjust.
5.  **Pass Criteria**:
    - [ ] Slider value is announced (e.g., "50 percent").
    - [ ] Feedback text ("Balanced", "Secure") is announced.

### Scenario C: Dynamic Updates
1.  Trigger a task (or wait for simulation).
2.  **Pass Criteria**:
    - [ ] New log entries in "Activity Log" are announced automatically (via `aria-live="polite"`).

## 3. Keyboard Navigation (Manual)

**Tools:** Keyboard only (Tab, Shift+Tab, Enter, Space, Arrows, Esc).

- [ ] **Tab Order**: Logical flow (Header -> Main -> Graph -> Intent -> Sliders -> Logs).
- [ ] **Visual Focus**: Focus ring is always visible.
- [ ] **Skip Links**: (Optional but recommended) "Skip to Main Content" link exists.
- [ ] **Graph Interaction**:
    - [ ] Tab into graph.
    - [ ] Arrow keys to move between nodes (if implemented) or list view fallback.
- [ ] **Modal Trapping**:
    - [ ] Open HITL Modal.
    - [ ] Tab should cycle *only* inside the modal.
    - [ ] `Esc` key should close the modal.

## 4. Neurodivergent User Testing Protocol

**Participants:** 3-5 Developers (ADHD, Autism, Dyslexia).

### Task 1: Intent Execution (Target: < 30s)
*   **Prompt**: "You found a bug in the payment API. Use the Intent Box to fix it."
*   **Observation**:
    -   Time to locate Intent Box.
    -   Distraction points (animations, colors).

### Task 2: Status Identification (Target: 100% Accuracy)
*   **Prompt**: "Which agent is currently working?"
*   **Observation**:
    -   Reliance on color vs. position/text.
    -   Confusion with "pulsing" animations.

### Task 3: Safety Configuration (Target: 100% Comprehension)
*   **Prompt**: "Set the Safety level to 20%. What does the system tell you?"
*   **Observation**:
    -   Do they notice the "⚠️ DANGER" feedback?
    -   Is the slider movement smooth or frustrating?

### Task 4: Budget Check (Target: < 5s)
*   **Prompt**: "How much money have we spent today?"
*   **Observation**:
    -   Eye movement (heatmap if possible, otherwise observation).
    -   Time to locate "CFO — Cost Tracker".

## 5. Subjective Feedback (Post-Test)

Rate on scale 1-5 (1=Poor, 5=Excellent):
1.  **Clarity**: How easy was it to understand what to do?
2.  **Calmness**: Did the interface feel overwhelming?
3.  **Control**: Did you feel in charge of the agents?
4.  **Daily Use**: Would you use this tool every day?

**Open Questions:**
- "What was the most distracting element?"
- "What was the most helpful feature?"
