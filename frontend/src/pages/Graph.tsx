import React, { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import * as d3 from 'd3';
import { Filter, Network, Sparkles, X } from 'lucide-react';
import apiService from '../services/api';
import { GraphData } from '../types';

const legend = [
  { label: 'Knowledge', color: '#3B82F6' },
  { label: 'Person', color: '#10B981' },
  { label: 'Topic', color: '#F59E0B' },
  { label: 'Team', color: '#8B5CF6' },
];

const Graph: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<GraphData['nodes'][number] | null>(null);
  const [focusTopic, setFocusTopic] = useState('');

  const { data: graphData, isLoading } = useQuery<GraphData>({
    queryKey: ['graph', focusTopic],
    queryFn: () => apiService.getGraph(focusTopic || undefined).then((res) => res.data),
  });

  useEffect(() => {
    if (!svgRef.current || !containerRef.current) {
      return;
    }

    const svgElement = svgRef.current;
    const svg = d3.select(svgElement);
    svg.selectAll('*').remove();

    if (!graphData?.nodes?.length) {
      return;
    }

    const width = Math.max(containerRef.current.clientWidth, 320);
    const height = 640;

    svg
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`);

    const simulation = d3
      .forceSimulation(graphData.nodes as d3.SimulationNodeDatum[])
      .force(
        'link',
        d3
          .forceLink(graphData.links as d3.SimulationLinkDatum<d3.SimulationNodeDatum>[])
          .id((d: any) => d.id)
          .distance((link: any) => (link.type === 'RELATED_TO' ? 90 : 130))
          .strength((link: any) => (link.type === 'RELATED_TO' ? 0.4 : 0.7))
      )
      .force('charge', d3.forceManyBody().strength(-280))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius((node: any) => (node.type === 'knowledge_item' ? 34 : 22)));

    const link = svg
      .append('g')
      .attr('stroke', 'rgba(148,163,184,0.35)')
      .attr('stroke-linecap', 'round')
      .selectAll('line')
      .data(graphData.links)
      .join('line')
      .attr('stroke-width', (d) => (d.type === 'RELATED_TO' ? 2.4 : 1.6))
      .attr('stroke-opacity', (d) => (d.type === 'RELATED_TO' ? 0.65 : 0.45));

    const node = svg
      .append('g')
      .selectAll('circle')
      .data(graphData.nodes)
      .join('circle')
      .attr('r', (d: any) => (d.type === 'knowledge_item' ? 8 + (d.data?.importance_score || 4) : 11))
      .attr('fill', (d) => d.color || '#3B82F6')
      .attr('stroke', '#0F1B2D')
      .attr('stroke-width', 3)
      .style('cursor', 'pointer')
      .on('click', (_, d) => setSelectedNode(d))
      .call(
        d3
          .drag<any, any>()
          .on('start', (event, d) => {
            if (!event.active) {
              simulation.alphaTarget(0.3).restart();
            }
            d.fx = d.x;
            d.fy = d.y;
          })
          .on('drag', (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on('end', (event, d) => {
            if (!event.active) {
              simulation.alphaTarget(0);
            }
            d.fx = null;
            d.fy = null;
          }) as any
      );

    const label = svg
      .append('g')
      .selectAll('text')
      .data(graphData.nodes)
      .join('text')
      .text((d) => d.label)
      .attr('fill', '#E2E8F0')
      .attr('font-size', (d: any) => (d.type === 'knowledge_item' ? 11 : 10))
      .attr('font-weight', (d: any) => (d.type === 'knowledge_item' ? 700 : 500))
      .attr('dx', (d: any) => (d.type === 'knowledge_item' ? 14 : 12))
      .attr('dy', 4)
      .style('pointer-events', 'none');

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);

      label.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y);
    });

    return () => {
      simulation.stop();
      svg.selectAll('*').remove();
    };
  }, [graphData]);

  const nodeCount = graphData?.nodes?.length ?? 0;
  const linkCount = graphData?.links?.length ?? 0;

  return (
    <div className="space-y-6">
      <section className="cb-panel overflow-hidden">
        <div className="grid gap-6 px-6 py-6 lg:grid-cols-[1.3fr_1fr] lg:px-8">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-violet-200">
              <Network className="h-4 w-4" />
              Knowledge graph
            </div>
            <h1 className="text-3xl font-extrabold text-slate-50 lg:text-4xl">
              Visualize how people, topics, teams, and institutional memory connect.
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-400">
              The graph now rebuilds from persisted Chroma data when needed, so the page survives
              backend restarts instead of depending on a single in-memory session.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Nodes</p>
              <p className="mt-2 text-3xl font-extrabold text-slate-50">{nodeCount}</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Edges</p>
              <p className="mt-2 text-3xl font-extrabold text-sky-300">{linkCount}</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Mode</p>
              <p className="mt-2 text-sm font-semibold text-slate-100">
                {focusTopic ? `Topic focus: ${focusTopic}` : 'Full organizational graph'}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.7fr_0.75fr]">
        <div className="cb-panel p-6">
          <div className="mb-5 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex flex-wrap items-center gap-3">
              {legend.map((item) => (
                <span key={item.label} className="cb-pill text-xs font-semibold">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  {item.label}
                </span>
              ))}
            </div>

            <label className="relative block w-full lg:max-w-xs">
              <Filter className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                value={focusTopic}
                onChange={(e) => setFocusTopic(e.target.value)}
                placeholder="Focus a topic, e.g. postgresql"
                className="cb-input py-3 pl-11 pr-10"
              />
              {focusTopic && (
                <button
                  type="button"
                  onClick={() => setFocusTopic('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 transition hover:text-slate-200"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </label>
          </div>

          <div
            ref={containerRef}
            className="cb-panel-muted relative min-h-[640px] overflow-hidden border-dashed border-slate-500/20"
          >
            {isLoading ? (
              <div className="flex h-[640px] items-center justify-center">
                <div className="text-center">
                  <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-sky-400" />
                  <p className="text-sm text-slate-400">Building graph view...</p>
                </div>
              </div>
            ) : nodeCount > 0 ? (
              <svg ref={svgRef} className="h-full w-full" />
            ) : (
              <div className="flex h-[640px] items-center justify-center px-6 text-center">
                <div>
                  <Sparkles className="mx-auto h-10 w-10 text-slate-500" />
                  <p className="mt-4 text-lg font-semibold text-slate-100">No graph data available</p>
                  <p className="mt-2 text-sm text-slate-500">
                    Seed the demo data or ingest records to populate the knowledge graph.
                  </p>
                </div>
              </div>
            )}
          </div>

          <p className="mt-4 text-sm text-slate-500">
            Drag nodes to reorganize the map. Click a node to inspect its metadata.
          </p>
        </div>

        <aside className="space-y-6">
          <div className="cb-panel p-6">
            <h2 className="text-lg font-bold text-slate-50">Node Details</h2>
            {selectedNode ? (
              <div className="mt-5 space-y-5">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Label</p>
                  <p className="mt-2 text-xl font-bold text-slate-100">{selectedNode.label}</p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Type</p>
                  <p className="mt-2 text-sm font-semibold capitalize text-sky-200">
                    {selectedNode.type.replace('_', ' ')}
                  </p>
                </div>

                {selectedNode.data?.summary && (
                  <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Summary</p>
                    <p className="mt-2 text-sm leading-7 text-slate-300">{selectedNode.data.summary}</p>
                  </div>
                )}

                {selectedNode.data?.topics?.length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Topics</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {selectedNode.data.topics.map((topic: string) => (
                        <span
                          key={topic}
                          className="rounded-full border border-amber-400/20 bg-amber-400/10 px-3 py-1 text-xs font-medium text-amber-200"
                        >
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {selectedNode.data?.importance_score && (
                  <div className="rounded-2xl border border-white/10 bg-slate-950/35 p-4">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Importance</p>
                    <div className="mt-3 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-2 rounded-full bg-gradient-to-r from-sky-500 to-emerald-400"
                        style={{ width: `${selectedNode.data.importance_score * 10}%` }}
                      />
                    </div>
                    <p className="mt-2 text-sm font-semibold text-slate-100">
                      {selectedNode.data.importance_score}/10
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="mt-5 rounded-2xl border border-dashed border-white/10 bg-slate-950/25 p-6 text-sm leading-7 text-slate-500">
                Select any node in the graph to inspect who was involved, what topics it touched,
                and how important the underlying knowledge item was.
              </div>
            )}
          </div>
        </aside>
      </section>
    </div>
  );
};

export default Graph;
