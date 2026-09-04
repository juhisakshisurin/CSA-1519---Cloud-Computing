import React, { useState } from 'react';
import { Sliders, Play, RefreshCw, Cpu, Zap, DollarSign, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function LiveSimulator() {
  const [concurrency, setConcurrency] = useState(16);
  const [resolution, setResolution] = useState('1080p');
  const [vGpuProfile, setVGpuProfile] = useState('2GB-Q'); // 2GB per VM = 12 VMs per 24GB GPU

  // Calculate dynamic metrics based on user sliders
  const vGpuVramMb = 2048; // 2GB
  const totalGpusNeededVirt = Math.ceil((concurrency * 2.5) / 24); // 2.5GB effective overhead
  const totalGpusNeededBare = concurrency; // 1 GPU per player

  // Latency dynamic modeling equation
  const baseVirtLatency = resolution === '4K' ? 38 : resolution === '1440p' ? 32 : 27;
  const baseBareLatency = resolution === '4K' ? 32 : resolution === '1440p' ? 26 : 22;

  // Queue penalty when concurrency > host limit
  const virtOverhead = Math.max(0, (concurrency - 32) * 0.4);
  const bareOverhead = Math.max(0, (concurrency - 8) * 4.2); // Bare metal queues crash faster under overload

  const virtLatency = (baseVirtLatency + virtOverhead + Math.random() * 0.8).toFixed(1);
  const bareLatency = (baseBareLatency + bareOverhead + Math.random() * 1.5).toFixed(1);

  const virtFps = Math.max(30, Math.round(120 - (concurrency * 0.6)));
  const bareFps = concurrency > 16 ? Math.max(15, Math.round(140 - (concurrency * 2.8))) : 135;

  const virtHourlyCost = (totalGpusNeededVirt * 1.45 + concurrency * 0.05).toFixed(2);
  const bareHourlyCost = (totalGpusNeededBare * 1.25).toFixed(2);

  const costSavings = (((bareHourlyCost - virtHourlyCost) / bareHourlyCost) * 100).toFixed(1);

  return (
    <div className="glass-panel p-6 mb-8 border border-indigo-500/30">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-xs uppercase tracking-wider">
            <Sliders className="w-4 h-4" /> Interactive Benchmark Lab
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            Real-Time Workload & Concurrency Stress Simulator
          </h2>
          <p className="text-sm text-slate-400">
            Dynamically adjust cloud gaming player load to simulate hypervisor queuing, vGPU slicing, and bare-metal resource saturation.
          </p>
        </div>

        <button
          onClick={() => setConcurrency(16)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all border border-slate-700 self-start md:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Reset Defaults
        </button>
      </div>

      {/* Control Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-5 rounded-2xl bg-slate-900/80 border border-slate-800 mb-6">
        {/* Slider 1: Concurrency */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wide">
              Active Concurrent Gamers
            </label>
            <span className="text-sm font-extrabold font-mono text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded border border-indigo-500/20">
              {concurrency} Players
            </span>
          </div>
          <input
            type="range"
            min="1"
            max="64"
            value={concurrency}
            onChange={(e) => setConcurrency(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
          />
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>1 Light Load</span>
            <span>32 Medium</span>
            <span>64 Heavy Cluster</span>
          </div>
        </div>

        {/* Option 2: Resolution */}
        <div>
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wide block mb-2">
            Streaming Resolution Target
          </label>
          <div className="grid grid-cols-3 gap-2">
            {['1080p', '1440p', '4K'].map((res) => (
              <button
                key={res}
                onClick={() => setResolution(res)}
                className={`py-2 rounded-xl text-xs font-bold transition-all ${
                  resolution === res
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-400'
                    : 'bg-slate-800 text-slate-400 hover:text-white border border-slate-700'
                }`}
              >
                {res}
              </button>
            ))}
          </div>
        </div>

        {/* Option 3: vGPU Profile Slicing */}
        <div>
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wide block mb-2">
            vGPU Framebuffer Slicing Profile
          </label>
          <select
            value={vGpuProfile}
            onChange={(e) => setVGpuProfile(e.target.value)}
            className="w-full bg-slate-800 text-slate-200 text-xs font-medium py-2.5 px-3 rounded-xl border border-slate-700 focus:outline-none focus:border-indigo-500"
          >
            <option value="1GB-Q">1GB-Q (High Density, eSports Games)</option>
            <option value="2GB-Q">2GB-Q (Balanced AAA 1080p Preset)</option>
            <option value="4GB-Q">4GB-Q (High VRAM / 1440p Raytracing)</option>
            <option value="8GB-Q">8GB-Q (Ultra Enthusiast 4K Slices)</option>
          </select>
        </div>
      </div>

      {/* Simulated Real-Time Metric Display Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Metric 1: Simulated Latency */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-medium text-slate-400 block mb-1">Simulated Latency</span>
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-xs text-indigo-400 block">Virtualized</span>
              <span className={`text-2xl font-black font-mono ${virtLatency > 50 ? 'text-amber-400' : 'text-white'}`}>
                {virtLatency} ms
              </span>
            </div>
            <div className="text-right">
              <span className="text-xs text-cyan-400 block">Bare-Metal</span>
              <span className={`text-xl font-bold font-mono ${bareLatency > 80 ? 'text-rose-500' : 'text-slate-300'}`}>
                {bareLatency} ms
              </span>
            </div>
          </div>
          {bareLatency > 70 && (
            <p className="text-[11px] text-rose-400 mt-2 flex items-center gap-1 font-semibold">
              <ShieldAlert className="w-3.5 h-3.5" /> Bare-Metal Queue Saturated!
            </p>
          )}
        </div>

        {/* Metric 2: Average Framerate */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-medium text-slate-400 block mb-1">Rendered FPS</span>
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-xs text-indigo-400 block">Virtualized</span>
              <span className="text-2xl font-black text-white font-mono">{virtFps} FPS</span>
            </div>
            <div className="text-right">
              <span className="text-xs text-cyan-400 block">Bare-Metal</span>
              <span className="text-xl font-bold text-slate-300 font-mono">{bareFps} FPS</span>
            </div>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Target: 60 FPS stable @ {resolution}
          </p>
        </div>

        {/* Metric 3: Required GPUs */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-medium text-slate-400 block mb-1">Hardware GPUs Required</span>
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-xs text-indigo-400 block">Virtualized Hosts</span>
              <span className="text-2xl font-black text-emerald-400 font-mono">{totalGpusNeededVirt} GPUs</span>
            </div>
            <div className="text-right">
              <span className="text-xs text-cyan-400 block">Bare-Metal Hosts</span>
              <span className="text-xl font-bold text-slate-300 font-mono">{totalGpusNeededBare} GPUs</span>
            </div>
          </div>
          <p className="text-[11px] text-emerald-400 mt-2 font-semibold">
            Saved {totalGpusNeededBare - totalGpusNeededVirt} Physical GPU Cards
          </p>
        </div>

        {/* Metric 4: Estimated Cluster Cost */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-medium text-slate-400 block mb-1">Cluster Hourly OpEx</span>
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-xs text-indigo-400 block">Virtualized</span>
              <span className="text-2xl font-black text-emerald-400 font-mono">${virtHourlyCost}/hr</span>
            </div>
            <div className="text-right">
              <span className="text-xs text-cyan-400 block">Bare-Metal</span>
              <span className="text-xl font-bold text-slate-300 font-mono">${bareHourlyCost}/hr</span>
            </div>
          </div>
          <p className="text-[11px] text-emerald-400 mt-2 font-bold flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> {costSavings}% OpEx Efficiency
          </p>
        </div>
      </div>
    </div>
  );
}
