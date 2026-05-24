from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom TokenAuthentication that uses the 'Bearer' keyword instead of 'Token'
    to align Django's authentication header with Laravel Sanctum (standard Bearer token).
    """
    keyword = 'Bearer'
