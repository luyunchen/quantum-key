import os
import socketserver
import socket
import sys

try:
    import http.server as server
except ImportError:
    # Handle Python 2.x
    import SimpleHTTPServer as server

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    def do_PUT(self):
        """Save or replace a file following an HTTP PUT request"""
        filename = os.path.basename(self.path)

        # Get the directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the 'Workspace' folder in the script directory
        workspace_directory = os.path.join(script_directory, 'Workspace')

        # Construct the full path to the file within the 'Workspace' directory
        full_file_path = os.path.join(workspace_directory, filename)

        file_length = int(self.headers['Content-Length'])
        with open(full_file_path, 'wb') as output_file:  # Use 'wb' mode for writing
            output_file.write(self.rfile.read(file_length))

        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved or replaced "%s" in the "Workspace" directory\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))

if __name__ == '__main__':

    with open('port.txt') as f:
        first_line = f.readline()
    port = int(first_line)


    # Change the current working directory to the 'Workspace' folder
    script_directory = os.path.dirname(os.path.abspath(__file__))
    workspace_directory = os.path.join(script_directory, 'Workspace')
    os.chdir(workspace_directory)

    httpd = socketserver.TCPServer((IPAddr, port), HTTPRequestHandler)

    print("Server started on: "+IPAddr)
    httpd.serve_forever()