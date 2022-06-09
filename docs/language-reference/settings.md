---
layout: default
title: Settings
parent: Language Reference
nav_order: 4
---

# Settings
{: .no_toc }

This page details Graphix-specific compiler settings that can be set on a per-request basis with the `SET` statement.
All settings described in this page are preceeded by `graphix.`.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

* * *

## MATCH-EVALUATION

Modifies what graph elements can be set equal to one another during pattern matching.
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
    SET       `graphix.match-evaluation` "homomorphism";
    
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


## PRINT-REWRITE

Prints and logs the normalized gSQL++ (an _almost_ valid SQL++ query) to the log file right before the query is transformed into a logical plan.
This setting is particularly useful when debugging gSQL++ queries, although future work entails adding this field in the response JSON of an HTTP request and adding proper language support (e.g. `EXPLAIN REWRITE ...`).
By default, this setting is turned off (i.e. set to `"false"`).

Example
:   ```
    SET     `graphix.print-rewrite` "true";
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
      WITH        `GGV_7` = ( `GGV_6` )
      WITH        `u` = ( `GGV_6` )
      WITH        `GGV_1` = ( { "user_id" : `GGV_2`.`user_id`, "friend" : `GGV_5` } )
      WHERE       `GGV_6` != `GGV_2`

      UNION ALL  

      SELECT      `u` AS `u`, `v` AS `v`
      FROM        `Yelp`.`Users` AS `GGV_8`
      WITH        `GGV_9` = ( `GGV_8` )
      WITH        `u` = ( `GGV_8` )
      UNNEST      `GGV_8`.`friends` AS `GGV_11`
      WITH        `GGV_10` = ( { "user_id" : `GGV_8`.`user_id`, "friend" : `GGV_11` } )
      INNER JOIN  `Yelp`.`Users` AS `GGV_12`
      ON          `GGV_10`.`friend` = `GGV_12`.`user_id`
      WITH        `GGV_13` = ( `GGV_12` )
      WITH        `v` = ( `GGV_12` )
      WITH        `GGV_1` = ( { "user_id" : `GGV_8`.`user_id`, "friend" : `GGV_11` } )
      WHERE       `GGV_8` != `GGV_12` ) ;
    ```

