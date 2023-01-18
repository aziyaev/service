import signal

from werkzeug.serving import WSGIRequestHandler

from pilaf_app import app


class ServerTerminationException(Exception):
    pass


def exit_gracefully(signum, frame):
    raise ServerTerminationException()


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except ServerTerminationException:
        pass
