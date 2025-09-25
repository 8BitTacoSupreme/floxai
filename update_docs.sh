#!/bin/bash
# FloxAI Documentation Auto-Update Script
# Can be run via cron or manually to keep docs current

set -e

PROJECT_DIR="${FLOX_ENV_PROJECT:-/Users/jhogan/floxai}"
DATA_DIR="$PROJECT_DIR/data"
LOG_FILE="$DATA_DIR/doc_update.log"
LOCK_FILE="/tmp/floxai_doc_update.lock"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check lock file to prevent multiple instances
if [ -f "$LOCK_FILE" ]; then
    log "Update already in progress (lock file exists)"
    exit 1
fi

# Create lock file
touch "$LOCK_FILE"

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

log "Starting FloxAI documentation update"

# Activate virtual environment if needed
if [ -d "$PROJECT_DIR/venv" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
fi

# Update Flox documentation sources
update_flox_docs() {
    log "Updating Flox documentation sources..."
    
    REPOS=(
        "https://github.com/flox/flox|main"
    )
    
    for repo_info in "${REPOS[@]}"; do
        IFS='|' read -r repo_url branch <<< "$repo_info"
        repo_name=$(basename "$repo_url" .git)
        repo_path="$DATA_DIR/flox_docs/$repo_name"
        
        if [ -d "$repo_path/.git" ]; then
            log "  Updating $repo_name..."
            cd "$repo_path"
            git fetch origin
            git reset --hard "origin/$branch"
            cd - > /dev/null
        else
            log "  Cloning $repo_name..."
            git clone --branch "$branch" "$repo_url" "$repo_path" || {
                log "  WARNING: Failed to clone $repo_name"
                continue
            }
        fi
    done
    
    # Also fetch documentation from the Flox website if available
    log "  Fetching Flox web documentation..."
    FLOX_WEB_DIR="$DATA_DIR/flox_docs/web"
    mkdir -p "$FLOX_WEB_DIR"
    
    # Key documentation pages from flox.dev
    FLOX_URLS=(
        "https://flox.dev/docs"
        "https://flox.dev/docs/install"
        "https://flox.dev/docs/tutorials/quickstart"
    )
    
    for url in "${FLOX_URLS[@]}"; do
        filename=$(echo "$url" | sed 's|https://||; s|/|_|g').txt
        log "    Fetching $(basename "$filename")..."
        
        curl -sL "$url" -o "$FLOX_WEB_DIR/$filename.html" 2>/dev/null || {
            log "    WARNING: Could not fetch $url"
        }
    done
}

# Fetch latest Nix documentation
update_nix_docs() {
    log "Updating Nix documentation..."
    
    NIX_DIR="$DATA_DIR/flox_docs/nix"
    mkdir -p "$NIX_DIR"
    
    # Download key Nix documentation pages
    URLS=(
        "https://nixos.org/manual/nix/stable/introduction.html"
        "https://nixos.org/manual/nix/stable/package-management/basic-package-mgmt.html"
    )
    
    for url in "${URLS[@]}"; do
        filename=$(echo "$url" | sed 's|https://||; s|/|_|g; s|\.html$||').txt
        log "  Fetching $(basename "$filename")..."
        
        curl -sL "$url" 2>/dev/null | \
            sed -n '/<body>/,/<\/body>/p' | \
            sed 's/<[^>]*>//g' | \
            sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g' | \
            sed '/^[[:space:]]*$/d' > "$NIX_DIR/$filename" || {
                log "  WARNING: Could not fetch $url"
            }
    done
}

