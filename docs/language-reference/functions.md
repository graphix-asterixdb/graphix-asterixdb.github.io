---
layout: default
title: Functions
parent: Extension Reference
nav_order: 3
---

# Functions
{: .no_toc }


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }


## Functions (Overview)

All graph elements (vertices, edges, and paths) in gSQL++ are logically represented as documents in AsterixDB.
Consequently, Graphix doesn't require users to learn about any _new_ functions.
For ease of use, however, Graphix provides two helper functions: `PATH_VERTICES(p)` and `PATH_EDGES(p)`.

### `PATH_VERTICES (p)`
Retrieve the vertices found in a given path.

Aliases
: `VERTICES (p)`

Input
: A path variable.

Output
: A list of vertex values.

Example
:   ```
    FROM    
        GRAPH GelpGraph
            (:User)-[p:{1,2}]->(:User),
        PATH_VERTICES(p) AS v
    SELECT  
        v.user_id AS user_id
    LIMIT   
        1;
    ```
    Returns the following:
    ```json
    { "user_id": 1 }
    ```

### `PATH_EDGES (p)`
Retrieve the edges found in a given path.

Aliases
: `EDGES (p)`

Input
: A path variable.

Output
: A list of edge values.

Example
:   ```
    FROM    
        GRAPH GelpGraph
            (:User)-[p:{1,2}]->(:User),
        PATH_EDGES(p) AS e
    SELECT  
        e.user_id, 
        e.friend
    LIMIT   
        1;
    ```
    Returns the following:
    ```json
    { "user_id": 1, "friend": 2 }
    ```
