=====
Usage
=====


java_call_tree
--------------

To generate Cypher code first generate a call tree with java-callgraph. Xou can download it from GitHub: 
https://github.com/gousiosg/java-callgraph. Then feed the output of `java-callgraph` into `java_call_tree`:

    java_call_tree <callgraph output> > calltree.cypher

Now you can paste the content of `calltree.cypher` into the Neo4j browser of your database.


java_dependencies
-----------------

First generate a dependency file with JDepend. You can download it from GitHub: https://github.com/clarkware/jdepend.
Then feed the output into `java_dependencies`:

    java_dependencies <jdepend output> > dependency.cypher

Now paste the content of `dependency.cypher` into the Neo4j browser to import your dependencies.


python_dependencies
-------------------

Just point `pyython_dependencies` to the package you want to analyze:

    python_dependencies <some package> > dependencies.cypher


Now paste the content of `dependency.cypher` into the Neo4j browser to import your dependencies.

