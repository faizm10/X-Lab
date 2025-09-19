'use client'

import { ThemeToggle } from '../components/theme-toggle'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h1 className="text-4xl font-bold text-foreground mb-4">
                Welcome to Your Lab
              </h1>
              <p className="text-lg text-muted-foreground">
                Start building something amazing from here.
              </p>
            </div>
            <ThemeToggle />
          </div>
          
          <div className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-card-foreground mb-4">
              Ready to begin?
            </h2>
            <p className="text-muted-foreground mb-4">
              Your project has been cleaned up and is ready for development. 
              Start adding your components and features here.
            </p>
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>✨ Now featuring the playful Poppins font</p>
              <p>🌓 Theme switching is enabled (try the toggle!)</p>
              <p>🎨 Clean, minimal starting point</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
