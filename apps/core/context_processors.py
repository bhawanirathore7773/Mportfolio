from .models import SiteSettings, SocialLink


def site_settings(request):
    return {
        "site_settings": SiteSettings.load(),
        "social_links": SocialLink.objects.filter(is_active=True),
    }
