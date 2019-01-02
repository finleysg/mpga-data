import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "grappelli.dashboard",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_auth.registration",
    "drfpasswordless",
    "corsheaders",
    "simple_history",
    "storages",
    "imagekit",
    "nested_admin",
    "clubs",
    "communication",
    "core",
    "documents",
    "events",
    "pages",
    "policies",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
)

SITE_ID = 1

ROOT_URLCONF = "mpga.urls"

PASSWORD_RESET_TIMEOUT_DAYS = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]

REST_FRAMEWORK = {
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "clubs.exception_handler.custom_exception_handler",
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "core.serializers.UserDetailSerializer"
}

PASSWORDLESS_AUTH = {
    "PASSWORDLESS_AUTH_TYPES": ["EMAIL", ],
    "PASSWORDLESS_EMAIL_NOREPLY_ADDRESS": "noreply@mpga.net",
    "PASSWORDLESS_REGISTER_NEW_USERS": False
}

CORS_ORIGIN_ALLOW_ALL = True

WSGI_APPLICATION = "mpga.wsgi.application"

GRAPPELLI_ADMIN_TITLE = "MPGA Administration"
GRAPPELLI_ADMIN_URL = "/admin/"
GRAPPELLI_INDEX_DASHBOARD = "dashboard.CustomIndexDashboard"

# LOGIN_URL = "/login/"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_L10N = True

USE_TZ = True

