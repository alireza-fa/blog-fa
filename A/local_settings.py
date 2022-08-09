SECRET_KEY = 'django-insecure-=41#l**(og*4$z9k3iq0))749#_jz2%#ahw_7#ka_e&i8jyu1)'

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database
DB_NAME = 'blog'
DB_USER = 'blog'
DB_PASS = 'blog'
DB_HOST = 'localhost'
DB_PORT = 5432

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_USE_SSL = True

# S3 AMAZON
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_SERVICE_NAME = 's3'
AWS_S3_ENDPOINT_URL = ''
AWS_S3_FILE_OVERWRITE = False
