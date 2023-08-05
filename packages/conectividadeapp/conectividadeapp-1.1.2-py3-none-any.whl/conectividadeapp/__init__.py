from extras.plugins import PluginConfig


class ConectividadeAppConfig(PluginConfig):
    name = 'conectividadeapp'
    verbose_name = 'conectividade'
    description = 'An plugin'
    version = '1.1.2'
    author = 'Johnny; Avando; Eduardo; Rary; Thiago'
    author_email = 'johnnyyuri56@gmail.com'
    required_settings = []
    default_settings = {
        'loud': False
    }
    middleware = ['simple_history.middleware.HistoryRequestMiddleware']
    # Base URL path. If not set, the plugin name will be used.
    base_url = 'conectividadeapp'
    # Caching config
    caching_config = {}


config = ConectividadeAppConfig
