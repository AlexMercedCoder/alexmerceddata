---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Trino (PrestoSQL)"
description: "A comprehensive deep dive into Trino, covering architecture, concepts, and real-world usage in Query Engines."
date: "2026-05-14"
tags: ["distributed SQL", "MPP", "federated queries", "interactive analytics"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Trino

In the early 2010s, Facebook possessed what was likely the largest Hadoop data warehouse in the world, storing over 300 petabytes of data. Their data scientists were using [Apache Hive](/knowledge/apache-hive) to run SQL queries against this massive dataset. However, Hive translated SQL into [MapReduce](/knowledge/mapreduce) jobs, meaning even a simple `SELECT COUNT(*)` query could take 30 minutes to execute. Interactive, ad-hoc analytics were impossible.

To solve this, a team of engineers at Facebook (including Martin Traverso, Dain Sundstrom, and David Phillips) built **Presto**—a distributed SQL query engine designed for blazing-fast, interactive analytics. 

In 2018, the original creators left Facebook and forked the project, rebranding it as **Trino** (formerly PrestoSQL). Today, Trino is a fiercely independent open-source project and one of the most powerful and widely adopted query engines in the modern Data Lakehouse ecosystem.

## The Architecture of Trino

Trino is not a database. It does not store data. It is purely a compute engine. 
It utilizes a **Massively Parallel Processing (MPP)** architecture designed to execute queries entirely in memory, completely bypassing the slow disk-writing phases that crippled Hadoop [MapReduce](/knowledge/mapreduce).

### The Coordinator and the Workers
A Trino cluster consists of two types of nodes:
1.  **The Coordinator**: The brain of the operation. When a user submits a SQL query, the Coordinator parses it, analyzes it, and creates an optimized distributed execution plan.
2.  **The Workers**: The muscle. The Coordinator divides the query plan into hundreds of tiny tasks and delegates them to the Worker nodes. The Workers execute these tasks in parallel, fetching the data directly from the storage system, processing it in RAM, and returning the aggregated results back to the Coordinator.

### The Connector Architecture
The genius of Trino lies in its Connector API. Because Trino separates compute from storage, it uses "Connectors" to talk to the outside world. 
Trino has native connectors for Apache Iceberg, [Amazon S3](/knowledge/amazon-s3), PostgreSQL, MySQL, Cassandra, Elasticsearch, and dozens of others. 

When a Worker node needs data, it uses the specific Connector to push down filters and retrieve data from the source system. This abstraction allows Trino to act as a universal SQL translator.

## Federated Analytics

The combination of the MPP engine and the Connector API enables Trino's defining superpower: **Federated Queries**.

In a traditional enterprise, if an analyst wants to join customer records stored in an Oracle database with clickstream logs stored in an S3 Data Lake, a data engineer must write an ETL pipeline to copy the Oracle data into S3.

With Trino, the analyst simply connects to the Trino Coordinator and writes:
```sql
SELECT c.name, s.clicks 
FROM oracle_db.customers c 
JOIN s3_lakehouse.clickstream s ON c.id = s.user_id
```

Trino pushes the Oracle query down to Oracle, pushes the S3 query down to the Iceberg tables, pulls the filtered results from both systems into the RAM of the Worker nodes, joins them in memory, and returns the result to the user in seconds. The data is never permanently moved or duplicated.

## Trino in the Modern Lakehouse

While federated querying across databases is a great feature, Trino's primary use case today is acting as the massive SQL engine powering Open Data Lakehouses.

When paired with an open table format like **Apache Iceberg**, Trino transforms a cheap [Amazon S3](/knowledge/amazon-s3) bucket into a fully functional, high-speed data warehouse.
*   **Performance**: Trino is heavily optimized for reading [Apache Parquet](/knowledge/apache-parquet) and ORC files. It utilizes advanced vectorized execution and highly tuned [Predicate Pushdown](/knowledge/predicate-pushdown) to skip irrelevant files.
*   **Cost Efficiency**: Because Trino scales horizontally, organizations can spin up a massive cluster of 100 Trino workers, execute complex end-of-month financial reports against an S3 lakehouse in minutes, and instantly spin the cluster down to zero, paying only for the exact compute used.

## Conclusion

Trino represents the pinnacle of decoupled data architecture. By entirely separating the query execution engine from the underlying storage infrastructure, Trino provides organizations with the ultimate flexibility. Whether performing federated joins across legacy silos or executing sub-second analytics over petabyte-scale Apache Iceberg tables, Trino delivers the interactive speed of a proprietary data warehouse at a fraction of the cost, using standard ANSI SQL.
