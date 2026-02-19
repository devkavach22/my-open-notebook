# Complete LLM Flow Example - Chat Feature

This shows EXACTLY how data flows from user to LLM and back, with real code.

---

## Scenario: User Chats with AI About Their Notebook

**User Action**: Types "What are the main points about AI?" in chat

---

## Step-by-Step Flow with Real Code

### STEP 1: Frontend - User Types Message

**File**: `frontend/src/components/notebooks/ChatColumn.tsx`

```typescript
// User types in input box
const [input, setInput] = useState('')

// User hits Enter or clicks Send
const handleSend = async () => {
  // 1. Add user message to UI immediately (optimistic update)
  const userMessage = {
    role: 'user',
    content: input  // "What are the main points about AI?"
  }
  setMessages(prev => [...prev, userMessage])
  
  // 2. Clear input
  setInput('')
  
  // 3. Call API
  await executeChatMutation.mutate({
    session_id: currentSessionId,
    message: input,
    context: contextData  // Sources and notes from notebook
  })
}
```

---

### STEP 2: Frontend - Build Context

**File**: `frontend/src/lib/hooks/useNotebookChat.ts`

```typescript
// Before sending message, build context
const buildContext = async () => {
  // Get context configuration (which sources/notes to include)
  const contextConfig = {
    sources: {
      'source:abc123': 'full content',  // Include full text
      'source:def456': 'insights only'  // Include only AI summary
    },
    notes: {
      'note:xyz789': 'full content'
    }
  }
  
  // Call API to build context
  const response = await fetch('/api/chat/context', {
    method: 'POST',
    body: JSON.stringify({
      notebook_id: notebookId,
      context_config: contextConfig
    })
  })
  
  const contextData = await response.json()
  // Returns:
  // {
  //   context: {
  //     sources: [
  //       {
  //         id: 'source:abc123',
  //         title: 'AI Research Paper',
  //         content: 'Full text of paper...'
  //       }
  //     ],
  //     notes: [...]
  //   },
  //   token_count: 5000
  // }
  
  return contextData
}
```

---

### STEP 3: Frontend - Execute Chat

**File**: `frontend/src/lib/api/chat.ts`

```typescript
export const chatApi = {
  executeChat: async (data) => {
    const response = await apiClient.post('/chat/execute', {
      session_id: data.session_id,
      message: data.message,
      context: data.context,
      model_override: data.model_override
    })
    return response.data
  }
}
```

**HTTP Request**:
```http
POST http://localhost:8000/api/chat/execute
Content-Type: application/json

{
  "session_id": "chat_session:abc123",
  "message": "What are the main points about AI?",
  "context": {
    "sources": [
      {
        "id": "source:abc123",
        "title": "AI Research Paper",
        "content": "Artificial intelligence is transforming..."
      }
    ],
    "notes": [
      {
        "id": "note:xyz789",
        "title": "My AI Notes",
        "content": "Key insights about AI..."
      }
    ]
  },
  "model_override": "gpt-4"
}
```

---

### STEP 4: Backend - Receive Request

**File**: `api/routers/chat.py`

```python
@router.post("/chat/execute", response_model=ExecuteChatResponse)
async def execute_chat(request: ExecuteChatRequest):
    """
    Execute a chat request and get AI response.
    """
    try:
        # 1. Verify session exists
        full_session_id = (
            request.session_id
            if request.session_id.startswith("chat_session:")
            else f"chat_session:{request.session_id}"
        )
        session = await ChatSession.get(full_session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # 2. Determine model override
        model_override = (
            request.model_override
            if request.model_override is not None
            else getattr(session, "model_override", None)
        )
        
        # 3. Get current conversation state from LangGraph
        current_state = await asyncio.to_thread(
            chat_graph.get_state,
            config=RunnableConfig(configurable={"thread_id": full_session_id}),
        )
        
        # 4. Prepare state for execution
        state_values = current_state.values if current_state else {}
        state_values["messages"] = state_values.get("messages", [])
        state_values["context"] = request.context
        state_values["model_override"] = model_override
        
        # 5. Add user message to state
        from langchain_core.messages import HumanMessage
        user_message = HumanMessage(content=request.message)
        state_values["messages"].append(user_message)
        
        # Now state_values looks like:
        # {
        #     "messages": [
        #         HumanMessage("Hello"),
        #         AIMessage("Hi! How can I help?"),
        #         HumanMessage("What are the main points about AI?")
        #     ],
        #     "context": {
        #         "sources": [...],
        #         "notes": [...]
        #     },
        #     "model_override": "gpt-4"
        # }
        
        # 6. Execute chat graph (THIS IS WHERE LLM IS CALLED)
        result = chat_graph.invoke(
            input=state_values,
            config=RunnableConfig(
                configurable={
                    "thread_id": full_session_id,
                    "model_id": model_override,
                }
            ),
        )
        
        # 7. Update session timestamp
        await session.save()
        
        # 8. Convert messages to response format
        messages = []
        for msg in result.get("messages", []):
            messages.append(
                ChatMessage(
                    id=getattr(msg, "id", f"msg_{len(messages)}"),
                    type=msg.type,
                    content=msg.content,
                    timestamp=None,
                )
            )
        
        # 9. Return response
        return ExecuteChatResponse(
            session_id=request.session_id,
            messages=messages
        )
        
    except Exception as e:
        logger.error(f"Error executing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing chat: {str(e)}")
```

