#!/bin/bash

# Script para testar conexão SSE com MCP
echo "=== Testando conexão SSE com MCP ==="
echo ""

# URL com parâmetros de autenticação
URL='https://www.mcp.run/api/mcp/sse?nonce=aN5rE5HO4uqXgzNZomcRNA&username=diegofornalha&exp=1749345684581&profile=diegofornalha%2Fdefault&sig=cnkj3lXiki_3meMvd86HvUsOJdHYYK349qf5X_SQGuY'

echo "Iniciando conexão SSE..."
echo "Pressione Ctrl+C para parar"
echo ""
echo "Headers e eventos SSE:"
echo "======================"

# Executa curl com:
# -i: mostra headers HTTP
# -N: desabilita buffer (essencial para SSE)
# --http2: força HTTP/2 se disponível
curl -i -N --http2 "$URL"