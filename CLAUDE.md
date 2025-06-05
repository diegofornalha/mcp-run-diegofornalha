# Regras do Projeto

Responda sempre em pt br portugues do brasil

comando usado: 
claude mcp remove mcp-run-diegofornalha && claude mcp add mcp-run-diegofornalha -- python3 /root/mcp-run-diegofornalha/mcp-bridge.py

## Comportamento
- Sempre conversar antes de criar ou fazer qualquer coisa
- Evitar proatividade excessiva - ela torna as coisas difíceis
- Focar apenas no que foi pedido, quando foi pedido
- Não assumir o que o usuário quer
- Não assumir que informações em documentos são verdadeiras - sempre verificar

## SSE (Server-Sent Events) no Claude Code

Para que SSE funcione no Claude Code com MCP:

1. O servidor MCP deve implementar o endpoint SSE corretamente
2. Use ferramentas como `curl` com flags `-N` (no buffer) e `--http2` para testar
3. O Claude Code não suporta SSE diretamente - use ferramentas externas para consumir streams SSE
4. Para integração, crie um script que capture eventos SSE e processe conforme necessário

## Script de teste SSE
- `diegofornalha-sse.sh`: Script bash para testar conexão SSE com servidor MCP
- `mcp-sse-client.py`: Cliente Python robusto para SSE

## Ciclo de Atualização do MCP
Sempre que modificar o bridge MCP, siga este ciclo:
1. Fazer mudanças no código do bridge
2. Remover: `claude mcp remove mcp-run-diegofornalha`
3. Adicionar: `claude mcp add mcp-run-diegofornalha -- python3 /root/mcp-run-diegofornalha/mcp-bridge.py`
4. Reiniciar o Claude Code para carregar as mudanças

## Bridge MCP Atual
- `mcp-bridge.py`: Bridge que conecta SSE do MCP.run ao Claude Code
- URL SSE está hardcoded no arquivo
- Capabilities devem ser objetos vazios `{}`, não booleanos


esse projeto 

é uma bridge que conecte o SSE do MCP.run
  com o Claude Code:

  1. Conectar ao SSE
  2. Responder ao protocolo MCP que o Claude espera
  3. Traduzir eventos SSE para comandos MCP