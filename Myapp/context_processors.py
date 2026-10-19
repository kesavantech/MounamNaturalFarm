from Myapp.models import Website, SocialMedia

def WebsiteSettings(request):
    website = Website.objects.get(id=1)

    return {
        "website": website
    }

def social_media_links(request):
    social_media = SocialMedia.objects.filter(
        is_active=True
    )

    return {
        "social_media_links": social_media
    }
