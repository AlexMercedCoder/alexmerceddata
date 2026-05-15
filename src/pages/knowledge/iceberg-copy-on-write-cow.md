---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Iceberg Copy-on-Write (CoW)"
description: "A comprehensive deep dive into Iceberg Copy-on-Write (CoW), covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["data updates", "file rewriting", "read optimized", "Apache Iceberg"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Copy-on-Write (CoW)

In a traditional relational database (like PostgreSQL), if you want to update a single row, the database simply goes to the specific sector on the hard drive, deletes the old data, and overwrites it with the new data.

In the Data Lakehouse, this is physically impossible. Data is stored in massive (e.g., 500MB) **[Apache Parquet](/knowledge/apache-parquet)** files sitting in [Amazon S3](/knowledge/amazon-s3). Cloud object storage is **immutable**. You cannot open a 500MB file, change a single row, and save it. 

So, how does a Data Lakehouse handle `UPDATE` or `DELETE` SQL commands? 
Apache Iceberg solves this using two distinct mathematical strategies. The first, and most common, is **Copy-on-Write (CoW)**.

## How Copy-on-Write Works

Copy-on-Write is exactly what it sounds like: to modify a file, you must copy the entire file, make your changes during the copy process, write the new file to disk, and then tell the database to ignore the old file.

Imagine an Iceberg table containing a 500MB Parquet file (`File_A.parquet`) that holds 1 million rows of customer data. 
A user submits a SQL command: `UPDATE customers SET status = 'Inactive' WHERE customer_id = 123;`

1.  **Read**: The compute engine (e.g., Spark) reads the entire `File_A.parquet` into memory.
2.  **Modify**: It locates `customer_id 123` and changes the status to 'Inactive'. The other 999,999 rows remain untouched in memory.
3.  **Write (The Copy)**: Spark writes all 1 million rows back out to S3 as a brand new file: `File_B.parquet`.
4.  **Metadata Swap**: Spark updates the Apache Iceberg metadata. It creates a new "Snapshot" of the table. In this new snapshot, Iceberg explicitly removes the pointer to `File_A` and adds a pointer to `File_B`. 

When the next user queries the table, Iceberg directs them to `File_B`. The `File_A` still exists physically on S3 (enabling Iceberg's "Time Travel" feature), but it is logically dead to the current state of the table.

## The Pros and Cons of CoW

### The Advantage: Massive Read Performance
Copy-on-Write is heavily **Read-Optimized**. 
Because the engine goes through the painful process of rewriting the entire Parquet file perfectly during the update, the resulting `File_B` is pristine. When a business analyst subsequently queries the table using Dremio or Snowflake, the read engine simply scans `File_B` at maximum speed. There is no complex logic required to figure out which rows were deleted or updated; the file is mathematically perfect.

### The Disadvantage: Write Amplification
Copy-on-Write suffers from massive **Write Amplification**. 
In our example, to change *one single row* (maybe 50 bytes of data), the compute engine had to rewrite 500 Megabytes of data. 

*   **When CoW is Good**: Batch processing. If you run a nightly ETL job that updates 500,000 rows spread across that Parquet file, CoW is highly efficient. You are rewriting the file anyway, so updating 500,000 rows takes the same amount of time as updating 1 row.
*   **When CoW is Terrible**: Streaming data. If you have a real-time CDC (Change Data Capture) pipeline that trickles in 1 update every second, CoW will completely destroy your infrastructure. It will force the cluster to rewrite the 500MB file every single second, consuming massive amounts of CPU and racking up astronomical cloud I/O costs.

## Conclusion

Copy-on-Write is the default operational mode for Apache Iceberg and most Data Lakehouse formats. It enforces a strict architectural tradeoff: it forces the Data Engineering team to pay a heavy computational penalty during the Write phase (the ETL pipeline) in order to guarantee absolute, blistering speed during the Read phase (the executive BI dashboards). For the vast majority of historical analytics and batch-oriented data warehouses, this is exactly the right tradeoff to make.
