"use client";

import { motion } from "framer-motion";
import { Terminal, Cpu, Shield, Database, Layout, Server, GitBranch, Activity, ExternalLink, Heart } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

const agents = [
  { name: "Project Strategist", icon: Activity, role: "Plan & Delegate", color: "text-purple-400" },
  { name: "Frontend Specialist", icon: Layout, role: "React & UI/UX", color: "text-blue-400" },
  { name: "Backend Specialist", icon: Server, role: "API & Python", color: "text-green-400" },
  { name: "Database Architect", icon: Database, role: "Schema & SQL", color: "text-yellow-400" },
  { name: "QA Engineer", icon: Shield, role: "Test & Verify", color: "text-red-400" },
  { name: "DevOps Engineer", icon: GitBranch, role: "CI/CD & Deploy", color: "text-orange-400" },
];

const sponsors = [
  { name: "Perplexity AI", tier: "Core Research Engine", url: "https://perplexity.ai", description: "Wishlist sponsor – not affiliated (yet)." },
  { name: "Anthropic", tier: "Reasoning Models", url: "https://anthropic.com", description: "Wishlist sponsor – not affiliated (yet)." },
  { name: "Docker", tier: "Container Backbone", url: "https://docker.com", description: "Wishlist sponsor – not affiliated (yet)." },
];

export default function LandingPage() {
  const [email, setEmail] = useState("");

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-100 font-sans selection:bg-purple-500/30">
      {/* Navigation */}
      <nav className="fixed w-full z-50 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="w-6 h-6 text-purple-500" />
            <span className="font-bold text-lg tracking-tight">HyperCode<span className="text-purple-500">.ai</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
            <Link href="#features" className="hover:text-white transition-colors">Agents</Link>
            <Link href="#workflow" className="hover:text-white transition-colors">Workflow</Link>
            <Link href="#sponsors" className="hover:text-white transition-colors">Sponsors</Link>
            <Link 
              href="/dashboard" 
              className="bg-white text-black px-4 py-2 rounded-full hover:bg-gray-200 transition-colors font-semibold"
            >
              Launch Console
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-[#0a0a0a] to-[#0a0a0a] z-0" />
        
        <div className="max-w-5xl mx-auto relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="inline-block px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-semibold mb-6">
              v2.3 NOW LIVE • AGENT SWARM INTELLIGENCE
            </span>
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-500">
              Build Software at <br />
              <span className="text-white">Hyper Speed</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
              Orchestrate a crew of 8 specialized AI agents to plan, code, test, and deploy full-stack applications. 
              No more context switching. Just pure flow.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link 
                href="/dashboard"
                className="w-full sm:w-auto px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold transition-all flex items-center justify-center gap-2 group"
              >
                Start Building
                <Terminal className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                href="https://github.com/hyperfocus/broski"
                target="_blank"
                className="w-full sm:w-auto px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg font-semibold transition-all flex items-center justify-center gap-2"
              >
                View on GitHub
                <ExternalLink className="w-4 h-4" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Agent Grid */}
      <section id="features" className="py-24 bg-black/50 border-y border-white/5">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Meet Your Crew</h2>
            <p className="text-gray-400">Specialized agents working in perfect harmony.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent, i) => (
              <motion.div
                key={agent.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                className="p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-purple-500/30 transition-colors group"
              >
                <div className={`w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center mb-4 ${agent.color} group-hover:scale-110 transition-transform`}>
                  <agent.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold mb-1">{agent.name}</h3>
                <p className="text-sm text-gray-400">{agent.role}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Sponsor Integration */}
      <section id="sponsors" className="py-24 relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-pink-500/10 border border-pink-500/20 text-pink-400 text-xs font-semibold mb-8">
            <Heart className="w-3 h-3 fill-current" /> COMMUNITY-SUPPORTED • WISHLIST PARTNERS
          </div>
          
          <h2 className="text-3xl font-bold mb-12">Tech We Build On (and Hope to Partner With)</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {sponsors.map((sponsor) => (
              <div 
                key={sponsor.name}
                className="group relative p-8 rounded-2xl bg-gradient-to-b from-white/5 to-transparent border border-white/5 hover:border-purple-500/30 transition-all"
              >
                <div className="absolute inset-0 bg-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />
                <h3 className="text-xl font-bold mb-2 relative z-10">{sponsor.name}</h3>
                <p className="text-xs text-purple-400 font-mono mb-4 uppercase tracking-wider relative z-10">{sponsor.tier}</p>
                <p className="text-sm text-gray-400 mb-6 relative z-10">{sponsor.description}</p>
                <a 
                  href={sponsor.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-sm font-medium text-white hover:text-purple-400 transition-colors relative z-10"
                >
                  Visit Website <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              </div>
            ))}
          </div>

          <div className="mt-16 p-8 rounded-2xl bg-gradient-to-r from-purple-900/20 to-blue-900/20 border border-white/10">
            <h3 className="text-xl font-semibold mb-4">Become a Sponsor</h3>
            <p className="text-gray-400 mb-6 max-w-xl mx-auto">
              Help keep HyperCode and BROski IDE alive. Get early access, roadmap influence, and shout-outs.
            </p>
            <a 
              href="https://github.com/sponsors/hyperfocus" 
              className="inline-flex items-center px-6 py-3 bg-white text-black rounded-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              <Heart className="w-4 h-4 mr-2 fill-red-500 text-red-500" />
              Sponsor on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5 text-center text-gray-500 text-sm">
        <div className="flex justify-center gap-6 mb-8 text-xs font-medium uppercase tracking-wider">
          <Link href="https://github.com/welshDog/HyperCode-V2.0/blob/main/HDVC-Technical.md" target="_blank" className="hover:text-purple-400 transition-colors">
            Technical Law
          </Link>
          <Link href="https://github.com/welshDog/HyperCode-V2.0/blob/main/docs/AGENTS.md" target="_blank" className="hover:text-blue-400 transition-colors">
            Meet the Agents
          </Link>
          <Link href="https://github.com/welshDog/HyperCode-V2.0/blob/main/docs/SETUP_GUIDE.md" target="_blank" className="hover:text-green-400 transition-colors">
            Setup Guide
          </Link>
        </div>
        <p>© 2026 HyperCode Inc. Built with ❤️ by Autonomous Agents.</p>
      </footer>
    </div>
  );
}
