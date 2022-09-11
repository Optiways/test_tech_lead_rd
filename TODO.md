Scaling:

- Handle large graphs like paris_map. Computation betweens pairs of odd nodes might be more efficient if we compute all pairs first (cf branch `feat/speedup`), instead of finding shortest paths one by one : the algorithm could use previously computed paths.

Architecture:

- If more algorithms were to come, create a file dedicated to the chinese postman problem, and externalize common functions in an `algorithms` module
- Although stated that the inital code could be modified, I chose to keep it "as is", and extend further on a dedicated module/file. In real world this helps adding features without interfering with existing data/code structure that could have several legacy dependencies. In this case, this was greatly helped with the use of the external library `networkx` : we only need a converter from original `Graph` class to `networkx.Graph`. Once we are ready, we can of course refactor the original code by taking into account the added features.

Deployment/dev:

- use logger instead of print()
- use poetry instead of pip. This helps resolve depencies, keep them up to date, and we can also separate dev dependies (formatter, debugger, linter...) with prod depencies