import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.utils.deprecation import MiddlewareMixin

signer = Signer()
User = get_user_model()

class ParseCodeDataMiddleware(MiddlewareMixin):
    
    def __call__(self, request):
        if ('/set-code/' in request.path or 
            '/admin/login/' in request.path or 
            '/login-checker/' in request.path):
            return self.get_response(request)
        
        access_code = request.COOKIES.get('access_code')
        my_code_mod = None
        remove_cookie = None
        if (not request.user.is_authenticated and 
            access_code):    

            try:
                user_data = request.COOKIES.get('user_data')
                user_data = signer.unsign_object(user_data)
                username = user_data['username']
            except:
                user_data = None

            if not user_data:
                sso_url = settings.SSO_SERVER + 'api/v1/session-checker/'
                headers = {
                    'Authorization': f'{settings.KEY}',
                    'Content-Type': 'application/json',  # Adjust the Content-Type if needed
                }

                response = requests.post(
                    url=sso_url,
                    json={
                        'access_code':access_code,
                        'application_id':settings.APPLICATION_ID
                    },
                    headers=headers
                )
                
                response_json = response.json()
                if not response.ok:
                    remove_cookie = True
                else:
                    username = response_json['username']
                    my_code_mod = True
                
            try:
                request.user = User.objects.filter(username=username).first()
            except:
                remove_cookie = True
                my_code_mod = False

        response = self.get_response(request)
        if my_code_mod and request.COOKIES.get('access_code'):
            user_data = signer.sign_object({
                'username' : username
            }) 
            response.set_cookie(
                'user_data', user_data, 
                httponly=True, expires=30
            )
        if remove_cookie:
            response.delete_cookie('access_code')
            response.delete_cookie('user_data')
            response.delete_cookie('is_logged_in')
        return response
