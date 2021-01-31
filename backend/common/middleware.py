import sys

from django.conf import settings
from django.db import connection
from django.utils import termcolors
from django.utils.deprecation import MiddlewareMixin

import colorama


class QueryPrintingMiddleware(MiddlewareMixin):
    """
    Taken from:
    http://www.szotten.com/david/show-number-of-queries-in-runserver-output.html
    """

    initial_queries = None

    def process_request(self, request):
        if settings.DEBUG:
            self.initial_queries = len(connection.queries)

    def process_response(self, request, response):
        if (
            settings.DEBUG
            and ("runserver" in sys.argv or "runserver_plus" in sys.argv)
            and self.initial_queries is not None
        ):
            colorama.init(autoreset=True)

            # Colour definition
            danger = termcolors.make_style(opts=("bold",), fg="red")
            warning = termcolors.make_style(opts=("bold",), fg="yellow")
            ok = termcolors.make_style(opts=("bold",), fg="green")

            # Calculate number of queries
            count = len(connection.queries) - self.initial_queries
            output = f"[DB queries: {count}] "

            # Apply colour threshold
            if count >= getattr(settings, "NUMBER_OF_QUERIES_DANGER", 50):
                output = danger(output)
            elif count >= getattr(settings, "NUMBER_OF_QUERIES_WARNING", 25):
                output = warning(output)
            else:
                output = ok(output)

            # runserver just prints its output to sys.stderr, so follow suite
            sys.stderr.write(output)

            # Stop colorama to avoid "RecursionError"
            colorama.deinit()

        return response
