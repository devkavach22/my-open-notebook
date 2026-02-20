'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ModelSelector } from '@/components/common/ModelSelector'
import { useTranslation } from '@/lib/hooks/use-translation'
import { api } from '@/lib/api-client'
import { Sparkles, Copy, Check, Download } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SummaryDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  notebookId: string
  notebookName?: string
}

export function SummaryDialog({ open, onOpenChange, notebookId, notebookName }: SummaryDialogProps) {
  const { t } = useTranslation()
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [summary, setSummary] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [copied, setCopied] = useState(false)

  const handleGenerate = async () => {
    if (!selectedModel) {
      setError('Please select a model')
      return
    }

    setIsGenerating(true)
    setError('')
    setSummary('')

    try {
      const response = await api.post(`/api/notebooks/${notebookId}/summary`, {
        notebook_id: notebookId,
        model_id: selectedModel
      })

      setSummary(response.summary)
    } catch (err: any) {
      console.error('Error generating summary:', err)
      setError(err.message || 'Failed to generate summary')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = async () => {
    if (summary) {
      await navigator.clipboard.writeText(summary)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleDownload = () => {
    if (summary) {
      const blob = new Blob([summary], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${notebookName || 'notebook'}-summary.md`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  }

  const handleClose = () => {
    onOpenChange(false)
    // Reset state after dialog closes
    setTimeout(() => {
      setSummary('')
      setError('')
      setCopied(false)
    }, 300)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Generate Summary
          </DialogTitle>
          <DialogDescription>
            Create a comprehensive AI-generated summary of all sources in {notebookName || 'this notebook'}
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {/* Model Selection */}
          {!summary && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Select AI Model</label>
              <ModelSelector
                value={selectedModel}
                onChange={setSelectedModel}
                modelType="language"
              />
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          {/* Loading State */}
          {isGenerating && (
            <div className="flex flex-col items-center justify-center py-12 space-y-4">
              <LoadingSpinner size="lg" />
              <div className="text-center space-y-2">
                <p className="text-sm font-medium">Generating summary...</p>
                <p className="text-xs text-muted-foreground">
                  This may take a minute depending on the amount of content
                </p>
              </div>
            </div>
          )}

          {/* Summary Display */}
          {summary && !isGenerating && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium">Generated Summary</h3>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleCopy}
                    className="gap-2"
                  >
                    {copied ? (
                      <>
                        <Check className="h-4 w-4" />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy className="h-4 w-4" />
                        Copy
                      </>
                    )}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleDownload}
                    className="gap-2"
                  >
                    <Download className="h-4 w-4" />
                    Download
                  </Button>
                </div>
              </div>

              <div className="prose prose-sm dark:prose-invert max-w-none p-4 bg-muted/30 rounded-lg border overflow-y-auto max-h-[500px]">
                <div className="whitespace-pre-wrap">{summary}</div>
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-2 pt-4 border-t">
          {!summary && (
            <>
              <Button variant="outline" onClick={handleClose}>
                Cancel
              </Button>
              <Button
                onClick={handleGenerate}
                disabled={!selectedModel || isGenerating}
                className="gap-2"
              >
                <Sparkles className="h-4 w-4" />
                Generate Summary
              </Button>
            </>
          )}
          {summary && (
            <>
              <Button variant="outline" onClick={() => setSummary('')}>
                Generate New
              </Button>
              <Button onClick={handleClose}>
                Close
              </Button>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
