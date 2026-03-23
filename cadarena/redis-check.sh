#!/bin/bash
# Quick Upstash check — run from cadarena/ directory
source site/.env.local

echo "=== PROMPTS (${UPSTASH_REDIS_REST_URL}) ==="
curl -s "${UPSTASH_REDIS_REST_URL}/llen/cad-arena:prompts" \
  -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  Total prompts logged: {d[\"result\"]}')"

echo ""
echo "=== RECENT PROMPTS (last 5) ==="
curl -s "${UPSTASH_REDIS_REST_URL}/lrange/cad-arena:prompts/-5/-1" \
  -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for i,entry in enumerate(d.get('result',[])):
  p=json.loads(entry)
  print(f'  [{p[\"ts\"][:16]}] {p[\"prompt\"][:80]}')
"

echo ""
echo "=== EMAILS ==="
curl -s "${UPSTASH_REDIS_REST_URL}/scard/cad-arena:emails" \
  -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  Total emails collected: {d[\"result\"]}')"

curl -s "${UPSTASH_REDIS_REST_URL}/smembers/cad-arena:emails" \
  -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for e in d.get('result',[]):
  print(f'  {e}')
"
