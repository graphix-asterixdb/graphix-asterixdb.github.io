---
layout: default
title: Style Guide 
parent: Language Reference
nav_order: 5 
---

# Style Guide
{: .no_toc }


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Style Guide (Overview)

The goal of this guide is to establish some conventions / recommendations for writing clean and readable gSQL++ queries.
Many of these conventions are borrowed from Neo4J's style guide [here](https://neo4j.com/developer/cypher/style-guide).

### Whitespace

Whitespace not only improves the readability of your query (and your code), but correct whitespace helps visualize the logical sequence of operations taken to produce a result.
We recommend left aligning the input expressions to each clause, to make the operations stand out.

Suppose we write the following query to find the top 10 mobile phone users that write reviews, ordered by the number of mobile phones they have.

```
FROM GRAPH GelpGraph MATCH (u1:User)-[:FRIENDS_WITH]->(u2:User)
UNNEST u1.phoneNumbers phn GROUP BY u2
SELECT u2, COUNT(phn) AS phnCount
ORDER BY u2.user_id LIMIT 10;
```

Now suppose we change the whitespace:

```
FROM      GRAPH GelpGraph
MATCH     (r:Review)-[:MADE_BY]->(u:User)
UNNEST    u.phoneNumbers phn
WHERE     phn.kind = 'MOBILE'
GROUP BY  u
SELECT    u, COUNT(*) AS phnCount
ORDER BY  phnCount DESC 
LIMIT     10;
```

At a glance, we can tell what operations Graphix (and consequently, AsterixDB) needs to take to realize the query above.
We contrast the second query with the first, which hides two significant result changing operations: `GROUP BY` (in the second line) and `LIMIT` (in the fourth line).
Furthermore, we could easily gloss over the fact that we even have a gSQL++ query (as opposed to a SQL++ query) due to the fact that our `MATCH` clause is buried in the top line. 


### Capitalization

Variables are styled in lowerCamelCase, where the first letter of each word (except the first) begins with a capital letter.
```
  personA,
  u1,
  lastName
```

All keywords are styled in uppercase, so as distinguish keywords from user identifiers.
```
  GROUP BY,
  MATCH,
  SELECT
```

### Vertex Definition
Vertex labels are styled in CamelCase, where the first letter of each word begins with a capital letter.
We distinguish CamelCase from lowerCamelCase, the latter of which is reserved for variable names.
```
  (:Person),
  (:LightBrown),
  (:Action)
```

### Edge Definition 
Edge labels are styled in all uppercase, where each word is separated with an underscore.
Using different naming styles for different classes of labels (i.e. vertex vs. edge) visually distinguishes what a vertex is and what an edge is in query.
```
  -[:FRIENDS_WITH]-,
  -[:COLOR_OF]-,
  -[:RELATED_TO]-
```

## Graph Query Elements

### Vertex / Edge Query Pattern
Graphix will resolve missing labels in a vertex or edge pattern, but when possible, a pattern should be as specific as possible.
For example, suppose we want to find users `n` that have writtern a review `m`.
We then (mistakenly) write the following query:

```
FROM    GRAPH GelpGraph
MATCH   (n)-[:MADE_BY]-(m)
SELECT  n.user_id, m.review_id;
```

We run our query, and we notice that we get a correct result-- but also a bunch of `NULL`s.
Internally, Graphix rewrites the query above into the following:

```
FROM    GRAPH GelpGraph
MATCH   (n:User)<-[:MADE_BY]-(m:Review)
SELECT  n.user_id, m.review_id;

UNION ALL

FROM    GRAPH GelpGraph
MATCH   (n:Review)-[:MADE_BY]->(m:User)
SELECT  n.user_id, m.review_id;
```

The first query includes an undirected edge, and we cannot infer the labels of `n` and `m` from our query.
Consequently, Graphix must consider two cases: one where `n` is a `User` and `m` is a `Review`, and one where `n` is a `Review` and `m` is a `User`.
In addition, Graphix cannot assume the existence of the `user_id` and `review_id` vertex properties -- a tradeoff that we have to accept for flexible data modeling in both Graphix and AsterixDB.

Although the second query is what actually occurs, we only want the first branch of the `UNION ALL`.
We could've avoided such a situation by just being specific about our vertex labels and edge direction when initially writing our query:
```
FROM    GRAPH GelpGraph
MATCH   (n:User)<-[:MADE_BY]-(m:Review)
SELECT  n.user_id, m.review_id;
```
