from functools import wraps
from flask import make_response


def add_headers(*args, **headers):
    '''Decorator for adding headers to a Flask response'''

    final_headers = {}
    for possible_dict in args:
        try:
            final_headers.update(possible_dict)
        except Exception, e:
            pass
    final_headers.update(headers)

    def _my_decorator(func):
        def _func(*args, **kwargs):
            resp = make_response(func(*args, **kwargs))
            h = resp.headers
            for header, value in final_headers.items():
                h[header] = value
            return resp
        return wraps(func)(_func)
    return _my_decorator





