==============
MyCustomMailer
==============

MyCustomMailer is a Django app to authenticate Gmails with a simple front-end flow and then used
programmatically to send emails.

Prerequisites
-------------
Creating an application on console.cloud.google.com, enabling the Gmail API and getting the credentials.json

* Go to this tutorial by Google https://developers.google.com/workspace/guides/create-project
* Follow the steps to create an application in the cloud
* Enable the Gmail API
* Add as Authorized redirect URI the localhost or production link (or both). These are the two variables used in the setting.py (see step 4).
* Finally download the client_secret.json and put it somewhere in your project you will need it later.


Quick start
-----------

1. Add "mcmailer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mcmailer',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('mcmailer/', include('mcmailer.urls')),

3. Run ``python manage.py migrate`` to create the mcmailer models.

4. In the settings.py you must declare the following four settings::

    JSON_PATH = "/my/path/to/client_secret.json"
    LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"
    PRODUCTION_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"

5. The JSON_PATH setting is the path that the 'credentials.json' will be located.

6. The LOCAL_HOST_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the DEBUG is equal to True. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"

7. The PRODUCTION_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the DEBUG is equal to False. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"

8. Start the development server and visit http://127.0.0.1:8000/mcmailer/connect/ enter the email you want to to grand access to your application and click submit.

9. Now that you have successfully granted access to your application from at least one Gmail, you can send emails from
that email using send_mc_email() function of the package::

        from mcmailer.utils.sendgmail import send_mc_email, load_credentials

        authorized_gmail_address = 'someaddress@gmail.com'
        success, credentials = load_credentials(authorized_gmail_address)
        send_mc_email(
            credentials,
            from_address=authorized_gmail_address,
            to_addresses=[
                'toaddress2@gmail.com',
                'toaddress3@gmail.com',
                'toaddress4@gmail.com'
            ],
            from_official_name='MY OFFICIAL NAME',
            subject='My Subject',
            msg_plain='My Plain Email Body',
            msg_html='My HTML Email Body'
        )


Now any user that has Gmail can grant 'gmail.send' access to your app by following the authorization flow (http://127.0.0.1:8000/mcmailer/connect/) and then you will be able to send emails on behalf of them.

If your app doesn't need to authenticate new users on production and you only need to authenticate a Gmail to sent emails programmatically then you can just authenticate your Gmail locally once and then remove the package variables from settings.py and the package's URL path from urls.py. Just leave the 'mcmailer' in your INSTALLED_APPS to be able to send emails programmatically.