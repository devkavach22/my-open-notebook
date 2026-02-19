'use client'

import { AppShell } from '@/components/layout/AppShell'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function HemanshiNotebookPage() {
  return (
    <AppShell>
      <div className="container mx-auto p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold">Hemanshi Notebook</h1>
          <p className="text-muted-foreground mt-2">
            Your personal notebook workspace
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Welcome to Hemanshi Notebook</CardTitle>
            <CardDescription>
              This is your custom notebook page. You can add your content here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p>Start building your notebook features here!</p>
          </CardContent>
        </Card>
      </div>
    </AppShell>
  )
}
