---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Iceberg Architecture: The Metadata Tree"
description: "A deep dive into the Apache Iceberg architecture, covering the metadata tree, snapshots, manifests, concurrency control, and query planning."
date: "2026-05-15"
tags: ["Apache Iceberg", "architecture", "data engineering", "metadata"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Apache Iceberg Architecture

The fundamental challenge of modern data engineering is managing data at petabyte scale without sacrificing the reliability of a traditional relational database. As organizations migrated from data warehouses to open data lakes, they gained infinite storage capacity but lost ACID transactions, safe schema evolution, and acceptable query performance. 

[Apache Iceberg](/knowledge/apache-iceberg) was designed specifically to solve this problem. It is a high performance open table format that acts as an intelligent metadata layer on top of cloud object storage. Rather than relying on the file system to determine the state of a table, Iceberg defines the table through an explicit, hierarchical metadata tree.

This architecture fundamentally changes how compute engines interact with data. By shifting the source of truth from slow directory listings to explicit metadata files, Iceberg enables query engines to perform massive analytical operations with unprecedented speed and safety. 

This guide provides a comprehensive technical deep dive into the Apache Iceberg architecture. It explores the components of the metadata tree, the mechanisms of optimistic concurrency control, the write commit flow, and the garbage collection processes required to maintain a healthy data lakehouse.

## The Problem with Directory Based Tables

Before examining Iceberg's architecture, we must understand the legacy approach it replaces: the Apache Hive directory structure. 

In the traditional data lake, a table is defined implicitly by a directory path in object storage (e.g., `s3://data-lake/sales/`). Partitions are represented as nested subdirectories (e.g., `s3://data-lake/sales/year=2026/month=05/`). When a query engine needs to read data, it must ask the object storage provider to perform a recursive listing of all the files inside these directories.

This implicit, directory based architecture suffers from several fatal flaws at scale:
1.  **O(N) Listing Time:** Object storage systems are not true file systems. Listing files requires expensive API calls. Finding 100,000 files in a deeply nested partition tree can take longer than the actual data processing.
2.  **No Transactional State:** The file system has no concept of a "commit." If a job writes 500 files and crashes after writing 250, those 250 files immediately become visible to anyone querying the directory, resulting in corrupted reads.
3.  **No File Level Statistics:** To know what is inside a file, the engine must open it and read the footer. This makes it impossible to skip irrelevant files without opening them first.

Apache Iceberg eliminates these problems by completely decoupling the logical state of the table from the physical layout of the files on disk.

## The Iceberg Metadata Tree

The Apache Iceberg architecture relies on a strict, four layer hierarchy known as the metadata tree. When a query engine interacts with an Iceberg table, it traverses this tree from top to bottom.

### Level 1: The Catalog
The top of the architecture is the Iceberg Catalog. Because data files and metadata files are stored immutably in object storage, there must be a single, mutable system that tracks the current state of the table.

The catalog acts as the authoritative entry point. Its primary responsibility is to maintain a pointer that maps a logical table name (e.g., `finance.transactions`) to the absolute URI of the current metadata JSON file. 

The catalog is also responsible for guaranteeing atomicity. When an engine commits new data to the table, it asks the catalog to update the pointer from the old metadata file to the new metadata file. The catalog ensures this operation is atomic. If two engines try to update the pointer simultaneously, the catalog allows one to succeed and forces the other to retry, preventing corruption. 

Organizations typically implement the catalog using specialized services like [Apache Polaris](/knowledge/apache-polaris) or Project Nessie, which implement the [Iceberg REST Catalog](/knowledge/apache-iceberg-rest-catalog) specification.

### Level 2: The Metadata File
The catalog pointer leads the query engine to a `.metadata.json` file. This file represents the absolute state of the table at a specific point in time. 

The metadata JSON file contains the foundational configuration of the table, including:
-   **Table Schema:** A complete record of the current columns, data types, and internal column IDs. Because Iceberg tracks columns by ID rather than by name, schema evolution (like renaming a column) is a simple metadata update.
-   **Partition Specification:** The rules defining how the data is partitioned (e.g., `days(event_timestamp)`). Because this is stored in the metadata, partition evolution is supported natively.
-   **Table Properties:** Configuration settings such as default compression algorithms or garbage collection policies.
-   **Snapshot Array:** A chronological list of every snapshot (commit) in the table's history.
-   **Current Snapshot ID:** A pointer to the specific snapshot that represents the current, active state of the table.

When a query engine reads the metadata file, it identifies the current snapshot ID and proceeds to the next level of the tree.

### Level 3: The Manifest List
Every snapshot points to exactly one Manifest List file. This file is written in Apache Avro format, which is a row based binary format highly optimized for rapid sequential reading.

The manifest list acts as a high level index for the snapshot. It contains a list of paths pointing to the underlying manifest files. Crucially, it does not just list paths; it stores aggregate statistics for each manifest file.

For every manifest file it tracks, the manifest list stores:
-   The absolute path to the manifest file.
-   The number of added, existing, and deleted data files within that manifest.
-   Partition summaries, including the lower and upper bounds of the partition values contained in the manifest.

This allows the query engine to perform massive optimizations. If a user queries data for `2026-05-15`, the engine inspects the manifest list. If a specific manifest file only contains data from `2025`, the engine completely ignores that manifest file, skipping thousands of data files without ever reading them.

### Level 4: The Manifest Files
The manifest list points the engine to one or more Manifest Files. These files, also written in Avro format, are the lowest level of the metadata tree.

A manifest file tracks a subset of the actual physical data files that make up the table. It is the granular tracking system of the Iceberg architecture. For every single data file (usually Parquet) it tracks, the manifest file records:
-   The absolute URI of the data file in cloud storage.
-   The file format (Parquet, ORC, or Avro).
-   The size of the file in bytes.
-   The specific partition values associated with the file.
-   Column level statistics, including the minimum and maximum values, null counts, and NaN counts for every column inside the data file.

Because these statistics are stored in the manifest file, the query engine can perform file level pruning. If a query includes a filter like `WHERE transaction_amount > 1000`, the engine checks the upper bounds stored in the manifest. If a data file's maximum transaction amount is `500`, the engine skips the data file entirely. 

### Level 5: The Data Files
At the bottom of the architecture are the physical data files. These files are completely immutable. Once written to object storage, they are never modified or appended to. 

These files are typically written using columnar formats like [Apache Parquet](/knowledge/apache-parquet). By the time the query engine reaches this layer, it has used the metadata tree to eliminate 99 percent of the files in the table. It opens only the exact subset of Parquet files required, reads the specific columns requested by the user, and returns the result.

## Understanding Snapshots and Time Travel

A core concept in the Apache Iceberg architecture is the snapshot. A snapshot represents the complete, immutable state of the table at a specific microsecond.

Every time a write operation occurs, whether it is an `INSERT`, `UPDATE`, `DELETE`, or a schema change, Iceberg creates a new snapshot. It does this by creating a new metadata JSON file that contains a new snapshot ID. This new metadata file points to a new manifest list, which points to a combination of existing manifest files and newly created manifest files.

Because existing metadata files and data files are immutable, they are left entirely intact. This architectural design enables powerful capabilities explored fully in our [Apache Iceberg Snapshots and Time Travel](/knowledge/apache-iceberg-snapshots-and-time-travel) guide.

Because previous snapshots are preserved, users can execute time travel queries. By specifying an older snapshot ID or timestamp in the SQL query, the query engine simply reads the older metadata JSON file. The engine traverses the old manifest list and the old manifest files, completely ignoring any data inserted after that point in time. 

This architecture also allows for instant rollbacks. If a bad ETL job corrupts the table, a data engineer can issue a command to roll back the table. The catalog simply updates its pointer from the corrupted `metadata.json` back to the previous, healthy `metadata.json`. The operation takes milliseconds and requires no data movement.

## The Commit Flow: How Iceberg Writes Data

To appreciate the elegance of the Iceberg architecture, we must examine the sequence of events that occurs when a compute engine writes data to the table. 

Apache Iceberg achieves ACID transactions through Optimistic Concurrency Control (OCC). This means it assumes that conflicts between writers are rare, so it allows multiple engines to prepare their writes simultaneously without locking the table.

When an engine, such as Apache Spark, wants to append data to an Iceberg table, it executes the following commit flow:

1.  **Read Current State:** The engine contacts the catalog and reads the current `metadata.json` file to understand the schema and partition spec. It notes the current snapshot ID, which serves as the "base version" for its transaction.
2.  **Write Data Files:** The engine processes the data and writes the new Parquet data files to object storage. These files are orphaned at this stage; no reader knows they exist.
3.  **Write Manifest Files:** The engine creates a new Avro manifest file. It records the paths and column level statistics for all the Parquet files it just wrote.
4.  **Write Manifest List:** The engine creates a new Avro manifest list. This new list includes the new manifest file it just created, alongside all the existing manifest files from the base version snapshot.
5.  **Write New Metadata File:** The engine creates a new `metadata.json` file. It generates a new snapshot ID and points this snapshot to the new manifest list it just created.
6.  **Atomic Commit Swap:** The engine contacts the catalog and requests a swap. It says, "Update the table pointer from the base metadata file to my new metadata file, but only if the pointer is still currently pointing to the base metadata file."

If no other engine has written to the table in the meantime, the catalog executes the swap. The transaction is instantly committed, and the new data becomes visible to all subsequent readers.

## Handling Concurrency and Retries

If the optimistic assumption fails and another engine commits a write before our engine finishes, the atomic swap in step six will fail. The catalog will reject the commit because the current metadata pointer no longer matches the base version our engine started with.

This is where Iceberg's architecture shines. In a legacy system, the job would fail entirely, requiring a costly rerun. In Iceberg, the engine automatically attempts a retry. 

Because the expensive part of the operation, writing the physical Parquet data files, is already complete and immutable, the engine does not need to reprocess the data. It simply performs the metadata steps again:
1. It reads the new `metadata.json` file to get the new base version.
2. It verifies that its new data files do not logically conflict with the changes made by the other engine. 
3. It creates a new manifest list incorporating both the other engine's manifests and its own new manifest.
4. It creates a new `metadata.json` and attempts the atomic swap again.

This retry process takes milliseconds. It ensures that massive distributed systems can write to the same table concurrently with complete safety and extreme efficiency.

## Delete Files and Row Level Updates

Handling updates and deletes in a massive data lake is notoriously difficult. If you want to delete a single row in a 10 gigabyte Parquet file, you cannot simply edit the file, as object storage objects are immutable. In the past, you had to rewrite the entire 10 gigabyte file minus the one row, which is a massive computational penalty known as write amplification.

Iceberg solves this through two different update strategies: Copy on Write (CoW) and Merge on Read (MoR).

### Copy on Write (CoW)
In Copy on Write, the engine reads the original data file, filters out the deleted rows or updates the modified rows, and writes a completely new data file. It then creates a new snapshot that removes the old data file from the manifest and adds the new data file. This slows down the write operation but guarantees that subsequent read queries are blazingly fast because there is no complexity during the read phase. 

### Merge on Read (MoR)
For workloads with high frequency updates, like streaming ingestion, Copy on Write is too slow. Iceberg provides Merge on Read. 

In Merge on Read, the engine does not rewrite the heavy data file. Instead, it writes a small "Delete File." This file simply records the file path and row positions of the data that has been deleted or updated. 

During the commit phase, the new snapshot points to both the original data file and the new delete file. When a user runs a query, the query engine reads the data file, reads the delete file in memory, and reconciles them on the fly, hiding the deleted rows from the user. This makes write operations incredibly fast, shifting the computational burden to the read phase.

## Table Maintenance: Compaction and Garbage Collection

Because Iceberg creates new snapshots, new manifest files, and new data files with every single commit, the metadata tree and the object storage bucket will eventually become bloated. If left unchecked, a table with frequent streaming updates will accumulate millions of tiny data files and thousands of obsolete snapshots, degrading query performance and driving up storage costs.

To maintain the health of the Apache Iceberg architecture, data engineering teams must run regular table maintenance routines.

### Data Compaction
If a table uses Merge on Read or receives continuous streaming inserts, it will generate thousands of tiny Parquet files and delete files. Reading thousands of tiny files is highly inefficient for query engines.

Data engineers run a compaction process (often using Apache Spark) to fix this. Compaction reads the thousands of small data files, applies any pending delete files, and rewrites the data into a smaller number of large, optimized Parquet files. It then commits a new snapshot to the metadata tree, updating the manifests to point to the large files and dropping the small files from the current state. This dramatically speeds up read performance.

### Snapshot Expiration and Garbage Collection
Every commit creates a new metadata JSON file, and old snapshots are preserved for time travel. However, an organization rarely needs to time travel back to a state from five years ago.

Organizations configure a snapshot expiration policy (e.g., retain snapshots for 30 days). A scheduled maintenance job evaluates the metadata tree. If a snapshot is older than 30 days, the job deletes the snapshot reference from the `metadata.json` file. 

Once the snapshot is expired, the garbage collection process kicks in. Iceberg evaluates all the manifest lists, manifest files, and physical Parquet data files. If an underlying data file is no longer referenced by any valid, unexpired snapshot, Iceberg securely deletes the file from the cloud object storage, freeing up space and reducing cloud infrastructure costs.

## Conclusion

The Apache Iceberg architecture represents a paradigm shift in data engineering. By deliberately moving the source of truth from implicit object storage directories to an explicit, meticulously structured metadata tree, Iceberg solves the most painful problems of the data lake.

The catalog guarantees transactional safety. The metadata files and manifest lists enable instantaneous schema and partition evolution. The manifest files provide precise file pruning, turning massive table scans into surgical data extraction. By mastering the components of the Iceberg architecture, data teams can build a [Data Lakehouse](/knowledge/data-lakehouse) capable of supporting the most demanding analytical and AI workloads at unprecedented scale.
