import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Users, TrendingUp, Target } from 'lucide-react';

const data = [
  { name: 'Loyalist', count: 420, color: '#10b981' },
  { name: 'VIP', count: 150, color: '#f59e0b' },
  { name: 'New', count: 320, color: '#3b82f6' },
  { name: 'Risk', count: 85, color: '#ef4444' },
];

const CustomerStats: React.FC = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-white font-bold mb-6 flex items-center gap-2">
          <Users className="text-blue-400" size={20} />
          Customer Segmentation Distribution
        </h3>
        <div className="h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex-1">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-indigo-500/10 rounded-lg text-indigo-400">
              <TrendingUp size={24} />
            </div>
            <div>
              <p className="text-slate-400 text-sm">Avg. Affinity Score</p>
              <h4 className="text-2xl font-bold text-white">84.2%</h4>
            </div>
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex-1">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-emerald-500/10 rounded-lg text-emerald-400">
              <Target size={24} />
            </div>
            <div>
              <p className="text-slate-400 text-sm">Real-Time Triggers Executed</p>
              <h4 className="text-2xl font-bold text-white">12,402</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerStats;