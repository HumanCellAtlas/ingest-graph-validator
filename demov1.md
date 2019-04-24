### v1 Demo

1. Outline the problem this tooling solves

1. Loading datasets with the ingest API 
    1. Loading 6/15 datasets (small bundles)
    1. Large load fail (plus thredding for speed). See https://metrics.data.humancellatlas.org/d/8htMNc4mk/ingest-prod?orgId=1
    1. Multiple dataset load
   
    **ingest-graph-validator/example_build_from_api.py**

1. Loading datasets with a spreadsheet

    **ingest-graph-validator/example_build_from_sheet.py**
    
1. Running tests

    1. Tests in ascii docs

    **ingest-graph-validator/example_run_tests.py**

1. Running reports

    **ingest-graph-validator/example_run_reports.py**

1. Adding new tests





## Ingest Crash

```
Traceback (most recent call last):
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connection.py", line 159, in _new_conn
    (self._dns_host, self.port), self.timeout, **extra_kw)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/util/connection.py", line 57, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/socket.py", line 748, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno 8] nodename nor servname provided, or not known
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connectionpool.py", line 600, in urlopen
    chunked=chunked)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connectionpool.py", line 343, in _make_request
    self._validate_conn(conn)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connectionpool.py", line 839, in _validate_conn
    conn.connect()
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connection.py", line 301, in connect
    conn = self._new_conn()
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connection.py", line 168, in _new_conn
    self, "Failed to establish a new connection: %s" % e)
urllib3.exceptions.NewConnectionError: <urllib3.connection.VerifiedHTTPSConnection object at 0x1198cfc88>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/adapters.py", line 449, in send
    timeout=timeout
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connectionpool.py", line 638, in urlopen
    _stacktrace=sys.exc_info()[2])
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/util/retry.py", line 398, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.ingest.data.humancellatlas.org', port=443): Max retries exceeded with url: /processes/5bdc21539460a300074b9c82/derivedBiomaterials (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x1198cfc88>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/IPython/core/interactiveshell.py", line 3291, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-61419c6e6ea4>", line 1, in <module>
    runfile('/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/examples/example_build_from_api.py', wdir='/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/examples')
  File "/Users/hewgreen/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/183.4284.139/PyCharm.app/Contents/helpers/pydev/_pydev_bundle/pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "/Users/hewgreen/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/183.4284.139/PyCharm.app/Contents/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/examples/example_build_from_api.py", line 38, in <module>
    subid2neo('5bdc209b9460a300074b7e67', threads=50)
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/graph_import/subid2neo.py", line 44, in subid2neo
    make_links(processes, threads)
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/graph_import/subid2neo.py", line 109, in make_links
    thread_pool.map(lambda process_node: get_rels(process_node, process_node["uuid"]["uuid"]), processes_list),
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/multiprocessing/pool.py", line 268, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/multiprocessing/pool.py", line 657, in get
    raise self._value
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/multiprocessing/pool.py", line 121, in worker
    result = (True, func(*args, **kwds))
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/multiprocessing/pool.py", line 44, in mapstar
    return list(map(*args))
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/graph_import/subid2neo.py", line 109, in <lambda>
    thread_pool.map(lambda process_node: get_rels(process_node, process_node["uuid"]["uuid"]), processes_list),
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/graph_import/subid2neo.py", line 88, in get_rels
    for link in links:
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/src/hca-ingest/ingest/api/ingestapi.py", line 287, in getRelatedEntities
    for entity in self._getAllObjectsFromSet(entityUri, entityType):
  File "/Users/hewgreen/google_drive_EBI/hca_clones/ingest-graph-validator/src/hca-ingest/ingest/api/ingestapi.py", line 273, in _getAllObjectsFromSet
    r = requests.get(url, headers=self.headers, params=params)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/api.py", line 75, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/api.py", line 60, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/sessions.py", line 533, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/sessions.py", line 646, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.ingest.data.humancellatlas.org', port=443): Max retries exceeded with url: /processes/5bdc21539460a300074b9c82/derivedBiomaterials (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x1198cfc88>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))

```
