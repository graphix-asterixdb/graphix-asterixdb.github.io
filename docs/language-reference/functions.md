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

* * *


## Vertex Functions

### `LABEL (v)`
Retrieves the label associated with the vertex.
The range of this function is the set of vertex labels of the graph that `v` belongs to.

Input
: A vertex variable.

Output
: A `string` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (v)
    SELECT  DISTINCT LABEL(n) AS nLabel;
    ```
    Returns the following:
    ```json
    { "nLabel": "User" }
    { "nLabel": "Review" }
    { "nLabel": "Business" }
    ```

### `VERTEX_DETAIL (v)`
Retrieves the Graphix-internal information associated with the vertex.
This does not include the properties of the vertex.

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (v)
    SELECT  VALUE VERTEX_DETAIL(v)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    {
      "Label": "User",
      "PrimaryKey": { "user_id": 1 }
    }
    ```

* * *

## Edge Functions

### `LABEL (e)`
Retrieves the label associated with the edge.
The range of this function is the set of edge labels of the graph that `e` belongs to.

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

### `EDGE_DETAIL (e)`
Retrieves the Graphix-internal information associated with the edge.
This does not include the properties of the edge.

Input
: An edge variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   ( )-[e]-( )
    SELECT  VALUE EDGE_DETAIL(e)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    {
      "Label": "ABOUT",
      "EdgeDirection": "LEFT_TO_RIGHT",
      "SourceKey": { "review_id": "R1" },
      "DestinationKey": { "business_id": "B3" }
    }
    ```

### `EDGE_DIRECTION (e)`
Retrieves the direction associated with the edge.
The range of this function is the following collection: `["LEFT_TO_RIGHT", "RIGHT_TO_LEFT"]`.

Aliases
: `DIR (e)`, `DIRECTION (e)`

Input
: An edge variable.

Output
: A `string` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (v1:Business|Review)-[e:ABOUT]-(v2:Business|Review)
    SELECT  LABEL(v1) AS v1Label,
            LABEL(v2) AS v2Label,
            EDGE_DIRECTION(e) AS eDirection
    LIMIT   2;
    ```
    Returns the following:
    ```json
    { "v1Label": "Business", "v2Label": "Review", "eDirection": "RIGHT_TO_LEFT" }
    { "v1Label": "Review", "v2Label": "Business", "eDirection": "LEFT_TO_RIGHT" }
    ```

### `EDGE_SOURCE_VERTEX (e)`
Retrieve the source vertex associated with the edge.
This function does **not** work on path variables.

Aliases
: `SOURCE_VERTEX (e)`

Input
: An edge variable.

Output
: A vertex value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (x1)-[e]-(x2)
    SELECT  DISTINCT LABEL(EDGE_SOURCE_VERTEX(e)) AS sourceVertexLabel;
    ```
    Returns the following:
    ```json
    { "sourceVertexLabel": "Review" }
    { "sourceVertexLabel": "User" }
    ```

### `EDGE_DEST_VERTEX (e)`
Retrieve the destination vertex associated with the edge.
This function does **not** work on path variables.

Aliases
: `EDGE_DESTINATION_VERTEX (e)`, `DESTINATION_VERTEX (e)`, `DEST_VERTEX (e)`

Input
: An edge variable.

Output
: A vertex value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (x1)-[e]-(x2)
    SELECT  DISTINCT LABEL(EDGE_DEST_VERTEX(e)) AS destVertexLabel;
    ```
    Returns the following:
    ```json
    { "destVertexLabel": "Review" }
    { "destVertexLabel": "User" }
    ```

* * *

## Path Functions

_Every function described in this section also applies to sub-paths, or paths that are defined using only the EdgePattern production._

### `PATH_HOP_COUNT (p)`
Retrieves the number of edges in a given path.

Aliases
: `HOP_COUNT (p)`, `EDGE_COUNT (p)`

Input
: A path variable.

Output
: A `bigint` value.

Example
:   ```
    LET     count1 = ( FROM    GRAPH GelpGraph
                       MATCH   ( ) AS p
                       SELECT  DISTINCT VALUE PATH_HOP_COUNT (p) ),
            count2 = ( FROM    GRAPH GelpGraph
                       MATCH   ( )-[{1,2}]-( ) AS p
                       SELECT  DISTINCT VALUE PATH_HOP_COUNT (p) )
    SELECT  count1, count2;
    ```
    Returns the following:
    ```json
    { "count1": [ 0 ], "count2": [ 1, 2 ] }
    ```

### `PATH_VERTICES (p)`
Retrieves the vertices found in a given path.

Aliases
: `VERTICES (p)`

Input
: A path variable.

Output
: A list of vertex values.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   ( )-( ) AS p
    UNNEST  PATH_VERTICES(p) AS v
    SELECT  VALUE LABEL(v) AS vertexLabel
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "vertexLabel": "User" }
    ```

### `PATH_EDGES (p)`
Retrieves the edges found in a given path.

Aliases
: `EDGES (p)`

Input
: A path variable.

Output
: A list of edge values.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   ( )-( ) AS p
    UNNEST  PATH_EDGES(p) AS e
    SELECT  VALUE LABEL(e) AS edgeLabel
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "edgeLabel": "FRIENDS_WITH" }
    ```