---

### STEP 5: LangGraph - Process Chat

**File**: `open_notebook/graphs/chat.py`

```python
from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage

class ThreadState(TypedDict):
    messages: list  # Conversation history
    context: dict   # Sources and notes
    model_override: str  # Which model to use

def call_model_with_messages(state: ThreadState, config: RunnableConfig) -> dict:
    """
    This function is called by LangGraph to generate AI response
    """
    
    # 1. Build system prompt with context
    system_prompt = build_system_prompt(state)
    # System prompt looks like:
    # """
    # You are a helpful AI assistant.
    # 
    # You have access to the following context from the user's notebook:
    # 
    # Sources:
    # - AI Research Paper: Artificial intelligence is transforming...
    # 
    # Notes:
    # - My AI Notes: Key insights about AI...
    # 
    # Answer the user's questions based on this context.
    # Be helpful, accurate, and cite sources when relevant.
    # """
    
    # 2. Prepare messages for LLM
    payload = [
        SystemMessage(content=system_prompt),
        ...state.get("messages", [])
    ]
    # payload now looks like:
    # [
    #     SystemMessage("You are a helpful AI assistant..."),
    #     HumanMessage("Hello"),
    #     AIMessage("Hi! How can I help?"),
    #     HumanMessage("What are the main points about AI?")
    # ]
    
    # 3. Get model ID
    model_id = config.get("configurable", {}).get("model_id") or state.get("model_override")
    # model_id = "gpt-4"
    
    # 4. Provision LangChain model
    model = await provision_langchain_model(
        str(payload),
        model_id,
        "chat",
        max_tokens=8192
    )
    # This creates a LangChain ChatOpenAI or ChatAnthropic instance
    
    # 5. Call LLM
    ai_message = model.invoke(payload)
    # LLM receives all messages and generates response
    
    # 6. Clean response (remove thinking tags)
    content = ai_message.content
    cleaned_content = clean_thinking_content(content)
    # Removes <think>...</think> tags if present
    
    cleaned_message = ai_message.model_copy(update={"content": cleaned_content})
    
    # 7. Return new message
    return {"messages": cleaned_message}

# Create LangGraph workflow
agent_state = StateGraph(ThreadState)
agent_state.add_node("agent", call_model_with_messages)
agent_state.add_edge(START, "agent")
agent_state.add_edge("agent", END)

# Compile with checkpoint (saves conversation state)
graph = agent_state.compile(checkpointer=memory)
```

---

### STEP 6: AI Provider - Call LLM

**File**: `open_notebook/ai/provision.py`

```python
async def provision_langchain_model(
    payload: str,
    model_id: str,
    purpose: str,
    max_tokens: int = 8192
):
    """
    Create LangChain model instance for the specified model
    """
    
    # 1. Get model configuration
    model = await Model.get(model_id)
    if not model:
        raise ValueError(f"Model {model_id} not found")
    
    # 2. Get API credentials
    credential = await model.get_credential()
    api_key = credential.decrypt_api_key()
    
    # 3. Create LangChain model based on provider
    if model.provider == "openai":
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model=model.model_name,  # "gpt-4"
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=0.7
        )
    
    elif model.provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        
        return ChatAnthropic(
            model=model.model_name,  # "claude-3-opus-20240229"
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=0.7
        )
    
    elif model.provider == "ollama":
        from langchain_ollama import ChatOllama
        
        return ChatOllama(
            model=model.model_name,  # "llama2"
            base_url="http://localhost:11434",
            temperature=0.7
        )
```

---

### STEP 7: OpenAI API - Generate Response

**What happens at OpenAI**:

```python
# LangChain internally makes this API call:

import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant.\n\nYou have access to the following context from the user's notebook:\n\nSources:\n- AI Research Paper: Artificial intelligence is transforming...\n\nNotes:\n- My AI Notes: Key insights about AI...\n\nAnswer the user's questions based on this context."
        },
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hi! How can I help?"
        },
        {
            "role": "user",
            "content": "What are the main points about AI?"
        }
    ],
    max_tokens=8192,
    temperature=0.7
)

# OpenAI returns:
# {
#     "choices": [{
#         "message": {
#             "role": "assistant",
#             "content": "Based on the sources in your notebook, here are the main points about AI:\n\n1. **Transformation**: AI is transforming various industries...\n2. **Key Technologies**: Machine learning, deep learning...\n3. **Applications**: Healthcare, finance, education...\n\nThese insights come from your AI Research Paper and notes."
#         }
#     }]
# }
```

