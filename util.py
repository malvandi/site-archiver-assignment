def get_site_key(site: str) -> str:
    key = site.replace('http://', '')
    return key.replace('https://', '')
