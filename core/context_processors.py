
# core/context_processors.py
from django.conf import settings

def site_info(request):
    """
    Adds site-wide info and Supabase/DEBUG settings to the template context.
    """
    return {
        'brand_name': 'Meridian',
        'support_email': 'meridian@info.com',
        'debug': settings.DEBUG,
        'supabase_ref': getattr(settings, 'SUPABASE_PROJECT_REF', ''),
        'bucket': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'blog-images'),
    }
