SSO-Client-Manager Docs
=========================

SSO-Client-Manager is a application designed to simplify the management of Single Sign-On (SSO) clients within a web application. \
It provides functionalities for handling login and logout processes and conveniently sets codes in cookies for seamless authentication and user session management. \
By integrating this app into a project, developers can streamline the implementation of SSO functionality and enhance the overall user experience.

Endpoint need to add in your application
------------------

1. login-checker api

    1. We start by getting the value of the 'next' query parameter from the request URL using $_GET['next']. If it's not present, we set it to the base URL of the current site, obtained from $_SERVER['HTTP_HOST'].

    2. We then generate the absolute URL for the 'set-code' route or api (assuming it's named 'set-code') using $_SERVER['HTTP_HOST'] . '/set-code', api that set access code to cookie.

    3. We create the base URL for the Single Sign-On (SSO) server by appending 'login-checker/' to the value retrieved from settings (assuming you have defined it in your configuration).

    4. The complete SSO URL is constructed by adding the necessary query parameters using concatenation and urlencode() function to properly encode the values.

    5. We perform a redirect to the SSO URL using the header() function, which will redirect the user to the SSO server with the appropriate query parameters.

    6. After the redirection, we delete specific cookies from the response using setcookie() with an expiration time in the past (i.e., immediately expiring the cookie) to effectively delete them.
    ```python
    next_url = request.GET.get('next') or request.build_absolute_uri('/')
    url_path = request.build_absolute_uri(reverse('set-code'))
    sso_url = settings.SSO_SERVER + 'login-checker/'
    sso_url = f'{sso_url}?next={url_path}&frontend_url={next_url}&application_id={settings.APPLICATION_ID}'
    response = redirect(sso_url)
    response.delete_cookie('user_data')
    response.delete_cookie('access_code')
    response.delete_cookie('is_logged_in')
    return response
    ```

    Please note that in the PHP code, we use $_GET and $_SERVER['HTTP_HOST'] to handle the GET parameters and server information, respectively. Also, we use header('Location: ...') for redirection, and setcookie() to delete the cookies. In a real PHP application, you would need to ensure you have the appropriate settings/configurations and replace settings() with the appropriate way to access your configuration values.

2. login api

    1. We start by getting the value of the 'next' query parameter from the request URL using $_GET['next']. If it's not present, we set it to the base URL of the current site, obtained from $_SERVER['HTTP_HOST'].

    2. We then generate the absolute URL for the 'set-code' route (assuming it's named 'set-code') using $_SERVER['HTTP_HOST'] . '/set-code'.

    3. We create the base URL for the Single Sign-On (SSO) server by appending 'login/' to the value retrieved from settings (assuming you have defined it in your configuration).

    4. The complete SSO URL is constructed by adding the necessary query parameters using concatenation and urlencode() function to properly encode the values.

    5. We perform a redirect to the SSO URL using the header() function, which will redirect the user to the SSO server with the appropriate query parameters.

    6. After the redirection, we delete specific cookies from the response using setcookie() with an expiration time in the past (i.e., immediately expiring the cookie) to effectively delete them.
    ```python
    next_url = request.GET.get('next') or '/'
    url_path = request.build_absolute_uri(reverse('set-code'))
    sso_url = settings.SSO_SERVER + 'login/'
    sso_url = f'{sso_url}?next={url_path}&frontend_url={next_url}&application_id={settings.APPLICATION_ID}'
    response = redirect(sso_url)
    response.delete_cookie('user_data')
    response.delete_cookie('access_code')
    response.delete_cookie('is_logged_in')
    return response
    ```

    Please note that in the PHP code, we use $_GET and $_SERVER['HTTP_HOST'] to handle the GET parameters and server information, respectively. Also, we use header('Location: ...') for redirection, and setcookie() to delete the cookies. In a real PHP application, you would need to ensure you have the appropriate settings/configurations and replace settings() with the appropriate way to access your configuration values.

2. logout api

    1. The code starts by checking if the user is authenticated (logged in) by verifying the value of $_SESSION['user_authenticated']. If the user is not authenticated, it returns a JSON response with a message indicating that the user has not logged in to the system.

    2. If the user is authenticated, the code proceeds with the logout process.

    3. It gets the 'next' query parameter from the request URL using $_GET['next']. If 'next' is not present, it sets it to the base URL of the current site obtained from $_SERVER['HTTP_HOST'].

    4. The code constructs the base URL for the Single Sign-On (SSO) server's logout endpoint by appending 'logout/' to the value retrieved from settings (assuming you have defined it in your configuration).

    5. The complete SSO logout URL is built by adding the 'next' query parameter using concatenation and urlencode() function to properly encode the value.

    6. The code then performs a redirect to the SSO logout URL using the header() function, which will redirect the user to the SSO server's logout endpoint with the appropriate 'next' query parameter.

    7. After the redirection, it deletes specific cookies from the response using setcookie() with an expiration time in the past (i.e., immediately expiring the cookies) to effectively delete them.
    ```python
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
    ```
    
    Please note that in the PHP code, we use $_SESSION['user_authenticated'] to check if the user is authenticated, and $_GET and $_SERVER['HTTP_HOST'] to handle the GET parameters and server information, respectively. Also, we use header('Location: ...') for redirection, and setcookie() to delete the cookies. In a real PHP application, you would need to ensure you have the appropriate settings/configurations and replace settings() with the appropriate way to access your configuration values.

3. set-code api

    1. The code starts by getting the 'access_code' from the request URL's GET parameters. If 'access_code' is not present, it checks for the 'frontend_url' and creates a redirect response to it, effectively redirecting the user back to where they came from.

    2. If 'access_code' is present, it proceeds with making a POST request to the SSO server's token checker endpoint. It sends the 'access_code' and the application ID to validate the token.

    3. If the token check fails (the request is not successful or there is an error in the response JSON), it creates a redirect response to the 'frontend_url' and deletes specific cookies.

    4. If the token check is successful, it proceeds to create or update the user using the response JSON data with appropriate function. Then, encryt the user data with appropriate encryption algorithms and sets cookies for the response containing the encryted user data with a 30-second expiration time, 'access_code', and a flag 'is_logged_in'.
    ```python
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
    user_data = encrypt({
        'username' : user.username
    }) 

    frontend_url = request.GET.get('frontend_url') or '/'
    response = HttpResponseRedirect(frontend_url)
    response.set_cookie('user_data', user_data, expires=30, httponly=True)
    response.set_cookie('access_code', access_code, httponly=True)
    response.set_cookie('is_logged_in', 'true')
    return response
    ```
    Please note that in the PHP code, we use various PHP functions such as isset(), header(), json_encode(), json_decode(), setcookie(), etc., to handle GET parameters, headers, JSON data, cookies, and redirection. Also, we use requests_post() to simulate the POST request (replace it with appropriate logic or use a PHP HTTP library like cURL for actual requests). In a real PHP application, you would need to ensure you have the appropriate settings/configurations and replace settings() with the appropriate way to access your configuration values.

To create a middleware that parses the access code to authenticate a user, implement it in a middleware.
------------------   

1. The middleware's handle method is called for each incoming request. It first checks if the request path matches any of the specified paths ('/set-code/', '/admin/login/', or '/login-checker/'). If it does, the middleware allows the request to continue its regular handling.

2. If the request path does not match the specified paths, the middleware proceeds to check if the user is not authenticated but has an 'access_code' cookie.

3. If the user is not authenticated and has an 'access_code' cookie, it attempts to decryt 'user_data' cookie with appropriate encryption algorithms to obtain the username. If 'user_data' is not present or invalid, it performs a session check with the SSO server to validate the 'access_code' and obtain the username.

4. Once it has the username, it tries to find the user with that username in the database and sets the user as the authenticated user in the request.

5. After the request is handled (i.e., the response is ready to be sent back), the middleware processes the response. If 'my_code_mod' is true (meaning the token check was successful) and 'access_code' cookie is present, encryt the 'user_data' with appropriate encryption algorithms and sets the 'user_data' cookie with a 30-second expiration time.

6. If 'remove_cookie' is true (meaning the token check failed or the user was not found), it deletes specific cookies ('access_code', 'user_data', 'is_logged_in') from the response.

```python
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
        user_data = decrypt(user_data)
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
    user_data = encrypt({
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
```

Please note that the actual implementation may vary depending on the PHP framework you are using and the specific functions for handling requests, responses, cookies, etc. Also, the code assumes the existence of appropriate functions (such as signer_unsign_object(), settings(), requests_post(), and others) for handling cryptographic operations, configurations, and HTTP requests in PHP. Replace these with appropriate logic and libraries as needed in your specific PHP application.

Explanation of the new field to need to add in User Model (if not exist).
------------

1. sso_id 

    The user model needs to be extended with an additional field called sso_id. This field will be used to store the unique user ID provided by the SSO (Single Sign-On) server.

    sso_id: This field will store the user ID assigned by the SSO server. When a user logs in through the SSO process, the SSO server will generate a unique ID for that user, and this ID needs to be stored in the local user model to associate the local user with the SSO user. Having this field will enable seamless user synchronization and authentication between the local application and the SSO server.

    By adding the sso_id field to the user model, the application can easily link local user accounts with their corresponding SSO accounts, allowing users to log in using their SSO credentials and access the application without the need to create separate login credentials. This enhances user experience and streamlines authentication processes.

2. username

To integrate the SSO (Single Sign-On) functionality into your application, you will need to add the following variables to your settings:
-----------------
1. APPLICATION_ID:

    This variable should store the unique identifier for your application within the SSO system. It is typically provided by the SSO server during the registration process.

2. SSO_SERVER:

    This variable holds the url of SSO server. 

3. KEY:

    This variable represents a secret key or encryption key used for secure communication or token validation between your application and the SSO server.

    ```python
    APPLICATION_ID = env.str('APPLICATION_ID')
    KEY = env.str('KEY')
    SSO_SERVER = env.str('SSO_SERVER') 
    ```

    By setting these variables in your settings, your application will be able to communicate with the SSO server, authenticate users, and manage the login/logout processes securely.





