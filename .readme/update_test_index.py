# A small script to automatically generate list of tests for the readme file in graph_test_set

# Opens readme file
# Opens and reads each test file
# reads lines
# append relevant lines to readme file
# stops writing when it gets to a cypher query or the actual test.

from datetime import datetime
import glob
import re

if __name__ == '__main__':

    with open("graph_test_set/README.md", "w") as readme:
        readme.write("# Index of tests currently performed by the validator\n\n")
        now = datetime.now()
        now_date = now.date()
        readme.write(f"Last updated: {now_date}\n\n")
        for test in glob.iglob("graph_test_set/*.adoc"):
            with open(test, "r") as test_file:
                for line in test_file.readlines():
                    if re.search("#### The test", line):
                        break
                    elif re.search("^----", line):
                        break
                    elif line == "\n":
                        continue
                    else:
                        if re.search("^## Test: ", line):
                            line = "##" + line[8:]
                        readme.write(line)
                readme.write("\n")
