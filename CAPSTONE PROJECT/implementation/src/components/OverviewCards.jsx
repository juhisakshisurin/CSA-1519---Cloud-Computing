import React from 'react';
import { Zap, Users, DollarSign, Gauge, ShieldCheck, ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function OverviewCards() {
  const cards = [
    {
      title: 'Avg. End-to-End Latency',
      virtVal: '34.2 ms',
      bareVal: '26.5 ms',
      diff: '+7.7 ms (+29%)',
      diffType: 'warn',
      subtext: 'Hypervisor overhead & buffer queue',
      icon: Zap,
      accent: 'indigo',
    },
    {
      title: 'Session Multi-Tenancy Density',
      virtVal: '8 Streams / Host',
      bareVal: '1 Stream / Host',
      diff: '800% Gain',
      diffType: 'good',
      subtext: 'vGPU Slicing (1/8th Profiles)',
      icon: Users,
      accent: 'emerald',
    },
    {
      title: 'Cost per Stream Hour',
      virtVal: '$0.18 / hr',
      bareVal: '$0.85 / hr',
      diff: '-78.8% Cost',
      diffType: 'good',
      subtext: 'Operational & CapEx Savings',
      icon: DollarSign,
      accent: 'cyan',
    },
    {
      title: 'Avg. GPU Utilization Efficiency',
      virtVal: '92.4%',
      bareVal: '38.1%',
      diff: '+54.3% Idle Harvested',
      diffType: 'good',
      subtext: 'Dynamic time-slicing load distribution',
      icon: Gauge,
      accent: 'purple',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div key={idx} className="glass-panel p-5 relative overflow-hidden group">
            <div className="flex items-start justify-between">
              <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 text-indigo-400 group-hover:scale-110 transition-transform">
                <Icon className="w-6 h-6" />
              </div>
              <span
                className={`inline-flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-md ${
                  card.diffType === 'good'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                }`}
              >
                {card.diffType === 'good' ? (
                  <ArrowUpRight className="w-3.5 h-3.5" />
                ) : (
                  <ArrowDownRight className="w-3.5 h-3.5" />
                )}
                {card.diff}
              </span>
            </div>

            <div className="mt-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                {card.title}
              </h3>
              
              <div className="mt-2 flex items-baseline justify-between">
                <div>
                  <span className="text-xs text-slate-400 block">Virtualized (vGPU)</span>
                  <span className="text-2xl font-black text-white font-mono">{card.virtVal}</span>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Bare-Metal</span>
                  <span className="text-lg font-bold text-slate-300 font-mono">{card.bareVal}</span>
                </div>
              </div>
            </div>

            <p className="mt-3 text-xs text-slate-500 border-t border-slate-800/80 pt-2">
              {card.subtext}
            </p>
          </div>
        );
      })}
    </div>
  );
}
