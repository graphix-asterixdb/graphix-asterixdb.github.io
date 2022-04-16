---
layout: default
title: Functions
parent: Language Reference
nav_order: 3
---

# Functions
{: .no_toc }


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Vertex Functions

### LABEL (v)
Retrieves the label associated with the vertex.

Input
: A vertex variable.

Output
: A `string` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (n)
    SELECT  DISTINCT LABEL(n) AS nLabel;
    ```
    Returns the following:
    ```json
    { "nLabel": "User" }
    { "nLabel": "Review" }
    { "nLabel": "Business" }
    ```

### VERTEX_PROPERTIES (v)
Retrieves the vertex properties (i.e. the vertex body) associated with the vertex.

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (n)
    SELECT  VALUE VERTEX_PROPERTIES(n)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "user_id": 1, "name": "Mary", "friends": [ 4, 5 ] }
    ```

### VERTEX_DETAIL (v)
Retrieves the Graphix-internal information associated with the vertex.
This does not include the properties of the vertex.

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (n)
    SELECT  VALUE VERTEX_DETAIL(n)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    {
      "_GraphixElementDetail": { "Label": "User" },
      "_GraphixVertexDetail": { "PrimaryKey": { "user_id": 1 } }
    }
    ```

### VERTEX_KEY (v)
Retrieves the primary key field(s) associated with the _vertex_.
The usage of "primary key" here refers to the primary key defined on the vertex itself, not the underlying dataset (if any).

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (n)
    SELECT  VALUE VERTEX_KEY(n)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "user_id": 1 }
    ```


## Edge Functions

### LABEL (v)
Retrieves the label associated with the edge.

Input
: An edge variable.

Output
: A `string` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   ( )-[e]-( )
    SELECT  DISTINCT LABEL(e) AS eLabel;
    ```
    Returns the following:
    ```json
    { "eLabel": "FRIENDS_WITH" }
    { "eLabel": "MADE_BY" }
    { "eLabel": "ABOUT" }
    ```

## Path Functions
