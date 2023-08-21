---
layout: default
title: Query Tuning 
parent: Extension Reference
nav_order: 4
---

# Query Tuning
{: .no_toc }

This page details Graphix-specific compiler settings and hints that can be set on a per-request basis OR globally in the configuration file.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Compiler Settings

### `semantics.pattern` Setting

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
    SET `graphix.semantics.pattern` "homomorphism";
    
    FROM      
        GRAPH GelpGraph
            (m:User)-(:Review)-(n:User)
    SELECT    
        m.user_id AS m_user_id,
        n.user_id AS n_user_id
    ORDER BY  
        m_user_id, 
        n_user_id
    LIMIT     
        1;
    ```
    Returns the following:
    ```json
    { "m_user_id": 1, "n_user_id": 1 }
    ```
    The result above would not have shown up without our `SET` statement.


### `semantics.navigation` Setting

Modifies what graph elements can be equal to one another during _navigation_.
We distinguish between the semantics of pattern matching, which applies to all explicitly specified vertices and edges, and the semantics of navigation, which only applies to vertices and edges traversed through a path.
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
    SET `graphix.semantics.navigation` "no-repeated-edges";
    FROM      
        GRAPH GelpGraph
            (:User)-[p+]->(:User)
    LET
        user_ids = ( FROM VERTICES(p) v SELECT VALUE v.user_id )
    SELECT    
        user_ids AS user_ids,
        EDGES(p) AS edges
    LIMIT     
        1;
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

### `evaluation.minimize-joins` Setting

In both Graphix and AsterixDB, referential integrity is not maintained (i.e. foreign keys cannot be enforced).
As an example, consider the following `Gelp` graph instance:
```
CREATE TYPE UsersType AS { user_id: bigint, friend: bigint };
CREATE DATASET Users (UsersType) PRIMARY KEY user_id;
CREATE GRAPH UsersGraph AS 
    VERTEX (:User)
        PRIMARY KEY (user_id)
        AS Users,
    EDGE (:User)-[:FRIENDS_WITH]->(:User)
        SOURCE KEY      (user_id)
        DESTINATION KEY (friend)
        AS ( 
            FROM    
                Gelp.Users U,
                U.friends F
            SELECT  
                F         AS friend,
                U.user_id AS user_id
        )

INSERT INTO Users [
    { "user_id": 1, "friends": [ 2 ] },
    { "user_id": 2, "friends": [ 3 ] }
];
```
Notice how the last friend in the `Users` dataset (`"friends": [ 3 ]`) does not exist.
Now let's take a look at a simple query on our graph to find the user IDs of all friends:
```
FROM 
    GRAPH UsersGraph
        (u1:User)-[fw:FRIENDS_WITH]->(u2:User)
SELECT
    u1.user_id AS u1_user_id,
    u2.user_id AS u2_user_id;
```

The query above translates into the pure SQL++ query below:
```
FROM
    Users u1,
    u1.friends u1f,
    Users u2,
LET
    fw = {
        "user_id": u1.user_id,
        "friend": u1f
    }
WHERE
    u1.user_id = fw.user_id AND
    fw.friend = u2.user_id
SELECT
    u1.user_id AS u1_user_id,
    u2.user_id AS u2_user_id
```
which would yield the single result below (because user 3 does not exist):
```json
{ "u1_user_id": 1, "u2_user_id": 2 }
```

Now suppose we make a slight change to the query to remove the `fw.friend = u2.user_id` JOIN:
```
FROM
    Users u1,
    u1.friends u1f
LET
    fw = {
        "user_id": u1.user_id,
        "friend": u1f
    }
SELECT
    u1.user_id AS u1_user_id,
    fw.friend  AS u2_user_id
```
If we were to execute this query, we would get the following _incorrect_ results:
```json
{ "u1_user_id": 1, "u2_user_id": 2 }
{ "u1_user_id": 2, "u2_user_id": 3 }
```
_However_, if your data is devoid of these edge cases, this JOIN pruning rewrite might greatly improve your query performance.
By default, Graphix will perform a minimum of two JOINs (one to connect the source vertex and one to connect the destination vertex) per edge -- but if you are confident that your data has valid references, then toggle this JOIN pruning rewrite with the `graphix.evaluation.minimize-joins` setting:
```
SET `graphix.evaluation.minimize-joins` "true";
```

### `evaluation.prefer-indexnl` Setting

For users with a very interactive workload (i.e. one that accesses a small portion of the overall graph), a pure index nested-loop JOIN approach toward evaluating your query may be preferable.
This setting will annotate all Graphix induced JOINs with the index nested-loop JOIN hint (see the section on [Query Hints](#query-hints) for more detail).
By default, this setting is disabled (set to `"false"`).
```
SET `graphix.evaluation.prefer-indexnl` "true";
```

### `compiler.lukmemory` Setting

To avoid enumerating all paths, Graphix is able to recognize when a user specifies a query that only requires to know about the existence of some path.
An example of such a query is given below:
```
FROM
    GRAPH GelpGraph
        (u1:User)-[:FRIENDS_WITH*]->(u2:User)
SELECT DISTINCT
    u1.user_id AS u1_user_id,
    u2.user_id AS u2_user_id;
