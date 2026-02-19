import asyncio
import sys
sys.path.insert(0, '.')

from open_notebook.domain.notebook import Notebook, Source

async def test():
    print("Testing mind map data fetching...")
    
    notebook_id = "notebook:kuo7qmjwlrbllbpxw4lm"
    
    # Get notebook
    print(f"\n1. Fetching notebook {notebook_id}...")
    notebook = await Notebook.get(notebook_id)
    print(f"   ✓ Found: {notebook.name}")
    
    # Get sources
    print(f"\n2. Fetching sources...")
    sources = await notebook.get_sources()
    print(f"   ✓ Found {len(sources)} sources")
    
    # Check each source
    for idx, source in enumerate(sources):
        print(f"\n3.{idx+1} Source: {source.title}")
        print(f"     ID: {source.id}")
        print(f"     Has full_text: {source.full_text is not None}")
        if source.full_text:
            print(f"     Length: {len(source.full_text)}")
        
        # Try fetching full source
        print(f"     Fetching full source...")
        try:
            full_source = await Source.get(source.id)
            print(f"     ✓ Got full source")
            print(f"     Has full_text: {full_source.full_text is not None}")
            if full_source.full_text:
                print(f"     Length: {len(full_source.full_text)}")
                print(f"     First 100 chars: {full_source.full_text[:100]}")
        except Exception as e:
            print(f"     ✗ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
