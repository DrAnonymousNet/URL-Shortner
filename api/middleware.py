
from urllib import response
from django.db import connection
from django.conf import settings
from .models import Link
import os

def ExposeModelRequestMiddleware(get_response):
    def middleware(request):
        Link.request = request
        response = get_response(request)
        return response
    return middleware


def terminal_width():
    """
    Function to compute the terminal width.
    """
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width


def SqlPrintingMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        

        indentation = 2
        print("\n\n%s\033[1;35m[SQL Queries for]\033[1;34m %s\033[0m\n" % (" " * indentation, request.path_info))
        width = terminal_width()
        total_time = 0.0
        for query in connection.queries:
            nice_sql = query['sql'].replace('"', '').replace(',', ', ')
            sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
            total_time = total_time + float(query['time'])
            while len(sql) > width - indentation:
                print("%s%s" % (" " * indentation, sql[:width - indentation]))
                sql = sql[width - indentation:]
            print("%s%s\n" % (" " * indentation, sql))
        replace_tuple = (" " * indentation, str(total_time))
        print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
        print("%s\033[1;32m[TOTAL QUERIES: %s]\033[0m" % (" " * indentation, len(connection.queries)))
        return response
    return middleware