
from graph_import.sheet2neo import fillNeoGraph

# fillNeoGraph('examples/xample_sheets/dcp_integration_test_metadata_1_SS2_bundle.xlsx')
fillNeoGraph('examples/example_sheets/E-GEOD-81547_HCAformat_final.xlsx', fresh_start=True) # takes 17 min
# fillNeoGraph('examples/example_sheets/mf-Teichmann-spreadsheet-v10.xlsx') # took longer than 45 min to run before I stopped it.





