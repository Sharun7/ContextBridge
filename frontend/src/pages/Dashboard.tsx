import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { AlertTriangle, BookOpenText, CheckCircle2, Database, Layers3 } from 'lucide-react';
import apiService from '../services/api';

const chartPalette = ['#60A5FA', '#10B981', '#F59E0B', '#8B5CF6', '#38BDF8', '#EF4444'];

const Dashboard: React.FC = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: () => apiService.getStats().then((res) => res.data),
  });

  const statsCards = [
    {
      title: 'Total Knowledge Items',
      value: stats?.total_knowledge_items || 0,
      icon: Database,
      accent: 'text-sky-300',
      glow: 'from-blue-500/20 to-sky-400/10',
    },
    {
      title: 'Decisions Captured',
      value: stats?.items_by_type?.decision || 0,
      icon: CheckCircle2,
      accent: 'text-emerald-300',
      glow: 'from-emerald-500/20 to-emerald-400/10',
    },
    {
      title: 'Failures Documented',
      value: stats?.items_by_type?.failure || 0,
      icon: AlertTriangle,
      accent: 'text-amber-300',
      glow: 'from-amber-500/20 to-red-400/10',
    },
    {
      title: 'Lessons Learned',
      value: stats?.items_by_type?.lesson || 0,
      icon: BookOpenText,
      accent: 'text-violet-300',
      glow: 'from-violet-500/20 to-fuchsia-400/10',
    },
  ];

  if (isLoading) {
    return (
      <div className="cb-panel flex min-h-[420px] items-center justify-center p-10">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-sky-400" />
          <p className="text-sm text-slate-400">Loading dashboard intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="cb-panel overflow-hidden">
        <div className="grid gap-8 px-6 py-6 lg:grid-cols-[1.4fr_1fr] lg:px-8">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">
              <Layers3 className="h-4 w-4" />
              NovaTech demo intelligence
            </div>
            <h1 className="text-3xl font-extrabold text-slate-50 lg:text-4xl">
              Your institutional memory, mapped into signals teams can act on.
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-400">
              ContextBridge connects past incidents, architecture choices, and team expertise
              into one operating view so the right context appears before work goes sideways.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            {statsCards.slice(0, 2).map((card) => (
              <div
                key={card.title}
                className={`rounded-2xl border border-white/10 bg-gradient-to-br ${card.glow} p-5`}
              >
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-slate-950/35">
                  <card.icon className={`h-5 w-5 ${card.accent}`} />
                </div>
                <p className="text-sm text-slate-400">{card.title}</p>
                <p className="mt-2 text-3xl font-extrabold text-slate-50">{card.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-4">
        {statsCards.map((card) => (
          <div key={card.title} className="cb-panel p-6">
            <div className="mb-5 flex items-center justify-between">
              <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-3">
                <card.icon className={`h-5 w-5 ${card.accent}`} />
              </div>
              <span className={`text-xs font-semibold uppercase tracking-[0.2em] ${card.accent}`}>
                Live
              </span>
            </div>
            <p className="text-sm text-slate-400">{card.title}</p>
            <p className="mt-2 text-4xl font-extrabold text-slate-50">{card.value}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.8fr_1fr]">
        <div className="cb-panel p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-50">Top Topics</h2>
              <p className="mt-1 text-sm text-slate-400">
                Most frequently referenced themes in the current knowledge base.
              </p>
            </div>
          </div>

          {stats?.top_topics && stats.top_topics.length > 0 ? (
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={stats.top_topics} margin={{ left: 0, right: 12, top: 8, bottom: 0 }}>
                <CartesianGrid stroke="rgba(148,163,184,0.08)" vertical={false} />
                <XAxis
                  dataKey="topic"
                  stroke="#94A3B8"
                  tickLine={false}
                  axisLine={false}
                  fontSize={12}
                />
                <YAxis
                  stroke="#64748B"
                  tickLine={false}
                  axisLine={false}
                  allowDecimals={false}
                  fontSize={12}
                />
                <Tooltip
                  cursor={{ fill: 'rgba(59,130,246,0.08)' }}
                  contentStyle={{
                    background: '#162032',
                    border: '1px solid rgba(255,255,255,0.08)',
                    borderRadius: '12px',
                    color: '#F1F5F9',
                  }}
                />
                <Bar dataKey="count" radius={[10, 10, 0, 0]}>
                  {stats.top_topics.map((entry: { topic: string; count: number }, index: number) => (
                    <Cell key={entry.topic} fill={chartPalette[index % chartPalette.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="cb-panel-muted flex min-h-[320px] items-center justify-center">
              <div className="text-center">
                <p className="text-lg font-semibold text-slate-200">No topic data yet</p>
                <p className="mt-2 text-sm text-slate-500">
                  Seed the demo data to populate topic analytics.
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="cb-panel p-6">
            <h2 className="text-xl font-bold text-slate-50">By Content Type</h2>
            <div className="mt-5 space-y-3">
              {stats?.items_by_type &&
                Object.entries(stats.items_by_type).map(([type, count]) => (
                  <div
                    key={type}
                    className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/30 px-4 py-3"
                  >
                    <span className="text-sm capitalize text-slate-300">{type}</span>
                    <span className="text-lg font-bold text-sky-300">{count as number}</span>
                  </div>
                ))}
            </div>
          </div>

          <div className="cb-panel p-6">
            <h2 className="text-xl font-bold text-slate-50">By Outcome</h2>
            <div className="mt-5 space-y-3">
              {stats?.items_by_outcome &&
                Object.entries(stats.items_by_outcome).map(([outcome, count]) => (
                  <div
                    key={outcome}
                    className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/30 px-4 py-3"
                  >
                    <span className="text-sm capitalize text-slate-300">{outcome}</span>
                    <span
                      className={[
                        'text-lg font-bold',
                        outcome === 'success'
                          ? 'text-emerald-300'
                          : outcome === 'failure'
                            ? 'text-amber-300'
                            : 'text-slate-200',
                      ].join(' ')}
                    >
                      {count as number}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