# Process the Flox repository documentation
process_flox_repo_docs() {
    log "Processing Flox repository documentation..."
    
    FLOX_REPO="$DATA_DIR/flox_docs/flox"
    PROCESSED_DIR="$DATA_DIR/flox_docs/processed"
    mkdir -p "$PROCESSED_DIR"
    
    if [ -d "$FLOX_REPO" ]; then
        # Extract markdown files from docs directory
        if [ -d "$FLOX_REPO/docs" ]; then
            log "  Processing docs directory..."
            find "$FLOX_REPO/docs" -name "*.md" -type f | while read -r doc; do
                basename_doc=$(basename "$doc")
                cp "$doc" "$PROCESSED_DIR/docs_$basename_doc" 2>/dev/null || true
            done
        fi
        
        # Extract README files
        log "  Processing README files..."
        find "$FLOX_REPO" -name "README.md" -type f | while read -r readme; do
            # Get relative path without using realpath --relative-to
            rel_path=${readme#$FLOX_REPO/}
            dest_name=$(echo "$rel_path" | sed 's|/|_|g')
            cp "$readme" "$PROCESSED_DIR/$dest_name" 2>/dev/null || true
        done
        
        # Extract example manifests
        log "  Processing example manifests..."
        find "$FLOX_REPO" -name "manifest.toml" -type f | head -20 | while read -r manifest; do
            # Get relative path without using realpath --relative-to
            rel_path=${manifest#$FLOX_REPO/}
            dest_name="example_$(echo "$rel_path" | sed 's|/|_|g')"
            cp "$manifest" "$PROCESSED_DIR/$dest_name" 2>/dev/null || true
        done
        
        # Count what we extracted
        md_count=$(find "$PROCESSED_DIR" -name "*.md" -type f | wc -l | tr -d ' ')
        toml_count=$(find "$PROCESSED_DIR" -name "*.toml" -type f | wc -l | tr -d ' ')
        log "  Extracted $md_count markdown files and $toml_count manifest examples"
    fi
}

# Ingest Flox blog posts
ingest_blogs() {
    log "Ingesting Flox blog posts..."
    
    cd "$PROJECT_DIR"
    if [ -f "ingest_flox_blogs.py" ]; then
        python3 ingest_flox_blogs.py 2>&1 | while read line; do log "  $line"; done
        if [ $? -eq 0 ]; then
            log "Blog ingestion completed successfully"
        else
            log "WARNING: Blog ingestion encountered issues"
        fi
    else
        log "WARNING: ingest_flox_blogs.py not found, skipping blog ingestion"
    fi
}

# Run the document ingestion pipeline
run_ingestion() {
    log "Running document ingestion pipeline..."
    
    cd "$PROJECT_DIR"
    python3 << 'PYTHON_EOF' 2>&1 | while read line; do log "  $line"; done
import sys
import os
import glob

docs_dir = './data/flox_docs'
file_counts = {}

# Count files by type
for ext in ['*.md', '*.txt', '*.toml', '*.html']:
    files = []
    for root, dirs, filenames in os.walk(docs_dir):
        for filename in filenames:
            if filename.endswith(ext.replace('*', '')):
                files.append(os.path.join(root, filename))
    file_counts[ext] = len(files)

total = sum(file_counts.values())
print(f"Found {total} documentation files:")
for ext, count in file_counts.items():
    print(f"  {ext}: {count} files")

# List some example files
print("\nSample files found:")
for root, dirs, filenames in os.walk(docs_dir):
    for filename in filenames[:5]:  # Just show first 5
        print(f"  - {os.path.relpath(os.path.join(root, filename), docs_dir)}")
    break

# Check if vector database exists
vector_db_dir = './data/vector_db'
if os.path.exists(vector_db_dir):
    print(f"\nVector database found at: {vector_db_dir}")
    print("Run 'python3 migrate_to_vector_rag.py' to update vector embeddings")
else:
    print(f"\nVector database not found at: {vector_db_dir}")
    print("Run 'python3 migrate_to_vector_rag.py' to create vector embeddings")
PYTHON_EOF
    
    if [ $? -eq 0 ]; then
        log "Document analysis completed successfully"
    else
        log "WARNING: Document processing encountered issues"
    fi
}

# Update vector database
update_vector_db() {
    log "Updating vector database..."
    
    cd "$PROJECT_DIR"
    if [ -f "migrate_to_vector_rag.py" ]; then
        python3 migrate_to_vector_rag.py 2>&1 | while read line; do log "  $line"; done
        if [ $? -eq 0 ]; then
            log "Vector database update completed successfully"
        else
            log "WARNING: Vector database update encountered issues"
        fi
    else
        log "WARNING: migrate_to_vector_rag.py not found, skipping vector update"
    fi
}

# Main execution flow
main() {
    log "=== Starting documentation update ==="
    
    # Create necessary directories
    mkdir -p "$DATA_DIR/flox_docs"
    mkdir -p "$DATA_DIR/vector_db"
    
    # Run updates
    update_flox_docs
    process_flox_repo_docs
    update_nix_docs
    ingest_blogs
    run_ingestion
    update_vector_db
    
    # Show summary
    log "=== Update Summary ==="
    log "Documentation stored in: $DATA_DIR/flox_docs"
    log "Vector database stored in: $DATA_DIR/vector_db"
    
    log "=== Documentation update completed ==="
}

# Parse command line arguments
case "${1:-}" in
    --flox-only)
        log "Updating only Flox documentation"
        update_flox_docs
        process_flox_repo_docs
        run_ingestion
        ;;
    --nix-only)
        log "Updating only Nix documentation"
        update_nix_docs
        run_ingestion
        ;;
    --blogs-only)
        log "Updating only Flox blog posts"
        ingest_blogs
        update_vector_db
        ;;
    --vector-only)
        log "Updating only vector database"
        update_vector_db
        ;;
    --help)
        echo "Usage: $0 [--flox-only|--nix-only|--blogs-only|--vector-only|--help]"
        echo "  --flox-only    Update only Flox documentation"
        echo "  --nix-only     Update only Nix documentation"
        echo "  --blogs-only   Update only Flox blog posts"
        echo "  --vector-only  Update only vector database"
        echo "  --help         Show this help message"
        echo ""
        echo "Run without arguments to perform full update"
        ;;
    *)
        main
        ;;
esac
