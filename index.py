from http.server import BaseHTTPRequestHandler

import json

import keelback
import keelsearch

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        payload = keelback.serve(self.path)
        self.wfile.write(payload.encode())
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        body = self.rfile.read(int(self.headers.get('Content-Length')))
        body_trimmed = str(body)[2:-1]
        if '=' in body_trimmed:
            post_request = dict(x.split('=') for x in body_trimmed.split(','))
            if 'search' in post_request:
                response = keelsearch.search(post_request['search'])
                payload = '<html lang="en"><head><title>Redirecting...</title><meta http-equiv="refresh" content="0;url=/{response}" /></head></html>'.format(response=response)
                self.wfile.write(payload.encode())
        else:
            payload = 'Internal search error.'
            self.wfile.write(payload.encode())
        return
