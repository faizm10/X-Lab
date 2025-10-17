import Link from "next/link";
import type { Lab, Tool } from "../types";
import { Sparkline } from "./Sparkline";

export function NarrativeCard({ 
  narrative, 
  baseUrl = "/labs" 
}: { 
  narrative: Lab | Tool;
  baseUrl?: string;
}) {
  return (
    <Link
      href={`${baseUrl}/${narrative.id}`}
      className="rounded-2xl border border-foreground/10 p-6 hover:bg-foreground/[.03] transition-colors"
    >
      <div className="flex items-start justify-between">
        <h3 className="text-base font-semibold tracking-tight max-w-[70%]">{narrative.title}</h3>
        <span className="text-xs text-foreground/60">{narrative.intensity}</span>
      </div>
      <p className="mt-2 text-sm text-foreground/70 min-h-10">{narrative.summary}</p>
      <div className="mt-4 flex items-center justify-between">
        <div className="text-xs text-foreground/50 truncate max-w-[60%]">
          {narrative.keywords.join(" · ")}
        </div>
        <Sparkline values={narrative.sparkline} />
      </div>
    </Link>
  );
}


