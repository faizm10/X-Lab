export function LabSidebar() {
  return (
    <div className="w-80 bg-sidebar border-r border-sidebar-border p-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2 bg-primary rounded-lg">
          <svg className="h-6 w-6 text-primary-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-sidebar-foreground">Faiz Lab</h1>
          <p className="text-sm text-muted-foreground">Development Environment</p>
        </div>
      </div>

      <div className="space-y-2">
        <div className="p-3 rounded-lg bg-card border border-border">
          <h3 className="font-medium text-card-foreground mb-2">Navigation</h3>
          <p className="text-sm text-muted-foreground">
            Add your navigation items here.
          </p>
        </div>
      </div>
    </div>
  )
}