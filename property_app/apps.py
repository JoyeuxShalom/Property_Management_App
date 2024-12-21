from django.apps import AppConfig

class PropertyAppConfig(AppConfig):
    name = 'property_app'

    def ready(self):
        import property_app.signals  # Ensure this import happens after app initialization
