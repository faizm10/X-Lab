"use client";
import * as React from "react";
import type { HighlightSpan, BiasDimension } from "@/types";

const colorByDim: Record<BiasDimension, string> = {
  ideology: "#3b82f6",
  factual: "#22c55e",
  framing: "#a855f7",
  emotion: "#ef4444",
  transparency: "#f59e0b",
};

export function Highlights({
  text,
  spans,
  showLegend = true,
}: {
  text: string;
  spans: HighlightSpan[];
  showLegend?: boolean;
}) {
  const [hovered, setHovered] = React.useState<number | null>(null);
  const [activeDims, setActiveDims] = React.useState<Record<BiasDimension, boolean>>({
    ideology: true,
    factual: true,
    framing: true,
    emotion: true,
    transparency: true,
  });
  const parts: Array<React.ReactNode> = [];

  let cursor = 0;
  spans
    .slice()
    .sort((a, b) => a.start - b.start)
    .forEach((span, idx) => {
      if (span.start > cursor) {
        parts.push(<span key={`t-${cursor}-${idx}`}>{text.slice(cursor, span.start)}</span>);
      }
      if (!activeDims[span.dimension]) {
        // Render the text as plain when this dimension is toggled off
        parts.push(<span key={`t-off-${span.start}-${idx}`}>{text.slice(span.start, span.end)}</span>);
        cursor = span.end;
        return;
      }
      const color = colorByDim[span.dimension];
      parts.push(
        <span
          key={`h-${idx}`}
          onMouseEnter={() => setHovered(idx)}
          onMouseLeave={() => setHovered(null)}
          style={{
            background: hovered === idx ? `${color}22` : `${color}14`,
            borderBottom: `1px solid ${color}44`,
          }}
          className="cursor-help rounded-[6px] px-0.5"
          title={`${span.dimension} • ${span.score}` + (span.note ? ` • ${span.note}` : "")}
        >
          {text.slice(span.start, span.end)}
        </span>
      );
      cursor = span.end;
    });
  if (cursor < text.length) parts.push(<span key={`t-${cursor}-final`}>{text.slice(cursor)}</span>);

  return (
    <div className="space-y-4">
      {showLegend && (
        <div className="flex flex-wrap gap-3 text-xs">
          {(Object.keys(colorByDim) as BiasDimension[]).map((dim) => (
            <button
              key={dim}
              onClick={() => setActiveDims((s) => ({ ...s, [dim]: !s[dim] }))}
              className={`inline-flex items-center gap-2 rounded-full border px-2.5 py-1 ${activeDims[dim] ? "border-foreground/20" : "border-foreground/10 opacity-50"}`}
              title={`Toggle ${dim}`}
            >
              <span className="size-2 rounded-full" style={{ background: colorByDim[dim] }} />
              <span className="capitalize">{dim}</span>
            </button>
          ))}
        </div>
      )}
      <p className="leading-relaxed text-foreground/80">{parts}</p>
    </div>
  );
}


