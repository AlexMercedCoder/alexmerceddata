---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Iceberg Merge-on-Read (MoR)"
description: "A comprehensive deep dive into Iceberg Merge-on-Read (MoR), covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["delete files", "position deletes", "write optimized", "Apache Iceberg"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Merge-on-Read (MoR)

In the Data Lakehouse, updating data stored in immutable cloud storage is a massive challenge. The default strategy, **Copy-on-Write (CoW)**, solves this by completely rewriting the entire data file even if only a single row changes. 

While CoW is fantastic for read performance, it is catastrophic for real-time streaming architectures. If an [Apache Flink](/knowledge/apache-flink) cluster is processing a continuous stream of e-commerce updates (e.g., 50 order status changes per second), forcing the cluster to constantly rewrite massive 500MB Parquet files every second will instantly crash the system and generate astronomical cloud compute bills.

To support high-velocity, continuous streaming ingestion, Apache Iceberg introduced a second, heavily write-optimized strategy: **Merge-on-Read (MoR)**.

## How Merge-on-Read Works

Merge-on-Read relies on a fundamental architectural shift: instead of rewriting the massive data file when an update occurs, Iceberg simply writes a tiny "Delete File" alongside it.

Imagine an Iceberg table containing a 500MB Parquet file (`Data_File_A`) with 1 million rows. 
A streaming application submits a SQL command: `UPDATE customers SET status = 'Inactive' WHERE customer_id = 123;`

1.  **The Delete File**: Instead of reading `Data_File_A`, the compute engine (like Flink or Spark) generates a microscopic, secondary file called a **Delete File**. 
2.  **Position vs. Equality**: 
    *   *Position Delete*: The file says, "Ignore Row #45,000 inside `Data_File_A`."
    *   *Equality Delete*: The file says, "Ignore any row anywhere where `customer_id = 123`."
3.  **The Insert**: The engine then writes the *new*, updated row (with the 'Inactive' status) into a brand new, tiny data file (`Data_File_B`).
4.  **Metadata Update**: Iceberg creates a new snapshot. The metadata now points to `Data_File_A`, `Data_File_B`, AND the Delete File.

The write operation took milliseconds. No massive files were rewritten. 

## The Read-Time Penalty

MoR defers the computational cost from the Write phase to the Read phase. 

When a business analyst queries the table using [Dremio](/knowledge/dremio) or Trino, the read engine must do heavy lifting:
1. It reads the massive `Data_File_A`.
2. It reads the Delete File.
3. It loads both into memory and executes an **In-Memory Merge**. It manually cross-references the files, dynamically discarding Row #45,000 from the result set on the fly.
4. It reads the new `Data_File_B` and appends it to the result.

If a table is heavily updated using MoR over several months, it might accumulate 1 massive data file and 10,000 microscopic Delete Files. If a BI tool tries to query that table, the query engine will choke attempting to merge 10,000 files in memory simultaneously, destroying dashboard performance.

## The Compaction Solution

Because MoR eventually destroys read performance, it requires aggressive maintenance. Data Engineering teams must schedule **Compaction Jobs** (usually running [Apache Spark](/knowledge/apache-spark) overnight).

The Compaction Job acts as a garbage collector. It wakes up, reads the massive `Data_File_A` and the 10,000 Delete Files, mathematically merges them all together, and writes out a brand new, perfectly pristine `Data_File_C`. It then deletes all the old files. 
The table is now fully optimized, and read performance returns to blistering speeds.

## Conclusion

Merge-on-Read is the technological breakthrough that allows the Open Data Lakehouse to act like a real-time operational database. By utilizing microscopic Delete Files to track modifications, MoR eliminates the Write Amplification problem, making it the absolute standard for streaming Change Data Capture (CDC) pipelines. However, this write agility comes with a strict operational tax: organizations utilizing MoR must implement automated, rigorous compaction routines to ensure their analytical dashboards remain fast and responsive.
