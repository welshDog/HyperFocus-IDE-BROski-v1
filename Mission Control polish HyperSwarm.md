Here’s how I’d apply what you wrote, as a clear action plan for you/your UI agent:

1️⃣ Button system: do this first
In your HyperSwarm Control Center HTML:

Replace the old generic .btn styles in <style> with your improved button + slider + focus CSS block.

In the markup:

Primary actions:

Execute Intent, Run HyperRun, etc. → class="btn btn-primary"

Secondary actions:

Simulate, Cancel, confirm dialogs → class="btn btn-secondary"

Ghost actions:

Refresh, Clear, “More details” links → class="btn btn-ghost"

Danger:

Any “Deny / Kill / Stop swarm” action → class="btn btn-danger" (if you add that from your spec).

That instantly gives you:

Visual hierarchy (one obvious primary).

Tactile press feel on click.

Better hover/active feedback without feeling “floaty”.

2️⃣ Accessibility: graph + Agent Contracts
Do these tweaks:

On the vis.js graph container:

xml
<div
  class="agent-graph"
  id="agentGraph"
  role="application"
  aria-label="Interactive agent network"
  aria-describedby="graph-instructions"
>
  <!-- vis.js canvas -->
</div>

<p id="graph-instructions" class="sr-only">
  Network graph showing agent connections. For a detailed list of agents and their status,
  refer to the Agent Contracts section below.
</p>
On your Agent Contracts list container, make sure it has a clear heading and semantics, e.g.:

xml
<section aria-label="Agent Contracts">
  <h2>Agent Contracts</h2>
  <ul id="agentContracts">
    <!-- li entries for agents -->
  </ul>
</section>
That way:

Screen reader users know the graph is visual only.

The list is clearly the accessible representation.

3️⃣ Replace alert() with the details modal
Add the Agent Details Modal HTML near the bottom of <body>:

xml
<div class="modal" id="detailsModal" role="dialog" aria-modal="true" aria-labelledby="details-title">
  <div class="modal-content">
    <div class="card-header" style="margin-bottom: 0; border: none;">
      <h2 id="details-title" class="modal-title">Agent Profile</h2>
      <button class="btn btn-ghost" onclick="closeDetailsModal()" aria-label="Close">✕</button>
    </div>
    <div id="detailsContent" class="modal-body">
      <!-- Populated via JS -->
    </div>
    <button class="btn btn-secondary" style="width: 100%" onclick="closeDetailsModal()">Close</button>
  </div>
</div>
Replace your old alert()-based detail handler with the new showAgentDetails(agent) you wrote.

Wherever you currently do something like:

js
function onNodeClick(agent) {
  alert(JSON.stringify(agent, null, 2));
}
change it to:

js
function onNodeClick(agent) {
  showAgentDetails(agent);
}
That gives you:

Rich details (role, status, cost, capabilities).

Keyboard-focusable, closable, screen-reader-friendly modal.

No more alert() UX jank.

4️⃣ Mobile touch target improvements
Add your media query block:

css
@media (max-width: 768px) {
  .btn,
  .btn-ghost,
  input[type="range"] {
    min-height: 48px;
  }

  .slider-group {
    padding: 0.5rem 0;
  }

  .agent-graph {
    touch-action: none;
  }
}
This will:

Make sliders and buttons fat-finger friendly.

Improve spacing between your Intent Box sliders.

Prevent the graph from hijacking scroll on touch devices.

5️⃣ Quick priorities (so you don’t get lost)
If you want a minimal “ship it” order:

Drop in the new button + slider + focus CSS.

Update key buttons to btn-primary, btn-secondary, btn-ghost.

Add the Agent Details modal HTML + JS and switch graph clicks to use it.

Add the aria- attributes to the graph + instructions paragraph.

Add the mobile media query for touch targets.

That’s enough to take HyperSwarm from “cool prototype” to “this feels like a real control center”.