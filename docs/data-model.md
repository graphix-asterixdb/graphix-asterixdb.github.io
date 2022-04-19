---
layout: default
title: Graphix Data Model
nav_order: 4
---

# Graphix Data Model
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Property Graph Model
A _graph_ is a structure composed of sets of _graph elements_ known as _vertices_ and _edges_.
Edges exactly two vertices together.
A _property graph_ has four defining characteristics that differentiate itself from your bog-standard undirected simple graph:
- Each edge is _directed_.
  Consequently, given an edge `e` that connects two vertices, we can talk about the _source vertex_ and the _destination vertex_ of `e`.
- Each graph element is potentially associated with a _label_.
  In the context of the property graph model labels are used to group vertices with other vertices, and edge with other edges.
- Two pairs of vertices may be connected by more than one edge.
- Each graph element possesses a set of key-value pairs, also known as _properties_.

The property graph model (in contrast to other types of graph models) has received a lot of attention this past decade for its flexibility and ability to express other types of graph models by omitting or re-purposing certain characteristics of the property graph model itself.
For example, if your domain requires weights on your vertices or edges, you simply add a weight property to the appropriate graph elements.
If your domain requires undirected graphs, then simply assign an arbitrary direction to your edge and ignore the direction when querying.
Property graphs can even be used to represent RDF graphs by repurposing graph element labels as URIs.

To better explain this section on property graph models and the following section on queries, we want to model a database

<p align="center">
    <img src="../images/GelpDataModel.svg" />
</p>
{: .code-example }

## Queries on Property Graphs

### Pattern Matching

### Regular Path Queries (RPQ)

### Conjunctive Regular Path Queries (CRPQ)

## Graphix Data Model
Having described the property graph model, let us now describe the data model for Graphix.
