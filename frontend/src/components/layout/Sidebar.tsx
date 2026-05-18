import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Database,
  LayoutDashboard,
  MessageSquareText,
  Network,
  Presentation,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/knowledge', icon: Database, label: 'Knowledge Base' },
    { path: '/query', icon: MessageSquareText, label: 'Ask Context' },
    { path: '/graph', icon: Network, label: 'Knowledge Graph' },
    { path: '/demo', icon: Presentation, label: 'Demo Scenarios' },
  ];

  return (
    <aside className="cb-panel flex w-full flex-col overflow-hidden lg:sticky lg:top-5 lg:h-[calc(100vh-2.5rem)] lg:w-[290px]">
      <div className="border-b border-white/10 px-6 py-6">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 via-sky-400 to-emerald-400 shadow-[0_18px_40px_rgba(59,130,246,0.35)]">
            <ShieldCheck className="h-7 w-7 text-slate-950" />
          </div>
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.35em] text-sky-300/80">
              NexaCore
            </p>
            <h1 className="text-2xl font-extrabold text-slate-50">ContextBridge</h1>
            <p className="text-sm text-slate-400">Institutional memory for enterprise teams</p>
          </div>
        </div>
      </div>

      <div className="border-b border-white/10 px-6 py-5">
        <div className="rounded-2xl border border-sky-400/20 bg-sky-400/10 p-4">
          <div className="mb-2 flex items-center gap-2 text-sky-200">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-semibold">Hackathon Track 4</span>
          </div>
          <p className="text-sm leading-6 text-slate-300">
            Surfacing past decisions, failures, and lessons before teams repeat them.
          </p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-5">
        <div className="space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                [
                  'group flex items-center gap-3 rounded-2xl px-4 py-3 transition-all duration-200',
                  isActive
                    ? 'bg-gradient-to-r from-blue-500/25 to-sky-400/15 text-slate-50 shadow-[0_16px_40px_rgba(37,99,235,0.16)]'
                    : 'text-slate-400 hover:bg-white/5 hover:text-slate-100',
                ].join(' ')
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={[
                      'flex h-10 w-10 items-center justify-center rounded-xl border transition-colors',
                      isActive
                        ? 'border-sky-300/30 bg-sky-300/15 text-sky-200'
                        : 'border-white/10 bg-white/5 text-slate-400 group-hover:text-slate-100',
                    ].join(' ')}
                  >
                    <item.icon className="h-5 w-5" />
                  </span>
                  <span className="text-sm font-semibold tracking-wide">{item.label}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>

      <div className="border-t border-white/10 px-6 py-5">
        <div className="rounded-2xl bg-slate-950/35 p-4">
          <p className="text-xs font-bold uppercase tracking-[0.28em] text-slate-500">
            Event
          </p>
          <p className="mt-2 text-sm font-semibold text-slate-100">
            TechEx Intelligent Enterprise Solutions Hackathon 2026
          </p>
          <p className="mt-1 text-sm text-slate-400">Track 4: Data &amp; Intelligence</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
