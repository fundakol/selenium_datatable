from threading import Thread

import requests
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


class MockServer(Thread):

    def __init__(self, port=5000):
        super().__init__()
        self.port = port
        self.app = app
        self.url = f'http://localhost:{self.port}'

        self.app.add_url_rule('/shutdown', view_func=self._shutdown_server)

    def _shutdown_server(self):
        from flask import request
        if 'werkzeug.server.shutdown' not in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get(f'{self.url}/shutdown')
        self.join()

    def run(self):
        self.app.run(port=self.port)
