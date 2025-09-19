import { LabSidebar } from "@/components/lab-sidebar"
import { LabContent } from "@/components/lab-content"

export default function LabPage() {
  return (
    <div className="flex h-screen bg-background">
      <LabSidebar />
      <LabContent />
    </div>
  )
}
