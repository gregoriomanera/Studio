#!/usr/bin/env python3
"""Avvia il server locale per Croissant Catalog. Esegui: python3 server.py"""
import http.server, socketserver, webbrowser, threading, os

PORT = 8765
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass  # silent

def open_browser():
    import time; time.sleep(0.4)
    webbrowser.open(f'http://localhost:{PORT}')

threading.Thread(target=open_browser, daemon=True).start()
print(f'\n🥐  Croissant Catalog → http://localhost:{PORT}')
print('   Premi Ctrl+C per fermare\n')
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    httpd.serve_forever()
