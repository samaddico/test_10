from http.server import HTTPServer

from core import PORT, RESTRequestHandler


if __name__ == '__main__':
    http_server = HTTPServer(('', PORT), RESTRequestHandler)
    print('Starting HTTP server at port {}'.format(PORT))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()