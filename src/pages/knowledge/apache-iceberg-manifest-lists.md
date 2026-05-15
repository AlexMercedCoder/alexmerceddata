---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Iceberg Manifest Lists"
description: "A comprehensive deep dive into Apache Iceberg Manifest Lists, covering architecture, concepts, and real-world usage in Data Architecture."
date: "2026-05-14"
tags: ["metadata", "file pruning", "query optimization", "avro"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Apache Iceberg Metadata Architecture

To understand the sheer performance and scalability of Apache Iceberg, one must look beyond the data files themselves and examine the elegant metadata tree that orchestrates them. Traditional data lakes (often reliant on Hive-style directory partitioning) struggle at scale. When a query is executed, engines are forced to perform slow, recursive file listing operations across object storage (like [Amazon S3](/knowledge/amazon-s3) or ADLS) to determine which files to read. 

Apache Iceberg solves this "listing bottleneck" by maintaining a precise, hierarchical metadata structure that tracks every single data file at the file level, rather than the directory level. This tree consists of three primary layers:
1.  **Metadata Files (`.json`)**: Track the table state, schema, partitioning, and snapshots.
2.  **Manifest Lists (`.avro`)**: Track the manifest files belonging to a specific snapshot.
3.  **Manifest Files (`.avro`)**: Track the individual data files (Parquet/ORC/Avro) and their column-level statistics.

In this deep dive, we will focus on the crucial middle layer: **The Manifest List**. The Manifest List is the engine's map. It is the core component that enables Iceberg to achieve O(1) file pruning, drastically reducing query planning time and enabling sub-second analytical performance on petabyte-scale datasets.

## What is a Manifest List?

When a commit occurs in an Apache Iceberg table (e.g., an `INSERT`, `UPDATE`, or `DELETE`), a new **Snapshot** is created. A snapshot represents the complete, consistent state of the table at that specific point in time. 

The Iceberg Metadata file (`.json`) points to the current snapshot. The snapshot, in turn, points to exactly one **Manifest List**.

A Manifest List is an Avro file that contains an array of records. Each record in this list does not point to data; instead, it points to a **Manifest File**. A manifest file is another Avro file that tracks the actual underlying data files (e.g., `data-001.parquet`).

### The Structure of a Manifest List

Because Manifest Lists are stored in the Avro format, they are row-oriented, highly compressible, and strictly typed. A Manifest List contains vital statistics about the manifest files it references. For every manifest file, the Manifest List stores:

*   **`manifest_path`**: The absolute URI to the manifest file in object storage.
*   **`manifest_length`**: The size of the manifest file.
*   **`partition_spec_id`**: The ID of the partition specification used by the files within the manifest.
*   **`added_snapshot_id`**: The ID of the snapshot in which this manifest file was created.
*   **`added_data_files_count`**: The number of new data files added in this manifest.
*   **`existing_data_files_count`**: The number of pre-existing data files tracked by this manifest.
*   **`deleted_data_files_count`**: The number of data files logically deleted in this manifest.
*   **`partitions`**: A highly critical array containing summary statistics for the partition fields. This includes the lower and upper bounds of the partition values found within the referenced manifest file.

## The Role of Manifest Lists in Query Optimization

The primary purpose of the Manifest List is to enable **Manifest Pruning** during the query planning phase. This is the secret sauce to Iceberg's performance.

Consider a massive table containing billions of rows of IoT sensor data, partitioned by `event_date`. 

### The Traditional Hive Approach
In a legacy Hive architecture, if you query `SELECT * FROM sensors WHERE event_date = '2026-05-14'`, the query engine must ask S3 to list all directories matching `event_date=2026-05-14/`. If the partition contains 10,000 files, S3 must return all 10,000 file paths before the engine can even begin reading. If the query spans a year, the listing operation alone can take minutes.

### The Iceberg Approach with Manifest Lists
When the same query is executed against an Iceberg table, the engine (like [Dremio](/knowledge/dremio) or Spark) follows these steps:
1.  **Read the Metadata JSON**: Identify the current snapshot and locate the Manifest List.
2.  **Read the Manifest List**: The engine reads the single Manifest List Avro file into memory.
3.  **Manifest Pruning ([Predicate Pushdown](/knowledge/predicate-pushdown))**: The engine evaluates the query predicate (`event_date = '2026-05-14'`) against the `partitions` array stored inside the Manifest List for *each* manifest file. 
    *   If a manifest file's lower and upper bounds for `event_date` are `['2025-01-01', '2025-12-31']`, the engine instantly knows this manifest contains no relevant data. It **skips** the manifest file entirely.
    *   If a manifest file's bounds include `2026-05-14`, the engine adds that manifest file to a "must read" list.
4.  **Read the Manifest Files**: The engine opens only the surviving manifest files to find the specific Parquet file paths.
5.  **Read the Data**: The engine fetches the Parquet files and executes the query.

By storing partition bounds in the Manifest List, Iceberg allows compute engines to filter out thousands of manifest files—and millions of data files—without ever touching them. This changes a slow network I/O listing operation into a lightning-fast, in-memory filtering operation.

## Optimizing Manifest Lists

While Manifest Lists are highly efficient, they can become fragmented over time, especially in streaming workloads where small batches of data are committed frequently.

### The Problem of Small Manifests
If a streaming job (like [Apache Flink](/knowledge/apache-flink)) commits every 1 minute, it creates a new snapshot, a new manifest file, and a new manifest list pointing to the previous manifests plus the new one. Over days and weeks, the Manifest List can grow to contain references to tens of thousands of tiny manifest files.

When a query planner runs, it has to download and open thousands of small manifest files to evaluate column-level statistics, causing the planning phase to slow down.

### Manifest Rewriting (Compaction)
To maintain peak performance, data engineers must regularly perform maintenance on Iceberg tables. One of the most important maintenance tasks is **Rewrite Manifests**.

Using [Apache Spark](/knowledge/apache-spark) or an automated service like Dremio Arctic, you can execute a procedure to compact these files:
```sql
CALL catalog.system.rewrite_manifests('my_namespace.my_table');
```

This procedure reads all the small manifest files and rewrites them into fewer, larger, highly optimized manifest files. It groups data files logically, often aligning them by partition boundaries. Finally, it generates a new, clean Manifest List. 

After rewriting manifests, the query engine has to read significantly fewer files during the planning phase, restoring sub-second query performance.

## Conclusion

Apache Iceberg's Manifest Lists are a masterclass in metadata engineering. By elevating partition statistics to the top of the metadata tree, Manifest Lists act as a highly efficient index, guiding query engines precisely to the data they need while ignoring everything else.

Understanding how Manifest Lists work is essential for any data engineer aiming to build highly performant, scalable lakehouses. By combining this architecture with regular maintenance (manifest rewriting), organizations can achieve data warehouse-level performance directly on their data lakes.
