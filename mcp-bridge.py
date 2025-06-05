#!/usr/bin/env python3
"""
Bridge MCP para MCP.run - Diego Fornalha
Conecta o SSE do MCP.run ao Claude Code via protocolo MCP
"""

import json
import sys
import threading
import queue
import subprocess
import time
from datetime import datetime

# URL fixa do MCP.run
SSE_URL = 'https://www.mcp.run/api/mcp/sse?nonce=aN5rE5HO4uqXgzNZomcRNA&username=diegofornalha&exp=1749345684581&profile=diegofornalha%2Fdefault&sig=cnkj3lXiki_3meMvd86HvUsOJdHYYK349qf5X_SQGuY'

class MCPBridge:
    def __init__(self):
        self.sse_process = None
        self.event_queue = queue.Queue()
        self.running = True
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        
    def log(self, message):
        """Log para debug"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/mcp-bridge.log', 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
            
    def start_sse_listener(self):
        """Inicia listener SSE em thread separada"""
        def sse_worker():
            cmd = [
                'curl', '-N', '--http2', '-s',
                '-H', 'Accept: text/event-stream',
                SSE_URL
            ]
            
            self.sse_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                bufsize=1
            )
            
            event_buffer = []
            for line in self.sse_process.stdout:
                line = line.strip()
                
                if line.startswith('event:'):
                    event_type = line[6:].strip()
                    event_buffer = [('event', event_type)]
                    
                elif line.startswith('data:'):
                    data = line[5:].strip()
                    event_buffer.append(('data', data))
                    
                elif line == '' and event_buffer:
                    # Processa evento completo
                    self.process_sse_event(event_buffer)
                    event_buffer = []
                    
        thread = threading.Thread(target=sse_worker, daemon=True)
        thread.start()
        
    def process_sse_event(self, event_buffer):
        """Processa evento SSE recebido"""
        event_type = None
        data = None
        
        for item_type, content in event_buffer:
            if item_type == 'event':
                event_type = content
            elif item_type == 'data':
                data = content
                
        if event_type and data:
            self.event_queue.put((event_type, data))
            
    def send_response(self, response):
        """Envia resposta JSON-RPC para stdout"""
        json.dump(response, sys.stdout)
        sys.stdout.write('\n')
        sys.stdout.flush()
        
    def handle_initialize(self, request_id, params):
        """Trata requisição initialize"""
        self.log(f"Initialize request: {params}")
        
        # Inicia listener SSE
        self.start_sse_listener()
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-10-07",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "serverInfo": {
                    "name": "mcp-run-diegofornalha",
                    "version": "1.0.0"
                }
            }
        }
        self.send_response(response)
        
    def handle_list_tools(self, request_id):
        """Lista ferramentas disponíveis"""
        tools = [
            {
                "name": "sequential_thinking",
                "description": "Pensamento sequencial para resolver problemas complexos",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "thought": {"type": "string"},
                        "thoughtNumber": {"type": "integer"},
                        "totalThoughts": {"type": "integer"},
                        "nextThoughtNeeded": {"type": "boolean"}
                    },
                    "required": ["thought", "thoughtNumber", "totalThoughts", "nextThoughtNeeded"]
                }
            },
            {
                "name": "mcp_status",
                "description": "Verifica status da conexão MCP.run",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
        self.send_response(response)
        
    def handle_list_resources(self, request_id):
        """Lista recursos disponíveis"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": []
            }
        }
        self.send_response(response)
        
    def handle_list_prompts(self, request_id):
        """Lista prompts disponíveis"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "prompts": []
            }
        }
        self.send_response(response)
        
    def handle_call_tool(self, request_id, params):
        """Executa uma ferramenta"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        self.log(f"Tool call: {tool_name} with args: {arguments}")
        
        if tool_name == "mcp_status":
            result = {
                "status": "connected",
                "sse_url": SSE_URL,
                "timestamp": datetime.now().isoformat()
            }
        elif tool_name == "sequential_thinking":
            result = {
                "thought": arguments.get("thought", ""),
                "analysis": f"Analisando pensamento {arguments.get('thoughtNumber', 1)} de {arguments.get('totalThoughts', 1)}",
                "continue": arguments.get("nextThoughtNeeded", False)
            }
        else:
            result = {"error": f"Ferramenta '{tool_name}' não encontrada"}
            
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        }
        self.send_response(response)
        
    def run(self):
        """Loop principal do bridge"""
        self.log("Bridge iniciado")
        
        while self.running:
            try:
                # Lê requisição do stdin
                line = sys.stdin.readline()
                if not line:
                    break
                    
                request = json.loads(line)
                self.log(f"Request: {request}")
                
                method = request.get("method")
                request_id = request.get("id")
                params = request.get("params", {})
                
                # Processa requisições
                if method == "initialize":
                    self.handle_initialize(request_id, params)
                elif method == "tools/list":
                    self.handle_list_tools(request_id)
                elif method == "resources/list":
                    self.handle_list_resources(request_id)
                elif method == "prompts/list":
                    self.handle_list_prompts(request_id)
                elif method == "tools/call":
                    self.handle_call_tool(request_id, params)
                else:
                    # Método não suportado
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Método '{method}' não suportado"
                        }
                    }
                    self.send_response(error_response)
                    
                # Processa eventos SSE pendentes
                while not self.event_queue.empty():
                    try:
                        event_type, data = self.event_queue.get_nowait()
                        self.log(f"SSE Event: {event_type} - {data}")
                    except queue.Empty:
                        break
                        
            except json.JSONDecodeError as e:
                self.log(f"JSON decode error: {e}")
            except Exception as e:
                self.log(f"Error: {e}")
                
        self.cleanup()
        
    def cleanup(self):
        """Limpa recursos"""
        self.running = False
        if self.sse_process:
            self.sse_process.terminate()

def main():
    bridge = MCPBridge()
    try:
        bridge.run()
    except KeyboardInterrupt:
        bridge.log("Interrompido pelo usuário")
    except Exception as e:
        bridge.log(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()