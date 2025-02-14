from functools import partial, wraps
from typing import Callable

from fastapi import status

from app.helpers.functions import error_response


def public(route_handler):
    route_handler.is_public = True
    return route_handler
