import os
from distutils.util import strtobool

from elasticsearch import AsyncElasticsearch

from quepid_es_proxy.exceptions import MissingEnvironmentVariable

_client = None

try:
    es_host = os.environ["ES_HOST"]
    es_port = os.environ["ES_PORT"]
    es_use_ssl = os.environ["ES_USE_SSL"]
    es_username = os.environ["PROXY_USERNAME"]
    es_password = os.environ["PROXY_PASSWORD"]
except KeyError as err:
    raise MissingEnvironmentVariable(f"Environment variable {err} is not set.")


async def get_connection() -> AsyncElasticsearch:
    """
    Returns a connection to the Elasticsearch.
    The connection is cached and reused. It is not
    creating a new connection every time.
    Required environment variables to create a connection:
        - ES_HOST
        - ES_PORT
        - ES_USE_SSL
    Optional parameters are ES_USERNAME and ES_PASSWORD which will add an http auth to the connection
    constructor
    """
    global _client
    if _client:
        return _client
    if es_username:
        client = AsyncElasticsearch(
            hosts=[es_host],
            port=int(es_port),
            use_ssl=bool(strtobool(es_use_ssl)),
            http_auth=(es_username, es_password),
            verify_certs=True,
            http_compress=True,
            max_retries=5,
            retry_on_timeout=True,
        )
    else:
        client = AsyncElasticsearch(
            hosts=[es_host],
            port=int(es_port),
            use_ssl=bool(strtobool(es_use_ssl)),
            verify_certs=True,
            http_compress=True,
            max_retries=5,
            retry_on_timeout=True,
        )
    _client = client
    return client
