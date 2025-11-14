interface StatGridProps {
  total: number;
  active: number;
  remote: number;
  cities: number;
}

const labels: Record<keyof StatGridProps, string> = {
  total: "Total roles",
  active: "Active right now",
  remote: "Remote-friendly",
  cities: "Cities represented",
};

export function StatGrid(stats: StatGridProps) {
  return (
    <section className="panel stat-grid">
      {Object.entries(stats).map(([key, value]) => (
        <article key={key} className="stat-grid__item">
          <p>{labels[key as keyof StatGridProps]}</p>
          <strong>{value}</strong>
        </article>
      ))}
    </section>
  );
}

