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

### LABEL (v)
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

### VERTEX_PROPERTIES (v)
Retrieves the vertex properties (i.e. the vertex body) associated with the vertex.

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (v)
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
    MATCH   (v)
    SELECT  VALUE VERTEX_DETAIL(v)
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
Retrieves the primary key value(s) associated with the _vertex_.
The usage of "primary key" here refers to the primary key defined on the vertex itself, not the underlying dataset (if any).

Input
: A vertex variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (v)
    SELECT  VALUE VERTEX_KEY(v)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "user_id": 1 }
    ```

* * *

## Edge Functions

### LABEL (e)
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

### EDGE_PROPERTIES (e)
Retrieves the edge properties (i.e. the edge body) associated with the edge.

Input
: An edge variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   ( )-[e]-( )
    SELECT  VALUE EDGE_PROPERTIES(e)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "review_id": "R1", "business_id": "B3" }
    ```

### EDGE_DETAIL (e)
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
      "_GraphixElementDetail": { "Label": "ABOUT" },
      "_GraphixEdgeDetail": {
        "EdgeDirection": "LEFT_TO_RIGHT",
        "SourceKey": { "review_id": "R1" },
        "DestinationKey": { "business_id": "B3" }
      }
    }
    ```

### EDGE_DIRECTION (e)
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

### EDGE_SOURCE_KEY (e)
Retrieves the foreign key value(s) of an edge's body that is used to reference its _source_ vertex.

Aliases
: `SOURCE_KEY (e)`

Input
: An edge variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (:Review)-[e:ABOUT]->(:Business)
    SELECT  VALUE EDGE_SOURCE_KEY(e)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "review_id": "R1" }
    ```

### EDGE_DEST_KEY (e)
Retrieves the foreign key value(s) of an edge's body that is used to reference its _destination_ vertex.

Aliases
: `EDGE_DESTINATION_KEY (e)`, `DEST_KEY (e)`, `DESTINATION_KEY (e)`

Input
: An edge variable.

Output
: An `object` value.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (:Review)-[e:ABOUT]->(:Business)
    SELECT  VALUE EDGE_DEST_KEY(e)
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "business_id": "B3" }
    ```

### EDGE_IF_LEFT_TO_RIGHT (e, x1, x2)
Conditions on the edge direction of `e` and returns `x1` if `e` is directed from left to right, and `x2` if `e` is directed from right to left.
Users can leverage this function to retrieve the source vertex of an edge, as shown in the example.

Aliases
: `LEFT_TO_RIGHT_IF (e, x1, x2)`

Input
: An edge variable `e`, and two expressions `x1` and `x2`.

Output
: The inputs `x1` or `x2`.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (x1)-[e]-(x2)
    LET     sourceVertex = EDGE_LEFT_TO_RIGHT_IF(e, x1, x2)
    SELECT  DISTINCT VALUE LABEL(sourceVertex) AS sourceVertex;
    ```
    Returns the following:
    ```json
    { "sourceVertex": "Review" }
    { "sourceVertex": "User" }
    ```

### EDGE_IF_RIGHT_TO_LEFT (e, x1, x2)
Conditions on the edge direction of `e` and returns `x1` if `e` is directed from right to left, and `x2` if `e` is directed from left to right.
Users can leverage this function to retrieve the destination vertex of an edge, as shown in the example.

Aliases
: `RIGHT_TO_LEFT_IF (e, x1, x2)`

Input
: An edge variable `e`, and two expressions `x1` and `x2`.

Output
: The inputs `x1` or `x2`.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (x1)-[e]-(x2)
    LET     destVertex = EDGE_RIGHT_TO_LEFT_IF(e, x1, x2)
    SELECT  DISTINCT VALUE LABEL(destVertex) AS destVertex;
    ```
    Returns the following:
    ```json
    { "destVertex": "Business" }
    { "destVertex": "User" }
    ```

* * *

## Path Functions

_Every function described in this section also applies to sub-paths, or paths that are defined using only the edge pattern production._

### PATH_HOP_COUNT (p)
Retrieves the number of _valid_ hops in a given path.
This function differs from taking the length of a path (i.e. `LEN (p)`) in that pseudo-path records (those that are produced for patterns without edges) do not contribute to this function's total hop count.

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
                       MATCH   ( )-[:{1,2}]-( ) AS p
                       SELECT  DISTINCT VALUE PATH_HOP_COUNT (p) )
    SELECT  count1, count2;
    ```
    Returns the following:
    ```json
    { "count1": [ 0 ], "count2": [ 1, 2 ] }
    ```

### PATH_LABELS (p)
Retrives all unique vertex and edge labels found in a given path.

Aliases
: `LABELS (p)`

Input
: A path variable.

Output
: An ordered list of `string` values.

Example
:   ```
    FROM    GRAPH GelpGraph
    MATCH   (x1)-[e]-(x2) AS p
    SELECT  DISTINCT VALUE PATH_LABELS(p)
    LIMIT   2;
    ```
    Returns the following:
    ```json
    [ "User", "FRIENDS_WITH", "User" ]
    [ "User", "MADE_BY", "Review" ]
    ```

### PATH_VERTICES (p)
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

### PATH_EDGES (p)
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

