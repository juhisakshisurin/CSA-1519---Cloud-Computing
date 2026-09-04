import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Server, Zap, Cpu, HardDrive } from 'lucide-react';

const radarData = [
  { metric: 'GPU Compute Efficiency', Virtualized: 92, BareMetal: 38 },
  { metric: 'VRAM Allocation Density', Virtualized: 88, BareMetal: 25 },
  { metric: 'Host Power Efficiency (FPS/W)', Virtualized: 85, BareMetal: 42 },
  { metric: 'Provisioning Speed', Virtualized: 95, BareMetal: 15 },
  { metric: 'Fault Isolation', Virtualized: 98, BareMetal: 50 },
  { metric: 'Cost Economy', Virtualized: 90, BareMetal: 20 },
];

const vramPieVirt = [
  { name: 'VM 1 (Cyberpunk)', value: 3.5, fill: '#6366f1' },
  { name: 'VM 2 (CS:GO 2)', value: 2.2, fill: '#06b6d4' },
  { name: 'VM 3 (Forza 5)', value: 3.8, fill: '#10b981' },
  { name: 'VM 4 (Overwatch 2)', value: 2.5, fill: '#a855f7' },
  { name: 'VM 5 (Valorant)', value: 2.0, fill: '#f59e0b' },
  { name: 'VM 6-8 (Lighter Titles)', value: 5.5, fill: '#ec4899' },
  { name: 'Unallocated Reserve', value: 4.5, fill: '#334155' },
];

const vramPieBare = [
  { name: 'Single Active Game Session', value: 8.5, fill: '#06b6d4' },
  { name: 'Wasted Idle VRAM Capacity', value: 15.5, fill: '#1e293b' },
];

export default function ResourceUtilizationChart() {
  return (
    <div className="glass-panel p-6 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-purple-400 font-semibold text-xs uppercase tracking-wider">
            <Server className="w-4 h-4" /> Benchmark Phase 03: Host Resource & Power Efficiency
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            Hardware Capacity Harvesting & Multi-Tenant VRAM Partitioning
          </h2>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Radar Chart */}
        <div className="bg-slate-900/50 p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center">
          <h3 className="text-sm font-semibold text-slate-300 mb-2">Architectural Comparison Radar</h3>
          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart outerRadius="70%" data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="metric" stroke="#94a3b8" tick={{ fill: '#cbd5e1', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
                <Radar name="Virtualized (vGPU)" dataKey="Virtualized" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} />
                <Radar name="Bare-Metal Dedicated" dataKey="BareMetal" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} />
                <Legend wrapperStyle={{ color: '#cbd5e1', fontSize: 12, paddingTop: '10px' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '10px', color: '#fff' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie VRAM Breakdown */}
        <div className="bg-slate-900/50 p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-1">VRAM Allocation (24GB Pool)</h3>
            <p className="text-xs text-slate-500 mb-4">Comparison of VRAM utilization per single host GPU</p>
          </div>

          <div className="grid grid-cols-2 gap-2 h-[220px]">
            <div className="flex flex-col items-center">
              <span className="text-xs font-semibold text-indigo-300 mb-1">Virtualized (8 VMs)</span>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={vramPieVirt} cx="50%" cy="50%" innerRadius={35} outerRadius={60} dataKey="value">
                    {vramPieVirt.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                </PieChart>
              </ResponsiveContainer>
              <span className="text-[11px] font-mono text-emerald-400">81.2% Utilized</span>
            </div>

            <div className="flex flex-col items-center">
              <span className="text-xs font-semibold text-cyan-300 mb-1">Bare-Metal (1 Session)</span>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={vramPieBare} cx="50%" cy="50%" innerRadius={35} outerRadius={60} dataKey="value">
                    {vramPieBare.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                </PieChart>
              </ResponsiveContainer>
              <span className="text-[11px] font-mono text-amber-400">35.4% Utilized (64.6% Wasted)</span>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Power per Stream: <strong>48.5W (Virt)</strong> vs <strong>280W (Bare-Metal)</strong></span>
            <span className="text-emerald-400 font-bold">82.6% Energy Reduction</span>
          </div>
        </div>
      </div>
    </div>
  );
}
