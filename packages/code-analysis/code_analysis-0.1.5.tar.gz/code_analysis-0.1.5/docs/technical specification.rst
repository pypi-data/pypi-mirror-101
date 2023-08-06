=======================
Technical Specification
=======================


Java call trees
---------------

The tool for the generation of the raw call tree data, `java-callgraph`, writes its output as formatted text. The structure follows this schema:::

    C:<qualified class name> <qualified class name>
    M:<qualified class name>:<method>(<params>) (x)<qualified class name>:<method>(<params>)

`java_call_tree` uses the first character to distinguish classes and methods. The second qualifier, denoted as `x`, is not used. Parameters are also cut off.

An example of the input format can be found in the `resources` folder of this project.

Java dependencies
-----------------

`jdepend.xmlui.JDepend` writes XML. `java_dependencies` uses only the subset related to dependencies. It looks like follows:::

    <JDepend>
        <Packages>
            <Package name = "some name" >
                <DependsUpon>
                    <Package>qualified.package.name</Package>
                    ...
                    <Package>another.package</Package>
                </DependsUpon>
            </Package>
            ...
        </Packages>
    </JDepend>


An example of the input format can be found in the `resources` folder of this project.

Python dependencies
-------------------

Dependencies of Python packages are determined using the `ast` module of the Python standard library. Modules of the analyzed package are parsed into an AST (abstract syntax tree). Then the imports are extracted by walking the tree.
In this case no intermediate file format is required, but the results of the tree walk are directly processed.
 