---

### STEP 8: Backend - Return Response

**Back in**: `api/routers/chat.py`

```python
# After LangGraph execution completes:

result = chat_graph.invoke(...)
# result = {
#     "messages": [
#         HumanMessage("Hello"),
#         AIMessage("Hi! How can I help?"),
#         HumanMessage("What are the main points about AI?"),
#         AIMessage("Based on the sources in your notebook...")
#     ],
#     "context": {...},
#     "model_override": "gpt-4"
# }

# Convert to response format
messages = []
for msg in result.get("messages", []):
    messages.append(
        ChatMessage(
            id=msg.id,
            type=msg.type,  # "human" or "ai"
            content=msg.content,
            timestamp=None
        )
    )

# Return HTTP response
return ExecuteChatResponse(
    session_id=request.session_id,
    messages=messages
)
```

**HTTP Response**:
```json
{
  "session_id": "chat_session:abc123",
  "messages": [
    {
      "id": "msg_0",
      "type": "human",
      "content": "Hello",
      "timestamp": null
    },
    {
      "id": "msg_1",
      "type": "ai",
      "content": "Hi! How can I help?",
      "timestamp": null
    },
    {
      "id": "msg_2",
      "type": "human",
      "content": "What are the main points about AI?",
      "timestamp": null
    },
    {
      "id": "msg_3",
      "type": "ai",
      "content": "Based on the sources in your notebook, here are the main points about AI:\n\n1. **Transformation**: AI is transforming various industries...\n2. **Key Technologies**: Machine learning, deep learning...\n3. **Applications**: Healthcare, finance, education...\n\nThese insights come from your AI Research Paper and notes.",
      "timestamp": null
    }
  ]
}
```

---

### STEP 9: Frontend - Display Response

**File**: `frontend/src/components/notebooks/ChatColumn.tsx`

```typescript
// React Query mutation onSuccess callback
const executeChatMutation = useMutation({
  mutationFn: chatApi.executeChat,
  onSuccess: (data) => {
    // Update messages state with response
    setMessages(data.messages)
    
    // Scroll to bottom
    scrollToBottom()
  }
})

// Render messages
return (
  <div className="chat-messages">
    {messages.map((msg, index) => (
      <div 
        key={index}
        className={msg.type === 'human' ? 'user-message' : 'ai-message'}
      >
        <div className="message-content">
          {msg.content}
        </div>
      </div>
    ))}
  </div>
)
```

---

### STEP 10: User Sees Response

**On Screen**:

```
┌─────────────────────────────────────────┐
│ Chat                                    │
├─────────────────────────────────────────┤
│                                         │
│  You: Hello                             │
│                                         │
│  AI: Hi! How can I help?                │
│                                         │
│  You: What are the main points about AI?│
│                                         │
│  AI: Based on the sources in your       │
│      notebook, here are the main        │
│      points about AI:                   │
│                                         │
│      1. Transformation: AI is           │
│         transforming various            │
│         industries...                   │
│                                         │
│      2. Key Technologies: Machine       │
│         learning, deep learning...      │
│                                         │
│      3. Applications: Healthcare,       │
│         finance, education...           │
│                                         │
│      These insights come from your      │
│      AI Research Paper and notes.       │
│                                         │
├─────────────────────────────────────────┤
│ [Type your message...]          [Send]  │
└─────────────────────────────────────────┘
```

---

## Complete Data Flow Summary

```
1. User types: "What are the main points about AI?"
   ↓
2. Frontend builds context (sources + notes)
   ↓
3. Frontend sends POST /api/chat/execute
   {
       session_id, message, context
   }
   ↓
4. Backend receives request
   ↓
5. Backend loads conversation history from LangGraph
   ↓
6. Backend adds user message to history
   ↓
7. LangGraph builds system prompt with context
   ↓
8. LangGraph calls LLM with:
   - System prompt (with sources/notes)
   - Conversation history
   - New user message
   ↓
9. LLM (OpenAI/Anthropic/Ollama) generates response
   ↓
10. LangGraph saves conversation state
    ↓
11. Backend returns response
    ↓
12. Frontend displays AI message
    ↓
13. User sees answer!
```

---

## Key Takeaways

1. **Context is King**: Sources and notes are included in every LLM call
2. **State Management**: LangGraph saves conversation history
3. **Model Flexibility**: Can override model per session or per message
4. **Clean Responses**: Thinking tags are removed before showing to user
5. **Error Handling**: Multiple layers of error handling
6. **Async Operations**: Everything is async for performance

---

## Try It Yourself!

1. Open the chat in a notebook
2. Type a message
3. Open browser DevTools → Network tab
4. Watch the API call to `/api/chat/execute`
5. See the request payload and response
6. Trace through the code files!

Happy learning! 🚀
