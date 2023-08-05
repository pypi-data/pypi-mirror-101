"""App Engine config. dev_appserver vs prod, logging, Google API clients, etc."""
import os

from .appengine_info import APP_ID, DEBUG

# Use lxml for BeautifulSoup explicitly.
from . import util
util.beautifulsoup_parser = 'lxml'

# # Suppress warnings
# import warnings
# warnings.filterwarnings('ignore', module='bs4',
#                         message='No parser was explicitly specified')
# if DEBUG:
#   warnings.filterwarnings('ignore', module='google.auth',
#     message='Your application has authenticated using end user credentials')

# make oauthlib let us use non-SSL http://localhost in dev_appserver etc
# https://oauthlib.readthedocs.io/en/latest/oauth2/security.html#envvar-OAUTHLIB_INSECURE_TRANSPORT
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

#
# Google API clients
#
if DEBUG:
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.path.dirname(__file__), 'fake_user_account.json')
  os.environ.setdefault('CLOUDSDK_CORE_PROJECT', 'app')
  os.environ.setdefault('DATASTORE_DATASET', 'app')
  os.environ.setdefault('GOOGLE_CLOUD_PROJECT', 'app')
  # work around that these APIs don't natively support dev_appserver.py
  # https://github.com/googleapis/python-ndb/issues/238
  # https://github.com/googleapis/python-ndb/issues/376#issuecomment-604991109
  os.environ.setdefault('DATASTORE_EMULATOR_HOST', 'localhost:8089')

# NDB (Cloud Datastore)
try:
  # TODO: make thread local?
  # https://googleapis.dev/python/python-ndb/latest/migrating.html#setting-up-a-connection
  from google.cloud import ndb
  ndb_client = ndb.Client()
except ImportError:
  pass

# Google Cloud Tasks
try:
  from google.cloud import tasks_v2
  tasks_client = tasks_v2.CloudTasksClient()
  if DEBUG:
    tasks_client.host = 'localhost:9999'
    tasks_client.secure = False
except ImportError:
  pass

# Stackdriver Error Reporting
try:
  from google.cloud import error_reporting
  error_reporting_client = error_reporting.Client()
  if DEBUG:
    error_reporting_client.host = 'localhost:9999'
    error_reporting_client.secure = False
except ImportError:
  pass

# Stackdriver Logging
import logging
# needed for visible logging in dev_appserver
logging.getLogger().setLevel(logging.DEBUG)

try:
  import google.cloud.logging
  logging_client = google.cloud.logging.Client()

  if not DEBUG:
    from google.cloud.logging.handlers import AppEngineHandler, setup_logging

    class Webapp2TraceHandler(AppEngineHandler):
      """Log handler that adds trace id based on webapp2 request header.

      https://github.com/googleapis/python-logging/issues/110#issuecomment-745534629
      https://github.com/googleapis/python-logging/issues/149#issuecomment-782693201

      Also note that AppEngineHandler is evidently deprecated, so I may need to
      port that whole class into webutil eventually. :(
      https://github.com/googleapis/python-logging/issues/202
      """
      def emit(self, record):
        try:
          import webapp2
          trace = webapp2.get_request().headers.get('X-Cloud-Trace-Context')
          if trace:
            trace_id = trace.split('/', 1)[0]
            record.trace = f'projects/{APP_ID}/traces/{trace_id}'
        except (ImportError, AssertionError):
          pass
        return super().emit(record)

    setup_logging(Webapp2TraceHandler(logging_client, name='stdout'),
                  log_level=logging.DEBUG)
    # this currently occasionally hits the 256KB stackdriver logging limit and
    # crashes in the background service. i've tried batch_size=1 and
    # SyncTransport, but no luck, same thing.
    # https://stackoverflow.com/questions/59398479
except ImportError:
  pass

for logger in ('google.cloud', 'oauthlib', 'requests', 'requests_oauthlib',
               'urllib3'):
  logging.getLogger(logger).setLevel(logging.INFO)
