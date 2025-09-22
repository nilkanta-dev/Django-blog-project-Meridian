import time
import logging

logger = logging.getLogger(__name__)


class RequestTimingMiddleware:

	def __init__(self,get_response):
		self.get_response = get_response
		logger.warning("RequestTimingMiddleware initialized.")

	def __call__(self,request):

		start_time = time.time()

		response = self.get_response(request)

		duration = time.time() - start_time

		logger.warning(f"{request.method} {request.path} took {duration:2f} seconds")

		return response
