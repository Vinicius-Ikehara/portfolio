"""Shared slowapi limiter — imported by main.py and routers so they share the same instance."""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
