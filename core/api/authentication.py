from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.models import APIKey
from rest_framework import exceptions


class APIKeyAuthentication(BaseAuthentication):
	keyword = "Api-Key"

	def authenticate(self,request):
		key = request.headers.get(self.keyword)
		if not key:
			return None

		try:
			api_key = APIKey.objects.get(key=key,is_active=True)

		except APIKey.DoesNotExist:
			raise AuthenticationFailed('Invalid API Key')

		#--Permission Logic--

		if request.method in ["POST","PUT","PATCH","DELETE"] and api_key.is_read_only:
			raise exceptions.PermissionDenied("This Api key is read-only")

		return (api_key.user,None)