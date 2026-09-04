import React from 'react';
import { Cpu, Server, Activity, Download, Layers, PlayCircle, BarChart3, Info, Database } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, liveMode, setLiveMode, onExport }) {
  return (
    <header className="glass-panel mb-8 p-6 sticky top-4 z-50 border-b border-indigo-500/20">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Title & Branding */}
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <Cpu className="w-7 h-7 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                SIMATS CAPSTONE PROJECT 2026
              </span>
              <span className="pulse-badge pulse-badge-active">
                <span className="pulse-dot"></span> BENCHMARK ACTIVE
              </span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-extrabold tracking-tight mt-1 text-white">
              Cloud Gaming Infrastructure Benchmark
            </h1>
            <p className="text-sm text-slate-400">
              Comparative Analysis: Virtualized (KVM/vGPU) vs. Traditional Bare-Metal Architecture
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => setLiveMode(!liveMode)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              liveMode
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-lg shadow-emerald-500/20'
                : 'bg-slate-800/80 text-slate-400 border border-slate-700 hover:text-white'
            }`}
          >
            <Activity className={`w-4 h-4 ${liveMode ? 'animate-pulse text-emerald-400' : ''}`} />
            {liveMode ? 'Live Telemetry: ON' : 'Telemetry Paused'}
          </button>

          <button
            onClick={onExport}
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 transition-all border border-indigo-400/30"
          >
            <Download className="w-4 h-4" />
            Export Benchmark PDF
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 mt-6 pt-4 border-t border-slate-800 overflow-x-auto no-scrollbar">
        {[
          { id: 'overview', label: 'Performance Analytics', icon: BarChart3 },
          { id: 'simulator', label: 'Live Workload Simulator', icon: PlayCircle },
          { id: 'topology', label: 'Infrastructure Topology', icon: Layers },
          { id: 'data', label: 'Raw Benchmark Logs', icon: Database },
          { id: 'metadata', label: 'Capstone Methodology & Abstract', icon: Info },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-indigo-600/30 text-indigo-200 border border-indigo-500/50 shadow-md shadow-indigo-500/10'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 border border-transparent'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-500'}`} />
              {tab.label}
            </button>
          );
        })}
      </div>
    </header>
  );
}
