import logging.config
logging.config.fileConfig('logging.conf')

from github_oauth_gateway import create_app
app = create_app()
app.app_context().push()
