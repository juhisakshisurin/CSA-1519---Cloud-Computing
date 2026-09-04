import React, { useState } from 'react';
import { Database, Search, Filter, Download, CheckCircle2, AlertTriangle } from 'lucide-react';

const benchmarkLogs = [
  { id: 'EXP-101', game: 'Cyberpunk 2077', resolution: '1080p Ultra', infra: 'Virtualized (vGPU)', latency: '34.2 ms', avgFps: 74, low1Fps: 61, vram: '3.8 GB', power: '52W', status: 'Optimal' },
  { id: 'EXP-102', game: 'Cyberpunk 2077', resolution: '1080p Ultra', infra: 'Bare-Metal', latency: '26.5 ms', avgFps: 82, low1Fps: 68, vram: '8.5 GB', power: '280W', status: 'Optimal' },
  { id: 'EXP-103', game: 'Shadow of Tomb Raider', resolution: '1440p High', infra: 'Virtualized (vGPU)', latency: '31.8 ms', avgFps: 118, low1Fps: 94, vram: '4.2 GB', power: '48W', status: 'Optimal' },
  { id: 'EXP-104', game: 'Shadow of Tomb Raider', resolution: '1440p High', infra: 'Bare-Metal', latency: '24.1 ms', avgFps: 126, low1Fps: 104, vram: '9.1 GB', power: '265W', status: 'Optimal' },
  { id: 'EXP-105', game: 'CS:GO 2', resolution: '1080p Low', infra: 'Virtualized (vGPU)', latency: '19.4 ms', avgFps: 245, low1Fps: 182, vram: '2.1 GB', power: '38W', status: 'Optimal' },
  { id: 'EXP-106', game: 'CS:GO 2', resolution: '1080p Low', infra: 'Bare-Metal', latency: '14.2 ms', avgFps: 280, low1Fps: 215, vram: '4.5 GB', power: '210W', status: 'Optimal' },
  { id: 'EXP-107', game: 'Forza Horizon 5', resolution: '4K Extreme', infra: 'Virtualized (vGPU)', latency: '42.5 ms', avgFps: 62, low1Fps: 51, vram: '7.8 GB', power: '64W', status: 'Warning' },
  { id: 'EXP-108', game: 'Forza Horizon 5', resolution: '4K Extreme', infra: 'Bare-Metal', latency: '35.0 ms', avgFps: 71, low1Fps: 59, vram: '14.2 GB', power: '310W', status: 'Optimal' },
  { id: 'EXP-109', game: '8-VM Stress Test', resolution: '1080p Mixed', infra: 'Virtualized (vGPU)', latency: '38.4 ms', avgFps: 68, low1Fps: 54, vram: '21.6 GB', power: '385W (Total)', status: 'Optimal' },
  { id: 'EXP-110', game: '8-VM Overcommit', resolution: '1080p Heavy', infra: 'Bare-Metal Queue', latency: '124.0 ms', avgFps: 22, low1Fps: 11, vram: '24.0 GB', power: '320W', status: 'Critical' },
];

export default function BenchmarkDataTable() {
  const [searchTerm, setSearchTerm] = useState('');
  const [infraFilter, setInfraFilter] = useState('All');

  const filteredLogs = benchmarkLogs.filter((log) => {
    const matchesSearch = log.game.toLowerCase().includes(searchTerm.toLowerCase()) || log.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesInfra = infraFilter === 'All' || log.infra.includes(infraFilter);
    return matchesSearch && matchesInfra;
  });

  const exportCSV = () => {
    const headers = ['Run ID,Game,Resolution,Infrastructure,Latency,Avg FPS,1% Low FPS,VRAM,Power,Status\n'];
    const rows = filteredLogs.map(l => `${l.id},${l.game},${l.resolution},${l.infra},${l.latency},${l.avgFps},${l.low1Fps},${l.vram},${l.power},${l.status}`);
    const blob = new Blob([headers.concat(rows.join('\n')).join('')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SIMATS_Cloud_Gaming_Benchmark_${Date.now()}.csv`;
    a.click();
  };

  return (
    <div className="glass-panel p-6 mb-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-semibold text-xs uppercase tracking-wider">
            <Database className="w-4 h-4" /> Empirical Telemetry Repository
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            Raw Test Run Benchmark Dataset
          </h2>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search game or run ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-900 text-xs text-white pl-9 pr-4 py-2 rounded-xl border border-slate-800 focus:outline-none focus:border-indigo-500 w-48 sm:w-60"
            />
          </div>

          {/* Filter */}
          <select
            value={infraFilter}
            onChange={(e) => setInfraFilter(e.target.value)}
            className="bg-slate-900 text-xs text-slate-300 px-3 py-2 rounded-xl border border-slate-800 focus:outline-none focus:border-indigo-500"
          >
            <option value="All">All Architectures</option>
            <option value="Virtualized">Virtualized Only</option>
            <option value="Bare-Metal">Bare-Metal Only</option>
          </select>

          <button
            onClick={exportCSV}
            className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
          >
            <Download className="w-3.5 h-3.5" /> CSV
          </button>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-800">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-900/90 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800">
              <th className="p-3.5">Run ID</th>
              <th className="p-3.5">Workload Title</th>
              <th className="p-3.5">Preset</th>
              <th className="p-3.5">Architecture</th>
              <th className="p-3.5">Latency</th>
              <th className="p-3.5">Avg FPS</th>
              <th className="p-3.5">1% Low</th>
              <th className="p-3.5">VRAM</th>
              <th className="p-3.5">Power</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
            {filteredLogs.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="p-3.5 text-indigo-400 font-bold">{row.id}</td>
                <td className="p-3.5 font-sans font-medium text-white">{row.game}</td>
                <td className="p-3.5 text-slate-400">{row.resolution}</td>
                <td className="p-3.5">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                    row.infra.includes('Virtualized')
                      ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/30'
                      : 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30'
                  }`}>
                    {row.infra}
                  </span>
                </td>
                <td className="p-3.5 font-bold text-white">{row.latency}</td>
                <td className="p-3.5 text-emerald-400 font-bold">{row.avgFps}</td>
                <td className="p-3.5 text-slate-400">{row.low1Fps}</td>
                <td className="p-3.5 text-slate-300">{row.vram}</td>
                <td className="p-3.5 text-slate-400">{row.power}</td>
                <td className="p-3.5">
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${
                    row.status === 'Optimal'
                      ? 'bg-emerald-500/10 text-emerald-400'
                      : row.status === 'Warning'
                      ? 'bg-amber-500/10 text-amber-400'
                      : 'bg-rose-500/10 text-rose-400'
                  }`}>
                    {row.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
