---
layout: default
title: Language Reference
nav_order: 5
has_children: true
---

# Language Reference

The query language for Graphix (referred to as gSQL++) is intended to be a superset of AsterixDB's query language SQL++.
gSQL++ was designed to "glue" the ASCII art syntax of vertices, edges, and paths in languages like Cypher to SQL++.
In doing so, existing users of not only AsterixDB but SQL as whole would be able to easily reason about gSQL++ queries.

Readers should familiarize themselves with the "Gelp" data model before proceeding.

### Disclaimer

This language reference is **not** intended to describe SQL++, rather it is meant to detail the differences between gSQL++ and SQL++. For a more complete resource on the latter, please see [here](https://asterixdb.apache.org/docs/0.9.7.1/sqlpp/manual.html#Introduction).
