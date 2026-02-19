# Mind Map Implementation Plan

## Goal
Create an interactive mind map that intelligently parses source content and creates a hierarchical visualization like the example image.

## Data Available
✅ Sources have `full_text` field with complete content
✅ Example: Criminal case with 9,243 and 17,190 characters
✅ Content includes incidents, people, locations, dates

## What Needs to Be Built

### 1. Backend: AI-Powered Content Analysis
Use LangChain/LLM to analyze `full_text` and extract:
- **Main Topics**: Key themes/events
- **Sub-topics**: Details under each theme
- **Entities**: People, places, dates
- **Relationships**: Connections between entities
- **Timeline**: Chronological order

### 2. Backend: Mind Map Endpoint
```python
POST /api/notebooks/{notebook_id}/mindmap
```

Response structure:
```json
{
  "notebook_id": "...",
  "notebook_name": "...",
  "root": {
    "id": "root",
    "label": "Notebook Name",
    "type": "root",
    "children": [
      {
        "id": "source_1",
        "label": "Source Title",
        "type": "main",
        "children": [
          {
            "id": "incident_1",
            "label": "1st Incident",
            "type": "sub",
            "children": [
              {"id": "detail_1", "label": "Date: 18 Feb 2012", "type": "detail"},
              {"id": "detail_2", "label": "Location: Jagsi", "type": "detail"},
              {"id": "detail_3", "label": "People: Ravi, Kapil", "type": "detail"}
            ]
          }
        ]
      }
    ]
  }
}
```

### 3. Frontend: Interactive Visualization
- Clickable nodes (expand/collapse)
- Zoom in/out
- Pan/drag
- Different colors for different node types
- Search/filter nodes
- Export as image/PDF

## Implementation Approach

### Option 1: Rule-Based Parsing (Simple)
- Split by keywords: "INCIDENT", "FIR", dates, etc.
- Extract entities using regex
- Create hierarchy based on structure
- **Pros**: Fast, no AI costs
- **Cons**: Limited, may miss context

### Option 2: AI-Powered Analysis (Recommended)
- Use LLM (OpenAI/Anthropic) to analyze content
- Prompt: "Extract key events, people, locations from this text and organize hierarchically"
- LLM returns structured JSON
- **Pros**: Intelligent, context-aware
- **Cons**: Requires AI API, costs money

### Option 3: Hybrid Approach
- Use rule-based for structure (incidents, dates)
- Use AI for summarization and entity extraction
- **Pros**: Balance of speed and intelligence
- **Cons**: More complex

## Example Prompt for AI Analysis

```
Analyze this criminal case document and extract:
1. List all incidents chronologically
2. For each incident, extract:
   - Date
   - Location
   - People involved
   - Crime type
   - FIR number
3. Organize as hierarchical JSON

Text: {full_text}

Return JSON format:
{
  "incidents": [
    {
      "title": "1st Incident",
      "date": "18 Feb 2012",
      "location": "Jagsi, Sonipat",
      "people": ["Ravi", "Kapil"],
      "crime": "Murder",
      "fir": "34/2012",
      "details": ["..."]
    }
  ]
}
```

## Technology Stack

### Backend
- Python + LangChain for AI analysis
- FastAPI endpoint
- Caching for performance

### Frontend
- React Flow or D3.js for visualization
- Or use a library like:
  - `react-d3-tree`
  - `reactflow`
  - `vis-network`

## Estimated Effort
- Backend AI analysis: 4-6 hours
- Backend endpoint: 2-3 hours
- Frontend visualization: 6-8 hours
- Testing & refinement: 3-4 hours
- **Total**: 15-21 hours

## Next Steps

1. **Choose approach** (AI-powered recommended)
2. **Set up AI provider** (OpenAI/Anthropic API key)
3. **Create prompt template** for content analysis
4. **Build backend endpoint** with AI integration
5. **Create frontend component** with visualization library
6. **Test with real data** and refine
7. **Add export/share features**

## Cost Considerations

Using OpenAI GPT-4:
- ~$0.03 per 1K tokens input
- ~$0.06 per 1K tokens output
- For 10K character document: ~$0.10-0.20 per analysis
- Can cache results to avoid re-analysis

## Alternative: Use Existing Mind Map Libraries

Instead of building from scratch, integrate:
- **Markmap**: Markdown to mind map
- **MindMup**: Open source mind mapping
- **Mermaid**: Diagram generation from text

These can generate mind maps from structured text, reducing development time.

## Recommendation

Start with a **simple AI-powered prototype**:
1. Use OpenAI to analyze one source
2. Extract 2-3 levels of hierarchy
3. Display in a simple tree view
4. Get feedback
5. Iterate and enhance

This approach allows quick validation before investing in complex visualization.
