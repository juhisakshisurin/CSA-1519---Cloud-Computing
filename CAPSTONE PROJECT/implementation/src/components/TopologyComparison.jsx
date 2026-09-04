import React from 'react';
import { Layers, Server, Cpu, Monitor, ShieldCheck, Check, X, ArrowRight } from 'lucide-react';

export default function TopologyComparison() {
  return (
    <div className="glass-panel p-6 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs uppercase tracking-wider">
            <Layers className="w-4 h-4" /> Architectural Blueprint
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            System Topology: Virtualized vGPU Stack vs. Bare-Metal Host
          </h2>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Topology 1: Virtualized vGPU Architecture */}
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-indigo-500/30 relative">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
            <span className="text-sm font-bold text-indigo-300 flex items-center gap-2">
              <Server className="w-4 h-4 text-indigo-400" /> Virtualized Infrastructure (KVM / NVIDIA vGPU)
            </span>
            <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">
              Multi-Tenant (N:1)
            </span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {/* Layer 1: Clients */}
            <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 text-center">
              <div className="text-indigo-400 font-bold mb-1">WebRTC / RTSP Client Devices</div>
              <div className="text-[11px] text-slate-400 flex justify-center gap-3">
                <span>Gamer 1</span> • <span>Gamer 2</span> • <span>Gamer 3 ... 8</span>
              </div>
            </div>

            <div className="flex justify-center text-slate-600">↓ Encoded H.265 / AV1 UDP Streams ↓</div>

            {/* Layer 2: Virtual Machines Layer */}
            <div className="p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/40">
              <div className="text-indigo-200 font-bold mb-1 text-center">Multi-VM Guest Layer (KVM QEMU)</div>
              <div className="grid grid-cols-4 gap-1.5 text-[10px] text-center">
                <div className="p-1.5 rounded bg-indigo-900/60 border border-indigo-700/50 text-indigo-100">VM 1 (Win 11)</div>
                <div className="p-1.5 rounded bg-indigo-900/60 border border-indigo-700/50 text-indigo-100">VM 2 (Win 11)</div>
                <div className="p-1.5 rounded bg-indigo-900/60 border border-indigo-700/50 text-indigo-100">VM 3 (Win 11)</div>
                <div className="p-1.5 rounded bg-indigo-900/60 border border-indigo-700/50 text-indigo-100">VM 4..8</div>
              </div>
            </div>

            <div className="flex justify-center text-slate-600">↓ SR-IOV vGPU Virtual Functions (VF) ↓</div>

            {/* Layer 3: Type-1 Hypervisor */}
            <div className="p-3 rounded-xl bg-purple-950/40 border border-purple-500/40 text-center">
              <div className="text-purple-300 font-bold">Type-1 Bare-Metal Hypervisor + vGPU Manager</div>
              <div className="text-[11px] text-purple-400">Proxmox VE / ESXi / KVM kernel scheduler</div>
            </div>

            <div className="flex justify-center text-slate-600">↓ Direct Hardware Access ↓</div>

            {/* Layer 4: Shared Physical GPU & Host */}
            <div className="p-3 rounded-xl bg-slate-800 border border-slate-700 text-center">
              <div className="text-emerald-400 font-bold">Single Physical GPU (e.g. RTX 4090 / L40S 24GB)</div>
              <div className="text-[11px] text-slate-400">Time-sliced NVENC encoders & CUDA cores</div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 space-y-1 text-xs text-slate-300">
            <div className="flex items-center gap-1.5 text-emerald-400">
              <Check className="w-4 h-4 flex-shrink-0" />
              <span>Dynamic resource isolation & high host density</span>
            </div>
            <div className="flex items-center gap-1.5 text-emerald-400">
              <Check className="w-4 h-4 flex-shrink-0" />
              <span>Instant snapshotting, migration, & fast spin-up</span>
            </div>
            <div className="flex items-center gap-1.5 text-amber-400">
              <X className="w-4 h-4 flex-shrink-0" />
              <span>~7.7ms Hypervisor context-switch overhead</span>
            </div>
          </div>
        </div>

        {/* Topology 2: Traditional Bare-Metal Architecture */}
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-cyan-500/30 relative">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
            <span className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Server className="w-4 h-4 text-cyan-400" /> Traditional Bare-Metal Architecture
            </span>
            <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
              Single-Tenant (1:1)
            </span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {/* Layer 1: Single Client */}
            <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 text-center">
              <div className="text-cyan-400 font-bold mb-1">WebRTC Client Device</div>
              <div className="text-[11px] text-slate-400">Single Gamer Session (Dedicated)</div>
            </div>

            <div className="flex justify-center text-slate-600">↓ Direct UDP H.264 / H.265 Stream ↓</div>

            {/* Layer 2: Host Operating System */}
            <div className="p-3 rounded-xl bg-cyan-950/40 border border-cyan-500/40 text-center">
              <div className="text-cyan-200 font-bold">Native Host OS (Windows 11 / Ubuntu Server)</div>
              <div className="text-[11px] text-cyan-400">Direct game executable process execution</div>
            </div>

            <div className="flex justify-center text-slate-600">↓ PCIe Gen5 x16 Bus ↓</div>

            {/* Layer 3: Dedicated Physical GPU */}
            <div className="p-3 rounded-xl bg-slate-800 border border-slate-700 text-center">
              <div className="text-cyan-400 font-bold">Dedicated Physical GPU (100% Locked)</div>
              <div className="text-[11px] text-slate-400">1 GPU assigned exclusively to 1 active user</div>
            </div>

            <div className="h-[44px]"></div> {/* Spacer alignment */}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 space-y-1 text-xs text-slate-300">
            <div className="flex items-center gap-1.5 text-emerald-400">
              <Check className="w-4 h-4 flex-shrink-0" />
              <span>Zero hypervisor latency (~26.5ms native baseline)</span>
            </div>
            <div className="flex items-center gap-1.5 text-rose-400">
              <X className="w-4 h-4 flex-shrink-0" />
              <span>Extremely high hardware cost ($0.85/hr per gamer)</span>
            </div>
            <div className="flex items-center gap-1.5 text-rose-400">
              <X className="w-4 h-4 flex-shrink-0" />
              <span>Severe GPU idle waste (64.6% VRAM unused)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
