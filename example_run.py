
from graph_import.subid2neo import subid2neo

# subid = '5c054a529460a300074f5007' # EMTAB5061 3514 bundles
subid = '5c06c6ad9460a300074fc27f' #Humphreys 7 bundles
# subid = '5bf53a6a9460a300074dc824'  # Neuron diff 1733 bundles
# subid = '5bdc209b9460a300074b7e67'  # Pancreas6D 2544 bundles


subid2neo(subid, fresh_start=True, threads=2)




