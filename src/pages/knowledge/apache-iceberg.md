---
layout: '../../layouts/KnowledgeLayout.astro'
title: "What is Apache Iceberg? The Definitive Guide"
description: "A comprehensive, authoritative overview of Apache Iceberg, the open table format for huge analytic datasets. Learn how it works, why it matters, and how to use it."
date: "2026-05-14"
tags: ["Apache Iceberg", "Data Lakehouse", "Data Engineering", "Open Source"]
---

## Introduction to Apache Iceberg

In the modern data ecosystem, the separation of storage and compute has led to the rise of the **Data Lakehouse**—a hybrid architecture combining the flexibility of a data lake with the reliability of a data warehouse. At the heart of this revolution is **Apache Iceberg**, an open table format originally developed at Netflix to solve the massive data challenges associated with [Apache Hive](/knowledge/apache-hive).

Apache Iceberg is designed for huge analytic datasets, typically stored in cloud object storage like [Amazon S3](/knowledge/amazon-s3), Google Cloud Storage (GCS), or Azure Data Lake Storage (ADLS). It brings ACID transactions, schema evolution, and time travel to the data lake, allowing engines like [Apache Spark](/knowledge/apache-spark), Trino, [Dremio](/knowledge/dremio), and Snowflake to work with the same data simultaneously without locking or inconsistency.

## Why Do We Need a Table Format?

Before Iceberg, the de facto standard for organizing data in a data lake was the Hive directory structure. Hive maps a table to a directory and partitions to sub-directories. However, this approach has severe limitations at scale:
- **Inefficient Listing:** Finding files in cloud storage requires recursive directory listing, which is extremely slow for thousands of partitions.
- **No Safe Schema Evolution:** Changing a column type or name could break existing queries or require a full rewrite of the table.
- **Lack of ACID Transactions:** Concurrent reads and writes often resulted in dirty reads, missing files, or data corruption.
- **Painful Partition Evolution:** If you wanted to change how data was partitioned (e.g., from daily to hourly), you had to rewrite the entire dataset.

Apache Iceberg solves these problems by tracking data at the **file level** instead of the directory level.

## Core Architectural Components of Iceberg

The magic of Iceberg lies in its metadata tree. When an engine reads an Iceberg table, it doesn't list directories; instead, it reads the metadata to find exactly which files to scan.

### 1. The Iceberg Catalog
The catalog is the entry point. It stores the current location of the metadata pointer for every table. Catalogs can be implemented using Hive Metastore, [AWS Glue](/knowledge/aws-glue), Nessie, [Apache Polaris](/knowledge/apache-polaris), or a simple JDBC database.

### 2. Metadata Files (JSON)
The catalog points to a `.json` metadata file. This file contains:
- The table schema.
- The partition spec.
- A snapshot history.
- The current snapshot ID.

### 3. Manifest Lists (Avro)
A snapshot points to a manifest list. The manifest list contains an array of manifest files that make up the snapshot, along with partition statistics (min/max values) for the files inside those manifests. This allows the query engine to prune entire manifests without reading them.

### 4. Manifest Files (Avro)
A manifest file tracks a subset of the actual data files (Parquet, ORC, or Avro). It contains file paths, partition data, and column-level metrics (e.g., null counts, min/max values) used for highly efficient file-level pruning during queries.

## Key Features and Benefits

### ACID Transactions
Iceberg uses Optimistic Concurrency Control (OCC). Multiple writers can write to the same table simultaneously. If there's a conflict, Iceberg will safely retry or fail the transaction without leaving corrupted data behind. This means you get fully isolated reads—if a query starts while a write is happening, the query will see the state of the table exactly as it was when the query began.

### Schema Evolution
Iceberg tracks columns by a unique ID, not by name. This means:
- You can add, drop, rename, or reorder columns instantly.
- You can change column types (e.g., from `int` to `bigint`).
- Dropping a column doesn't require rewriting the data; the metadata simply ignores the column in older files.

### Hidden Partitioning
In Hive, partitioning is explicit and must be handled by the user (e.g., creating a separate `date` column derived from a `timestamp`). Iceberg handles this internally. You can partition by `day(timestamp)`, and the query engine will automatically translate a query filtering on `timestamp` into a partition filter.

### Partition Evolution
As your data volume grows, your partitioning strategy might need to change. Iceberg allows you to update the partition spec on a live table. Old data remains partitioned the old way, and new data uses the new partitioning. The engine handles this seamlessly during queries.

### Time Travel and Rollbacks
Because Iceberg maintains a history of snapshots, you can query the table exactly as it looked at a specific point in time or at a specific snapshot ID. This is invaluable for machine learning reproducibility, auditing, or rolling back a bad data pipeline deployment.

## Engines and Ecosystem Integration

Iceberg is engine-agnostic. It is supported by a massive ecosystem:
- **[Apache Spark](/knowledge/apache-spark):** Full support for reads, writes, and streaming.
- **[Apache Flink](/knowledge/apache-flink):** Excellent for real-time ingestion into Iceberg tables.
- **Dremio:** Native, lightning-fast reads and writes with built-in optimizations.
- **Trino/Starburst:** Highly optimized distributed SQL querying.
- **Snowflake:** Can read Iceberg tables directly from your external cloud storage.
- **AWS Athena:** Native support for querying Iceberg.

## Conclusion

Apache Iceberg has fundamentally changed how we think about data architecture. By bringing database-like capabilities to the data lake, it enables the Data Lakehouse vision—providing the performance of a warehouse with the scalability, flexibility, and cost-effectiveness of cloud object storage.

As the industry standardizes on open table formats, mastering Apache Iceberg is crucial for any modern data engineer, architect, or data scientist.
