#!/usr/bin/env python
"""
Script para gestionar el sistema RAG con FAISS (versión simplificada y confiable)
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Gestión del sistema RAG con FAISS")
    
    # Comandos principales
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando: status
    status_parser = subparsers.add_parser('status', help='Ver estado del sistema RAG')
    
    # Comando: index
    index_parser = subparsers.add_parser('index', help='Indexar documentos')
    index_parser.add_argument('--force', '-f', action='store_true', 
                            help='Forzar re-indexación')
    
    # Comando: search
    search_parser = subparsers.add_parser('search', help='Buscar en la base de conocimiento')
    search_parser.add_argument('query', type=str, help='Consulta de búsqueda')
    search_parser.add_argument('--category', '-c', type=str, default='General',
                             help='Categoría de salud mental')
    search_parser.add_argument('--k', type=int, default=3,
                             help='Número de resultados')
    
    # Comando: add
    add_parser = subparsers.add_parser('add', help='Añadir documento desde texto')
    add_parser.add_argument('text', type=str, help='Texto del documento')
    add_parser.add_argument('--title', '-t', type=str, help='Título del documento')
    add_parser.add_argument('--category', '-c', type=str, default='General',
                          help='Categoría del documento')
    
    # Comando: create-examples
    examples_parser = subparsers.add_parser('create-examples', 
                                          help='Crear documentos de ejemplo')
    examples_parser.add_argument('--overwrite', action='store_true',
                               help='Sobrescribir documentos existentes')
    
    # Comando: list-docs
    list_parser = subparsers.add_parser('list-docs', help='Listar documentos disponibles')
    
    # Comando: clean
    clean_parser = subparsers.add_parser('clean', help='Limpiar índice y empezar de nuevo')
    
    return parser.parse_args()

def check_status():
    """Ver estado del sistema RAG"""
    print("📊 Estado del sistema RAG (FAISS):")
    
    # Verificar directorios
    docs_dir = Path("src/data/documents")
    index_dir = Path("src/data/faiss_index")
    
    print(f"  📁 Directorio documentos: {'✅ Existe' if docs_dir.exists() else '❌ No existe'}")
    print(f"  📁 Directorio índice FAISS: {'✅ Existe' if index_dir.exists() else '❌ No existe'}")
    
    # Contar documentos
    if docs_dir.exists():
        files = list(docs_dir.glob("**/*.md")) + list(docs_dir.glob("**/*.txt"))
        print(f"  📄 Documentos disponibles: {len(files)}")
        
        if files:
            print("     Archivos encontrados:")
            for f in files[:5]:  # Mostrar solo los primeros 5
                print(f"     - {f.name}")
            if len(files) > 5:
                print(f"     ... y {len(files) - 5} más")
    else:
        print("  📄 Documentos disponibles: 0 (directorio no existe)")
    
    # Verificar índice FAISS
    index_path = index_dir / "index.faiss"
    docs_path = index_dir / "documents.pkl"
    
    if index_path.exists() and docs_path.exists():
        try:
            import faiss
            import pickle
            
            # Cargar índice
            index = faiss.read_index(str(index_path))
            
            # Cargar documentos
            with open(docs_path, 'rb') as f:
                documents = pickle.load(f)
            
            print(f"  🗂️ Índice FAISS: ✅ {index.ntotal} chunks indexados")
            print(f"  📐 Dimensión embeddings: {index.d}")
            print(f"  📚 Documentos en memoria: {len(documents)}")
            
        except Exception as e:
            print(f"  🗂️ Índice FAISS: ❌ Error leyendo índice: {e}")
    else:
        print("  🗂️ Índice FAISS: ❌ No existe")
    
    # Verificar dependencias
    try:
        import faiss
        print(f"  📦 FAISS: ✅ Disponible")
    except ImportError:
        print("  📦 FAISS: ❌ No instalado")
    
    try:
        from sentence_transformers import SentenceTransformer
        print(f"  🧠 SentenceTransformers: ✅ Disponible")
    except ImportError:
        print("  🧠 SentenceTransformers: ❌ No instalado")
    
    # Verificar API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(f"  🔑 GROQ_API_KEY: ✅ Configurada (...{groq_key[-4:]})")
    else:
        print("  🔑 GROQ_API_KEY: ❌ No configurada")

def create_example_documents(overwrite: bool = False):
    """Crea documentos de ejemplo para el sistema RAG"""
    
    documents_dir = Path("src/data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    
    # Documentos de ejemplo optimizados para FAISS
    examples = {
        "respiracion_tecnicas.md": """# Técnicas de Respiración para la Ansiedad

