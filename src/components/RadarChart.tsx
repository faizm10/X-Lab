"use client";
import * as React from "react";
import type { BiasScores } from "@/types";

const dimensions: Array<{ key: keyof BiasScores; label: string; color: string }> = [
  { key: "ideology", label: "Ideology", color: "#3b82f6" },
  { key: "factual", label: "Factual", color: "#22c55e" },
  { key: "framing", label: "Framing", color: "#a855f7" },
  { key: "emotion", label: "Emotion", color: "#ef4444" },
  { key: "transparency", label: "Transparency", color: "#f59e0b" },
];

export function RadarChart({ scores }: { scores: BiasScores }) {
  const size = 260;
  const center = size / 2;
  const radius = size * 0.38;
  const angleStep = (Math.PI * 2) / dimensions.length;

  const points = dimensions.map((d, i) => {
    const value = Math.max(0, Math.min(100, scores[d.key])) / 100;
    const angle = -Math.PI / 2 + i * angleStep;
    const x = center + Math.cos(angle) * radius * value;
    const y = center + Math.sin(angle) * radius * value;
    return `${x},${y}`;
  });

  const gridRings = [0.25, 0.5, 0.75, 1];

  return (
    <div className="block mx-auto">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <g>
          {gridRings.map((r) => (
            <circle
              key={r}
              cx={center}
              cy={center}
              r={radius * r}
              fill="none"
              stroke="currentColor"
              strokeOpacity={0.12}
            />
          ))}
          {dimensions.map((_, i) => {
            const angle = -Math.PI / 2 + i * angleStep;
            const x = center + Math.cos(angle) * radius;
            const y = center + Math.sin(angle) * radius;
            return (
              <line
                key={i}
                x1={center}
                y1={center}
                x2={x}
                y2={y}
                stroke="currentColor"
                strokeOpacity={0.12}
              />
            );
          })}
        </g>

        <polygon
          points={points.join(" ")}
          fill="#0ea5e9"
          fillOpacity={0.15}
          stroke="#0ea5e9"
          strokeOpacity={0.8}
        />

        {dimensions.map((d, i) => {
          const angle = -Math.PI / 2 + i * angleStep;
          const x = center + Math.cos(angle) * (radius + 18);
          const y = center + Math.sin(angle) * (radius + 18);
          return (
            <text key={d.key} x={x} y={y} textAnchor="middle" dominantBaseline="middle" fontSize={11} fill="currentColor" fillOpacity={0.75}>
              {d.label}
            </text>
          );
        })}
      </svg>
    </div>
  );
}


