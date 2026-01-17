import React from 'react';
import { Activity, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { RealTimeEvent } from '../types/dashboard';

const RealTimeFeed: React.FC<{ events: RealTimeEvent[] }> = ({ events }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full overflow-hidden flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-bold flex items-center gap-2">
          <Activity className="text-emerald-400" size={20} />
          Real-Time Decision Stream
        </h3>
        <span className="bg-emerald-500/10 text-emerald-400 text-xs px-2 py-1 rounded-full animate-pulse">
          Live
        </span>
      </div>
      
      <div className="space-y-4 overflow-y-auto flex-1 pr-2 custom-scrollbar">
        <AnimatePresence initial={false}>
          {events.map((event) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="bg-slate-800/50 border border-slate-700 p-3 rounded-lg flex items-center gap-4"
            >
              <div className={`p-2 rounded-full ${
                event.priority === 'critical' ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'
              }`}>
                <Zap size={16} />
              </div>
              <div className="flex-1">
                <div className="flex justify-between">
                  <span className="text-slate-200 text-sm font-medium">{event.eventType}</span>
                  <span className="text-slate-500 text-xs">{new Date(event.timestamp).toLocaleTimeString()}</span>
                </div>
                <p className="text-slate-400 text-xs mt-1">CID: {event.customerId}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default RealTimeFeed;