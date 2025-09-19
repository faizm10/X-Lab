"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  FlaskConical,
  Code2,
  Database,
  StickyNote,
  Zap,
  GitBranch,
  Server,
  Brain,
  ChevronRight,
  ChevronDown,
} from "lucide-react"

const labSections = [
  {
    id: "system-design",
    title: "System Design",
    icon: Server,
    items: [
      { id: "microservices", title: "Microservices Architecture", status: "active" },
      { id: "load-balancing", title: "Load Balancing Patterns", status: "draft" },
      { id: "caching", title: "Caching Strategies", status: "complete" },
      { id: "database-sharding", title: "Database Sharding", status: "draft" },
    ],
  },
  {
    id: "software-engineering",
    title: "Software Engineering",
    icon: Code2,
    items: [
      { id: "design-patterns", title: "Design Patterns Lab", status: "active" },
      { id: "algorithms", title: "Algorithm Analysis", status: "complete" },
      { id: "testing", title: "Testing Strategies", status: "draft" },
      { id: "refactoring", title: "Refactoring Techniques", status: "complete" },
    ],
  },
  {
    id: "research-notes",
    title: "Research Notes",
    icon: Brain,
    items: [
      { id: "ai-papers", title: "AI/ML Paper Reviews", status: "active" },
      { id: "tech-trends", title: "Tech Trend Analysis", status: "draft" },
      { id: "performance", title: "Performance Benchmarks", status: "complete" },
      { id: "security", title: "Security Research", status: "draft" },
    ],
  },
]

interface LabSidebarProps {
  onItemSelect?: (sectionId: string, itemId: string) => void
}

export function LabSidebar({ onItemSelect }: LabSidebarProps) {
  const [expandedSections, setExpandedSections] = useState<string[]>(["system-design"])
  const [activeItem, setActiveItem] = useState("microservices")

  const toggleSection = (sectionId: string) => {
    setExpandedSections((prev) =>
      prev.includes(sectionId) ? prev.filter((id) => id !== sectionId) : [...prev, sectionId],
    )
  }

  const handleItemClick = (sectionId: string, itemId: string) => {
    setActiveItem(itemId)
    onItemSelect?.(sectionId, itemId)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-primary text-primary-foreground"
      case "complete":
        return "bg-secondary text-secondary-foreground"
      case "draft":
        return "bg-muted text-muted-foreground"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  return (
    <div className="w-80 bg-sidebar border-r border-sidebar-border p-4 overflow-y-auto">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2 bg-primary rounded-lg">
          <FlaskConical className="h-6 w-6 text-primary-foreground" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-sidebar-foreground">Engineering Lab</h1>
          <p className="text-sm text-muted-foreground">Research & Development</p>
        </div>
      </div>

      <div className="space-y-4">
        {labSections.map((section) => {
          const Icon = section.icon
          const isExpanded = expandedSections.includes(section.id)

          return (
            <Card key={section.id} className="bg-card border-border">
              <Button
                variant="ghost"
                className="w-full justify-between p-4 h-auto"
                onClick={() => toggleSection(section.id)}
              >
                <div className="flex items-center gap-3">
                  <Icon className="h-5 w-5 text-sidebar-accent" />
                  <span className="font-medium text-card-foreground">{section.title}</span>
                </div>
                {isExpanded ? (
                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>

              {isExpanded && (
                <div className="px-4 pb-4 space-y-2">
                  {section.items.map((item) => (
                    <Button
                      key={item.id}
                      variant={activeItem === item.id ? "secondary" : "ghost"}
                      className="w-full justify-between p-3 h-auto"
                      onClick={() => handleItemClick(section.id, item.id)}
                    >
                      <span className="text-sm font-medium">{item.title}</span>
                      <Badge variant="outline" className={`text-xs ${getStatusColor(item.status)}`}>
                        {item.status}
                      </Badge>
                    </Button>
                  ))}
                </div>
              )}
            </Card>
          )
        })}
      </div>

      <div className="mt-8 p-4 bg-card rounded-lg border border-border">
        <div className="flex items-center gap-2 mb-2">
          <Zap className="h-4 w-4 text-primary" />
          <span className="text-sm font-medium text-card-foreground">Quick Actions</span>
        </div>
        <div className="space-y-2">
          <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
            <GitBranch className="h-4 w-4 mr-2" />
            New Experiment
          </Button>
          <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
            <Database className="h-4 w-4 mr-2" />
            Import Data
          </Button>
          <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
            <StickyNote className="h-4 w-4 mr-2" />
            Quick Note
          </Button>
        </div>
      </div>
    </div>
  )
}
