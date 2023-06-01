"""
Base settings to build other settings files upon.
"""
import os

import environ
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_mapengine import setup

ROOT_DIR = environ.Path(__file__) - 3  # (egon/config/settings/base.py - 3 = egon/)
APPS_DIR = ROOT_DIR.path("egon")
DATA_DIR = APPS_DIR.path("data")
METADATA_DIR = APPS_DIR.path("metadata")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
)
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
# 'de' is the standard language
LANGUAGE_CODE = "de"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": env.db("DATABASE_URL")}
else:
    POSTGRES_USER = env.str("POSTGRES_USER")
    POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
    POSTGRES_HOST = env.str("POSTGRES_HOST")
    POSTGRES_PORT = env.str("POSTGRES_PORT")
    POSTGRES_DB = env.str("POSTGRES_DB")
    DATABASE_URL = f"postgis://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    os.environ["DATABASE_URL"] = DATABASE_URL
    DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    # "django.contrib.humanize", # Handy template tags
    "django.forms",
    "django.contrib.gis",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_distill",
    "import_export",
]

LOCAL_APPS = ["egon.map.apps.MapConfig", "django_mapengine"]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "egon.contrib.sites.migrations"}

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("data"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "egon.utils.context_processors.settings_context",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Hendrik Huyskens""", "hendrik.huyskens@rl-institut.de")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {"level": "INFO", "handlers": ["console"]},
}


# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# django-libsass
COMPRESS_PRECOMPILERS = [("text/x-scss", "django_libsass.SassCompiler")]

COMPRESS_CACHEABLE_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# django-mapengine
# ------------------------------------------------------------------------------
# https://github.com/rl-institut/django-mapengine

MAP_ENGINE_CENTER_AT_STARTUP = [10.407237624103573, 51.22757621251938]
MAP_ENGINE_ZOOM_AT_STARTUP = 5.546712433728557
MAP_ENGINE_MAX_BOUNDS: [[-2.54, 46.35], [23.93, 55.87]]
MAP_ENGINE_LAYERS_AT_STARTUP = []

MAP_ENGINE_STYLES_FOLDER = "egon/static/styles/"
MAP_ENGINE_MIN_ZOOM = 2

# needs to be empty to disable centration- and moveto-behavior onclick
MAP_ENGINE_ZOOM_LEVELS = {
    # "country": setup.Zoom(2, 7),
    # "state": setup.Zoom(7, 9),
    # "district": setup.Zoom(9, 11),
    # "municipality": setup.Zoom(11, 13),
}

MAP_ENGINE_API_MVTS = {
    "mv_grid_district_data": [
        setup.MVTAPI("mv_grid_district_data", "map", "MVGridDistrictData"),
        setup.MVTAPI("mv_grid_district_data_line", "map", "MVGridDistrictData"),
    ],
    "load_area": [
        setup.MVTAPI("load_area", "map", "LoadArea"),
    ],
    "load_area_line": [
        setup.MVTAPI("load_area_line", "map", "LoadArea"),
    ],
    "h2_voronoi": [
        setup.MVTAPI("h2_voronoi", "map", "H2Voronoi"),
        setup.MVTAPI("h2_voronoi_line", "map", "H2Voronoi"),
    ],
    "ch4_voronoi": [
        setup.MVTAPI("ch4_voronoi", "map", "CH4Voronoi"),
        setup.MVTAPI("ch4_voronoi_line", "map", "CH4Voronoi"),
    ],
    "gas_potential_biogas_production_2035": [
        setup.MVTAPI("gas_potential_biogas_production_2035", "map", "GasPotentialBiogasProduction")
    ],
    "gas_potential_natural_gas_production_2035": [
        setup.MVTAPI("gas_potential_natural_gas_production_2035", "map", "GasPotentialNaturalGasProduction")
    ],
    "gas_methane_for_industry": [setup.MVTAPI("gas_methane_for_industry", "map", "GasCH4Industry")],
    "gas_hydrogen_for_industry": [setup.MVTAPI("gas_hydrogen_for_industry", "map", "GasH2Industry")],
    "demand_transport_heavy_duty_transport_2035": [
        setup.MVTAPI("demand_transport_heavy_duty_transport_2035", "map", "TransportHeavyDuty")
    ],
    "static": [
        setup.MVTAPI("wind_onshore_potential_areas_2035", "map", "WindOnshorePotentialArea"),
        setup.MVTAPI(
            "pv_ground-mounted_potential_areas_agriculture_2035", "map", "PVGroundMountedPotentialAreaAgriculture"
        ),
        setup.MVTAPI(
            "pv_ground-mounted_potential_areas_highways_railroad_2035",
            "map",
            "PVGroundMountedPotentialAreaHighways_Railroads",
        ),
        setup.MVTAPI("ehv_line", "map", "EHVLine"),
        setup.MVTAPI("hv_line", "map", "HVLine"),
        setup.MVTAPI("methan_grid_line_2035", "map", "MethaneGridLine"),
    ],
    "potential_h2_underground_storage_2035": [
        setup.MVTAPI("potential_h2_underground_storage_2035", "map", "PotentialH2UndergroundStorage"),
    ],
    "potential_ch4_store_2035": [
        setup.MVTAPI("potential_ch4_store_2035", "map", "PotentialCH4Stores"),
    ],
    "heat_solarthermal_2035": [
        setup.MVTAPI("heat_solarthermal_2035", "map", "HeatSolarthermal"),
    ],
    "heat_geothermal_2035": [
        setup.MVTAPI("heat_geothermal_2035", "map", "HeatGeothermal"),
    ],
    "central_heatpumps_2035": [
        setup.MVTAPI("central_heatpumps_2035", "map", "CentralHeatPumps"),
    ],
    "heating_households_cts_2035": [
        setup.MVTAPI("heating_households_cts_2035", "map", "HeatingHouseholdsCts"),
    ],
    "country": [
        setup.MVTAPI("country", "map", "Country"),
        setup.MVTAPI("countrylabel", "map", "Country", "label_tiles"),
    ],
    "state": [
        setup.MVTAPI("state", "map", "State"),
        setup.MVTAPI("statelabel", "map", "State", "label_tiles"),
    ],
    "district": [
        setup.MVTAPI("district", "map", "District"),
        setup.MVTAPI("districtlabel", "map", "District", "label_tiles"),
    ],
    "municipality": [
        setup.MVTAPI("municipality", "map", "Municipality"),
        setup.MVTAPI("municipalitylabel", "map", "Municipality", "label_tiles"),
    ],
}

MAP_ENGINE_API_CLUSTERS = [
    setup.ClusterAPI("wind_offshore_wind_parks_2035", "map", "WindOffshoreWindPark"),
    setup.ClusterAPI("wind_onshore_wind_parks_2035", "map", "WindOnshoreWindPark"),
    setup.ClusterAPI("ehv_hv_station", "map", "EHVHVSubstation"),
    setup.ClusterAPI("hv_mv_station", "map", "HVMVSubstation"),
    setup.ClusterAPI("pv_roof-top_pv_plants_2035", "map", "PVRoofTopPVPlant"),
    setup.ClusterAPI("pv_ground-mounted_pv_plants_2035", "map", "PVGroundMountedPVPlant"),
]

MAP_ENGINE_IMAGES = [
    setup.MapImage("solar", "images/icons/solar.png"),
    setup.MapImage("wind", "images/icons/wind.png"),
    setup.MapImage("station", "images/icons/station.png"),
]

MAP_ENGINE_MAPLAYER_MODEL = "MapLayer"
# not needed when using MAPLAYER_MODEL
MAP_ENGINE_CHOROPLETHS = []
MAP_ENGINE_POPUPS = []

# Your stuff...
# ------------------------------------------------------------------------------
PASSWORD_PROTECTION = env.bool("PASSWORD_PROTECTION", False)
PASSWORD = env.str("PASSWORD", default=None)
if PASSWORD_PROTECTION and PASSWORD is None:
    raise ValidationError("Password protection is on, but no password is given")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
