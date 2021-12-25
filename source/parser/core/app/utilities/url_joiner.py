def construct_parameterized_url(base_url: str, parameters: dict = {}):
    return f"{base_url}?{'&'.join(param_key+'='+param_val for param_key, param_val in parameters.items())}"\
        if len(parameters) > 0 else base_url
    

def urljoin(*url_components):
    return '/'.join(url_component.strip('/') for url_component in url_components)