import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { CalendarDays, Database, Filter, Search, Tag, Users, X } from 'lucide-react';
import apiService from '../services/api';
import { KnowledgeItem } from '../types';

const typeStyles: Record<string, string> = {
  decision: 'border-sky-400/25 bg-sky-400/10 text-sky-200',
  failure: 'border-amber-400/25 bg-amber-400/10 text-amber-200',
  lesson: 'border-emerald-400/25 bg-emerald-400/10 text-emerald-200',
  success: 'border-emerald-400/25 bg-emerald-400/10 text-emerald-200',
};

const outcomeStyles: Record<string, string> = {
  success: 'border-emerald-400/25 bg-emerald-400/10 text-emerald-200',
  failure: 'border-rose-400/25 bg-rose-400/10 text-rose-200',
  ongoing: 'border-amber-400/25 bg-amber-400/10 text-amber-200',
  unknown: 'border-slate-400/20 bg-slate-400/10 text-slate-300',
};

const KnowledgeBase: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [outcomeFilter, setOutcomeFilter] = useState('');
  const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);

  const { data: items = [], isLoading } = useQuery<KnowledgeItem[]>({
    queryKey: ['knowledge', searchQuery, typeFilter, outcomeFilter],
    queryFn: async () => {
      const response = await apiService.searchKnowledge({
        q: searchQuery,
        type: typeFilter || undefined,
        outcome: outcomeFilter || undefined,
        limit: 100,
      });
      return response.data;
    },
  });

  const hasFilters = Boolean(searchQuery || typeFilter || outcomeFilter);

  const failures = items.filter((item) => item.outcome === 'failure').length;
  const decisions = items.filter((item) => item.content_type === 'decision').length;

  const clearFilters = () => {
    setSearchQuery('');
    setTypeFilter('');
    setOutcomeFilter('');
  };

  return (
    <div className="space-y-6">
      <section className="cb-panel overflow-hidden">
        <div className="grid gap-6 px-6 py-6 lg:grid-cols-[1.3fr_1fr] lg:px-8">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-blue-200">
              <Database className="h-4 w-4" />
              Knowledge repository
            </div>
            <h1 className="text-3xl font-extrabold text-slate-50 lg:text-4xl">
              Search captured decisions, failures, and lessons without waiting for someone to remember them.
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-400">
              Blank-on-load is fixed here by loading the stored knowledge set immediately, then
              narrowing it with semantic search and metadata filters as the user explores.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
                Loaded
              </p>
              <p className="mt-2 text-3xl font-extrabold text-slate-50">{items.length}</p>
              <p className="mt-1 text-sm text-slate-400">knowledge items</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
                Decisions
              </p>
              <p className="mt-2 text-3xl font-extrabold text-sky-300">{decisions}</p>
              <p className="mt-1 text-sm text-slate-400">architecture and process calls</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
                Failures
              </p>
              <p className="mt-2 text-3xl font-extrabold text-amber-300">{failures}</p>
              <p className="mt-1 text-sm text-slate-400">history that can prevent repeats</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cb-panel p-6">
        <div className="grid gap-4 lg:grid-cols-[1.4fr_repeat(3,minmax(0,1fr))]">
          <label className="relative block">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search migrations, outages, architecture decisions..."
              className="cb-input py-3 pl-12 pr-4"
            />
          </label>

          <label className="relative block">
            <Filter className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="cb-input appearance-none py-3 pl-12 pr-4"
            >
              <option value="">All types</option>
              <option value="decision">Decision</option>
              <option value="failure">Failure</option>
              <option value="lesson">Lesson</option>
              <option value="success">Success</option>
            </select>
          </label>

          <select
            value={outcomeFilter}
            onChange={(e) => setOutcomeFilter(e.target.value)}
            className="cb-input appearance-none px-4 py-3"
          >
            <option value="">All outcomes</option>
            <option value="success">Success</option>
            <option value="failure">Failure</option>
            <option value="ongoing">Ongoing</option>
            <option value="unknown">Unknown</option>
          </select>

          <button
            onClick={clearFilters}
            disabled={!hasFilters}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-semibold text-slate-300 transition hover:border-white/20 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <X className="h-4 w-4" />
            Clear filters
          </button>
        </div>
      </section>

      {isLoading ? (
        <div className="cb-panel flex min-h-[340px] items-center justify-center">
          <div className="text-center">
            <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-sky-400" />
            <p className="text-sm text-slate-400">Searching the memory graph...</p>
          </div>
        </div>
      ) : items.length > 0 ? (
        <div className="grid gap-4">
          {items.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setSelectedItem(item)}
              className="cb-panel group w-full p-6 text-left transition hover:border-sky-400/30 hover:bg-white/[0.055]"
            >
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div className="min-w-0 flex-1">
                  <div className="mb-3 flex flex-wrap items-center gap-2">
                    <span
                      className={[
                        'rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]',
                        typeStyles[item.content_type] || 'border-white/10 bg-white/5 text-slate-300',
                      ].join(' ')}
                    >
                      {item.content_type}
                    </span>
                    <span
                      className={[
                        'rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]',
                        outcomeStyles[item.outcome] || outcomeStyles.unknown,
                      ].join(' ')}
                    >
                      {item.outcome}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-slate-50 transition group-hover:text-sky-200">
                    {item.title}
                  </h3>
                  <p className="mt-3 max-w-4xl text-sm leading-7 text-slate-400">{item.summary}</p>
                </div>

                <div className="flex flex-wrap items-center gap-3 lg:max-w-[240px] lg:justify-end">
                  <span className="cb-pill text-xs font-semibold text-slate-300">
                    Importance {item.importance_score}/10
                  </span>
                  {item.date_occurred && (
                    <span className="cb-pill text-xs">
                      <CalendarDays className="h-3.5 w-3.5" />
                      {item.date_occurred}
                    </span>
                  )}
                </div>
              </div>

              <div className="mt-5 flex flex-wrap gap-2">
                {item.topics.map((topic) => (
                  <span
                    key={`${item.id}-${topic}`}
                    className="rounded-full border border-slate-400/15 bg-slate-50/[0.03] px-3 py-1 text-xs font-medium text-slate-300"
                  >
                    {topic}
                  </span>
                ))}
              </div>

              <div className="mt-5 flex flex-col gap-3 text-sm text-slate-400 lg:flex-row lg:items-center lg:justify-between">
                <div className="flex flex-wrap items-center gap-4">
                  {item.people_involved.length > 0 && (
                    <span className="inline-flex items-center gap-2">
                      <Users className="h-4 w-4 text-sky-300" />
                      {item.people_involved.join(', ')}
                    </span>
                  )}
                  <span className="inline-flex items-center gap-2">
                    <Tag className="h-4 w-4 text-amber-300" />
                    {item.source_type}: {item.source_reference}
                  </span>
                </div>
                <span className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                  Click for detail
                </span>
              </div>
            </button>
          ))}
        </div>
      ) : (
        <div className="cb-panel flex min-h-[320px] items-center justify-center">
          <div className="text-center">
            <p className="text-lg font-semibold text-slate-100">No matching knowledge found</p>
            <p className="mt-2 text-sm text-slate-500">
              Try clearing filters or seeding the demo dataset again.
            </p>
          </div>
        </div>
      )}

      {selectedItem && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4 py-6 backdrop-blur-sm"
          onClick={() => setSelectedItem(null)}
        >
          <div
            className="cb-panel max-h-[90vh] w-full max-w-4xl overflow-y-auto p-8"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-6 flex items-start justify-between gap-4">
              <div>
                <div className="mb-3 flex flex-wrap items-center gap-2">
                  <span
                    className={[
                      'rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]',
                      typeStyles[selectedItem.content_type] || 'border-white/10 bg-white/5 text-slate-300',
                    ].join(' ')}
                  >
                    {selectedItem.content_type}
                  </span>
                  <span
                    className={[
                      'rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]',
                      outcomeStyles[selectedItem.outcome] || outcomeStyles.unknown,
                    ].join(' ')}
                  >
                    {selectedItem.outcome}
                  </span>
                </div>
                <h2 className="text-3xl font-extrabold text-slate-50">{selectedItem.title}</h2>
                <p className="mt-3 text-sm leading-7 text-slate-400">{selectedItem.summary}</p>
              </div>

              <button
                type="button"
                onClick={() => setSelectedItem(null)}
                className="rounded-full border border-white/10 bg-white/5 p-2 text-slate-300 transition hover:text-slate-50"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
              <div className="space-y-6">
                <div className="cb-panel-muted p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">
                    Key Facts
                  </h3>
                  {selectedItem.key_facts.length > 0 ? (
                    <ul className="mt-4 space-y-3">
                      {selectedItem.key_facts.map((fact, index) => (
                        <li key={index} className="flex gap-3 text-sm leading-6 text-slate-300">
                          <span className="mt-1 h-2 w-2 rounded-full bg-sky-400" />
                          <span>{fact}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-4 text-sm text-slate-500">No extracted key facts for this item.</p>
                  )}
                </div>

                <div className="cb-panel-muted p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">
                    Topics
                  </h3>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {selectedItem.topics.map((topic) => (
                      <span
                        key={topic}
                        className="rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-medium text-sky-200"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <div className="cb-panel-muted p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">
                    Metadata
                  </h3>
                  <div className="mt-4 space-y-4 text-sm text-slate-300">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-slate-500">Importance</span>
                      <span className="font-semibold text-slate-100">
                        {selectedItem.importance_score}/10
                      </span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-slate-500">Date</span>
                      <span className="font-semibold text-slate-100">
                        {selectedItem.date_occurred || 'Unknown'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-slate-500">Source</span>
                      <span className="font-semibold text-slate-100">
                        {selectedItem.source_type}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="cb-panel-muted p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">
                    People Involved
                  </h3>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {selectedItem.people_involved.length > 0 ? (
                      selectedItem.people_involved.map((person) => (
                        <span
                          key={person}
                          className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-200"
                        >
                          {person}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-slate-500">No people attached to this record.</p>
                    )}
                  </div>
                </div>

                <div className="cb-panel-muted p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">
                    Teams Involved
                  </h3>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {selectedItem.teams_involved.length > 0 ? (
                      selectedItem.teams_involved.map((team) => (
                        <span
                          key={team}
                          className="rounded-full border border-violet-400/20 bg-violet-400/10 px-3 py-1 text-xs font-medium text-violet-200"
                        >
                          {team}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-slate-500">No team labels for this record.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KnowledgeBase;
