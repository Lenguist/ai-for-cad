#!/bin/bash
# Download arxiv papers as PDFs from papers-database.md
# Extracts arxiv IDs from abs/, html/, and pdf/ URLs, deduplicates, and downloads

PAPERS_DIR="/Users/mbondarenko/Desktop/ai-for-cad/feb8/papers"
DB_FILE="/Users/mbondarenko/Desktop/ai-for-cad/feb8/papers-database.md"

mkdir -p "$PAPERS_DIR"

# Extract all arxiv URLs, normalize to arxiv IDs
# Handles: arxiv.org/abs/XXXX.XXXXX, arxiv.org/html/XXXX.XXXXXvN, arxiv.org/pdf/XXXX.XXXXX
grep -oE 'https://arxiv\.org/(abs|html|pdf)/[0-9]+\.[0-9]+(v[0-9]+)?' "$DB_FILE" | \
    sed -E 's|https://arxiv.org/abs/||; s|https://arxiv.org/html/||; s|https://arxiv.org/pdf/||' | \
    sed -E 's/v[0-9]+$//' | \
    sort -u > /tmp/arxiv_ids.txt

TOTAL=$(wc -l < /tmp/arxiv_ids.txt)
echo "Found $TOTAL unique arxiv paper IDs to download"
echo ""

COUNT=0
SKIP=0
FAIL=0

while IFS= read -r arxiv_id; do
    COUNT=$((COUNT + 1))
    FILENAME="${arxiv_id}.pdf"
    FILEPATH="$PAPERS_DIR/$FILENAME"

    if [ -f "$FILEPATH" ] && [ -s "$FILEPATH" ]; then
        echo "[$COUNT/$TOTAL] SKIP (exists): $FILENAME"
        SKIP=$((SKIP + 1))
        continue
    fi

    PDF_URL="https://arxiv.org/pdf/${arxiv_id}.pdf"
    echo "[$COUNT/$TOTAL] Downloading: $PDF_URL"

    curl -sL -o "$FILEPATH" \
        -H "User-Agent: Mozilla/5.0 (academic research)" \
        --connect-timeout 15 \
        --max-time 60 \
        "$PDF_URL"

    # Check if download succeeded (PDF files start with %PDF)
    if [ -f "$FILEPATH" ] && [ -s "$FILEPATH" ] && head -c 4 "$FILEPATH" | grep -q '%PDF'; then
        echo "  -> OK ($(du -h "$FILEPATH" | cut -f1))"
    else
        echo "  -> FAILED"
        rm -f "$FILEPATH"
        FAIL=$((FAIL + 1))
    fi

    # Rate limit: 1 second between requests to be polite to arxiv
    sleep 1
done < /tmp/arxiv_ids.txt

echo ""
echo "=== Download Complete ==="
echo "Total IDs: $TOTAL"
echo "Downloaded: $((TOTAL - SKIP - FAIL))"
echo "Skipped (existing): $SKIP"
echo "Failed: $FAIL"
echo "Files in papers/: $(ls -1 "$PAPERS_DIR"/*.pdf 2>/dev/null | wc -l)"
