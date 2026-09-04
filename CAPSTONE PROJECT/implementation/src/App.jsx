import React, { useState, useEffect } from 'react';
import Header from './components/Header.jsx';
import OverviewCards from './components/OverviewCards.jsx';
import LatencyComparisonChart from './components/LatencyComparisonChart.jsx';
import FpsPerformanceChart from './components/FpsPerformanceChart.jsx';
import ResourceUtilizationChart from './components/ResourceUtilizationChart.jsx';
import LiveSimulator from './components/LiveSimulator.jsx';
import TopologyComparison from './components/TopologyComparison.jsx';
import BenchmarkDataTable from './components/BenchmarkDataTable.jsx';
import CapstoneMetadata from './components/CapstoneMetadata.jsx';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [liveMode, setLiveMode] = useState(true);

  // Print / PDF Export Handler
  const handleExportPDF = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
      {/* Top Header Navigation */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        liveMode={liveMode}
        setLiveMode={setLiveMode}
        onExport={handleExportPDF}
      />

      {/* View Switcher based on Active Tab */}
      {activeTab === 'overview' && (
        <main className="space-y-6">
          <OverviewCards />
          <LatencyComparisonChart />
          <FpsPerformanceChart />
          <ResourceUtilizationChart />
        </main>
      )}

      {activeTab === 'simulator' && (
        <main>
          <LiveSimulator />
          <OverviewCards />
        </main>
      )}

      {activeTab === 'topology' && (
        <main>
          <TopologyComparison />
          <ResourceUtilizationChart />
        </main>
      )}

      {activeTab === 'data' && (
        <main>
          <BenchmarkDataTable />
        </main>
      )}

      {activeTab === 'metadata' && (
        <main>
          <CapstoneMetadata />
          <TopologyComparison />
        </main>
      )}

      {/* Footer */}
      <footer className="mt-12 pt-6 border-t border-slate-800 text-center text-xs text-slate-500">
        <p>
          Performance Comparison of Virtualized & Traditional Cloud Gaming Infrastructure • SIMATS Capstone 2026
        </p>
        <p className="mt-1 text-slate-600 font-mono">
          Powered by React 18 • Recharts • Vite • KVM / NVIDIA vGPU Testbed Telemetry
        </p>
      </footer>
    </div>
  );
}
