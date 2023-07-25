import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

User = get_user_model()
signer = Signer()

def profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'user_data':None
        }, status=401)
    
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    })

def login_checker(request):
    next_url = request.GET.get('next') or request.build_absolute_uri('/')
    url_path = request.build_absolute_uri(reverse('set-code'))
    sso_url = settings.SSO_SERVER + 'login-checker/'
    sso_url = f'{sso_url}?next={url_path}&frontend_url={next_url}&application_id={settings.APPLICATION_ID}'
    response = redirect(sso_url)
    response.delete_cookie('user_data')
    response.delete_cookie('access_code')
    response.delete_cookie('is_logged_in')
    return response
   
def login(request):
    next_url = request.GET.get('next') or '/'
    url_path = request.build_absolute_uri(reverse('set-code'))
    sso_url = settings.SSO_SERVER + 'login/'
    sso_url = f'{sso_url}?next={url_path}&frontend_url={next_url}&application_id={settings.APPLICATION_ID}'
    response = redirect(sso_url)
    response.delete_cookie('user_data')
    response.delete_cookie('access_code')
    response.delete_cookie('is_logged_in')
    return response

def logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message':'You have not login to this sytem.'})

    next_url = request.GET.get('next') or request.build_absolute_uri('/')
    sso_url = settings.SSO_SERVER + 'logout/'
    sso_url = f'{sso_url}?next={next_url}'
    response = redirect(sso_url)
    response.delete_cookie('user_data')
    response.delete_cookie('access_code')
    response.delete_cookie('is_logged_in')
    return response

class SetCodeView(View):
    def create_or_update_user(self, user_data):
        try:
            username=user_data['username']
        except Exception as e:
            raise ValueError(
                f"Error due to {e}"
            )
        
        try:
            user = User.objects.get(username=username)
            user.last_login = user_data.get('last_login', timezone.now())
            user.save()
        except:
            user = User.objects.create(
                username=user_data.get('username'),
                is_staff = user_data.get('is_staff', False),
                is_active = user_data.get('is_active', False),
                is_superuser = user_data.get('is_superuser', False),
                date_joined = user_data.get('date_joined', timezone.now()),
                last_login = user_data.get('last_login', timezone.now()),
            )

        if hasattr(user, 'sso_id') and user_data.get('id'):
            user.sso_id = user_data.get('id')
            user.save()

        return user

    def get(self, request):
        access_code = request.GET.get('access_code')
        if not access_code:
            frontend_url = request.GET.get('frontend_url') or '/'
            response = HttpResponseRedirect(frontend_url)
            response.delete_cookie('access_code')
            response.delete_cookie('user_data')
            response.delete_cookie('is_logged_in')
            return response
        
        sso_url = settings.SSO_SERVER + 'api/v1/token-checker/'
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
            frontend_url = request.GET.get('frontend_url') or '/'
            response = HttpResponseRedirect(frontend_url)
            response.delete_cookie('access_code')
            response.delete_cookie('user_data')
            response.delete_cookie('is_logged_in')
            return response
        
        try:
            access_code = response_json.pop('access_code')
        except:
            frontend_url = request.GET.get('frontend_url') or '/'
            response = HttpResponseRedirect(frontend_url)
            response.delete_cookie('access_code')
            response.delete_cookie('user_data')
            response.delete_cookie('is_logged_in')
            return response

        user = self.create_or_update_user(response_json)
        user_data = signer.sign_object({
            'username' : user.username
        }) 

        frontend_url = request.GET.get('frontend_url') or '/'
        response = HttpResponseRedirect(frontend_url)
        response.set_cookie('user_data', user_data, expires=30, httponly=True)
        response.set_cookie('access_code', access_code, httponly=True)
        response.set_cookie('is_logged_in', 'true')
        return response
