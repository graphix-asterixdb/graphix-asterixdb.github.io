---
layout: default
title: Home
nav_order: 1
permalink: /
---

# What is Graphix?

Graphix is an extension for the Big Data Management System [Apache AsterixDB](https://asterixdb.apache.org) that allows users to issue graph queries on conceptual graphs over existing data managed by AsterixDB itself.
Our motto is "one analyst's document store is another analyst's graph", originating from the thought that developers shouldn't have to choose between two different technologies (i.e. a document database _or_ a graph database).


# Why use Graphix?

Large graphs are ubiquitous in today's big data, highlighting the need to analyze said data in the form of a graph (as opposed to a collection of tuples or documents).
Suppose that you are a developer using AsterixDB, but are interested in viewing your existing data under graph lens.
Let's walk through your options:

> _Option 1: Setup an ETL (extract, transform, load) pipeline to a dedicated graph database._

Not only is setting up an ETL pipeline costly to develop, this option increases the cost (both in hardware and in developer resources) to _own_ your existing data.

> _Option 2: Write your graph queries in SQL++ (AsterixDB's query language)._

While this option avoids incurring an additional cost to own your data, the cost to develop and maintain your _queries_ increases. Additionally, certain queries (e.g. reachability, shortest path) cannot be expressed in native SQL++.

> _Option 3: Install Graphix and write your queries in a Graphix-extended flavor of SQL++._

Graphix is meant to offer the developers the best of both worlds.
You do not have to introduce a new graph database just to write readable, maintainable, and efficient graph queries.
Furthermore, Graphix offers developers a) physical _and_ logical data independence for your graphs, b) built-in parallel execution (via AsterixDB's existing runtime), and c) all the existing features AsterixDB already offers (rich set of builtin data types, numerous indexing options, ingestion with feeds, etc...).  

