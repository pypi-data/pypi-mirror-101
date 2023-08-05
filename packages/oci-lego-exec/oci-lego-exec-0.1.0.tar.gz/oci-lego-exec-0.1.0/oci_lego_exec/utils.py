

def zone_names(domain):
    """
    Return a list of progressively less-specific domain names.
    """
    fragments = domain.split('.')
    return ['.'.join(fragments[i:]) for i in range(0, len(fragments))]


def cleanup(name):
    """
    Return a cleaned string based on OCI constraints
    """
    cleaned_name = name.rstrip(".")
    return cleaned_name
