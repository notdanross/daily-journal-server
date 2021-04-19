import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from moods import get_all_moods, get_mood_by_id
from entries import get_all_entries, get_single_entry, delete_entry, get_entries_by_search

class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            # GIVEN: /entries?q=search_term

            param = resource.split("?")[1] # q=search_term
            resource = resource.split("?")[0] # 'entries
            pair = param.split("=") # [ 'q', 'search_term' ]
            key = pair[0] # 'q'
            value = pair[1] # 'search_term'

            return ( resource, key, value )

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  
            except ValueError:
                pass  

            return (resource, id)  

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            
            if resource == "moods":
                if id is not None:
                    response = get_mood_by_id(id)
                else:
                    response = get_all_moods()
        
        elif len(parsed) ==3:
            ( resource, key, value ) = parsed

            if key == "q" and resource == "entries":
                response = get_entries_by_search(value)

        self.wfile.write(f"{response}".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()