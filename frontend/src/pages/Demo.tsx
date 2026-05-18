import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Info, Loader2, PlayCircle, Users } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';
import apiService from '../services/api';
import { ProactiveAlert } from '../types';

const Demo: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [alert, setAlert] = useState<ProactiveAlert | null>(null);

  const scenarioMutation = useMutation({
    mutationFn: (scenarioId: string) => apiService.runScenario(scenarioId),
    onSuccess: (response) => {
      setAlert(response.data);
    },
  });

  const scenarios = [
    {
      id: 'A',
      title: 'Prevent a Mistake',
      icon: AlertTriangle,
      accent: 'text-amber-300',
      activeClass: 'border-amber-400/30 bg-amber-400/10',
      description: 'Warns about the failed PostgreSQL migration before a team repeats it.',
    },
    {
      id: 'B',
      title: 'Answer Why',
      icon: Info,
      accent: 'text-sky-300',
      activeClass: 'border-sky-400/30 bg-sky-400/10',
      description: 'Explains the React over Vue decision using stored architectural context.',
    },
    {
      id: 'C',
      title: 'Find the Expert',
      icon: Users,
      accent: 'text-emerald-300',
      activeClass: 'border-emerald-400/30 bg-emerald-400/10',
      description: 'Finds people with migration experience and the evidence behind that expertise.',
    },
  ];

  const handleScenarioClick = (scenarioId: string) => {
    setSelectedScenario(scenarioId);
    setAlert(null);
    scenarioMutation.mutate(scenarioId);
  };

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <section className="cb-panel overflow-hidden">
        <div className="grid gap-6 px-6 py-6 lg:grid-cols-[1.3fr_1fr] lg:px-8">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">
              <PlayCircle className="h-4 w-4" />
              Hackathon demo mode
            </div>
            <h1 className="text-3xl font-extrabold text-slate-50 lg:text-4xl">
              Run the three demo stories that show ContextBridge warning, explaining, and routing expertise.
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-400">
              These scenarios turn the NovaTech seed data into a guided demo flow for the hackathon pitch.
            </p>
          </div>

          <div className="rounded-3xl border border-white/10 bg-slate-950/35 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Presentation note</p>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              Start with Scenario A for the strongest “prevent the mistake before it happens” moment,
              then use B and C to show retrieval depth and expert routing.
            </p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            type="button"
            onClick={() => handleScenarioClick(scenario.id)}
            disabled={scenarioMutation.isPending}
            className={[
              'cb-panel p-6 text-left transition hover:border-white/20 disabled:cursor-not-allowed disabled:opacity-50',
              selectedScenario === scenario.id ? scenario.activeClass : 'border-white/10 bg-white/[0.03]',
            ].join(' ')}
          >
            <scenario.icon className={`mb-4 h-8 w-8 ${scenario.accent}`} />
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
              Scenario {scenario.id}
            </p>
            <h3 className="mt-2 text-xl font-bold text-slate-50">{scenario.title}</h3>
            <p className="mt-3 text-sm leading-7 text-slate-400">{scenario.description}</p>
          </button>
        ))}
      </section>

      <AnimatePresence>
        {scenarioMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="cb-panel p-10 text-center"
          >
            <Loader2 className="mx-auto mb-4 h-12 w-12 animate-spin text-sky-300" />
            <h3 className="text-xl font-semibold text-slate-100">ContextBridge is analyzing...</h3>
            <p className="mt-2 text-sm text-slate-400">
              Searching the enterprise memory graph for the strongest supporting context.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {alert && !scenarioMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-6"
          >
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="cb-panel border border-sky-400/20 bg-sky-400/10 p-6"
            >
              <h2 className="text-2xl font-bold text-slate-50">{alert.headline}</h2>
              <div className="mt-3 flex flex-wrap gap-3">
                <span className="cb-pill text-xs font-semibold text-slate-200">
                  Confidence {alert.confidence_score}%
                </span>
                <span className="cb-pill text-xs font-semibold text-slate-200">
                  {alert.context_items.length} relevant records
                </span>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="cb-panel p-6"
            >
              <h3 className="text-lg font-bold text-slate-50">Synthesized Insight</h3>
              <p className="mt-4 whitespace-pre-line text-sm leading-7 text-slate-300">
                {alert.synthesized_insight}
              </p>
            </motion.div>

            {alert.recommended_actions.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="cb-panel p-6"
              >
                <h3 className="text-lg font-bold text-slate-50">Recommended Actions</h3>
                <ul className="mt-4 space-y-3">
                  {alert.recommended_actions.map((action, index) => (
                    <li key={index} className="flex gap-3 text-sm leading-7 text-slate-300">
                      <span className="mt-2 h-2 w-2 rounded-full bg-sky-400" />
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}

            {alert.relevant_people.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
                className="cb-panel p-6"
              >
                <h3 className="text-lg font-bold text-slate-50">People to Pull In</h3>
                <div className="mt-4 flex flex-wrap gap-2">
                  {alert.relevant_people.map((person) => (
                    <span
                      key={person}
                      className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm font-medium text-emerald-200"
                    >
                      {person}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Demo;
