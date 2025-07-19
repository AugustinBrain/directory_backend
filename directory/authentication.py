import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import AdminAccount

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account_id = payload.get('account_id')
            
            if not account_id:
                raise exceptions.AuthenticationFailed('Invalid token')
            
            try:
                admin = AdminAccount.objects.get(account_id=account_id)
                return (admin, token)
            except AdminAccount.DoesNotExist:
                raise exceptions.AuthenticationFailed('Admin not found')
                
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
    
    def authenticate_header(self, request):
        return 'Bearer'