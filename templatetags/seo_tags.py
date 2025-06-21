from django import template
import re

register = template.Library()


@register.simple_tag
def get_meta_description(text, max_length=160):
    """
    Generate a meta description from text content.
    Removes HTML tags and truncates to specified length.
    """
    if not text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Truncate to max_length
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length-3] + "..."
    
    return clean_text


@register.simple_tag
def get_page_title(title, site_name="Avagen"):
    """
    Generate a page title with site name.
    """
    if not title:
        return site_name
    
    return f"{title} | {site_name}"


@register.simple_tag
def get_canonical_url(request):
    """
    Generate canonical URL for the current page.
    """
    return request.build_absolute_uri() 