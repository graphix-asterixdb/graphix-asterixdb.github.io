---
layout: default
title: Architecture Overview 
parent: Technical Reference
nav_order: 1
---

# Architecture Overview 
{: .no_toc }

This page aims to give a high level overview of the software architecture that supports Graphix, in the context of AsterixDB, Algebricks (a heuristic query optimizer), and Hyracks (a parallel runtime engine).

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Components of Graphix 

For the purpose of this discussion, we divide Graphix into three parts: 
1. gSQL++ Query Parsing
2. gSQL++ AST Rewriting
3. Algebricks Plan Optimization

With respect to query planning, Graphix / AsterixDB works with queries in four representations:
1. As a string of tokens, which gets lexed and parsed into ...
2. An abstract syntax tree (AST), which undergoes rewrites and gets translated into ...
3. An Algebricks logical plan, which gets optimized under a set of heuristics / rules and get translated into ...
4. A Hyracks job specification, which will be issued to all participating Graphix cluster nodes and executed.

## gSQL++ Query Parsing

AsterixDB uses [JavaCC](https://javacc.github.io/javacc/) to generate a lexer and parser for SQL++.
To extend SQL++ with navigational pattern matching, all Graphix specific language constructs (e.g. the `MATCH` clause) are also specified in JavaCC.
The output of JavaCC for both Graphix and AsterixDB are the same: an abstract syntax tree.

## gSQL++ AST Rewriting

To start, we distinguish AST rewrites from Algebricks optimization passes, as both work with different representations of our query.

In AsterixDB, a SQL++ query immediately after parsing undergoes several rewrites to more easily generate an Algebricks plan.
In Graphix, a gSQL++ query immediately after parsing undergoes several rewrites to "handoff" to the SQL++ set of rewrites and eventually generate an Algebricks plan.
This "handoff" allows Graphix to reuse SQL++ language features that would otherwise have to be implemented ourselves (e.g. `RIGHT JOIN`, `WINDOW BY`), and can be thought of as "partially lowering" gSQL++ to SQL++.
Fun fact: the original version of Graphix stopped at this "handoff" process, acting solely as a SQL++ rewrite layer with write access to AsterixDB's metadata datasets.

For a detailed explanation on the rewrites a Graphix AST undergoes to be handed off, see [here](../technical-reference/ast.html).

## Algebricks Plan Optimization

For a detailed explanation on Graphix specific Algebricks rules, see [here](../technical-reference/ast.html).

