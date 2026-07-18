def generate_meta_description(title, article):
    """
    Generate SEO Meta Description
    """

    # Remove line breaks
    article = article.replace("\n", " ")

    # First 150 characters
    meta = article[:150].strip()

    # Add title if needed
    if title.lower() not in meta.lower():
        meta = f"{title} - {meta}"

    # Limit to 160 characters
    return meta[:160]
