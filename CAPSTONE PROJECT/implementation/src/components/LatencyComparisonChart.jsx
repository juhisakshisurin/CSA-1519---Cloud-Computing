import React, { useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, AreaChart, Area } from 'recharts';
import { Clock, ShieldAlert } from 'lucide-react';

const latencyBreakdownData = [
  {
    stage: 'Input Poll & Capture',
    Virtualized: 3.1,
    BareMetal: 2.8,
    overhead: '+0.3ms',
  },
  {
    stage: 'Frame Render (1080p)',
    Virtualized: 12.8,
    BareMetal: 11.2,
    overhead: '+1.6ms',
  },
  {
    stage: 'NVENC Encode (AV1/H.265)',
    Virtualized: 6.4,
    BareMetal: 5.1,
    overhead: '+1.3ms',
  },
  {
    stage: 'Network Transport (RTT)',
    Virtualized: 8.5,
    BareMetal: 8.4,
    overhead: '+0.1ms',
  },
  {
    stage: 'Client Decode & Display',
    Virtualized: 3.4,
    BareMetal: 3.3,
    overhead: '+0.1ms',
  },
];

const latencyVsClientsData = [
  { clients: '1 Active', Virtualized: 28.5, BareMetal: 24.2, P99_Virt: 32.1 },
  { clients: '2 Active', Virtualized: 29.8, BareMetal: 25.0, P99_Virt: 34.0 },
  { clients: '4 Active', Virtualized: 32.1, BareMetal: 28.4, P99_Virt: 38.5 },
  { clients: '8 Active (Full Slice)', Virtualized: 34.2, BareMetal: 48.0, P99_Virt: 42.1 },
  { clients: '12 Active (Overcommit)', Virtualized: 41.5, BareMetal: 89.2, P99_Virt: 68.0 },
  { clients: '16 Active (Heavy Load)', Virtualized: 52.8, BareMetal: 135.0, P99_Virt: 94.2 },
];

export default function LatencyComparisonChart() {
  const [activeMetric, setActiveMetric] = useState('breakdown');

  return (
    <div className="glass-panel p-6 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs uppercase tracking-wider">
            <Clock className="w-4 h-4" /> Benchmark Phase 01: Latency & Jitter Analysis
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            End-to-End Latency Breakdown & Scalability
          </h2>
        </div>

        <div className="flex items-center gap-2 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveMetric('breakdown')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeMetric === 'breakdown'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Pipeline Stage Breakdown
          </button>
          <button
            onClick={() => setActiveMetric('scaling')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeMetric === 'scaling'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Concurrency Scaling (1-16 Users)
          </button>
        </div>
      </div>

      <div className="h-[320px] w-full">
        {activeMetric === 'breakdown' ? (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={latencyBreakdownData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="stage" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} unit=" ms" />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
                formatter={(val) => [`${val} ms`, '']}
              />
              <Legend wrapperStyle={{ color: '#cbd5e1', paddingTop: '10px' }} />
              <Bar dataKey="Virtualized" name="Virtualized (vGPU - 1/8th Slice)" fill="#6366f1" radius={[6, 6, 0, 0]} />
              <Bar dataKey="BareMetal" name="Bare-Metal (Dedicated GPU)" fill="#06b6d4" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={latencyVsClientsData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <defs>
                <linearGradient id="virtGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0}/>
                </linearGradient>
                <linearGradient id="bareGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="clients" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} unit=" ms" />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
                formatter={(val) => [`${val} ms`, 'Avg. Latency']}
              />
              <Legend wrapperStyle={{ color: '#cbd5e1', paddingTop: '10px' }} />
              <Area type="monotone" dataKey="Virtualized" name="Virtualized (Graceful Degrade)" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#virtGrad)" />
              <Area type="monotone" dataKey="BareMetal" name="Bare-Metal (Resource Exhaustion Queue)" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#bareGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="mt-4 p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-200 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-indigo-400 flex-shrink-0" />
          <span>
            <strong>Key Insight:</strong> Virtualization adds only ~4.4ms - 7.7ms of total latency pipeline overhead during normal load, but prevents catastrophic queue collapse when multi-client demand spikes beyond single-tenant limits.
          </span>
        </div>
      </div>
    </div>
  );
}
