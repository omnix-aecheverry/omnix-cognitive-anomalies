"""AsyncResponse extension for Flask."""
import traceback
from werkzeug.wsgi import ClosingIterator

class AsyncResponse:
    """AsyncResponse extension for Flask."""
    def __init__(self, app=None):
        self.callbacks = []
        if app:
            self.init_app(app)

    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback

    def init_app(self, app):
        """Initialize the extension."""
        app.async_response = self
        app.wsgi_app = AsyncResponseMiddleware(app.wsgi_app, self)

    def flush(self):
        """Flush the callbacks."""
        for fn in self.callbacks:
            try:
                fn()
            except Exception:
                traceback.print_exc()

class AsyncResponseMiddleware:
    """AsyncResponse middleware."""
    def __init__(self, application, async_response_ext):
        self.application = application
        self.async_response_ext = async_response_ext

    def __call__(self, environ, async_response):
        iterator = self.application(environ, async_response)
        try:
            return ClosingIterator(iterator, [self.async_response_ext.flush])
        except Exception:
            traceback.print_exc()
            return iterator