## Respiración 4-7-8 (Técnica del Dr. Weil)

### Pasos:
1. **Inhala** por la nariz contando hasta 4
2. **Mantén** la respiración contando hasta 7
3. **Exhala** por la boca contando hasta 8
4. **Repite** el ciclo 3-4 veces

### Beneficios:
- Activa el sistema nervioso parasimpático
- Reduce la ansiedad inmediatamente
- Ayuda a conciliar el sueño

## Respiración Diafragmática

### Técnica:
1. Siéntate cómodamente o acuéstate
2. Coloca una mano en el pecho, otra en el abdomen
3. Inhala lentamente por la nariz (el abdomen debe subir)
4. Exhala por la boca (el abdomen baja)
5. Practica 5-10 minutos diarios

### Para qué sirve:
- Reduce el estrés crónico
- Mejora la concentración
- Fortalece el diafragma
""",

        "manejo_estres_tecnicas.md": """# Técnicas para el Manejo del Estrés

## Técnica STOP

### Los 4 pasos:
- **S**top: Para lo que estás haciendo
- **T**ake a breath: Respira profundamente
- **O**bserve: Observa qué está pasando en tu mente y cuerpo
- **P**roceed: Continúa con intención y consciencia

### Cuándo usarla:
- Momentos de estrés agudo
- Antes de reaccionar impulsivamente
- Cuando sientes tensión acumulada

## Técnica de Grounding 5-4-3-2-1

### Para la ansiedad inmediata:
- **5** cosas que puedes ver
- **4** cosas que puedes tocar
- **3** cosas que puedes escuchar
- **2** cosas que puedes oler
- **1** cosa que puedes saborear

### Propósito:
Reconectar con el presente y salir de pensamientos ansiosos.

## Mindfulness Express (3 minutos)

### Pasos rápidos:
1. **Minuto 1**: Enfócate en tu respiración
2. **Minuto 2**: Observa las sensaciones corporales
3. **Minuto 3**: Amplía la conciencia al entorno

Ideal para descansos en el trabajo o momentos de tensión.
""",

        "autoestima_ejercicios.md": """# Ejercicios para Fortalecer la Autoestima

## Diario de Gratitud

### Práctica diaria:
- Escribe **3 cosas** por las que te sientes agradecido
- Incluye **1 logro** personal del día (por pequeño que sea)
- Anota **1 cualidad** tuya que aprecias

### Beneficios:
- Cambia el enfoque hacia lo positivo
- Incrementa la consciencia de fortalezas
- Mejora el estado de ánimo

## Técnica del Mejor Amigo

### Cuando tengas autocrítica:
1. **Pregúntate**: "¿Qué le diría a mi mejor amigo en esta situación?"
2. **Respóndete** con la misma compasión
3. **Aplica** ese consejo a ti mismo

### Para qué sirve:
- Reduce la autocrítica destructiva
- Desarrolla autocompasión
- Cambia el diálogo interno

## Afirmaciones Realistas

### Ejemplos efectivos:
- "Estoy aprendiendo y creciendo cada día"
- "Merezco respeto y amor"
- "Mis errores son oportunidades de aprendizaje"
- "Tengo fortalezas únicas que aporto al mundo"

### Cómo usarlas:
- Repite cada mañana
- Personaliza según tus necesidades
- Mantenlas realistas y creíbles

## Ejercicio de Fortalezas

### Pasos:
1. **Lista** 10 fortalezas personales
2. **Identifica** cómo las usas en tu vida diaria
3. **Planifica** cómo desarrollar más cada una
4. **Celebra** cuando las uses conscientemente

