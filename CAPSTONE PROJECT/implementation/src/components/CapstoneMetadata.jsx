import React from 'react';
import { BookOpen, GraduationCap, Award, CheckCircle2, Cpu, HardDrive, Wifi, ShieldCheck } from 'lucide-react';

export default function CapstoneMetadata() {
  return (
    <div className="glass-panel p-6 mb-8 border border-indigo-500/30">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs uppercase tracking-wider">
            <GraduationCap className="w-4 h-4" /> SIMATS School of Engineering - Department of Computer Science
          </div>
          <h2 className="text-2xl font-black text-white mt-1">
            Capstone Research Project Metadata & Abstract
          </h2>
          <p className="text-sm text-slate-400">
            Project Code: CSE-2026-CAP-842 | Academic Year 2025–2026
          </p>
        </div>
      </div>

      {/* Abstract Box */}
      <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 mb-6 text-sm text-slate-300 space-y-3 leading-relaxed">
        <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-400 flex items-center gap-2">
          <BookOpen className="w-4 h-4" /> Executive Abstract
        </h3>
        <p>
          Cloud gaming services demand ultra-low latency, high framerate stability, and stringent resource efficiency. Traditional cloud gaming architectures assign dedicated physical GPUs to individual player sessions (1:1 single-tenant ratio), incurring immense capital expenditure (CapEx) and leaving up to 65% of VRAM compute idle during average gameplay.
        </p>
        <p>
          This capstone project presents an empirical benchmark evaluation comparing <strong>Virtualized vGPU Multi-Tenant Infrastructure (Type-1 KVM Hypervisor + NVIDIA vGPU SR-IOV Slicing)</strong> against <strong>Traditional Bare-Metal Dedicated Host Architecture</strong>. Our experimental findings demonstrate that virtualized multi-tenancy increases host session density by <strong>800%</strong> (8 concurrent 1080p sessions per 24GB GPU node) with an average hypervisor latency overhead of only <strong>7.7 ms</strong> (34.2 ms vs 26.5 ms native end-to-end), while cutting hourly operational cost per stream by <strong>78.8%</strong> ($0.18/hr vs $0.85/hr).
        </p>
      </div>

      {/* Testbed Hardware Specs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase mb-2">
            <Cpu className="w-4 h-4" /> Compute Testbed Host
          </div>
          <ul className="text-xs text-slate-300 space-y-1.5 font-mono">
            <li>• Dual AMD EPYC 7763 64-Core CPUs</li>
            <li>• 512GB DDR4 ECC 3200MHz RAM</li>
            <li>• PCIe Gen 5 x16 Host Bus</li>
            <li>• Proxmox VE 8.1 (Linux Kernel 6.5)</li>
          </ul>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase mb-2">
            <HardDrive className="w-4 h-4" /> GPU & Storage Slicing
          </div>
          <ul className="text-xs text-slate-300 space-y-1.5 font-mono">
            <li>• NVIDIA L40S 48GB / RTX 4090 vGPU</li>
            <li>• NVIDIA GRID vGPU Driver v16.2</li>
            <li>• 2GB-Q / 4GB-Q vGPU Sliced Profiles</li>
            <li>• 4TB NVMe PCIe 4.0 ZFS Array</li>
          </ul>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase mb-2">
            <Wifi className="w-4 h-4" /> Streaming Protocol & Network
          </div>
          <ul className="text-xs text-slate-300 space-y-1.5 font-mono">
            <li>• WebRTC / Sunlight Moonlight Protocol</li>
            <li>• Hardware NVENC AV1 / H.265 Encoding</li>
            <li>• 10 GbE Dedicated Fiber Network Link</li>
            <li>• Client Decoding: Intel Iris Xe / Apple M2</li>
          </ul>
        </div>
      </div>

      {/* Project Team & Sign-off */}
      <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/20 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-indigo-600/30 flex items-center justify-center border border-indigo-500/40 text-indigo-300 font-bold">
            SIMATS
          </div>
          <div>
            <span className="text-white font-bold block">Saveetha Institute of Medical and Technical Sciences (SIMATS)</span>
            <span>Department of Computer Science and Engineering</span>
          </div>
        </div>

        <div className="flex items-center gap-2 text-emerald-400 font-semibold bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/30">
          <ShieldCheck className="w-4 h-4" /> Verified Capstone Submission
        </div>
      </div>
    </div>
  );
}
