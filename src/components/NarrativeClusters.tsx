"use client";
import * as React from "react";
import { useRouter } from "next/navigation";
import type { NarrativeCluster } from "@/types";

function hashToNumber(input: string): number {
  let h = 2166136261;
  for (let i = 0; i < input.length; i++) {
    h ^= input.charCodeAt(i);
    h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
  }
  return Math.abs(h >>> 0) / 2 ** 32;
}

export function NarrativeClusters({ items }: { items: NarrativeCluster[] }) {
  const router = useRouter();
  const width = 900;
  const height = 420;

  // Deterministic positions using simple jittered grid based on id hash
  const cols = 6;
  const cellW = width / cols;
  const cellH = height / Math.ceil(items.length / cols);

  const nodes = items.map((n, idx) => {
    const r = 24 + (n.intensity / 100) * 36;
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    const jx = (hashToNumber(n.id + "x") - 0.5) * cellW * 0.3;
    const jy = (hashToNumber(n.id + "y") - 0.5) * cellH * 0.3;
    const cx = col * cellW + cellW / 2 + jx;
    const cy = row * cellH + cellH / 2 + jy;
    const hue = 210 + Math.round((n.sentiment + 1) * 30); // blueish range by sentiment
    const fill = `hsl(${hue} 80% 60% / 0.20)`;
    const stroke = `hsl(${hue} 80% 55% / 0.75)`;
    return { n, r, cx, cy, fill, stroke };
  });

  return (
    <div className="w-full overflow-x-auto">
      <svg width={width} height={height} className="mx-auto block">
        {nodes.map(({ n, r, cx, cy, fill, stroke }) => (
          <g key={n.id} transform={`translate(${cx},${cy})`} className="cursor-pointer" onClick={() => router.push(`/narratives/${n.id}`)}>
            <circle r={r} fill={fill} stroke={stroke} strokeWidth={2} />
            <text textAnchor="middle" dominantBaseline="middle" fontSize={11} fill="currentColor" fillOpacity={0.85} style={{ pointerEvents: "none" }}>
              {n.title}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
}


