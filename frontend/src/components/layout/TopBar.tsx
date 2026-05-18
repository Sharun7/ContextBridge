import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Activity, Bot, Sparkles } from 'lucide-react';
import apiService from '../../services/api';

const TopBar: React.FC = () => {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: () => apiService.getStats().then((res) => res.data),
    refetchInterval: 30000,
  });

  return (
    <header className="cb-panel overflow-hidden">
      <div className="flex flex-col gap-5 px-6 py-5 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.26em] text-emerald-300">
            <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.8)]" />
            System Active
          </div>
          <h2 className="text-2xl font-extrabold text-slate-50 lg:text-3xl">
            Institutional memory that steps in before teams repeat history
          </h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
            Slack, Jira, Drive, and meeting context are unified into one graph so decisions,
            failures, and ownership stay searchable.
          </p>
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-slate-950/35 px-4 py-3">
            <div className="mb-2 flex items-center gap-2 text-slate-400">
              <Activity className="h-4 w-4 text-sky-300" />
              <span className="text-xs font-semibold uppercase tracking-[0.2em]">Knowledge</span>
            </div>
            <p className="text-2xl font-extrabold text-slate-50">
              {stats?.total_knowledge_items ?? 0}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-slate-950/35 px-4 py-3">
            <div className="mb-2 flex items-center gap-2 text-slate-400">
              <Bot className="h-4 w-4 text-blue-300" />
              <span className="text-xs font-semibold uppercase tracking-[0.2em]">Engine</span>
            </div>
            <p className="text-sm font-semibold text-slate-100">Gemini + Graph + Chroma</p>
            <p className="mt-1 text-xs text-slate-500">Proactive context synthesis</p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-slate-950/35 px-4 py-3">
            <div className="mb-2 flex items-center gap-2 text-slate-400">
              <Sparkles className="h-4 w-4 text-amber-300" />
              <span className="text-xs font-semibold uppercase tracking-[0.2em]">Mission</span>
            </div>
            <p className="text-sm font-semibold text-slate-100">Prevent repeated mistakes</p>
            <p className="mt-1 text-xs text-slate-500">Institutional memory on demand</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
