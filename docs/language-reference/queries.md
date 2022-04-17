---
layout: default
title: Queries
parent: Language Reference
nav_order: 1
---

# Queries
{: .no_toc }


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }


## Queries (Overview)

A _query_ can either be an expression (whose composition remains unchanged from SQL++), or a construction of _query blocks_.
A _query block_ may contain several clauses, including `SELECT`, `FROM`, `LET`, `WHERE`, `GROUP BY`, and `HAVING`.
The following productions are also unchanged from SQL++.

* * * 

Query
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/Query.svg" />
</p>
{: .code-example }
<br>

Selection
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/Selection.svg" />
</p>
{: .code-example }
<br>

Query Block
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/QueryBlock.svg" />
</p>
{: .code-example }
<br>

Stream Generator
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/StreamGenerator.svg" />
</p>
{: .code-example }

* * * 

Similar to SQL++ (but unlike SQL), gSQL++ allows the `SELECT` clause to appear either at the beginning or the end of a query black.
For some queries, placing the `SELECT` clause at the end may make a query block easier to understand because the `SELECT` clause refers to variables defined in the _stream generator_ production.


## FROM Clause

The purpose of a `FROM` clause is to iterate over a collection.
An additional function of the `FROM` clause in gSQL++ is to introduce an iteration over collections of graph elements (vertices, edges, and paths) involved in mapping a graph query pattern (the `MATCH` clause) to a graph schema (an unmanaged `GraphConstructor` or a managed graph identified by its `QualifiedName`).

* * *

Qualified Name
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/QualifiedName.svg" />
</p>
{: .code-example }
<br>

FROM Clause
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/FromClause.svg" />
</p>
{: .code-example }
<br>

Named Expression
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/NamedExpr.svg" />
</p>
{: .code-example }
<br>

FROM Term
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/FromTerm.svg" />
</p>
{: .code-example }
<br>

JOIN Step
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/JoinStep.svg" />
</p>
{: .code-example }
<br>

UNNEST Step
{: .text-gamma .fw-500 .lh-0 }
<p align="center">
    <img src="../../images/UnnestStep.svg" />
</p>
{: .code-example }

* * *

Below is a query that illustrates the usage of gSQL++'s extended `FROM` clause to iterate over mappings of a single-edge pattern to our managed graph `GelpGraph`.
```
FROM    GRAPH GelpGraph
MATCH   (u1:User)-[:FRIENDS_WITH]->(u2:User)
SELECT  u1, u2;
```


## MATCH Clause


## LET Clause


## WHERE Clause


## GROUP BY Clause


## HAVING Clause


## GROUP AS Clause

