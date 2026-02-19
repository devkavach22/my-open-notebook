'use client'

import { useMemo, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Brain, 
  Mic, 
  Sparkles, 
  Video,
  BarChart3,
  BookOpen,
  Presentation,
  Table,
  Plus
} from 'lucide-react'
import { CollapsibleColumn, createCollapseButton } from '@/components/notebooks/CollapsibleColumn'
import { useNotebookColumnsStore } from '@/lib/stores/notebook-columns-store'
import { useTranslation } from '@/lib/hooks/use-translation'
import { NoteResponse } from '@/lib/types/api'
import { cn } from '@/lib/utils'
import { MindMapDialog } from '@/components/notebooks/MindMapDialog'

interface StudioColumnProps {
  notebookId: string
  notebookName?: string
  notes?: NoteResponse[]
}

interface StudioFeature {
  id: string
  icon: React.ElementType
  label: string
  description: string
  available: boolean
  onClick?: () => void
}

export function StudioColumn({ notebookId, notebookName, notes }: StudioColumnProps) {
  const { t } = useTranslation()
  const [mindMapOpen, setMindMapOpen] = useState(false)

  // Collapsible column state
  const { studioCollapsed, toggleStudio } = useNotebookColumnsStore()
  const collapseButton = useMemo(
    () => createCollapseButton(toggleStudio, 'Studio'),
    [toggleStudio]
  )

  const features: StudioFeature[] = [
    {
      id: 'audio',
      icon: Mic,
      label: 'Audio Overview',
      description: 'Generate podcast from sources',
      available: true,
      onClick: () => {
        // Navigate to podcasts page or open dialog
        window.location.href = '/podcasts'
      }
    },
    {
      id: 'video',
      icon: Video,
      label: 'Video Overview',
      description: 'Create video summary',
      available: true,
      onClick: () => {
        alert('Video Overview feature coming soon! This will create video summaries with visuals and voiceover.')
      }
    },
    {
      id: 'mindmap',
      icon: Brain,
      label: 'Mind Map',
      description: 'Visualize connections',
      available: true,
      onClick: () => {
        setMindMapOpen(true)
      }
    },
    {
      id: 'reports',
      icon: BarChart3,
      label: 'Reports',
      description: 'Generate analysis reports',
      available: true,
      onClick: () => {
        alert('Reports feature coming soon! This will generate detailed analysis reports with charts and insights.')
      }
    },
    {
      id: 'flashcards',
      icon: BookOpen,
      label: 'Flashcards',
      description: 'Study cards from content',
      available: true,
      onClick: () => {
        alert('Flashcards feature coming soon! This will auto-generate study cards from your sources.')
      }
    },
    {
      id: 'quiz',
      icon: Sparkles,
      label: 'Quiz',
      description: 'Test your knowledge',
      available: true,
      onClick: () => {
        alert('Quiz feature coming soon! This will create interactive quizzes to test your knowledge.')
      }
    },
    {
      id: 'infographic',
      icon: Presentation,
      label: 'Infographic',
      description: 'Visual summary',
      available: true,
      onClick: () => {
        alert('Infographic feature coming soon! This will create beautiful visual summaries of your content.')
      }
    },
    {
      id: 'slides',
      icon: Presentation,
      label: 'Slide Deck',
      description: 'Create presentation',
      available: true,
      onClick: () => {
        alert('Slide Deck feature coming soon! This will auto-generate presentation slides from your sources.')
      }
    },
    {
      id: 'table',
      icon: Table,
      label: 'Data Table',
      description: 'Structured data view',
      available: true,
      onClick: () => {
        alert('Data Table feature coming soon! This will extract and organize data from your sources.')
      }
    }
  ]

  return (
    <CollapsibleColumn
      isCollapsed={studioCollapsed}
      onToggle={toggleStudio}
      collapsedIcon={Sparkles}
      collapsedLabel="Studio"
    >
      <Card className="h-full flex flex-col flex-1 overflow-hidden">
        <CardHeader className="pb-3 flex-shrink-0 border-b">
          <div className="flex items-center justify-between gap-2">
            <CardTitle className="text-lg">Studio</CardTitle>
            {collapseButton}
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto min-h-0 p-6">
          {/* Audio Overview Banner */}
       

          {/* Studio Features Grid */}
          <div className="grid grid-cols-2 gap-3">
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <button
                  key={feature.id}
                  onClick={feature.available ? feature.onClick : undefined}
                  className={cn(
                    'p-4 rounded-lg border text-left transition-all',
                    'hover:border-primary/50 hover:bg-accent/50',
                    'focus:outline-none focus:ring-2 focus:ring-primary/20',
                    'group relative'
                  )}
                >
                  <div className="flex flex-col gap-2">
                    <Icon className="h-5 w-5 text-primary" />
                    <div>
                      <div className="font-medium text-sm mb-0.5">
                        {feature.label}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {feature.description}
                      </div>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>

          {/* Add Note Button */}
          <div className="mt-6 pt-6 border-t">
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => {
                // Open note dialog
                console.log('Add note clicked')
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add note
            </Button>
            <p className="text-xs text-muted-foreground text-center mt-2">
              Studio output will be saved here
            </p>
          </div>
        </CardContent>
      </Card>

      <MindMapDialog
        open={mindMapOpen}
        onOpenChange={setMindMapOpen}
        notebookId={notebookId}
        notebookName={notebookName}
      />
    </CollapsibleColumn>
  )
}
