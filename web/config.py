import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="mydemoserver.postgres.database.azure.com"
    POSTGRES_USER="bipinsa@mydemoserver"
    POSTGRES_PW="Mydatabase33#"
    POSTGRES_DB="postgres"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://notificationqueue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=akkBF6HVMz7q3XbRyWDFXEQkim1JvHNF4I4wBMJbdYA='
    SERVICE_BUS_QUEUE_NAME ='confqueue'
    ADMIN_EMAIL_ADDRESS: 'mytechstuff.bipin@gmail.com'
    SENDGRID_API_KEY = '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'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False