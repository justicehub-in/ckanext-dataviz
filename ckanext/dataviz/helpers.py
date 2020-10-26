from ckan.plugins.toolkit import config


# TODO: Not implemented
def dataviz_theme():
    """
    Return dataviz theme string from config file
    """
    theme = config.get("ckan.dataviz.theme")
    return theme if theme else str(theme)
