---
layout: default
title: Language Reference
nav_order: 5
has_children: true
---

# Language Reference

The query language for Graphix (referred to as GSQL++) is intended to be a superset of AsterixDB's query language SQL++.
GSQL++ was designed to "glue" the ASCII art syntax of graph patterns in languages like Cypher to SQL++.
In doing so, existing users of not only AsterixDB but SQL as whole would be able to easily reason about GSQL++ queries.

Readers should familarize themselves with the "Gelp" data model before proceeding.

### Disclaimer

This language reference is **not** intended to describe SQL++, rather it is meant to detail the differences between GSQL++ and SQL++. For a more complete resource on the latter, please see [here](https://asterixdb.apache.org/docs/0.9.7.1/sqlpp/manual.html#Introduction).
