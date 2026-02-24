"use client";

import { useState, useEffect, useRef } from "react";
import { Terminal, Play, Loader2, Activity, Zap, Shield, DollarSign, Layers, RotateCcw, Trash2, X } from "lucide-react";
import dynamic from "next/dynamic";

// Dynamically import AgentGraph to avoid SSR issues with vis-network
const AgentGraph = dynamic(() => import("../../components/AgentGraph"), { ssr: false });

interface Agent {
  id: string;
  name: string;
  role: string;
  status: string;
  latencyClass: string;
  cost: number;
  capabilities: string[];
  color: string;
}

interface LogEntry {
  id: number;
  time: string;
  agent: string;
  message: string;
}

export default function DashboardPage() {
  const [task, setTask] = useState("My API is down. Fix it and explain what happened.");
  const [isLoading, setIsLoading] = useState(false);
  
  // Sliders
  const [speed, setSpeed] = useState(50);
  const [safety, setSafety] = useState(80);
  const [cost, setCost] = useState(40);
  const [depth, setDepth] = useState(60);

  // Stats
  const [costToday, setCostToday] = useState(3.47);
  const [agentCount, setAgentCount] = useState(5);
  
  // Logs
  const [logs, setLogs] = useState<LogEntry[]>([]);
  
  // Modal
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const agents: Agent[] = [
    { id: 'phoenix', name: 'PHOENIX', role: 'System Guardian', latencyClass: 'HRT', status: 'active', cost: 0.02, capabilities: ['self-healing', 'rollback', 'monitoring'], color: '#38bdf8' },
    { id: 'architect', name: 'ARCHITECT', role: 'Design & Refactor', latencyClass: 'SRT', status: 'idle', cost: 0.10, capabilities: ['planning', 'design', 'refactoring'], color: '#a855f7' },
    { id: 'researcher', name: 'RESEARCHER', role: 'Deep Dive', latencyClass: 'DT', status: 'active', cost: 0.05, capabilities: ['research', 'analysis', 'documentation'], color: '#22c55e' },
    { id: 'cfo', name: 'CFO', role: 'Cost Controller', latencyClass: 'SRT', status: 'active', cost: 0.01, capabilities: ['budget', 'routing', 'optimization'], color: '#f59e0b' },
    { id: 'narrator', name: 'NARRATOR', role: 'UX Specialist', latencyClass: 'SRT', status: 'active', cost: 0.02, capabilities: ['explanation', 'visualization', 'communication'], color: '#ec4899' },
    { id: 'google-adk', name: 'Google ADK', role: 'External Planner', latencyClass: 'SRT', status: 'available', cost: 0.15, capabilities: ['event-driven', 'architecture', 'patterns'], color: '#94a3b8' }
  ];

  const addLog = (agent: string, message: string) => {
    const entry: LogEntry = {
      id: Date.now(),
      time: new Date().toLocaleTimeString(),
      agent,
      message
    };
    setLogs(prev => [entry, ...prev].slice(0, 10));
  };

  useEffect(() => {
    addLog('SYSTEM', 'HyperSwarm Control Center initialized');
  }, []);

  async function handleExecute() {
    if (!task.trim()) return;
    
    setIsLoading(true);
    addLog('CONDUCTOR', `Processing intent: "${task.substring(0, 30)}..."`);

    try {
      const res = await fetch("http://localhost:8080/hyperrun", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task, context: { speed, safety, cost, depth } }),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      addLog('ORCHESTRATOR', `✅ Plan accepted. ID: ${data.task_id || 'UNKNOWN'}`);
      setCostToday(prev => prev + 0.05); // Simulated cost
    } catch (err: any) {
      addLog('SYSTEM', `⚠️ Backend offline (${err.message}). Switching to SIMULATION mode.`);
      setTimeout(() => {
        addLog('SIMULATOR', '🧪 Simulation complete. No issues detected.');
        setCostToday(prev => prev + 0.01);
      }, 1500);
    } finally {
      setIsLoading(false);
    }
  }

  const getSliderFeedback = (type: string, value: number) => {
    let text = '', color = 'text-green-500';
    if (type === 'safety') {
      if (value < 20) { text = '⚠️ DANGER: Tests Skipped'; color = 'text-red-500'; }
      else if (value < 60) { text = '⚠️ Risky'; color = 'text-yellow-500'; }
      else { text = 'Secure'; color = 'text-green-500'; }
    } else if (type === 'speed') {
      if (value > 90) { text = '⚡ Max Velocity'; color = 'text-yellow-500'; }
      else { text = 'Balanced'; color = 'text-green-500'; }
    } else if (type === 'cost') {
      if (value > 80) { text = '💸 Expensive'; color = 'text-yellow-500'; }
      else { text = 'Budget Friendly'; color = 'text-green-500'; }
    } else { // depth
      if (value > 80) { text = '🔬 Comprehensive'; color = 'text-green-500'; }
      else { text = 'Standard'; color = 'text-green-500'; }
    }
    return { text, color };
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-100 font-sans p-4 md:p-8">
      <div className="max-w-[1600px] mx-auto">
        
        {/* Header */}
        <header className="mb-8 pb-6 border-b border-sky-500/30">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-purple-500">
                🧠 HYPERSWARM Control Center
              </h1>
              <p className="text-slate-400 text-sm mt-1">Self-Healing Agent Operating System • Built for Neurodivergent Minds</p>
            </div>
            
            <div className="flex flex-wrap gap-6 items-center bg-[#1e293b] p-3 rounded-xl border border-slate-700">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                <span className="text-xs font-semibold text-slate-400">STATUS:</span>
                <span className="font-bold text-green-400">OPERATIONAL</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-slate-400">AGENTS:</span>
                <span className="font-bold">{agentCount}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-slate-400">BUDGET:</span>
                <span className="font-bold text-sky-400">${costToday.toFixed(2)} / $10.00</span>
              </div>
            </div>
          </div>
        </header>

        {/* Visual Cortex */}
        <section className="mb-8 bg-[#1e293b] rounded-xl border border-slate-700 p-6 relative">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Activity className="w-5 h-5 text-sky-400" /> 🎯 Visual Cortex — Agent Mesh
            </h2>
            <button className="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition-colors">
              <RotateCcw className="w-3 h-3" /> Refresh
            </button>
          </div>
          <div className="h-[400px] w-full bg-[#0f172a] rounded-lg border border-slate-800 relative overflow-hidden">
            <AgentGraph agents={agents} onSelectAgent={(id) => {
              const agent = agents.find(a => a.id === id);
              if (agent) setSelectedAgent(agent);
            }} />
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Interactive Agent Network. Scroll to zoom, drag to pan. Click nodes for details.
          </p>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          
          {/* Intent Box */}
          <section className="bg-[#1e293b] rounded-xl border border-slate-700 p-6 flex flex-col h-full">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" /> 💭 Intent Box
            </h2>
            <div className="bg-[#0f172a] border-2 border-sky-500/30 rounded-lg p-4 flex-1 flex flex-col gap-4">
              <textarea 
                value={task}
                onChange={e => setTask(e.target.value)}
                placeholder="Describe your intent..."
                className="w-full bg-[#1e293b] border-none text-slate-100 p-3 rounded-lg resize-none focus:ring-2 focus:ring-sky-500 min-h-[100px]"
              />
              
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Speed', value: speed, setter: setSpeed, type: 'speed' },
                  { label: 'Safety', value: safety, setter: setSafety, type: 'safety' },
                  { label: 'Cost', value: cost, setter: setCost, type: 'cost' },
                  { label: 'Depth', value: depth, setter: setDepth, type: 'depth' },
                ].map((s) => {
                  const fb = getSliderFeedback(s.type, s.value);
                  return (
                    <div key={s.type} className="flex flex-col gap-1">
                      <div className="flex justify-between text-xs text-slate-400">
                        <span>{s.label}: {s.value}%</span>
                        <span className={`font-bold ${fb.color}`}>{fb.text}</span>
                      </div>
                      <input 
                        type="range" min="0" max="100" value={s.value} 
                        onChange={e => s.setter(parseInt(e.target.value))}
                        className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-sky-500"
                      />
                    </div>
                  );
                })}
              </div>

              <div className="flex gap-3 mt-auto pt-4">
                <button 
                  onClick={handleExecute}
                  disabled={isLoading}
                  className="flex-1 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-bold py-3 px-4 rounded-lg shadow-lg shadow-sky-500/20 transition-all flex items-center justify-center gap-2"
                >
                  {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : '🚀 Execute Intent'}
                </button>
                <button className="px-4 py-3 bg-[#1e293b] border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors">
                  🧪 Simulate
                </button>
              </div>
            </div>
          </section>

          {/* Agent Contracts */}
          <section className="bg-[#1e293b] rounded-xl border border-slate-700 p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-purple-400" /> 📜 Agent Contracts
            </h2>
            <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              {agents.map(agent => (
                <div key={agent.id} className="bg-[#334155]/50 p-3 rounded-lg border border-slate-700/50 hover:border-slate-600 transition-colors cursor-pointer" onClick={() => setSelectedAgent(agent)}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-slate-200">{agent.name}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      agent.latencyClass === 'HRT' ? 'bg-red-500/20 text-red-400' : 
                      agent.latencyClass === 'SRT' ? 'bg-yellow-500/20 text-yellow-400' : 
                      'bg-green-500/20 text-green-400'
                    }`}>{agent.latencyClass}</span>
                  </div>
                  <div className="text-xs text-slate-400">
                    <div className="mb-1">{agent.role}</div>
                    <div className="flex gap-2">
                      <span className="text-sky-400">${agent.cost}/task</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Cost & Logs */}
          <div className="flex flex-col gap-6">
            {/* Cost Tracker */}
            <section className="bg-[#1e293b] rounded-xl border border-slate-700 p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-green-400" /> 💰 CFO — Cost Tracker
              </h2>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="bg-[#0f172a] p-3 rounded-lg text-center">
                  <div className="text-[10px] text-slate-500 uppercase">Today</div>
                  <div className="text-xl font-bold text-sky-400">${costToday.toFixed(2)}</div>
                </div>
                <div className="bg-[#0f172a] p-3 rounded-lg text-center">
                  <div className="text-[10px] text-slate-500 uppercase">Week</div>
                  <div className="text-xl font-bold text-sky-400">$18.24</div>
                </div>
                <div className="bg-[#0f172a] p-3 rounded-lg text-center">
                  <div className="text-[10px] text-slate-500 uppercase">Last</div>
                  <div className="text-xl font-bold text-sky-400">$0.27</div>
                </div>
              </div>
            </section>

            {/* Activity Log */}
            <section className="bg-[#1e293b] rounded-xl border border-slate-700 p-6 flex-1 flex flex-col">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <Layers className="w-5 h-5 text-pink-400" /> 📋 Activity Log
                </h2>
                <button onClick={() => setLogs([])} className="text-slate-400 hover:text-white transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              <div className="bg-[#0f172a] rounded-lg p-3 flex-1 overflow-y-auto max-h-[200px] font-mono text-xs space-y-2">
                {logs.length === 0 && <div className="text-slate-600 text-center py-4">No activity yet</div>}
                {logs.map(log => (
                  <div key={log.id} className="border-l-2 border-slate-700 pl-2 py-1">
                    <span className="text-slate-500">[{log.time}]</span>{' '}
                    <span className="text-sky-400 font-bold">{log.agent}:</span>{' '}
                    <span className="text-slate-300">{log.message}</span>
                  </div>
                ))}
              </div>
            </section>
          </div>

        </div>
      </div>

      {/* Agent Details Modal */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => setSelectedAgent(null)}>
          <div className="bg-[#1e293b] border border-sky-500 rounded-xl max-w-md w-full p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center text-2xl" style={{color: selectedAgent.color}}>
                  ●
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">{selectedAgent.name}</h3>
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-700 text-slate-300 uppercase">{selectedAgent.latencyClass}</span>
                </div>
              </div>
              <button onClick={() => setSelectedAgent(null)} className="text-slate-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="bg-[#0f172a] rounded-lg p-4 mb-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Role:</span>
                <span className="font-semibold text-slate-200">{selectedAgent.role}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Status:</span>
                <span className={`font-bold ${selectedAgent.status === 'active' ? 'text-green-400' : 'text-yellow-400'}`}>
                  {selectedAgent.status.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Cost:</span>
                <span className="font-semibold text-slate-200">${selectedAgent.cost}/task</span>
              </div>
            </div>

            <div className="mb-6">
              <h4 className="text-xs text-slate-500 uppercase font-bold mb-2">Core Capabilities</h4>
              <div className="flex flex-wrap gap-2">
                {selectedAgent.capabilities.map(cap => (
                  <span key={cap} className="px-3 py-1 bg-slate-800 rounded-full text-xs text-slate-300 border border-slate-700">
                    {cap}
                  </span>
                ))}
              </div>
            </div>

            <button 
              onClick={() => setSelectedAgent(null)}
              className="w-full py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition-colors"
            >
              Close Profile
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
