import os
import environ
import warnings

from django.urls import reverse_lazy


PROJECT_ROOT = environ.Path(__file__) - 3
BACKEND_DIR = environ.Path(__file__) - 2
FRONTEND_DIR = environ.Path(PROJECT_ROOT("frontend"))


# Load env config (.env file or env vars)

DEFAULT_DATABASE_URL = f"sqlite:///{BACKEND_DIR('db.sqlite3')}"

env = environ.Env(
    ENV=(str, os.environ.get("TEMAT_ENV", default="production")),
    DEBUG=(bool, os.environ.get("TEMAT_DEBUG", default=False)),
    SECRET_KEY=(str, os.environ.get("TEMAT_SECRET_KEY")),
    DATABASE_URL=(str, os.environ.get("TEMAT_DATABASE_URL", default=DEFAULT_DATABASE_URL)),
)

environ.Env.read_env()

if env("DATABASE_URL") == DEFAULT_DATABASE_URL:
    warnings.warn("(TEMAT_)DATABASE_URL has not been set. Using default SQLite local database...")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["localhost", "127.0.0.1"]

ADMINS = [("Pablo", "pablolmedorado@gmail.com")]


# Application definition

INSTALLED_APPS = [
    "django_db_prefix",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "webpack_loader",
    "pwa",
    "rest_framework",
    "django_filters",
    "crispy_forms",
    "hijack",
    "hijack.contrib.admin",
    "django_js_reverse",
    "import_export",
    "ordered_model",
    "colorfield",
    "taggit",
    "notifications",
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "events.apps.EventsConfig",
    "work_organization.apps.WorkOrganizationConfig",
    "scrum.apps.ScrumConfig",
    "breakfasts.apps.BreakfastsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "hijack.middleware.HijackUserMiddleware",
]

ROOT_URLCONF = "temat.urls"

TEMPLATES_DIR = BACKEND_DIR("templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WSGI_APPLICATION = "temat.wsgi.application"


# Database

DB_PREFIX = "temat_"

DATABASES = {"default": env.db("DATABASE_URL")}

if env("ENV") == "production":
    DATABASES["default"]["CONN_MAX_AGE"] = 300


# Auth

if env("ENV") == "production":
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL


# Internationalization

LANGUAGE_CODE = "es"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

STATIC_ROOT = BACKEND_DIR("static")

if env("ENV") == "production":
    STATICFILES_DIRS = (FRONTEND_DIR("dist"),)
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

    def set_static_cache_header(headers, path, url):
        headers["Cache-Control"] = "max-age=31536000"

    WHITENOISE_ADD_HEADERS_FUNCTION = set_static_cache_header


# Django Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "common.api.pagination.Pagination",
}


# Django JS Reverse

JS_REVERSE_EXCLUDE_NAMESPACES = ["admin", "djdt", "rest_framework", "hijack"]

JS_REVERSE_OUTPUT_PATH = FRONTEND_DIR("src", "plugins")

JS_REVERSE_JS_GLOBAL_OBJECT_NAME = "window"


# Webpack Loader

WEBPACK_STATS_FILE = f"webpack-stats-{env('ENV')}.json"

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": env("ENV") == "development",
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": FRONTEND_DIR("config", WEBPACK_STATS_FILE),
    }
}


# Pwa

PWA_APP_NAME = "TeMaT"
PWA_APP_DESCRIPTION = "Team Management Tool"
PWA_APP_THEME_COLOR = "#00205b"
PWA_APP_BACKGROUND_COLOR = "#00205b"
PWA_APP_ICONS = [
    {"src": "/static/img/icons/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/static/img/icons/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
]
PWA_APP_ICONS_APPLE = [{"src": "/static/img/icons/apple_icon.png", "sizes": "180x180"}]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/img/icons/splash-640x1136.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "es-ES"
PWA_SERVICE_WORKER_PATH = BACKEND_DIR("common", "static", "js", "service-worker.js")
PWA_APP_DEBUG_MODE = False


# Django Taggit

TAGGIT_CASE_INSENSITIVE = True


# Debug

if env("ENV") == "development":
    DEBUG = True

    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware", "common.middleware.QueryPrintingMiddleware"]

    # Debug Toolbar
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar, "SHOW_COLLAPSED": True}

    # Django Rest Framework
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += ["rest_framework.renderers.BrowsableAPIRenderer"]  # type: ignore

    # Django Extensions
    RUNSERVERPLUS_SERVER_ADDRESS_PORT = "0.0.0.0:8000"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
        "loggers": {"werkzeug": {"handlers": ["console"], "level": "DEBUG", "propagate": True}},
    }

    # Pwa
    PWA_APP_DEBUG_MODE = True
