from django.apps import AppConfig
# from . import signals

class InstructorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instructor'
    
    def ready(self):
        import instructor.signals