```
The `SELECT DISTINCT` allows Graphix to make an optimization to "stop early" when any path between `u1` and `u2` is found.
After recognition (during compilation), Graphix inserts a hash-partitioned `DISTINCT` operator on the vertex endpoints of the path into the recursive portion of a query plan.
This hash-partitioned `DISTINCT` operator has a memory budget to remember the vertex endpoints the operator has seen.
Similar to an LSM tree, once this budget is exceeded, this `DISTINCT` operator flushes its in-memory data structure to disk and proceeds to a) populate a new in-memory data structure for writes, and b) searches the flushed data structure (and its current in-memory data structure) for reads.
This setting modifies the default memory budget, which might be helpful in minimizing the amount of disk I/O during query processing.
```
SET `graphix.compiler.lukmemory` "192KB";
```

## Query Hints

By default, Graphix uses AsterixDB's CBO (cost-based-optimizer) to determine 1) which order to perform JOINs in, and 2) which algorithm to use for each JOIN.
For more fine-grained control over the JOIN algorithm used for each pattern, users can specify JOIN hints.

### `+hashjoin` Hint

When AsterixDB's CBO is disabled, JOINs are evaluated using a hybrid hash JOIN algorithm by default.
This algorithm involves:
1. Consuming all build-side tuples of a JOIN (by default, the right side) to build an in-memory hash table, and spilling tuples that can't fit into the hash table to a set of partitioned files on disk.
2. Consuming all probe-side tuples of a JOIN (by default, the left side) and either forwarding probe-build tuple pairs that satisfy the JOIN condition or spilling the candidate probe tuples to another set of partitioned files on disk.
3. Recursively JOINing the spilled build and probe tuples until all work is exhausted.

_While this hint is available for use with JOINs generated by gSQL++, the current hint grammar does not allow users to describe non-trivial JOINs._
_To enable hybrid hash JOINs, the recommended approach is to simply disable CBO._

### `+hash-bcast` Hint

While hybrid hash JOIN is a great "default" algorithm for big data with high-cardinality JOINs, it assumes that both the probe and build side of the JOIN do not fit into memory.
If all build-side tuples (by default, the right side) can fit into memory, then users could choose a potentially faster JOIN algorithm that broadcasts the build side to all partitions instead of distributing the work based on the JOIN key.
This algorithm is known as broadcast hash JOIN.
Graphix users can enable this JOIN algorithm by inserting the query hint `+hash-bcast` into the appropriate places of a vertex, edge, or path pattern.

Vertex to Edge 
: To tell Graphix that the `JOIN` used to connect a vertex and an edge should be evaluated with broadcast hash JOIN, insert the `+hash-bcast` hint immediately before the brackets of an edge (`()-/*+hash-bcast*/[]-()`) or after the brackets of an edge (`()-[]/*+hash-bcast*/-()`).

Correlated Vertex
: To tell Graphix that the `JOIN` used to connect a correlated vertex from another `MATCH` clause should be evaluated with broadcast hash JOIN, insert the `+hash-bcast` immediately before the closing parentheses of the vertex in the nested `MATCH` clause (`(/*+hash-bcast*/)`).

Example
:   ```
    FROM      
        GRAPH GelpGraph
            (u1)-[:FRIENDS_WITH]/*+hash-bcast*/->(u2:User)
    WHERE     
        NOT EXISTS ( 
            FROM   
                GRAPH GelpGraph
                    (u2/*+hash-bcast*/)<-/*+hash-bcast*/-[:MADE_BY]-(:Review)
            SELECT 
                1 
        )
    SELECT    
        u1, 
        u2
    LIMIT     
        1;
    ```

### `+indexnl` Hint

For analytical queries with many high-degree vertices, using a hash JOIN algorithm makes sense.
For more interactive queries however (i.e. queries that access a small portion of the graph), the cost of scanning an entire dataset to build a hash table might be too prohibitive.
If there are indexes built on the JOIN field (either primary indexes or secondary indexes), an alternative JOIN method offered by Graphix is the index nested loop JOIN (INLJ).
Graphix users can enable this JOIN algorithm by inserting the query hint `+indexnl` into the appropriate places of a vertex, edge, or path pattern.

Vertex to Edge 
: To tell Graphix that the `JOIN` used to connect a vertex and an edge should be evaluated with INLJ, insert the `+indexnl` hint immediately before the brackets of an edge (`()-/*+indexnl*/[]-()`) or after the brackets of an edge (`()-[]/*+indexnl*/-()`).

Correlated Vertex
: To tell Graphix that the `JOIN` used to connect a correlated vertex from another `MATCH` clause should be evaluated with INLJ, insert the `+indexnl` immediately before the closing parentheses of the vertex in the nested `MATCH` clause (`(/*+indexnl*/)`).

Path Navigation
: To tell Graphix that the `JOIN` used to evaluate each hop of a path should be evaluated with INLJ, insert the `+indexnl` hint immediately before the closing brackets of a path (`()-[+/*+indexnl*/]-()`).

Example
:   ```
    FROM      
        GRAPH GelpGraph
            (u1:User)-[:FRIENDS_WITH{,5}/*+indexnl*/]->(u2:User),
            (u2)-[:FRIENDS_WITH]/*+indexnl*/->(u3:User)
    WHERE     
        NOT EXISTS ( 
            FROM   
                GRAPH GelpGraph
                    (u3/*+indexnl*/)<-/*+indexnl*/-[:MADE_BY]-(:Review)
            SELECT 
                1 
        )
    SELECT    
        u1, 
        u2, 
        u3
    LIMIT     
        1;
    ```
