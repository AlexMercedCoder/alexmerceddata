---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Iceberg Explained"
description: "A complete guide to Apache Iceberg, detailing how this open table format provides ACID transactions, schema evolution, and time travel to the data lakehouse."
date: "2026-05-15"
tags: ["Apache Iceberg", "open table formats", "data lakehouse", "architecture"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Apache Iceberg

As organizations scale their data infrastructure to petabytes of storage, the traditional limitations of data lakes become impossible to ignore. A data lake provides incredibly cheap and scalable storage, but it fundamentally lacks the reliability, transactional guarantees, and performance optimization of a relational database. To bridge this gap, the industry relies on open table formats. Among these formats, [Apache Iceberg](/knowledge/apache-iceberg) has emerged as the definitive standard for building the modern [Data Lakehouse](/knowledge/data-lakehouse).

Apache Iceberg is a high performance, open source table format originally developed at Netflix. It is designed to manage massive analytic datasets stored in cloud object storage systems like [Amazon S3](/knowledge/amazon-s3), Azure Data Lake Storage, and Google Cloud Storage. Instead of forcing data engineers to rely on brittle directory structures and the legacy [Apache Hive](/knowledge/apache-hive) metastore, Iceberg tracks data at the individual file level. 

By treating the data lake like a fully functional database, Apache Iceberg brings ACID transactions, schema evolution, hidden partitioning, and time travel to the open data ecosystem. It allows disparate compute engines, including [Apache Spark](/knowledge/apache-spark), Trino, [Dremio](/knowledge/dremio), and Snowflake, to query and update the same data simultaneously without locking conflicts or data corruption. 

This guide provides a comprehensive explanation of what Apache Iceberg is, the engineering problems it solves, the underlying architecture that powers its performance, and how it integrates into the broader data landscape.

## The Problem With Legacy Data Lakes

To understand the value of Apache Iceberg, one must first understand the severe limitations of the system it was designed to replace: the Apache Hive directory structure.

For years, the standard way to organize a data lake was to use the Hive model. In this model, a "table" is simply a directory in object storage, and a "partition" is a nested sub directory. If you partition a table by date, your storage path looks like `s3://bucket/table_name/date=2026-05-15/`. 

This approach works for small datasets but collapses under the weight of petabyte scale analytics due to four fundamental design flaws.

### 1. The Directory Listing Bottleneck
When a query engine needs to find data in a Hive table, it must ask the cloud storage provider to list all the files in the relevant directories. Object storage APIs are notoriously slow at recursive directory listing. If a table has tens of thousands of partitions and millions of files, the simple act of listing the files can take longer than the actual execution of the SQL query.

### 2. Lack of ACID Transactions
The Hive model relies on the file system to manage state. There is no central transaction log. If a distributed ETL job writes new files to a directory and fails halfway through, half of the files are committed and half are missing. Any user querying the table at that exact moment will read corrupted, incomplete data. There is no way to perform safe, concurrent writes without implementing fragile, external locking mechanisms.

### 3. Painful Schema Evolution
In the legacy model, adding or dropping columns requires extreme caution. If you drop a column, the old data files still contain that column. If a query engine reads the old files, it might crash or return misaligned data. Often, the only safe way to change a schema is to completely rewrite the entire massive historical dataset.

### 4. Explicit Partitioning
Hive partitioning is explicit. If you want to partition a table by month based on a timestamp column, you must create a separate, explicit "month" column in the data. The users querying the data must remember to include `WHERE month = '2026-05'` in their SQL queries. If they filter on the timestamp directly without mentioning the month column, the query engine will perform a full table scan, reading every single file and causing massive compute spikes. 

Apache Iceberg was built from the ground up to solve these exact problems.

## The Core Concept: File Level Tracking

The core architectural breakthrough of Apache Iceberg is that it abandons directory level tracking entirely. 

In Iceberg, the physical layout of the folders in cloud storage is irrelevant to the query engine. The folder structure does not define the table. Instead, Iceberg uses a hierarchy of explicit metadata files to track the exact list of individual data files that make up the table at any given microsecond. 

When a query engine interacts with an Iceberg table, it never performs an expensive directory listing. It reads the metadata file, gets the exact, explicit paths of the necessary data files, and reads them directly. This shifts the computational burden from the slow object storage listing APIs to the fast, vectorized query engines processing the metadata.

## Key Capabilities of Apache Iceberg

By moving the table state into explicit metadata, Apache Iceberg unlocks capabilities previously reserved for proprietary data warehouses.

### ACID Transactions and Serializable Isolation

Apache Iceberg provides full ACID (Atomicity, Consistency, Isolation, Durability) guarantees. It achieves this using a technique called [Optimistic Concurrency Control (OCC)](/knowledge/optimistic-concurrency-control-occ).

When a query engine (like Spark) writes new data to an Iceberg table, it does not overwrite existing files. It creates new data files and attempts to commit a new metadata file that points to these new additions. Before committing, it checks the catalog to ensure no other engine has updated the table since the operation began. If another engine has made an update, the first engine simply reads the new metadata, rebases its changes, and retries the commit.

This provides serializable isolation. A user running a reporting query will always see a consistent, point in time snapshot of the table, even if massive data ingestion jobs are writing to the table concurrently. There are no dirty reads and no partial commits.

### Schema Evolution

Schema evolution in Apache Iceberg is completely safe, independent of the underlying data files, and instantaneous. 

Iceberg tracks columns using unique internal IDs, rather than relying on column names. If you rename a column from `user_id` to `account_id`, Iceberg simply updates the metadata file to map the new name to the existing ID. The underlying Parquet data files do not need to be rewritten. 

Similarly, you can add, drop, or reorder columns safely. If you drop a column, Iceberg marks the internal ID as deleted in the metadata. When a query engine reads an old data file that still contains the dropped column, Iceberg instructs the engine to ignore the data. This decoupling of logical schema from physical files saves thousands of hours of data engineering time.

### Hidden Partitioning

Apache Iceberg solves the problem of explicit partitioning through a feature called Hidden Partitioning. 

With Iceberg, you do not need to create explicit derivative columns for partitioning. You simply tell Iceberg to partition the table based on a transformation of an existing column. For example, you can partition by `days(timestamp_column)`. 

The partitioning logic is hidden in the metadata. When a user runs a query with `WHERE timestamp_column = '2026-05-15'`, Iceberg automatically translates that filter into the correct partition layout. The user does not need to know how the table is partitioned, and they cannot accidentally trigger a full table scan by forgetting to include a derived partition column in their `WHERE` clause.

### Partition Evolution

As a business grows, its partitioning strategy often needs to change. A table that was partitioned by month when it had gigabytes of data might need to be partitioned by day when it grows to terabytes.

In the legacy model, changing the partition strategy required rewriting the entire historical dataset to fit the new directory structure. Apache Iceberg enables Partition Evolution. You can update the partition specification on a live table instantly. Old data remains partitioned by month, and all new data written from that moment onward is partitioned by day. The metadata seamlessly stitches the two strategies together, allowing query engines to scan the entire table without error.

### Time Travel and Rollbacks

Because Apache Iceberg never overwrites existing metadata files, it maintains a linear history of snapshots. Every commit creates a new snapshot ID representing the exact state of the table at that moment.

This enables Time Travel queries. A data scientist can execute a query to view the table exactly as it looked at 2:00 PM last Tuesday, which is essential for reproducing machine learning models. 

Additionally, if a data pipeline introduces corrupted data, a data engineer can instantly execute a rollback command. The catalog simply reverts the table pointer to the previous healthy snapshot ID, instantly undoing the damage without needing to manually delete files or run complex restoration scripts.

## The Apache Iceberg Architecture

To understand how Iceberg achieves these capabilities, it is necessary to examine the physical structure of an Iceberg table. A complete deep dive into this topic is available in our [Apache Iceberg Architecture](/knowledge/apache-iceberg-architecture) guide, but the core structure consists of a catalog and three distinct layers of metadata.

### The Catalog
The catalog is the absolute source of truth. Its only job is to map a table name (like `sales.transactions`) to the storage path of the most recent metadata file. When a query engine wants to read or write to Iceberg, it must consult the catalog first. The catalog enforces the atomic swap of metadata pointers during write operations, guaranteeing ACID compliance. The [Iceberg REST Catalog](/knowledge/apache-iceberg-rest-catalog) specification is the modern standard, enabling seamless interoperability across diverse compute engines.

### 1. Metadata Files
The catalog points to a `.metadata.json` file. This file contains the complete logical state of the table. It stores the schema, the partitioning specification, and an array of all historical snapshots. It defines which snapshot is the current, active version of the table.

### 2. Manifest Lists
The current snapshot points to a single manifest list file (typically in Avro format). The manifest list acts as an index. It contains a list of underlying manifest files. For each manifest file, the manifest list stores aggregate statistics, such as the minimum and maximum partition values contained within it. This allows the query engine to completely skip reading manifest files that do not match the user's query filters.

### 3. Manifest Files
A manifest file (also in Avro format) tracks a subset of the actual data files. For every individual data file, the manifest stores its exact cloud storage path, its partition assignment, and column level metrics (such as the upper and lower bounds for every column). This is the level where precise file pruning occurs.

### 4. Data Files
Finally, the manifest files point to the actual physical data files, which are typically stored in columnar formats like [Apache Parquet](/knowledge/apache-parquet) or [ORC Format](/knowledge/orc-format), though Avro is also supported for streaming use cases.

When a query is executed, the engine traverses this tree from top to bottom. It reads the catalog, parses the metadata file, filters the manifest list, filters the manifest files, and ultimately reads only the exact data files necessary to answer the query.

## Apache Iceberg vs Delta Lake vs Apache Hudi

Apache Iceberg is not the only open table format on the market. It frequently competes with [Delta Lake](/knowledge/delta-lake) and [Apache Hudi](/knowledge/apache-hudi). A detailed comparison is available in our [Apache Iceberg vs Delta Lake vs Apache Hudi](/knowledge/apache-iceberg-vs-delta-lake-vs-hudi) guide, but the high level distinctions are important to understand.

**Delta Lake** was originally developed by [Databricks](/knowledge/databricks). While it is now fully open source, it still shares a strong historical and architectural alignment with the Spark ecosystem. Delta Lake tracks state using a chronological transaction log (the `_delta_log` directory) rather than Iceberg's hierarchical metadata tree.

**Apache Hudi** (Hadoop Upserts Deletes and Incrementals) was created at Uber. It is specifically optimized for heavy streaming workloads, fast incremental processing, and efficient record level upserts. 

**Apache Iceberg** is characterized by its strict separation of logical and physical execution, its complete engine neutrality, and its hierarchical metadata design, which arguably scales better for massive tables spanning tens of thousands of partitions. Iceberg is heavily championed by companies like Apple, Netflix, [Dremio](/knowledge/dremio), and Snowflake.

## Engine Support and Interoperability

One of the greatest strengths of Apache Iceberg is its vast ecosystem. Because it is an open standard governed by the Apache Software Foundation, no single vendor dictates its roadmap. This has resulted in broad adoption across the data industry.

- **[Apache Spark](/knowledge/apache-spark):** Provides complete support for reading, writing, and streaming Iceberg tables.
- **[Dremio](/knowledge/dremio):** Offers native, highly optimized read and write access to Iceberg, leveraging [Apache Arrow](/knowledge/apache-arrow) for sub second BI performance.
- **Trino and Starburst:** Provide distributed SQL querying capabilities against Iceberg.
- **Snowflake:** Can read Iceberg tables directly from external object storage, preventing vendor lock in while utilizing Snowflake's compute engine.
- **[Apache Flink](/knowledge/apache-flink):** Ideal for continuous streaming ingestion directly into Iceberg tables.

This interoperability is the cornerstone of the [Data Lakehouse vs Data Lake vs Data Warehouse](/knowledge/data-lakehouse-vs-data-lake-vs-data-warehouse) debate. Iceberg allows organizations to use multiple specialized compute engines against the exact same copy of data without moving or copying it.

## When Not to Use Apache Iceberg

While Apache Iceberg solves immense challenges, it is not the correct solution for every database workload.

Iceberg is an analytical table format designed for OLAP (Online Analytical Processing) workloads involving millions or billions of rows. It is not an OLTP (Online Transaction Processing) database. You should never use Apache Iceberg as the primary backing database for a high frequency transactional web application. Applications requiring low latency single row inserts and updates (like an e-commerce checkout cart) should use traditional operational databases like PostgreSQL or MySQL.

Additionally, if your total data volume is very small (under a few hundred gigabytes), the metadata management overhead of Iceberg may exceed the performance benefits. For small, simple datasets, querying raw Parquet files directly or utilizing a managed data warehouse may be sufficient.

## The Future: Iceberg and the Agentic Lakehouse

As artificial intelligence reshapes the data landscape, Apache Iceberg is emerging as the critical foundation for the [Agentic Lakehouse](/knowledge/agentic-lakehouse). 

Autonomous AI agents require highly reliable, strictly governed, and perfectly schema enforced data environments to operate safely. The wild west of a raw data lake is too chaotic for an AI agent to reliably query. Iceberg provides the transactional guarantees, time travel for reproducible ML training, and clear metadata structure that AI agents need to successfully perform natural language analytics and automated reporting across enterprise datasets.

## Final Thoughts

Apache Iceberg has solved the fundamental scaling problems of the data lake. By tracking data at the file level and enforcing rigid ACID compliance through its hierarchical metadata tree, it provides the reliability of a proprietary data warehouse on top of open, cheap cloud storage. 

As the foundation of the modern [data lakehouse](/knowledge/data-lakehouse), Iceberg allows organizations to eliminate data silos, avoid vendor lock in, and deploy the best compute engines for their specific workloads. It is a mandatory technology for any modern data architecture seeking to operate at enterprise scale.
