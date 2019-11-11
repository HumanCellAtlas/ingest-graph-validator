import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from graph_import.sheet2neo import fillNeoGraph

#fillNeoGraph('examples/example_sheets/dcp_integration_test_metadata_1_SS2_bundle.xlsx', fresh_start=True)
#fillNeoGraph('examples/example_sheets/E-GEOD-81547_HCAformat_final.xlsx', fresh_start=True) # takes 17 min
#fillNeoGraph('examples/example_sheets/mf-Teichmann-spreadsheet-v10.xlsx', fresh_start=True) # took longer than 45 min to run before I stopped it.
fillNeoGraph("examples/example_sheets/Test_small.xlsx", fresh_start=True)
#fillNeoGraph("examples/example_sheets/MouseGastrulation.xlsx", fresh_start=True)
#fillNeoGraph("examples/example_sheets/Tcells.xlsx", fresh_start=True)
#fillNeoGraph("examples/example_sheets/mock.xlsx", fresh_start=True)

