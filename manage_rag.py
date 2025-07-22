#!/usr/bin/env python
"""
Script to manage RAG system with FAISS
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict

# Add root directory to path for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="RAG system management with FAISS")
    
    # Main commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command: status
    status_parser = subparsers.add_parser('status', help='View RAG system status')
    
    # Command: index
    index_parser = subparsers.add_parser('index', help='Index documents')
    index_parser.add_argument('--force', '-f', action='store_true', 
                            help='Force re-indexing')
    
    # Command: search
    search_parser = subparsers.add_parser('search', help='Search in knowledge base')
    search_parser.add_argument('query', type=str, help='Search query')
    search_parser.add_argument('--category', '-c', type=str, default='General',
                             help='Mental health category')
    search_parser.add_argument('--k', type=int, default=3,
                             help='Number of results')
    
    # Command: add
    add_parser = subparsers.add_parser('add', help='Add document from text')
    add_parser.add_argument('text', type=str, help='Document text')
    add_parser.add_argument('--title', '-t', type=str, help='Document title')
    add_parser.add_argument('--category', '-c', type=str, default='General',
                          help='Document category')
    
    # Command: create-examples
    examples_parser = subparsers.add_parser('create-examples', 
                                          help='Create example documents')
    examples_parser.add_argument('--overwrite', action='store_true',
                               help='Overwrite existing documents')
    
    # Command: list-docs
    list_parser = subparsers.add_parser('list-docs', help='List available documents')
    
    # Command: clean
    clean_parser = subparsers.add_parser('clean', help='Clean index and start over')
    
    return parser.parse_args()

def check_status():
    """View RAG system status"""
    print("📊 RAG system status (FAISS):")
    
    from src.config.settings import RAG_CONFIG
    docs_dir = Path(RAG_CONFIG["documents_dir"])
    index_dir = Path(RAG_CONFIG["index_dir"])
    
    print(f"  📁 Documents directory: {'✅ Exists' if docs_dir.exists() else '❌ Does not exist'}")
    print(f"  📁 FAISS index directory: {'✅ Exists' if index_dir.exists() else '❌ Does not exist'}")
    
    # Count documents
    if docs_dir.exists():
        files = list(docs_dir.glob("**/*.md")) + list(docs_dir.glob("**/*.txt"))
        print(f"  📄 Available documents: {len(files)}")
        
        if files:
            print("     Files found:")
            for f in files[:5]:  # Show only first 5
                print(f"     - {f.name}")
            if len(files) > 5:
                print(f"     ... and {len(files) - 5} more")
    else:
        print("  📄 Available documents: 0 (directory does not exist)")
    
    # Check FAISS index
    index_path = index_dir / "index.faiss"
    docs_path = index_dir / "documents.pkl"
    
    if index_path.exists() and docs_path.exists():
        try:
            import faiss
            import pickle
            
            # Load index
            index = faiss.read_index(str(index_path))
            
            # Load documents
            with open(docs_path, 'rb') as f:
                documents = pickle.load(f)
            
            print(f"  🗂️ FAISS Index: ✅ {index.ntotal} chunks indexed")
            print(f"  📐 Embedding dimension: {index.d}")
            print(f"  📚 Documents in memory: {len(documents)}")
            
        except Exception as e:
            print(f"  🗂️ FAISS Index: ❌ Error reading index: {e}")
    else:
        print("  🗂️ FAISS Index: ❌ Does not exist")
    
    # Check dependencies
    try:
        import faiss
        print(f"  📦 FAISS: ✅ Available")
    except ImportError:
        print("  📦 FAISS: ❌ Not installed")
    
    try:
        from sentence_transformers import SentenceTransformer
        print(f"  🧠 SentenceTransformers: ✅ Available")
    except ImportError:
        print("  🧠 SentenceTransformers: ❌ Not installed")
    
    # Check API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(f"  🔑 GROQ_API_KEY: ✅ Configured (...{groq_key[-4:]})")
    else:
        print("  🔑 GROQ_API_KEY: ❌ Not configured")

def create_example_documents(overwrite: bool = False):
    """Creates example documents for RAG system"""
    
    documents_dir = Path("src/data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    
    # Example documents optimized for FAISS (English content)
    examples = {
        "breathing_techniques.md": """# Breathing Techniques for Anxiety

## 4-7-8 Breathing (Dr. Weil's Technique)

### Steps:
1. **Inhale** through your nose counting to 4
2. **Hold** your breath counting to 7
3. **Exhale** through your mouth counting to 8
4. **Repeat** the cycle 3-4 times

### Benefits:
- Activates the parasympathetic nervous system
- Reduces anxiety immediately
- Helps with falling asleep

## Diaphragmatic Breathing

### Technique:
1. Sit comfortably or lie down
2. Place one hand on your chest, another on your abdomen
3. Breathe slowly through your nose (abdomen should rise)
4. Exhale through your mouth (abdomen lowers)
5. Practice 5-10 minutes daily

### What it's for:
- Reduces chronic stress
- Improves concentration
- Strengthens the diaphragm
""",

        "stress_management_techniques.md": """# Stress Management Techniques

## STOP Technique

### The 4 steps:
- **S**top: Stop what you're doing
- **T**ake a breath: Breathe deeply
- **O**bserve: Notice what's happening in your mind and body
- **P**roceed: Continue with intention and awareness

### When to use it:
- Moments of acute stress
- Before reacting impulsively
- When you feel accumulated tension

