'use client'

import { useState, useEffect } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { 
  Brain, 
  Download, 
  ZoomIn, 
  ZoomOut, 
  ChevronDown, 
  ChevronRight,
  Maximize2,
  Minimize2,
  RefreshCw,
  Sparkles
} from 'lucide-react'

interface MindMapNode {
  id: string
  label: string
  type: 'root' | 'main' | 'sub' | 'detail'
  children?: MindMapNode[]
}

interface MindMapDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  notebookId: string
  notebookName?: string
}

export function MindMapDialog({
  open,
  onOpenChange,
  notebookId,
  notebookName,
}: MindMapDialogProps) {
  const [loading, setLoading] = useState(false)
  const [mindMapData, setMindMapData] = useState<MindMapNode | null>(null)
  const [zoom, setZoom] = useState(0.9)
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set(['root']))
  const [fullscreen, setFullscreen] = useState(false)

  useEffect(() => {
    if (open && !mindMapData) {
      generateMindMap()
    }
  }, [open])

  const generateMindMap = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/notebooks/${notebookId}/mindmap`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate mind map')
      }

      const data = await response.json()
      setMindMapData(data.root)
      // Auto-expand root and first level
      const newExpanded = new Set<string>(['root'])
      if (data.root.children) {
        data.root.children.forEach((child: MindMapNode) => {
          newExpanded.add(child.id)
        })
      }
      setExpandedNodes(newExpanded)
    } catch (error) {
      console.error('Failed to generate mind map:', error)
      alert(`Failed to generate mind map: ${error}`)
    } finally {
      setLoading(false)
    }
  }

  const toggleNode = (nodeId: string) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId)
    } else {
      newExpanded.add(nodeId)
    }
    setExpandedNodes(newExpanded)
  }

  const expandAll = () => {
    const allIds = new Set<string>()
    const collectIds = (node: MindMapNode) => {
      allIds.add(node.id)
      node.children?.forEach(collectIds)
    }
    if (mindMapData) collectIds(mindMapData)
    setExpandedNodes(allIds)
  }

  const collapseAll = () => {
    setExpandedNodes(new Set(['root']))
  }

  const renderNode = (node: MindMapNode, level: number = 0) => {
    const isExpanded = expandedNodes.has(node.id)
    const hasChildren = node.children && node.children.length > 0

    // Professional color schemes with depth
    const nodeStyles = {
      root: {
        bg: 'bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700',
        border: 'border-violet-400',
        text: 'text-white',
        shadow: 'shadow-2xl shadow-violet-500/50',
        hover: 'hover:shadow-violet-500/70 hover:scale-105',
        glow: 'ring-4 ring-violet-300/30',
      },
      main: {
        bg: 'bg-gradient-to-br from-blue-500 to-cyan-600',
        border: 'border-blue-300 dark:border-blue-600',
        text: 'text-white',
        shadow: 'shadow-xl shadow-blue-500/40',
        hover: 'hover:shadow-blue-500/60 hover:scale-105',
        glow: 'ring-2 ring-blue-300/20',
      },
      sub: {
        bg: 'bg-gradient-to-br from-emerald-400 to-teal-500 dark:from-emerald-600 dark:to-teal-700',
        border: 'border-emerald-300 dark:border-emerald-600',
        text: 'text-white',
        shadow: 'shadow-lg shadow-emerald-500/30',
        hover: 'hover:shadow-emerald-500/50 hover:scale-103',
        glow: 'ring-2 ring-emerald-300/20',
      },
      detail: {
        bg: 'bg-white dark:bg-gray-800',
        border: 'border-gray-300 dark:border-gray-600',
        text: 'text-gray-800 dark:text-gray-200',
        shadow: 'shadow-md shadow-gray-400/20 dark:shadow-gray-900/40',
        hover: 'hover:shadow-lg hover:scale-102',
        glow: 'ring-1 ring-gray-200 dark:ring-gray-700',
      },
    }

    const sizes = {
      root: 'text-2xl font-bold px-10 py-6 min-w-[280px]',
      main: 'text-lg font-semibold px-8 py-5 min-w-[240px]',
      sub: 'text-base font-medium px-6 py-4 min-w-[200px]',
      detail: 'text-sm px-5 py-3 min-w-[160px]',
    }

    const style = nodeStyles[node.type]

    return (
      <div 
        key={node.id} 
        className="flex flex-row items-center gap-6 animate-in fade-in slide-in-from-left-5 duration-500"
        style={{ animationDelay: `${level * 50}ms` }}
      >
        {/* Node Container */}
        <div className="relative group">
          {/* Glow effect on hover */}
          {node.type === 'root' && (
            <div className="absolute -inset-1 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl blur opacity-30 group-hover:opacity-50 transition duration-300" />
          )}
          
          {/* Main Node */}
          <div
            className={`
              relative rounded-2xl border-2 
              ${style.bg} ${style.border} ${style.text} ${style.shadow} ${style.glow}
              ${sizes[node.type]}
              ${hasChildren ? 'cursor-pointer' : 'cursor-default'}
              ${style.hover}
              transition-all duration-300 ease-out
              flex items-center gap-4
              backdrop-blur-sm
            `}
            onClick={() => hasChildren && toggleNode(node.id)}
          >
            {/* Expand/Collapse Icon */}
            {hasChildren && (
              <div className={`
                flex-shrink-0 p-1.5 rounded-lg
                ${node.type === 'root' ? 'bg-white/20' : 'bg-black/10 dark:bg-white/10'}
                transition-transform duration-300
                ${isExpanded ? 'rotate-0' : '-rotate-90'}
              `}>
                <ChevronDown className="h-5 w-5" />
              </div>
            )}
            
            {/* Icon for root node */}
            {node.type === 'root' && (
              <Sparkles className="h-6 w-6 flex-shrink-0 animate-pulse" />
            )}
            
            {/* Label */}
            <span className="break-words text-left flex-1 leading-relaxed">
              {node.label}
            </span>
            
            {/* Child Count Badge */}
            {hasChildren && (
              <div className={`
                flex-shrink-0 px-3 py-1 rounded-full text-xs font-bold
                ${node.type === 'root' 
                  ? 'bg-white/30 text-white' 
                  : node.type === 'main'
                  ? 'bg-white/30 text-white'
                  : node.type === 'sub'
                  ? 'bg-white/30 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }
                backdrop-blur-sm
              `}>
                {node.children?.length}
              </div>
            )}
          </div>

          {/* Hover Tooltip for long text */}
          {node.label.length > 60 && (
            <div className="absolute left-full top-1/2 -translate-y-1/2 ml-4 px-4 py-3 bg-gray-900 text-white text-sm rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-normal max-w-md z-50 shadow-2xl">
              <div className="font-medium mb-1">Full Content:</div>
              <div className="text-gray-300">{node.label}</div>
            </div>
          )}
        </div>

        {/* Children Container - Expand to RIGHT */}
        {hasChildren && isExpanded && (
          <div className="flex flex-col gap-5 animate-in slide-in-from-left-3 duration-400">
            {node.children!.map((child, index) => (
              <div 
                key={child.id} 
                className="flex flex-row items-center gap-4"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Connection Line with gradient */}
                <div className="relative flex items-center">
                  <div className={`
                    w-12 h-0.5 
                    ${node.type === 'root' 
                      ? 'bg-gradient-to-r from-violet-400 to-blue-500' 
                      : node.type === 'main'
                      ? 'bg-gradient-to-r from-blue-400 to-emerald-500'
                      : node.type === 'sub'
                      ? 'bg-gradient-to-r from-emerald-400 to-gray-400'
                      : 'bg-gray-300 dark:bg-gray-600'
                    }
                    shadow-sm
                  `} />
                  {/* Connection dot */}
                  <div className={`
                    absolute left-0 w-2 h-2 rounded-full -translate-x-1
                    ${node.type === 'root' 
                      ? 'bg-violet-400' 
                      : node.type === 'main'
                      ? 'bg-blue-400'
                      : node.type === 'sub'
                      ? 'bg-emerald-400'
                      : 'bg-gray-400'
                    }
                  `} />
                </div>
                
                {/* Recursive Child Node */}
                {renderNode(child, level + 1)}
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={`
        ${fullscreen ? 'max-w-[98vw] h-[98vh]' : 'max-w-[95vw] max-h-[92vh]'} 
        overflow-hidden flex flex-col transition-all duration-300
        bg-gradient-to-br from-white via-blue-50/30 to-purple-50/30
        dark:from-gray-950 dark:via-blue-950/20 dark:to-purple-950/20
      `}>
        <DialogHeader className="border-b border-gray-200 dark:border-gray-800 pb-4">
          <DialogTitle className="flex items-center gap-4 text-3xl">
            <div className="p-2 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 shadow-lg">
              <Brain className="h-7 w-7 text-white" />
            </div>
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-3">
                <span className="bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent font-bold">
                  AI Mind Map
                </span>
                <span className="text-sm px-3 py-1 rounded-full bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300 font-medium">
                  Powered by AI
                </span>
              </div>
              <span className="text-base font-normal text-gray-600 dark:text-gray-400">
                {notebookName}
              </span>
            </div>
          </DialogTitle>
          <DialogDescription className="text-base mt-2 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-violet-500" />
            <span>Click nodes to explore • AI-generated intelligent hierarchy</span>
          </DialogDescription>
        </DialogHeader>

        {/* Toolbar */}
        <div className="flex items-center gap-2 py-3 border-b border-gray-200 dark:border-gray-800 flex-wrap bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm">
          {/* Zoom Controls */}
          <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-800">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setZoom(Math.min(zoom + 0.1, 2))}
              className="h-8 w-8 p-0 hover:bg-blue-100 dark:hover:bg-blue-900/30"
            >
              <ZoomIn className="h-4 w-4" />
            </Button>
            <span className="text-sm font-mono font-medium px-2 min-w-[60px] text-center">
              {Math.round(zoom * 100)}%
            </span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setZoom(Math.max(zoom - 0.1, 0.5))}
              className="h-8 w-8 p-0 hover:bg-blue-100 dark:hover:bg-blue-900/30"
            >
              <ZoomOut className="h-4 w-4" />
            </Button>
          </div>

          <div className="w-px h-8 bg-gray-300 dark:bg-gray-700" />

          {/* Expand/Collapse */}
          <Button
            variant="outline"
            size="sm"
            onClick={expandAll}
            className="hover:bg-green-50 dark:hover:bg-green-900/20 hover:border-green-300"
          >
            <ChevronDown className="h-4 w-4 mr-2" />
            Expand All
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={collapseAll}
            className="hover:bg-orange-50 dark:hover:bg-orange-900/20 hover:border-orange-300"
          >
            <ChevronRight className="h-4 w-4 mr-2" />
            Collapse All
          </Button>

          <div className="w-px h-8 bg-gray-300 dark:bg-gray-700" />

          {/* Regenerate */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setMindMapData(null)
              generateMindMap()
            }}
            className="hover:bg-purple-50 dark:hover:bg-purple-900/20 hover:border-purple-300"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Regenerate
          </Button>

          <div className="flex-1" />

          {/* Fullscreen */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => setFullscreen(!fullscreen)}
            className="hover:bg-indigo-50 dark:hover:bg-indigo-900/20 hover:border-indigo-300"
          >
            {fullscreen ? (
              <Minimize2 className="h-4 w-4" />
            ) : (
              <Maximize2 className="h-4 w-4" />
            )}
          </Button>

          {/* Export (disabled) */}
          <Button 
            variant="outline" 
            size="sm" 
            disabled 
            className="opacity-50"
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>

        {/* Canvas */}
        <div className="flex-1 overflow-auto p-8 relative">
          {/* Background pattern */}
          <div className="absolute inset-0 opacity-30 dark:opacity-10" style={{
            backgroundImage: 'radial-gradient(circle, #e5e7eb 1px, transparent 1px)',
            backgroundSize: '30px 30px'
          }} />

          {loading ? (
            <div className="flex items-center justify-center h-full relative z-10">
              <div className="text-center space-y-6">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-24 h-24 rounded-full bg-gradient-to-r from-violet-600 to-indigo-600 opacity-20 animate-ping" />
                  </div>
                  <LoadingSpinner size="lg" />
                </div>
                <div className="space-y-3">
                  <p className="text-xl font-semibold text-gray-800 dark:text-gray-200 flex items-center justify-center gap-2">
                    <Sparkles className="h-5 w-5 text-violet-500 animate-pulse" />
                    AI is analyzing your sources...
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Extracting insights and building intelligent hierarchy
                  </p>
                </div>
              </div>
            </div>
          ) : mindMapData ? (
            <div
              className="flex items-start min-w-max transition-transform duration-200 relative z-10"
              style={{ 
                transform: `scale(${zoom})`, 
                transformOrigin: 'left center',
                paddingLeft: '40px'
              }}
            >
              {renderNode(mindMapData)}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full relative z-10">
              <div className="text-center space-y-6">
                <div className="p-6 rounded-full bg-gradient-to-br from-violet-100 to-indigo-100 dark:from-violet-900/30 dark:to-indigo-900/30 inline-block">
                  <Brain className="h-16 w-16 text-violet-600 dark:text-violet-400" />
                </div>
                <div className="space-y-2">
                  <p className="text-xl font-semibold text-gray-800 dark:text-gray-200">
                    No sources available
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Add sources to your notebook to generate a mind map
                  </p>
                </div>
                <Button
                  variant="outline"
                  className="mt-4"
                  onClick={generateMindMap}
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Try Again
                </Button>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
