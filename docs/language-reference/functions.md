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
                       MATCH   (:User)-[p:{1,2}]->(:User)
                       SELECT  DISTINCT VALUE PATH_HOP_COUNT (p) ),
            count2 = ( FROM    GRAPH GelpGraph
                       MATCH   (:User)-[p+]->(:User)
                       SELECT  DISTINCT VALUE PATH_HOP_COUNT (p) )
    SELECT  count1, count2;
    ```
    Returns the following:
    ```json
    { "count1": [ 1, 2 ], "count2": [ 1, 2, 3 ] }
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
    MATCH   (:User)-[p:{1,2}]->(:User)
    UNNEST  PATH_VERTICES(p) AS v
    SELECT  v.user_id AS user_id
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "user_id": 1 }
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
    MATCH   (:User)-[p:{1,2}]->(:User)
    UNNEST  PATH_EDGES(p) AS e
    SELECT  e.user_id, e.friend
    LIMIT   1;
    ```
    Returns the following:
    ```json
    { "user_id": 1, "friend": 2 }
    ```

