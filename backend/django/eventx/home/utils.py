from .models import APIKey

def validate_api_key(api_key):
    try:
        APIKey.objects.get(api_key=api_key)
        return True
    except APIKey.DoesNotExist:
        return False