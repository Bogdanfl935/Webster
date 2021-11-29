def urljoin(*url_components):
    return '/'.join(url_component.strip('/') for url_component in url_components)