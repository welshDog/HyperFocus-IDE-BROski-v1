"use client";

import { useEffect, useRef } from "react";
import { Network, DataSet } from "vis-network/standalone";

interface Agent {
  id: string;
  name: string;
  role: string;
  status: string;
  color: string;
}

interface AgentGraphProps {
  agents: Agent[];
  onSelectAgent: (agentId: string) => void;
}

export default function AgentGraph({ agents, onSelectAgent }: AgentGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Data Transformation
    // @ts-ignore
    const nodes = new DataSet(
      agents.map((agent) => ({
        id: agent.id,
        label: agent.name,
        title: `${agent.role} (${agent.status})`,
        color: {
          background: "#1e293b",
          border: agent.status === "active" ? "#22c55e" : agent.status === "waiting" ? "#f59e0b" : agent.color,
          highlight: { background: "#334155", border: "#fff" },
        },
        font: { color: "#f1f5f9", face: "system-ui" },
        shape: "box",
        borderWidth: 2,
        shadow: true,
        margin: { top: 10, right: 10, bottom: 10, left: 10 },
      }))
    );

    // Hardcoded edges based on HyperSwarm topology
    // @ts-ignore
    const edges = new DataSet([
      { from: "phoenix", to: "cfo", color: { color: "#38bdf8", opacity: 0.4 }, arrows: "to", width: 2 },
      { from: "architect", to: "cfo", color: { color: "#38bdf8", opacity: 0.4 }, arrows: "to", width: 2 },
      { from: "architect", to: "google-adk", color: { color: "#38bdf8", opacity: 0.4 }, arrows: "to", width: 2 },
      { from: "researcher", to: "narrator", color: { color: "#38bdf8", opacity: 0.4 }, arrows: "to", width: 2 },
      { from: "cfo", to: "narrator", color: { color: "#38bdf8", opacity: 0.4 }, arrows: "to", width: 2 },
    ]);

    const data = { nodes, edges };
    const options: any = {
      nodes: {
        shape: "box",
        margin: 10,
        widthConstraint: { maximum: 150 },
        shadow: false,
      },
      edges: {
        shadow: false,
        smooth: { type: "continuous" },
      },
      physics: {
        enabled: true,
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity: 0.3,
          springLength: 95,
          springConstant: 0.04,
          damping: 0.09,
          avoidOverlap: 0.1,
        },
        stabilization: {
          enabled: true,
          iterations: 1000,
          updateInterval: 100,
          onlyDynamicEdges: false,
          fit: true,
        },
        adaptiveTimestep: true,
      },
      interaction: {
        hover: true,
        tooltipDelay: 200,
        zoomView: true,
        hideEdgesOnDrag: true,
      },
      layout: {
        improvedLayout: false,
      },
      height: "100%",
      width: "100%",
    };

    networkRef.current = new Network(containerRef.current, data, options);

    networkRef.current.on("click", (params) => {
      if (params.nodes.length > 0) {
        onSelectAgent(params.nodes[0]);
      }
    });

    networkRef.current.on("hoverNode", () => {
      if (containerRef.current) containerRef.current.style.cursor = "pointer";
    });
    networkRef.current.on("blurNode", () => {
      if (containerRef.current) containerRef.current.style.cursor = "default";
    });

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
    };
  }, []); // Run once on mount. Real updates would use a separate useEffect watching 'agents'

  // Update nodes when agents prop changes
  useEffect(() => {
    if (!networkRef.current) return;
    
    // We can update specific properties without re-creating the whole network
    // For simplicity, we assume the network is initialized.
    // In a real app, we'd use DataSet.update()
    // Here we just trigger a fit/stabilize if needed or handle updates via vis-network's dataset API if exposed
  }, [agents]);

  return <div ref={containerRef} className="w-full h-full min-h-[400px] bg-[#0f172a] rounded-lg border border-slate-700" />;
}
