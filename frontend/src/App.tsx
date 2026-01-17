import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Megaphone, Users as UsersIcon, Settings, BrainCircuit } from 'lucide-react';
import RealTimeFeed from './components/RealTimeFeed';
import CustomerStats from './components/CustomerStats';
import { RealTimeEvent } from './types/dashboard';

const App: React.FC = () => {
  const [events, setEvents] = useState<RealTimeEvent[]>([]);

  // Simulation: Add random events to the real-time feed
  useEffect(() => {
    const interval = setInterval(() => {
      const newEvent: RealTimeEvent = {
        id: Math.random().toString(36).substr(2, 9),
        customerId: `USER-${Math.floor(Math.random() * 1000)}`,
        eventType: ['view_product', 'add_to_cart', 'search_query', 'email_click'][Math.floor(Math.random() * 4)],
        timestamp: new Date().toISOString(),
        priority: Math.random() > 0.8 ? 'critical' : 'medium'
      };
      setEvents(prev => [newEvent, ...prev].slice(0, 15));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-black text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-slate-950 border-r border-slate-800 p-6 flex flex-col">
        <div className="flex items-center gap-3 mb-12">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <BrainCircuit className="text-white" size={24} />
          </div>
          <span className="font-bold text-xl tracking-tight text-white">AXON AI</span>
        </div>

        <nav className="flex-1 space-y-2">
          {[
            { icon: LayoutDashboard, label: 'Dashboard', active: true },
            { icon: UsersIcon, label: 'Customer Segments' },
            { icon: Megaphone, label: 'Campaigns' },
            { icon: Settings, label: 'AI Configuration' },
          ].map((item) => (
            <a
              key={item.label}
              href="#"
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                item.active ? 'bg-slate-900 text-indigo-400' : 'hover:bg-slate-900 text-slate-400 hover:text-slate-200'
              }`}
            >
              <item.icon size={20} />
              <span className="font-medium">{item.label}</span>
            </a>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-800">
          <div className="bg-gradient-to-br from-indigo-900/40 to-slate-900 p-4 rounded-xl border border-indigo-500/20">
            <p className="text-xs text-indigo-300 font-semibold mb-1 uppercase tracking-wider">AI System Health</p>
            <div className="flex items-center justify-between">
              <span className="text-sm">Inference Latency</span>
              <span className="text-emerald-400 text-sm font-mono">14ms</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="pl-64 p-8">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">Personalization Command Center</h1>
            <p className="text-slate-400 mt-1">มุ่งสู่ความเป็นผู้นำด้านการตลาดเฉพาะบุคคลด้วยเทคโนโลยี AI</p>
          </div>
          <div className="flex gap-3">
            <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
              Export Analytics
            </button>
            <button className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-600/20">
              New Campaign
            </button>
          </div>
        </header>

        <CustomerStats />

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <div className="xl:col-span-2 space-y-8">
            {/* Active Campaigns Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
              <div className="p-6 border-b border-slate-800">
                <h3 className="text-white font-bold">High-Affinity Campaign Performance</h3>
              </div>
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 text-slate-500 uppercase text-[11px] tracking-widest">
                  <tr>
                    <th className="px-6 py-4 font-semibold">Campaign Name</th>
                    <th className="px-6 py-4 font-semibold">Target Segment</th>
                    <th className="px-6 py-4 font-semibold">Conv. Rate</th>
                    <th className="px-6 py-4 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {[
                    { name: 'VIP Summer Rewards', segment: 'VIPs', conv: '12.4%', status: 'Active' },
                    { name: 'Churn Prevention Alpha', segment: 'Risk', conv: '5.2%', status: 'Optimization' },
                    { name: 'Cross-Sell: Tech Essentials', segment: 'Loyalists', conv: '8.1%', status: 'Active' },
                  ].map((camp, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                      <td className="px-6 py-4 text-white font-medium">{camp.name}</td>
                      <td className="px-6 py-4 text-slate-400">{camp.segment}</td>
                      <td className="px-6 py-4">
                        <span className="text-emerald-400 font-mono">{camp.conv}</span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 rounded-full bg-slate-800 text-[10px] font-bold text-slate-300">
                          {camp.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="xl:col-span-1">
            <RealTimeFeed events={events} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;