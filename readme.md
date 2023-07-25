django-sso-client-manager
=========================

django-sso-client-manager is a Django application designed to simplify the management of Single Sign-On (SSO) clients within a web application. \
It provides functionalities for handling login and logout processes and conveniently sets codes in cookies for seamless authentication and user session management.\
By integrating this app into a Django project, developers can streamline the implementation of SSO functionality and enhance the overall user experience.

To install the django-sso-client-manager package and integrate it into your Django project, follow these steps:
------------

1. Use pip to install the package:

    ```python
    pip install django-sso-client-manager    
    ```

2. Add sso_client_manager to the INSTALLED_APPS list in your project's settings.py file:
    ```python
    INSTALLED_APPS = [
        # other apps
        'sso_client_manager',
    ]  
    ```
        

3. Include the ParseCodeDataMiddleware in your project's middleware configuration by adding it to the MIDDLEWARE list in settings.py:
    ```python
    MIDDLEWARE = [
        # other middleware
        'sso_client_manager.middlewares.ParseCodeDataMiddleware',
    ]  
    ```   

4. Finally, include the sso_client_manager.urls in your project's urls.py file to set up the necessary URL routes for the SSO functionality:
    ```python
    urlpatterns = [
        # other URL patterns
        path('', include('sso_client_manager.urls')),
    ]  
    ```
    Once you've completed these steps, the django-sso-client-manager package will be installed, and you'll have integrated its features into your Django project, allowing you to manage SSO clients with login, logout, and code handling functionalities.

Explanation of the new field to need to add in User Model (if not exist).
------------

1. sso_id 

    The user model needs to be extended with an additional field called sso_id. This field will be used to store the unique user ID provided by the SSO (Single Sign-On) server.

    sso_id: This field will store the user ID assigned by the SSO server. When a user logs in through the SSO process, the SSO server will generate a unique ID for that user, and this ID needs to be stored in the local user model to associate the local user with the SSO user. Having this field will enable seamless user synchronization and authentication between the local application and the SSO server.

    By adding the sso_id field to the user model, the application can easily link local user accounts with their corresponding SSO accounts, allowing users to log in using their SSO credentials and access the application without the need to create separate login credentials. This enhances user experience and streamlines authentication processes.

2. username

To integrate the SSO (Single Sign-On) functionality into your Django application, you will need to add the following variables to your settings:
-----------------
1. APPLICATION_ID:

    This variable should store the unique identifier for your application within the SSO system. It is typically provided by the SSO server during the registration process.

2. SSO_SERVER:

    This variable holds the url of the SSO server.

3. KEY:

    This variable represents a secret key or encryption key used for secure communication or token validation between your application and the SSO server.
    ```python
    APPLICATION_ID = env.str('APPLICATION_ID')
    KEY = env.str('KEY')
    SSO_SERVER = env.str('SSO_SERVER') 
    ```

    By setting these variables in your Django settings, your application will be able to communicate with the SSO server, authenticate users, and manage the login/logout processes securely.

Compatibility
-------------
The compatibility information you provided indicates that the django-sso-client-manager package is compatible with Python 3.8 and Django versions 4 and above.

To ensure proper compatibility, always check the official documentation and release notes of the django-sso-client-manager package to confirm its support for specific Python and Django versions.
