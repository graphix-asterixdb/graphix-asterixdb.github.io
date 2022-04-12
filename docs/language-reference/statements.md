---
layout: default
title: Statements
parent: Language Reference
nav_order: 2
---

# Statements
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta } 

1. TOC
{: toc }

## Statements (Overview)

In addition to queries, GSQL++ needs to support statements for a) managing the definition of graphs, and b) for controlling the context used in query evaluation.

## CREATE Statement

## DROP Statement

## SET Statement

## [IN|UP]SERT Statement

GSQL++ does not directly support the creation of vertices and edges, as each vertex and edge body represents a _view_ of your logical model.

## DELETE Statement

GSQL++ also does not directly support the deletion of vertices and edges.
Users can however use a GSQL++ query to locate documents they want to delete.
Suppose that we want to delete all users that have made reviews for a fake business.
We can accomplish this with the query below:

```sql
DELETE FROM  Users u
WHERE EXISTS (
    FROM    GRAPH GelpGraph
    MATCH   (gu:User)-(:Review)-(gb:Business)
    WHERE   gu = u AND 
            "fake" IN gb.annotations
    SELECT  1
);
```
