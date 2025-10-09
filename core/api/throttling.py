from rest_framework.throttling import SimpleRateThrottle


class APIKeyRateThrottle(SimpleRateThrottle):
	scope = "api_key"

	def get_cache_key(self,request,view):
		key = request.headers.get("Api-Key")
		if not key:
			return None
		return self.cache_format % {"scope":self.scope,"ident":key}



