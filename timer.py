import functools
import time


def timer(func):
	@functools.wraps(func)
	def wrap_timer(*args, **kwargs):
		start = time.perf_counter()
		value = func(*args, **kwargs)
		end = time.perf_counter()
		print(f"{func.__name__} took {end-start:.5f} s")
		return value
	return wrap_timer
