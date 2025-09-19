"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Clock, Star, GitCommit, TrendingUp, Code, Database, Cpu, Network, Bookmark, Edit3, Share2 } from "lucide-react"

const mockSystemDesignContent = {
  title: "Microservices Architecture",
  description: "Comprehensive analysis of microservices patterns and implementation strategies",
  lastUpdated: "2 hours ago",
  progress: 75,
  highlights: [
    "Service decomposition strategies",
    "Inter-service communication patterns",
    "Data consistency challenges",
  ],
  sections: [
    {
      title: "Architecture Overview",
      content:
        "Microservices architecture breaks down applications into small, independent services that communicate over well-defined APIs.",
      highlighted: true,
    },
    {
      title: "Key Benefits",
      content: "Scalability, technology diversity, fault isolation, and independent deployment cycles.",
      highlighted: false,
    },
    {
      title: "Implementation Challenges",
      content: "Network latency, data consistency, service discovery, and monitoring complexity.",
      highlighted: true,
    },
  ],
}

const mockCodeExamples = [
  {
    title: "Service Discovery Pattern",
    language: "TypeScript",
    code: `// Service Registry Implementation
class ServiceRegistry {
  private services = new Map<string, ServiceInstance[]>()
  
  register(name: string, instance: ServiceInstance) {
    if (!this.services.has(name)) {
      this.services.set(name, [])
    }
    this.services.get(name)!.push(instance)
  }
  
  discover(name: string): ServiceInstance[] {
    return this.services.get(name) || []
  }
}`,
  },
  {
    title: "Circuit Breaker Pattern",
    language: "Python",
    code: `class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN`,
  },
]

const mockResearchNotes = [
  {
    title: "Attention Is All You Need",
    authors: "Vaswani et al.",
    year: "2017",
    summary: "Introduced the Transformer architecture, revolutionizing NLP with self-attention mechanisms.",
    tags: ["transformer", "attention", "nlp"],
    rating: 5,
    highlighted: "Self-attention allows the model to weigh the importance of different words in a sequence",
  },
  {
    title: "BERT: Pre-training of Deep Bidirectional Transformers",
    authors: "Devlin et al.",
    year: "2018",
    summary: "Bidirectional training of transformers for language understanding tasks.",
    tags: ["bert", "bidirectional", "pretraining"],
    rating: 5,
    highlighted: "Bidirectional context understanding significantly improves performance",
  },
]

export function LabContent() {
  const [activeTab, setActiveTab] = useState("overview")

  return (
    <div className="flex-1 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground mb-2">{mockSystemDesignContent.title}</h1>
            <p className="text-muted-foreground">{mockSystemDesignContent.description}</p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Button variant="outline" size="sm">
              <Bookmark className="h-4 w-4 mr-2" />
              Save
            </Button>
            <Button size="sm">
              <Edit3 className="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>
        </div>

        {/* Status Bar */}
        <Card className="bg-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">Updated {mockSystemDesignContent.lastUpdated}</span>
                </div>
                <div className="flex items-center gap-2">
                  <GitCommit className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">12 revisions</span>
                </div>
                <div className="flex items-center gap-2">
                  <Star className="h-4 w-4 text-primary" />
                  <span className="text-sm text-muted-foreground">Starred</span>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Progress</span>
                  <Progress value={mockSystemDesignContent.progress} className="w-24" />
                  <span className="text-sm font-medium">{mockSystemDesignContent.progress}%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="code">Code Examples</TabsTrigger>
            <TabsTrigger value="research">Research Notes</TabsTrigger>
            <TabsTrigger value="metrics">Metrics</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Key Highlights */}
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-primary" />
                  Key Highlights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-3">
                  {mockSystemDesignContent.highlights.map((highlight, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full" />
                      <span className="highlight-yellow px-1 py-0.5 rounded text-sm font-medium">{highlight}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Content Sections */}
            <div className="grid gap-6">
              {mockSystemDesignContent.sections.map((section, index) => (
                <Card key={index} className="bg-card border-border">
                  <CardHeader>
                    <CardTitle className="text-lg">{section.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p
                      className={`text-muted-foreground leading-relaxed ${
                        section.highlighted ? "highlight-pink px-2 py-1 rounded" : ""
                      }`}
                    >
                      {section.content}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="code" className="space-y-6">
            <div className="grid gap-6">
              {mockCodeExamples.map((example, index) => (
                <Card key={index} className="bg-card border-border">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        <Code className="h-5 w-5 text-secondary" />
                        {example.title}
                      </CardTitle>
                      <Badge variant="outline">{example.language}</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
                      <code className="text-sm font-mono text-muted-foreground">{example.code}</code>
                    </pre>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="research" className="space-y-6">
            <div className="grid gap-6">
              {mockResearchNotes.map((note, index) => (
                <Card key={index} className="bg-card border-border">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg mb-2">{note.title}</CardTitle>
                        <CardDescription>
                          {note.authors} • {note.year}
                        </CardDescription>
                      </div>
                      <div className="flex items-center gap-1">
                        {Array.from({ length: note.rating }).map((_, i) => (
                          <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                        ))}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-muted-foreground leading-relaxed">{note.summary}</p>
                    <div className="highlight-yellow px-3 py-2 rounded-lg">
                      <p className="text-sm font-medium text-foreground">💡 Key Insight: {note.highlighted}</p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {note.tags.map((tag, tagIndex) => (
                        <Badge key={tagIndex} variant="secondary" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="metrics" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <Cpu className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-foreground">94%</p>
                      <p className="text-sm text-muted-foreground">CPU Efficiency</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-secondary/10 rounded-lg">
                      <Network className="h-5 w-5 text-secondary" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-foreground">2.3ms</p>
                      <p className="text-sm text-muted-foreground">Avg Latency</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-chart-3/10 rounded-lg">
                      <Database className="h-5 w-5 text-chart-3" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-foreground">1.2TB</p>
                      <p className="text-sm text-muted-foreground">Data Processed</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-chart-4/10 rounded-lg">
                      <TrendingUp className="h-5 w-5 text-chart-4" />
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-foreground">99.9%</p>
                      <p className="text-sm text-muted-foreground">Uptime</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
