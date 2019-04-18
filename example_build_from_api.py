
from graph_import.subid2neo import subid2neo


# subid = '5c054a529460a300074f5007' # EMTAB5061 3514 bundles, too large for ingest at the moment
# subid = '5bf53a6a9460a300074dc824'  # Neuron diff 1733 bundles, too large for ingest at the moment
# subid = '5bdc209b9460a300074b7e67'  # Pancreas6D 2544 bundles, too large for ingest at the moment
# subid = '5c48410e1603f500078b4c3a' # Fetal maternal 7628 bundles, too large for ingest at the moment
# subid = '5c06ccdc9460a300074fc2a7' # 10x mosue brain 5459 bundles , too large for ingest at the moment
# subid = '5c51805d5fc0000007998f72' # TM 99,840 bundles , too large for ingest at the moment
# subid = '5be1bede9460a300074d1fe2' # mouse melanoma 6639 bundles , too large for ingest at the moment
# subid = '5bfe4d3a9460a300074eebc8' # Ido MARS seq 25 bundles, too large for ingest at the moment
# subid = '5bffae409460a300074f3815' # Regev 254, too large for ingest at the moment



# subid = '5c8acacd53367400073122db' # Meyer 7 bundles, works
# subid = '5c06c6ad9460a300074fc27f' # Humphreys 7 bundles, works
# subid = '5c2dfb101603f500078b28de' # Treutlein 6 bundles, works
# subid = '5c06cf339460a30007501909' # Peer 14 bundles
# subid = '5c06a9cf9460a300074fc183' # Basu 22 bundles, quicker with 25 threads, 30 breaks ingest
# subid = '5c06c34f9460a300074fc246' # Rsatija 3 bundles


# load_list = ['5c8acacd53367400073122db', '5c06c6ad9460a300074fc27f', '5c2dfb101603f500078b28de', '5c06cf339460a30007501909', '5c06a9cf9460a300074fc183', '5c06c34f9460a300074fc246'] # use 5 threads only!
load_list = ['5c8acacd53367400073122db', '5c06c6ad9460a300074fc27f', '5c2dfb101603f500078b28de']

# wipe graph then load all projects in the list
for idx, subid in enumerate(load_list):
    print('Starting {}'.format(subid))
    if idx == 0:
        subid2neo(subid, fresh_start=True, threads=5)
    else:
        subid2neo(subid, fresh_start=False, threads=5)
    print('Done {}'.format(subid))

