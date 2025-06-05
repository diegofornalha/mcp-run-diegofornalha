Execute claude com --mcp-debug para ver os logs de erro embutidos ou verificar nessa pasta

# Regras do Projeto

Responda sempre em pt br portugues do brasil

comando usado: 
# IMPORTANTE: Verificar o caminho correto antes de executar!
# O caminho pode variar dependendo de onde o projeto está localizado
# Para verificar o caminho atual, use: pwd

# Se estiver em /root/.cache/claude-cli-nodejs/-root--claude/:
claude mcp remove mcp-run-diegofornalha && claude mcp add mcp-run-diegofornalha -- python3 /root/.cache/claude-cli-nodejs/-root--claude/mcp-run-diegofornalha/mcp-bridge.py

# Se estiver em /root/:
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

## Ferramentas MCP Disponíveis
Sempre que possível, use essas ferramentas para melhorar a qualidade das respostas:

### 1. mcp_status
- **Uso**: `mcp__mcp-run-diegofornalha__mcp_status`
- **Função**: Verifica se a conexão com o MCP.run está ativa
- **Quando usar**: Para verificar status da conexão, diagnosticar problemas ou confirmar que o bridge está funcionando

### 2. sequential_thinking
- **Uso**: `mcp__mcp-run-diegofornalha__sequential_thinking`
- **Função**: Ferramenta de pensamento sequencial estruturado
- **Parâmetros**:
  - `thought`: O pensamento atual
  - `thoughtNumber`: Número do pensamento atual
  - `totalThoughts`: Total de pensamentos planejados
  - `nextThoughtNeeded`: Se precisa continuar (true/false)
- **Quando usar**: Para resolver problemas complexos, organizar tarefas em etapas ou quando precisar de raciocínio estruturado


esse projeto 

é uma bridge que conecte o SSE do MCP.run
  com o Claude Code:

  1. Conectar ao SSE
  2. Responder ao protocolo MCP que o Claude espera
  3. Traduzir eventos SSE para comandos MCP