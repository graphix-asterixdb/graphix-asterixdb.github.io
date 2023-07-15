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
By default, navigation is evaluated with the `no-repeated-anything` setting, which does not allow duplicate vertices OR edges to be traversed.
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
    MATCH     (:User)-[p+]->(:User)
    SELECT    ( FROM   VERTICES(p) v
                SELECT VALUE v.user_id ) AS user_ids,
              EDGES(p) AS edges
    LIMIT     1;
    ```
    Returns the following:
    ```json
    { "user_ids": [ 1, 2, 3, 2 ],
      "edges": [ { "user_id": 1, "friend": 2 },
                 { "user_id": 2, "friend": 3 },
                 { "user_id": 3, "friend": 2 } ] }
    ```
    Notice how the vertex with ID = `2` appears twice in our path.
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

### `INDEXNL`

By default, Graphix chooses to evaluate all JOINs using a hybrid hash JOIN (HHJ).
For analytical queries with many high-degree vertices, such a JOIN operator makes sense.
For more interactive queries however (queries that access a small portion of the graph), the cost of scanning an entire dataset to build a hash table might be too prohibitive.
If there are indexes built on the JOIN field, an alternative JOIN method offered by Graphix is the index nested loop JOIN (INLJ).
Graphix users can enable this JOIN algorithm by inserting the query hint `+indexnl` into the appropriate places of a vertex, edge, or path pattern.

Vertex to Edge 
: To tell Graphix that the `JOIN` used to connect a vertex and an edge should be evaluated with INLJ, insert the `+indexnl` hint immediately before the brackets of an edge (`()-/*+indexnl*/[]-()`) or after the brackets of an edge (`()-[]/*+indexnl*/-()`).

Correlated Vertex
: To tell Graphix that the `JOIN` used to connect a correlated vertex from another `MATCH` clause should be evaluated with INLJ, insert the `+indexnl` immediately before the closing parentheses of the vertex in the nested `MATCH` clause (`(/*+indexnl*/)`).

Path Navigation
: To tell Graphix that the `JOIN` used to evaluate each hop of a path should be evaluated with INLJ, insert the `+indexnl` hint immediately before the closing brackets of a path (`()-[+/*+indexnl*/]-()`).

Example
:   ```
    FROM      GRAPH GelpGraph
    MATCH     (u1:User)-[:FRIENDS_WITH{,5}/*+indexnl*/]->(u2:User),
              (u2)-[:FRIENDS_WITH]/*indexnl*/->(u3:User)
    WHERE     NOT EXISTS ( FROM   GRAPH GelpGraph
                           MATCH  (u3/*+indexnl*/)<-/*+indexnl*/-[:MADE_BY]-(:Review)
                           SELECT 1 )
    SELECT    u1, u2, u3
    LIMIT     1;
    ```
