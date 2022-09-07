from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_app'
    
    #import the signals to be fired
    def ready(self):
        import users_app.signals