"""
Simple IP-based rate limiter (protects /auth/login and /chatbot from abuse).
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
