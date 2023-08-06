==============
MyCustomMailer
==============

MyCustomMailer is a Django app to authenticate Gmails with a simple front-end flow and then used
programmatically to send emails.

Prerequisites
-------------
Creating an application on console.cloud.google.com, enabling the Gmail API and getting the credentials.json

* Go to this quickstart by Google https://developers.google.com/gmail/api/quickstart/python and click on the blue
  button that says "Enable the Gmail API"
* Give your project a name
* Choose Web Server
* Add the following address as one of the Authorized redirect URIs "http://localhost:8000/mcmailer/g-auth-endpoint/"
* Click "Create"
* Click "DOWNLOAD CLIENT CONFIGURATION"
* Finally click the blue link that says 'API Console' at the bottom right of the pop-up to open the new project in
  the console.
* If you want language support then, when you install this package, before migrating the migrations,
    make sure that you have installed this pip package -> 'django-modeltranslation' and you have in
    your setting.py the following in your installed apps -> 'modeltranslation', at the first position
    then run the 'python manage.py update_translation_fields' management command to populate any existing fields.

That's is, now you've created an application in the cloud, enabled the Gmail API and added as Authorized redirect URI
the localhost link that this package will use. Now you can grant 'gmail.send' access to your app from any Gmail address
following the authorization flow and send emails on behalf of that address through your Django-app.

Production
----------
If you want your users to be able to grant access to your application in a production environment and implement this
to your Django application flow so you can send emails programmatically on behalf of them, then you need to add your
live production URL (e.g. "https://example.com/mcmailer/g-auth-endpoint/") to the Authorized redirect URIs. To do this
you need to console.developers.google.com, select the project you've created earlier, click credentials from the left
menu, under 'OAuth 2.0 Client IDs' there is you will see the credentials you created earlier, click on the pencil to edit
the credentials, add your production URI click save, download the updated credentials.json and replace it in your project.

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
    LOCAL_HOST = True
    LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"
    PRODUCTION_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"

5. The JSON_PATH setting is the path that the 'credentials.json' will be located.

7. The LOCAL_HOST_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the LOCAL_HOST is equal to True. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "http://localhost:8000/mcmailer/g-auth-endpoint/"

8. The PRODUCTION_REDIRECT_URI setting is one (or the only one) of the Authorized redirect URIs that you will put in your credentials in the console.cloud.google.com. This URI will be used if the LOCAL_HOST is equal to False. The URI must point to a specific view so just change the part (if needed) before the /mcmailer/g-auth-endpoint/. Example: LOCAL_HOST_REDIRECT_URI = "https://example.com/mcmailer/g-auth-endpoint/"
    * If your app doesn't need to authenticate new users on production and you only need to authenticate your own Gmail to sent emails programmatically then you can just authenticate your Gmail locally once and leave the LOCAL_HOST variable to False and don't declare the PRODUCTION_REDIRECT_URI variable in your settings.py.

9. Start the development server and visit http://127.0.0.1:8000/mcmailer/connect/
   enter the email you want to to grand access to your application and click submit.

10. Now that you have successfully granted access to your application from at least one Gmail, you can send emails from
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

