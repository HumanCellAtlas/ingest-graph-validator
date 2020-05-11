---
name: Test addition
about: Use this template to request new tests.
title: [DATE]: <TEST_REQUEST_SHORTNAME>
labels: test request
---
**Describe the issue**

<!--Describe the issue in a short paragraph. e.g. 
"As a data wrangler, I would like to test the integrity of the dataset I'm wrangling by ensuring linked biomaterials always share the same species in the metadata"-->


**Test template**

<!--Please fill in as much as possible:-->

- Test name: <!--Short, descriptive name for the test-->
- Test Description: <!--Short paragraph describing the test-->
- Cypher query:
```
<Fill in a Cypher query or suggest a human-readable test>
```


** Acceptance criteria**

- [ ] The test has been reviewed
- [ ] The test has been implemented into the `graph_test_set` folder
