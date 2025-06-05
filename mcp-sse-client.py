#!/usr/bin/env python3
"""
Cliente SSE definitivo para MCP.run - Diego Fornalha
Implementação robusta com reconexão e tratamento de erros
"""

import json
import time
import signal
import sys
from datetime import datetime
import subprocess

# URL fixa de conexão
SSE_URL = 'https://www.mcp.run/api/mcp/sse?nonce=aN5rE5HO4uqXgzNZomcRNA&username=diegofornalha&exp=1749345684581&profile=diegofornalha%2Fdefault&sig=cnkj3lXiki_3meMvd86HvUsOJdHYYK349qf5X_SQGuY'

class MCPSSEClient:
    def __init__(self):
        self.running = True
        self.process = None
        
    def start(self):
        """Inicia o cliente SSE"""
        print("╔═══════════════════════════════════════════════════╗")
        print("║      MCP.run SSE Client - Diego Fornalha         ║")
        print("╚═══════════════════════════════════════════════════╝")
        print(f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔌 Conectando ao MCP.run...")
        print("⏸️  Pressione Ctrl+C para parar\n")
        
        # Comando curl otimizado para SSE
        cmd = [
            'curl',
            '-N',           # No buffer
            '--http2',      # HTTP/2
            '-s',           # Silent
            '-S',           # Show errors
            '-H', 'Accept: text/event-stream',
            '-H', 'Cache-Control: no-cache',
            '-H', 'Connection: keep-alive',
            SSE_URL
        ]
        
        try:
            # Inicia o processo curl
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Verifica se conectou
            time.sleep(1)
            if self.process.poll() is not None:
                error = self.process.stderr.read()
                if "403" in error:
                    print("❌ Erro 403: Acesso negado")
                    print("   Possíveis causas:")
                    print("   - URL expirada")
                    print("   - Assinatura inválida")
                    print("   - IP não autorizado")
                elif "400" in error:
                    print("❌ Erro 400: Requisição inválida")
                    print("   A URL pode ter expirado")
                else:
                    print(f"❌ Erro de conexão: {error}")
                return False
            
            print("✅ Conectado com sucesso!")
            print("📡 Recebendo eventos:\n")
            
            # Processa eventos
            event_buffer = []
            for line in self.process.stdout:
                if not self.running:
                    break
                    
                line = line.strip()
                
                # Processa linha SSE
                if line.startswith('event:'):
                    event_type = line[6:].strip()
                    event_buffer = [('event', event_type)]
                    
                elif line.startswith('data:'):
                    data = line[5:].strip()
                    event_buffer.append(('data', data))
                    
                elif line == '' and event_buffer:
                    # Fim do evento, processa
                    self.process_event(event_buffer)
                    event_buffer = []
                    
                elif line.startswith(':'):
                    # Comentário SSE (heartbeat)
                    print(f"💓 {datetime.now().strftime('%H:%M:%S')} - Heartbeat")
                    
            return True
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Parando cliente...")
            return True
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            return False
        finally:
            self.cleanup()
            
    def process_event(self, event_buffer):
        """Processa um evento SSE completo"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        event_type = None
        data_parts = []
        
        for item_type, content in event_buffer:
            if item_type == 'event':
                event_type = content
            elif item_type == 'data':
                data_parts.append(content)
                
        # Monta o evento
        if event_type:
            print(f"\n┌─ [{timestamp}] Evento: {event_type}")
        else:
            print(f"\n┌─ [{timestamp}] Mensagem")
            
        # Processa dados
        full_data = '\n'.join(data_parts)
        try:
            json_data = json.loads(full_data)
            print("├─ Dados (JSON):")
            formatted = json.dumps(json_data, indent=2)
            for line in formatted.split('\n'):
                print(f"│  {line}")
        except:
            print(f"├─ Dados: {full_data}")
            
        print("└─────────────────────────────")
        
    def cleanup(self):
        """Limpa recursos"""
        if self.process:
            self.process.terminate()
            self.process = None
            
    def stop(self):
        """Para o cliente"""
        self.running = False
        self.cleanup()

def main():
    client = MCPSSEClient()
    
    # Handler para Ctrl+C
    def signal_handler(sig, frame):
        client.stop()
        print("\n👋 Até logo!")
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # Inicia cliente
    success = client.start()
    
    if not success:
        print("\n💡 Dicas:")
        print("   1. Verifique se a URL ainda é válida")
        print("   2. Obtenha nova URL em https://www.mcp.run")
        print("   3. Atualize a URL no código")
        sys.exit(1)

if __name__ == "__main__":
    main()