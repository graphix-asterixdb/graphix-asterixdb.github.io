---
layout: default
title: Query Tuning 
parent: Language Reference
nav_order: 4
---

# Query Tuning
{: .no_toc }

This page details Graphix-specific compiler settings and hints that can be set on a per-request basis.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Compiler Settings

### `GRAPHIX.SEMANTICS.PATTERN`

Modifies what graph elements are allowed to be equal to one another during _pattern matching_.
By default, pattern matching is evaluated with the `"isomorphism"` setting, which does not allow duplicate vertices OR edges.
In contrast to languages like Cypher which enforce pattern matching semantics locally within a `MATCH` clause, in gSQL++ such semantics are enforced across _all_ `MATCH` clauses.

Homomorphism
: Under homomorphism pattern matching semantics, vertices can be equal to other vertices, and edges can be equal to other edges.
    
Vertex-Isomorphism
: Under vertex isomorphism pattern matching semantics, vertices cannot be equal to other vertices, but edges can be equal to other edges.

Edge-Isomorphism
: Under edge isomorphism pattern matching semantics, edges cannot be equal to other edges, but vertices can be equal to other vertices.

Isomorphism
: Under strict isomorphism pattern matching semantics, vertices cannot be equal to other vertices, and edges cannot be equal to other edges.

Example
:   ```
    SET       `graphix.semantics.pattern` "homomorphism";
    
    FROM      GRAPH GelpGraph
    MATCH     (m:User)-(:Review)-(n:User)
    SELECT    m.user_id AS m_user_id,
              n.user_id AS n_user_id
    ORDER BY  m_user_id, n_user_id
    LIMIT     1;
    ```
    Returns the following:
    ```json
    { "m_user_id": 1, "n_user_id": 1 }
    ```
    The result above would not have shown up without our `SET` statement.


### `GRAPHIX.SEMANTICS.NAVIGATION`

Modifies what graph elements can be equal to one another during _navigation_.
We distinguish between the semantics of pattern matching, which applies to all explicitly specified vertices and edges, and the semantics of navigation, which only applies to vertices and edges traversed through a sub-path.
By default, navigation is evaluted with the `no-repeated-anything` setting, which does not allow duplicate vertices OR edges to be traversed.
Some form of uniqueness must be specified for navigation to guarantee that cycles are not processed.

No-Repeated-Vertices
: Under no-repeated-vertices navigation semantics, vertices cannot be traversed more than once, but edges can be traversed multiple times (such a situation may occur if the vertex key is not the primary key of the underlying data).

No-Repeated-Edges
: Under no-repeated-edges navigation semantics, edges cannot be traversed more than once, but vertices can be traversed multiple times.

No-Repeated-Anything
: Under no-repeated-anything navigation semantics, neither vertices nor edges can be traversed more than once.

Example
:   ```
    SET       `graphix.semantics.navigation` "no-repeated-edges";
    
    FROM      GRAPH GelpGraph
    MATCH     (:User)-[p+]-(:User)
    LET       vertexIDs = (
        FROM   PATH_VERTICES(p) pv
        LET    vertexLabel = LABEL(pv)
        SELECT CASE WHEN vertexLabel = "User"
                    THEN pv.user_id
                    WHEN vertexLabel = "Review"
                    THEN pv.review_id
                    WHEN vertexLabel = "Business"
                    THEN pv.business_id
               END AS vertexKey, vertexLabel
              )
    SELECT    VALUE vertexIDs 
    LIMIT     1;
    ```
    Returns the following:
    ```json
    [ { "vertexKey": 1,    "vertexLabel": "User" },
      { "vertexKey": "R1", "vertexLabel": "Review" },
      { "vertexKey": "B3", "vertexLabel": "Business" },
      { "vertexKey": "R4", "vertexLabel": "Review" },
      { "vertexKey": 6,    "vertexLabel": "User" },
      { "vertexKey": "R2", "vertexLabel": "Review" },
      { "vertexKey": "B3", "vertexLabel": "Business" },
      { "vertexKey": "R7", "vertexLabel": "Review" },
      { "vertexKey": 2,    "vertexLabel": "User" } ]
    ```
    Notice how the business `"B3"` appears twice in our list of traversed vertices.
    Such a path would not be returned without our `SET` statement.



### `GRAPHIX.LOG-REWRITE`

Prints and logs the normalized gSQL++ (an _almost_ valid SQL++ query) to the log file right before the query is transformed into a logical plan.
This setting is particularly useful when debugging gSQL++ queries.
By default, this setting is turned off (i.e. set to `"false"`).

Example
:   ```
    SET     `graphix.log-rewrite` "true";
    FROM    GRAPH GelpGraph
    MATCH   (u:User)-(v:User)
    SELECT  u, v;
    ```
    Would display the following (unformatted) string in your cluster controller's console output / log file:
    ```
    ( SELECT      `u` AS `u`, `v` AS `v`
      FROM        `Yelp`.`Users` AS `GGV_2`
      WITH        `GGV_3` = ( `GGV_2` )
      WITH        `v` = ( `GGV_2` )
      UNNEST      `GGV_2`.`friends` AS `GGV_5`
      WITH        `GGV_4` = ( { "user_id" : `GGV_2`.`user_id`, "friend" : `GGV_5` } )
      INNER JOIN  `Yelp`.`Users` AS `GGV_6`
      ON          `GGV_4`.`friend` = `GGV_6`.`user_id`
      WITH        `GGV_6` != `GGV_2`
      WITH        `GGV_7` = ( `GGV_6` )
      WITH        `u` = ( `GGV_6` )
      WITH        `GGV_1` = ( { "user_id" : `GGV_2`.`user_id`, "friend" : `GGV_5` } )

      UNION ALL  

      SELECT      `u` AS `u`, `v` AS `v`
      FROM        `Yelp`.`Users` AS `GGV_8`
      WITH        `GGV_9` = ( `GGV_8` )
      WITH        `u` = ( `GGV_8` )
      UNNEST      `GGV_8`.`friends` AS `GGV_11`
      WITH        `GGV_10` = ( { "user_id" : `GGV_8`.`user_id`, "friend" : `GGV_11` } )
      INNER JOIN  `Yelp`.`Users` AS `GGV_12`
      ON          `GGV_10`.`friend` = `GGV_12`.`user_id`
      WITH        `GGV_8` != `GGV_12`
      WITH        `GGV_13` = ( `GGV_12` )
      WITH        `v` = ( `GGV_12` )
      WITH        `GGV_1` = ( { "user_id" : `GGV_8`.`user_id`, "friend" : `GGV_11` } ) ) ;
    ```

## Query Hints

### `PATH-EXPAND`

If an edge pattern contains a sub-path whose number of hops is _bounded_, then we have two ways we can evaluate our pattern: 
1. Rewrite our sub-path into a `UNION-ALL` of all possible ways our sub-path could be evaluated. 
2. Evaluate our sub-path using a dedicated fixed-point operator.

By default, sub-paths are evaluated using the latter.
To evaluate an edge pattern using the former, add the query hint after all detail in the pattern itself:
```
FROM    GRAPH GelpGraph
MATCH   (u)-[{1,4} /* +path-expand */]-(v)
SELECT  u, v;
```

### `PATH-FIXED-POINT`

By default, sub-paths are evaluated using a dedicated fixed-point operator.
To be explicit in the way your sub-paths are evaluated, you can annotate your sub-path with this hint:
```
FROM    GRAPH GelpGraph
MATCH   (u)-[{1,4} /* +path-fixed-point */]-(v)
SELECT  u, v;
```
