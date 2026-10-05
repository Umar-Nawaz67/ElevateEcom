import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
FIREBASE_SERVICE_ACCOUNT = BASE_DIR / "firebase-service-account.json"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
SECRET_KEY=os.getenv('SECRET_KEY','dev-key'); DEBUG=os.getenv('DEBUG','True')=='True'
ALLOWED_HOSTS = [
    x.strip()
    for x in os.getenv('ALLOWED_HOSTS', '77.237.238.177,localhost,127.0.0.1,.trycloudflare.com').split(',')
    if x.strip()
]
INSTALLED_APPS=[
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles','corsheaders','rest_framework','apps.accounts','apps.services','apps.categories','apps.packages','apps.products','apps.orders','apps.notifications']
MIDDLEWARE=['corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF='config.urls'; WSGI_APPLICATION='config.wsgi.application'; ASGI_APPLICATION='config.asgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('DB_NAME','elevate'),'USER':os.getenv('DB_USER','postgres'),'PASSWORD':os.getenv('DB_PASSWORD','postgres'),'HOST':os.getenv('DB_HOST','127.0.0.1'),'PORT':os.getenv('DB_PORT','5432')}}
AUTH_USER_MODEL='accounts.User'
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework_simplejwt.authentication.JWTAuthentication',),'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',)}
SIMPLE_JWT={
    'ACCESS_TOKEN_LIFETIME':timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=30),
    'AUTH_HEADER_TYPES':('Bearer',)
    }
CORS_ALLOW_ALL_ORIGINS=True
LANGUAGE_CODE='en-us'; TIME_ZONE='Asia/Karachi'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; MEDIA_URL='/media/'; MEDIA_ROOT=BASE_DIR/'media'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
GOOGLE_WEB_CLIENT_ID=os.getenv('GOOGLE_WEB_CLIENT_ID',''); FACEBOOK_APP_ID=os.getenv('FACEBOOK_APP_ID',''); FACEBOOK_APP_SECRET=os.getenv('FACEBOOK_APP_SECRET',''); APPLE_CLIENT_ID=os.getenv('APPLE_CLIENT_ID','')
JAZZMIN_SETTINGS = {
    "site_title": "Elevate Admin",
    "site_header": "Elevate Services",
    "site_brand": "ELEVATE",
    "site_logo": None,
    "login_logo": None,

    "welcome_sign": "Welcome to Elevate Services",
    "copyright": "Elevate Services",

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,

    # Search
    "search_model": [
        "accounts.User",
        "services.Service",
        "categories.Category",
        "packages.Package",
        "products.Product",
        "orders.Order",
    ],

    # Sidebar ordering
    "order_with_respect_to": [
        "orders",
        "services",
        "categories",
        "packages",
        "products",
        "accounts",
        "notifications",
        "auth",
    ],

    # Icons
    "icons": {
        "orders": "fas fa-shopping-cart",
        "orders.order": "fas fa-clipboard-list",

        "services": "fas fa-tools",
        "services.service": "fas fa-tools",

        "categories": "fas fa-layer-group",
        "categories.category": "fas fa-th-large",

        "packages": "fas fa-box-open",
        "packages.package": "fas fa-box",

        "products": "fas fa-cube",
        "products.product": "fas fa-cube",
        "products.ingredient": "fas fa-carrot",

        "accounts": "fas fa-users",
        "accounts.user": "fas fa-user",
        "accounts.socialaccount": "fas fa-link",

        "notifications": "fas fa-bell",
        "notifications.notification": "fas fa-bell",

        "auth": "fas fa-lock",
        "auth.group": "fas fa-users-cog",
    },

    # Top navigation
    "topmenu_links": [
        {
            "name": "Orders",
            "url": "/admin/orders/order/",
            "permissions": ["auth.view_user"],
        },
        {
            "name": "Services",
            "url": "/admin/services/service/",
            "permissions": ["auth.view_user"],
        },
    ],

    # User menu
    "usermenu_links": [
        {
            "name": "View Orders",
            "url": "/admin/orders/order/",
        },
    ],

    "related_modal_active": True,

    # UI behavior
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
}
JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "dark_mode_theme": "darkly",

    # Elevate green branding
    "accent": "accent-success",

    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-dark-success",

    "no_navbar_border": False,

    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,

    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    "button_classes": {
        "primary": "btn-success",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
    },
}

# gr-l6)$i6xq-c3n%rn$$ie9g7#3vjpsd#lg^-=e1bmct+w!z39
from corsheaders.defaults import default_headers

CORS_ALLOWED_ORIGINS = [
    "http://localhost:57099",
    "http://localhost:3000",
    "https://nutrinestmobileapplication.vercel.app",
]

CORS_ALLOW_HEADERS = [
    *default_headers,
    "authorization-primary",
]