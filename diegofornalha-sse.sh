#!/bin/bash

# Conexão SSE com MCP.run - Diego Fornalha
echo "=== MCP.run SSE - Diego Fornalha ==="
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando conexão"
echo ""

# URL fixa de conexão
URL='https://www.mcp.run/api/mcp/sse?nonce=aN5rE5HO4uqXgzNZomcRNA&username=diegofornalha&exp=1749345684581&profile=diegofornalha%2Fdefault&sig=cnkj3lXiki_3meMvd86HvUsOJdHYYK349qf5X_SQGuY'

# Arquivo de log (opcional)
LOG_FILE="sse-events-$(date '+%Y%m%d-%H%M%S').log"

echo "Conectando ao MCP.run..."
echo "Eventos serão salvos em: $LOG_FILE"
echo "Pressione Ctrl+C para parar"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Função para processar eventos
process_sse() {
    while IFS= read -r line; do
        # Adiciona timestamp e mostra na tela
        echo "[$(date '+%H:%M:%S')] $line"
        # Salva no arquivo de log
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line" >> "$LOG_FILE"
    done
}

# Executa curl e processa a saída
curl -s -N --http2 "$URL" | process_sse