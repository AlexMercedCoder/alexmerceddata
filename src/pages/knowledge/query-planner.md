---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Query Planner"
description: "A comprehensive deep dive into Query Planners, covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["SQL parsing", "execution plan", "logical plan", "physical plan"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to the Query Planner

Structured Query Language (SQL) is a declarative language. When a business analyst writes a SQL query—e.g., `SELECT * FROM sales JOIN customers ON sales.id = customers.id`—they are simply declaring *what* they want the final result to look like. They do absolutely nothing to specify *how* the computer should retrieve that data. 

Should the database read the `sales` table first, or the `customers` table first? Should it load the data into memory and perform a Hash Join, or sort the data and perform a Merge Join? Should it scan every file, or utilize a specific index?

The component responsible for making these critical, sub-second architectural decisions is the **Query Planner** (often used interchangeably with Query Optimizer). 

The Query Planner is the brain of any modern database, data warehouse, or compute engine (like Trino, Spark, or Snowflake). It translates the human-readable SQL text into a highly optimized, machine-executable set of instructions.

## The Lifecycle of a Query Plan

When a SQL string is submitted to an engine, the Query Planner pushes it through a rigorous, multi-stage compilation pipeline.

### 1. Parsing and Syntax Analysis
The engine first checks the SQL string for basic grammatical correctness. Did the user misspell `SELECT` as `SLCT`? Are the parentheses balanced? The parser takes the raw string and converts it into a structured programming object known as an Abstract Syntax Tree (AST).

### 2. Semantic Analysis and Binding
Next, the engine validates the *meaning* of the query against the actual database metadata (the Catalog). 
Does the table `sales` actually exist? Does the user have the RBAC permissions to read it? Does the column `id` exist, and is it a type that can be joined mathematically to `customers.id`?

### 3. The Logical Plan (Rule-Based Optimization)
Once validated, the planner constructs an initial **Logical Plan**. This is a theoretical map of relational algebra operators (Filter, Project, Join).
At this stage, the planner applies **Rule-Based Optimization (RBO)**. It uses hard-coded heuristic rules to rewrite the logical plan to be inherently faster, regardless of the underlying data.
*   **[Predicate Pushdown](/knowledge/predicate-pushdown)**: If the query filters `WHERE year = 2026` *after* the join, the RBO rewrites the plan to filter the data *before* the join, mathematically ensuring less data is processed.
*   **Constant Folding**: If a query has `WHERE price > 10 * 5`, the planner rewrites it to `WHERE price > 50` so the math isn't calculated millions of times during execution.

### 4. The Physical Plan (Cost-Based Optimization)
The logical plan dictates *what* operations to perform, but the **Physical Plan** dictates *how* to physically execute them on the hardware.
A single logical plan might have dozens of viable physical execution paths. Should the engine use a Broadcast Join or a Shuffle Hash Join? 

To decide, the planner hands the options over to the **Cost-Based Optimizer (CBO)**. The CBO looks at the actual statistical metadata of the tables (e.g., "The sales table has 1 billion rows, the customers table has 1,000 rows"). It calculates a mathematical "cost" for each possible physical plan based on estimated CPU, memory, and network I/O usage. It selects the physical plan with the lowest overall cost.

### 5. Execution
The winning Physical Plan is compiled into executable code (often using advanced techniques like LLVM Just-In-Time compilation). The engine distributes this code to the worker nodes, reads the storage layer (like S3/Iceberg), and returns the results to the user.

## The Evolution in the Lakehouse

In a traditional, monolithic database (like Oracle), the Query Planner is tightly coupled to the storage engine. It knows exactly where every byte sits on the spinning hard drive.

In a modern, decoupled Data Lakehouse, the Query Planner (living inside an engine like Dremio or Trino) does not own the storage. The data sits as raw Parquet files on [Amazon S3](/knowledge/amazon-s3). 

To plan queries effectively, modern lakehouse planners rely heavily on open table formats like **Apache Iceberg**. Iceberg acts as the metadata layer, providing the Query Planner with the precise file locations, partition maps, and min/max column statistics required to accurately feed the Cost-Based Optimizer and generate highly efficient, distributed execution plans.

## Conclusion

The Query Planner is arguably the most complex and critical piece of software in the data ecosystem. It is the invisible intelligence that abstracts away the staggering complexity of distributed computing. By automatically transforming declarative SQL into optimized algebraic execution paths, the Query Planner allows analysts to query petabytes of data without needing to know a single thing about distributed networking or memory management.
