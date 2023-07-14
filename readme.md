django-sso-client-manager
=========================

django-sso-client-manager is a Django app for the managing sso client that have login, logout and set code a in cookies.

Installation
------------

    * pip install django-sso-client-manager
    * Add ``sso_client_manager`` to your ``INSTALLED_APPS``
    * Add ``sso_client_manager.middlewares.ParseCodeDataMiddleware`` to your ``MIDDLEWARE``
    * Add ``path('', include('sso_client_manager.urls')),`` to your project urls.py

::

Setup in settings
-----------------

    *APPLICATION_ID
    *SSO_SERVER_TOKEN
    *SSO_SERVER_SESSIONID
    *SSO_SERVER_USER
    *SSO_SERVER_LOGIN
    *SSO_SERVER_LOGOUT
    *KEY
    
    Add this variable with value.

::


Compatibility
-------------
{py310}-django{4.* above}
