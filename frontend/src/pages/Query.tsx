import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Info, Loader2, Search, Users } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';
import apiService from '../services/api';
import { ProactiveAlert } from '../types';

const Query: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [alert, setAlert] = useState<ProactiveAlert | null>(null);

  const queryMutation = useMutation({
    mutationFn: (q: string) => apiService.query(q),
    onSuccess: (response) => {
      setAlert(response.data);
    },
  });

  const suggestedQuestions = [
    'Why did we choose React over Vue?',
    'What happened with the PostgreSQL migration?',
    'Who has experience with database migrations?',
    'What lessons did we learn from the APAC expansion?',
    'Why did we choose Stripe for payments?',
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim()) {
      queryMutation.mutate(question);
    }
  };

  const handleSuggestedClick = (q: string) => {
    setQuestion(q);
    queryMutation.mutate(q);
  };

  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'warning':
        return <AlertTriangle className="h-7 w-7 text-amber-300" />;
      case 'expert_needed':
        return <Users className="h-7 w-7 text-emerald-300" />;
      default:
        return <Info className="h-7 w-7 text-sky-300" />;
    }
  };

  const getAlertTone = (level: string) => {
    switch (level) {
      case 'warning':
        return 'border-amber-400/30 bg-amber-400/10';
      case 'expert_needed':
        return 'border-emerald-400/30 bg-emerald-400/10';
      default:
        return 'border-sky-400/30 bg-sky-400/10';
    }
  };

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <section className="cb-panel overflow-hidden">
        <div className="px-6 py-6 lg:px-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">
            Ask Context
          </div>
          <h1 className="text-3xl font-extrabold text-slate-50 lg:text-4xl">
            Ask why something happened, who knows a topic, or what went wrong last time.
          </h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-400">
            Query the institutional memory layer in natural language and let ContextBridge pull
            together the best historical evidence before answering.
          </p>
        </div>
      </section>

      <section className="cb-panel p-6">
        <form onSubmit={handleSubmit}>
          <div className="relative">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask anything about your organization's history..."
              className="cb-input py-4 pl-6 pr-16 text-lg"
              disabled={queryMutation.isPending}
            />
            <button
              type="submit"
              disabled={queryMutation.isPending || !question.trim()}
              className="absolute right-2 top-1/2 inline-flex -translate-y-1/2 items-center justify-center rounded-xl bg-blue-500 px-4 py-3 text-slate-950 transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Search className="h-5 w-5" />
            </button>
          </div>
        </form>

        {!alert && !queryMutation.isPending && (
          <div className="mt-5 flex flex-wrap gap-2">
            {suggestedQuestions.map((q) => (
              <button
                key={q}
                type="button"
                onClick={() => handleSuggestedClick(q)}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 transition hover:border-sky-400/30 hover:text-slate-100"
              >
                {q}
              </button>
            ))}
          </div>
        )}
      </section>

      <AnimatePresence>
        {queryMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="cb-panel p-10 text-center"
          >
            <Loader2 className="mx-auto mb-4 h-12 w-12 animate-spin text-sky-300" />
            <h3 className="text-xl font-semibold text-slate-100">Searching institutional memory...</h3>
            <p className="mt-2 text-sm text-slate-400">
              Analyzing historical context, linked people, and past decisions.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {alert && !queryMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-6"
          >
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className={`cb-panel border p-6 ${getAlertTone(alert.alert_level)}`}
            >
              <div className="flex items-start gap-4">
                <div className="rounded-2xl border border-white/10 bg-slate-950/30 p-3">
                  {getAlertIcon(alert.alert_level)}
                </div>
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-slate-50">{alert.headline}</h2>
                  <div className="mt-3 flex flex-wrap gap-3 text-sm text-slate-300">
                    <span className="cb-pill text-xs font-semibold text-slate-200">
                      Confidence {alert.confidence_score}%
                    </span>
                    <span className="cb-pill text-xs font-semibold text-slate-200">
                      {alert.context_items.length} supporting records
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="cb-panel p-6"
            >
              <h3 className="text-lg font-bold text-slate-50">Synthesized Answer</h3>
              <p className="mt-4 whitespace-pre-line text-sm leading-7 text-slate-300">
                {alert.synthesized_insight}
              </p>
            </motion.div>

            {alert.relevant_people.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="cb-panel p-6"
              >
                <h3 className="text-lg font-bold text-slate-50">Relevant People</h3>
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

            {alert.context_items.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
                className="cb-panel p-6"
              >
                <h3 className="text-lg font-bold text-slate-50">
                  Source Context ({alert.context_items.length})
                </h3>
                <div className="mt-4 space-y-3">
                  {alert.context_items.map((item: any, index: number) => (
                    <div
                      key={`${item.id ?? item.title}-${index}`}
                      className="rounded-2xl border border-white/10 bg-slate-950/30 p-4"
                    >
                      <h4 className="font-semibold text-slate-100">{item.title}</h4>
                      <p className="mt-2 text-sm leading-6 text-slate-400">{item.summary}</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        <span className="rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-xs font-medium text-sky-200">
                          {item.content_type}
                        </span>
                        {item.date_occurred && (
                          <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">
                            {item.date_occurred}
                          </span>
                        )}
                      </div>
                    </div>
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

export default Query;
