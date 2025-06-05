# Regras do Projeto

## Comportamento
- Sempre conversar antes de criar ou fazer qualquer coisa
- Evitar proatividade excessiva - ela torna as coisas difíceis
- Focar apenas no que foi pedido, quando foi pedido
- Não assumir o que o usuário quer

## SSE (Server-Sent Events) no Claude Code

Para que SSE funcione no Claude Code com MCP:

1. O servidor MCP deve implementar o endpoint SSE corretamente
2. Use ferramentas como `curl` com flags `-N` (no buffer) e `--http2` para testar
3. O Claude Code não suporta SSE diretamente - use ferramentas externas para consumir streams SSE
4. Para integração, crie um script que capture eventos SSE e processe conforme necessário

## Script de teste SSE
- `test-sse.sh`: Script para testar conexão SSE com servidor MCP