Esto construye una base sólida de autoconocimiento positivo.
""",
    }
    
    created_count = 0
    
    for filename, content in examples.items():
        file_path = documents_dir / filename
        
        if file_path.exists() and not overwrite:
            print(f"⚠️  {filename} ya existe. Usa --overwrite para sobrescribir.")
            continue
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Creado: {filename}")
            created_count += 1
        except Exception as e:
            print(f"❌ Error creando {filename}: {e}")
    
    print(f"\n📝 Documentos creados: {created_count}")
    return created_count > 0

def main():
    """Función principal"""
    args = parse_args()
    
    if not args.command:
        print("❌ Debes especificar un comando. Usa --help para ver las opciones.")
        return 1
    
    try:
        if args.command == 'status':
            check_status()
            return 0
        
        elif args.command == 'create-examples':
            print("📚 Creando documentos de ejemplo...")
            success = create_example_documents(args.overwrite)
            if success:
                print("\n💡 Ahora puedes indexar con: python manage_rag.py index")
            return 0 if success else 1
        
        elif args.command == 'list-docs':
            print("📋 Documentos disponibles:")
            docs_dir = Path("src/data/documents")
            if not docs_dir.exists():
                print("❌ Directorio de documentos no existe")
                return 1
            
            files = list(docs_dir.rglob("*"))
            files = [f for f in files if f.is_file() and f.suffix in ['.md', '.txt']]
            
            if not files:
                print("📂 No hay documentos disponibles")
                print("💡 Crea algunos con: python manage_rag.py create-examples")
                return 0
            
            for file in files:
                size = file.stat().st_size
                print(f"  - {file.name} ({size} bytes)")
            
            print(f"\nTotal: {len(files)} archivos")
            return 0
        
        elif args.command == 'clean':
            print("🧹 Limpiando índice FAISS...")
            index_dir = Path("src/data/faiss_index")
            if index_dir.exists():
                import shutil
                shutil.rmtree(index_dir)
                print("✅ Índice FAISS eliminado")
            else:
                print("⚠️ No había índice que limpiar")
            return 0
        
        # Para otros comandos que requieren RAG
        elif args.command in ['index', 'search', 'add']:
            print("🔄 Inicializando sistema RAG con FAISS...")
            
            from src.utils.rag_manager import initialize_rag_manager
            
            rag_manager = initialize_rag_manager(
                embeddings_model='all-MiniLM-L6-v2'
            )
            
            if not rag_manager:
                print("❌ No se pudo inicializar RAG Manager")
                print("💡 Verifica que tengas FAISS instalado: pip install faiss-cpu")
                return 1
            
            # Ejecutar comando específico
            if args.command == 'index':
                print("📚 Indexando documentos...")
                success = rag_manager.index_documents()
                if success:
                    print("✅ Documentos indexados correctamente")
                    stats = rag_manager.get_stats()
                    print(f"📊 Documentos en el índice: {stats.get('documents_indexed', 'Desconocido')}")
                else:
                    print("❌ Error al indexar documentos")
                    return 1
            
            elif args.command == 'search':
                print(f"🔍 Buscando: '{args.query}' (Categoría: {args.category})")
                results = rag_manager.search_relevant_content(
                    args.query, 
                    k=args.k,
                    category=args.category
                )
                
                if not results:
                    print("📭 No se encontraron resultados relevantes")
                    return 0
                
                print(f"\n📋 Encontrados {len(results)} resultados:")
                for i, result in enumerate(results, 1):
                    print(f"\n--- Resultado {i} ---")
                    print(f"Fuente: {result['source']}")
                    print(f"Puntuación: {result['relevance_score']:.3f}")
                    print(f"Contenido: {result['content'][:200]}...")
                    if len(result['content']) > 200:
                        print("  [...]")
            
            elif args.command == 'add':
                print(f"📝 Añadiendo documento: '{args.text[:50]}...'")
                metadata = {
                    'title': args.title or 'Documento añadido manualmente',
                    'category': args.category,
                    'source': 'manual_input'
                }
                
                success = rag_manager.add_document_from_text(args.text, metadata)
                if success:
                    print("✅ Documento añadido correctamente")
                else:
                    print("❌ Error al añadir documento")
                    return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Proceso cancelado por el usuario")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())