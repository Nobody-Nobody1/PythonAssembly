from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

def read_html_file(file_path):
            with open(file_path, 'r') as file:
                return file.read()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        def read_html_file(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        self.wfile.write(bytes(read_html_file("index.html"), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")