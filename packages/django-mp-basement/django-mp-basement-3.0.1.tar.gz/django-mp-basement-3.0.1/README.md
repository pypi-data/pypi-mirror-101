Install with pip:

```
pip install django-mp-basement
```

Settings:
```
from basement.settings import BasementSettings


BASE_DIR = dirname(dirname(abspath(__file__)))
 
 
class BaseSettings(BasementSettings):
 
    BASE_DIR = BASE_DIR
    DB_NAME = 'example'
    DOMAIN = 'example.com'
    SECRET_KEY = 'some_secret_key'
    
    IS_LESS_ENABLED = True  # this option enables less files compiler

    BOWER_INSTALLED_APPS = (
        'jquery#1.11.0',
        'bootstrap#3.3.7',
        ...
    )

    STYLESHEETS = (
        'bootstrap/less/bootstrap.less',
        'bootstrap/less/theme.less',
        ...
    )

    JAVASCRIPT = (
        'jquery/dist/jquery.js',
        'bootstrap/dist/js/bootstrap.js',
        ...
    )
```

Add static to template:

```
{% load pipeline %}

{% stylesheet 'generic' %}
{% javascript 'generic' %}
```

Local settings:
```
from basement.settings import LocalSettingsMixin
from core.common_settings import CommonSettings
 
 
class Settings(LocalSettingsMixin, CommonSettings):
    pass

```

Production settings:
```
from basement.settings import ProductionSettingsMixin
from core.common_settings import CommonSettings
 
 
class Settings(ProductionSettingsMixin, CommonSettings):
    pass
```

Migrate to 3+ version:
* replace `assets.images` with `basement.images`
* remove `StaticFileSettings` from settings
* remove `MediaFileSettings` from settings
* remove `path('images/', include('assets.images.urls')),` from core urls.
* add next items to `BaseSettings`
```
STATIC_APPS = [
    'basement',
    'jquery',
    'bootstrap',
    'fa',
    'qtip2',
    'autocomplete',
    'fancybox',
    'pgwslideshow',
    'cookie',
]

@property
def STYLESHEETS(self):
    return super().STYLESHEETS + (
        'css/indents.css',
        'css/header.css',
        'css/footer.css',
        'css/common.css',
    )

@property
def JAVASCRIPT(self):
    return super().JAVASCRIPT + (
        'js/search.js',
    )
```