## 5-4-3-2-1 Grounding Technique

### For immediate anxiety:
- **5** things you can see
- **4** things you can touch
- **3** things you can hear
- **2** things you can smell
- **1** thing you can taste

### Purpose:
Reconnect with the present and exit anxious thoughts.

## Express Mindfulness (3 minutes)

### Quick steps:
1. **Minute 1**: Focus on your breathing
2. **Minute 2**: Notice body sensations
3. **Minute 3**: Expand awareness to surroundings

Perfect for work breaks or moments of tension.
""",

        "self_esteem_exercises.md": """# Self-Esteem Strengthening Exercises

## Gratitude Journal

### Daily practice:
- Write **3 things** you're grateful for
- Include **1 personal achievement** from the day (however small)
- Note **1 quality** of yours that you appreciate

### Benefits:
- Shifts focus to the positive
- Increases awareness of strengths
- Improves mood

## Best Friend Technique

### When you have self-criticism:
1. **Ask yourself**: "What would I tell my best friend in this situation?"
2. **Respond** with the same compassion
3. **Apply** that advice to yourself

### What it's for:
- Reduces destructive self-criticism
- Develops self-compassion
- Changes internal dialogue

## Realistic Affirmations

### Effective examples:
- "I am learning and growing every day"
- "I deserve respect and love"
- "My mistakes are learning opportunities"
- "I have unique strengths that I bring to the world"

### How to use them:
- Repeat every morning
- Personalize according to your needs
- Keep them realistic and believable

## Strengths Exercise

### Steps:
1. **List** 10 personal strengths
2. **Identify** how you use them in daily life
3. **Plan** how to develop each one further
4. **Celebrate** when you use them consciously

This builds a solid foundation of positive self-knowledge.
""",
    }
    
    created_count = 0
    
    for filename, content in examples.items():
        file_path = documents_dir / filename
        
        if file_path.exists() and not overwrite:
            print(f"⚠️  {filename} already exists. Use --overwrite to overwrite.")
            continue
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {filename}")
            created_count += 1
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")
    
    print(f"\n📝 Documents created: {created_count}")
    return created_count > 0

def main():
    """Main function"""
    args = parse_args()
    
    if not args.command:
        print("❌ You must specify a command. Use --help to see options.")
        return 1
    
    try:
        if args.command == 'status':
            check_status()
            return 0
        
        elif args.command == 'create-examples':
            print("📚 Creating example documents...")
            success = create_example_documents(args.overwrite)
            if success:
                print("\n💡 Now you can index with: python manage_rag.py index")
            return 0 if success else 1
        
        elif args.command == 'list-docs':
            print("📋 Available documents:")
            docs_dir = Path("src/data/documents")
            if not docs_dir.exists():
                print("❌ Documents directory does not exist")
                return 1
            
            files = list(docs_dir.rglob("*"))
            files = [f for f in files if f.is_file() and f.suffix in ['.md', '.txt']]
            
            if not files:
                print("📂 No documents available")
                print("💡 Create some with: python manage_rag.py create-examples")
                return 0
            
            for file in files:
                size = file.stat().st_size
                print(f"  - {file.name} ({size} bytes)")
            
            print(f"\nTotal: {len(files)} files")
            return 0
        
        elif args.command == 'clean':
            print("🧹 Cleaning FAISS index...")
            index_dir = Path("src/data/faiss_index")
            if index_dir.exists():
                import shutil
                shutil.rmtree(index_dir)
                print("✅ FAISS index deleted")
            else:
                print("⚠️ No index to clean")
            return 0
        
        # For other commands that require RAG
        elif args.command in ['index', 'search', 'add']:
            print("🔄 Initializing RAG system with FAISS...")
            
            from src.utils.rag_manager import initialize_rag_manager
            
            rag_manager = initialize_rag_manager(
                embeddings_model='all-MiniLM-L6-v2'
            )
            
            if not rag_manager:
                print("❌ Could not initialize RAG Manager")
                print("💡 Check that you have FAISS installed: pip install faiss-cpu")
                return 1
            
            # Execute specific command
            if args.command == 'index':
                print("📚 Indexing documents...")
                success = rag_manager.index_documents()
                if success:
                    print("✅ Documents indexed correctly")
                    stats = rag_manager.get_stats()
                    print(f"📊 Documents in index: {stats.get('documents_indexed', 'Unknown')}")
                else:
                    print("❌ Error indexing documents")
                    return 1
            
            elif args.command == 'search':
                print(f"🔍 Searching: '{args.query}' (Category: {args.category})")
                results = rag_manager.search_relevant_content(
                    args.query, 
                    k=args.k,
                    category=args.category
                )
                
                if not results:
                    print("📭 No relevant results found")
                    return 0
                
                print(f"\n📋 Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(f"Source: {result['source']}")
                    print(f"Score: {result['relevance_score']:.3f}")
                    print(f"Content: {result['content'][:200]}...")
                    if len(result['content']) > 200:
                        print("  [...]")
            
            elif args.command == 'add':
                print(f"📝 Adding document: '{args.text[:50]}...'")
                metadata = {
                    'title': args.title or 'Manually added document',
                    'category': args.category,
                    'source': 'manual_input'
                }
                
                success = rag_manager.add_document_from_text(args.text, metadata)
                if success:
                    print("✅ Document added correctly")
                else:
                    print("❌ Error adding document")
                    return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Process cancelled by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())