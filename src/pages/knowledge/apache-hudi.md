---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Hudi"
description: "A comprehensive deep dive into Apache Hudi, covering architecture, concepts, and real-world usage in Data Formats."
date: "2026-05-14"
tags: ["table formats", "upserts", "incremental processing", "lakehouse"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Apache Hudi

In the mid-2010s, organizations attempting to build massive data lakes on Hadoop or [Amazon S3](/knowledge/amazon-s3) ran into a brick wall: dealing with changing data. Data lakes were built on immutable files (like Parquet). If a user updated their profile picture on a mobile app, pushing that single database `UPDATE` to the data lake required a data engineer to write a complex Spark job to read a massive Parquet file, apply the update in memory, and rewrite the entire file back to S3. 

This process was brutally slow, incredibly expensive, and impossible to scale for real-time streaming use cases.

**Apache Hudi (Hadoop Upserts Deletes and Incrementals)** was created by Uber in 2016 to solve this exact problem. Hudi is an open-source [data lakehouse](/knowledge/data-lakehouse) table format that sits on top of raw storage. It brings database-like transactional capabilities (ACID) to the data lake, and it was the first open-source project to solve the massive engineering challenge of performing fast, record-level updates and deletes on cloud object storage.

## The Core Capabilities of Hudi

Hudi's architecture is explicitly designed around three primary operations that traditional data lakes struggled with:

### 1. Upserts (Update or Insert)
Hudi allows streaming ingestion engines (like Kafka Connect or Spark Streaming) to ingest a continuous stream of Change Data Capture (CDC) events from operational databases. If Hudi sees an `UPDATE` event for User 123, it natively "upserts" it into the lake, handling the complex file management behind the scenes without forcing the user to write heavy merge logic.

### 2. Deletes
With the advent of privacy laws like [GDPR and CCPA](/knowledge/gdpr-and-ccpa), organizations must be able to securely delete individual user records from massive datasets upon request. Hudi natively supports row-level deletes, locating and removing specific records from underlying Parquet files efficiently.

### 3. Incremental Processing
Before Hudi, if a downstream pipeline needed to calculate new metrics, it had to scan the entire data lake table. Hudi introduced the ability to pull a stream of *incremental changes*. A downstream Spark job can ask Hudi: *"Give me only the records that have changed since 8:00 AM."* Hudi acts like a message queue, returning only the modified rows. This drastically reduces compute costs by eliminating full-table scans.

## Hudi Storage Types: CoW vs MoR

To optimize performance for different workloads, Hudi requires users to configure a table as one of two distinct storage types.

### Copy-on-Write (CoW)
In a CoW table, data is stored exclusively in columnar Parquet files. When an update arrives, Hudi immediately reads the affected Parquet file, applies the update, and synchronously writes a brand new Parquet file.
*   **Pros**: Query performance is blazing fast because the compute engine (like Trino or Presto) only has to read highly optimized Parquet files.
*   **Cons**: Write performance is slow (high write amplification). It is not suited for continuous, millisecond streaming ingestion.

### Merge-on-Read (MoR)
In a MoR table, data is stored using a combination of columnar files (Parquet) and row-based log files (Avro). When an update arrives, Hudi does not rewrite the Parquet file. Instead, it quickly appends the update to an Avro log file. 
During a read query, the engine reads the base Parquet file, reads the Avro log file, and merges them *on the fly in memory* to present the most current state. Later, a background compaction process asynchronously merges the Avro logs into the base Parquet files.
*   **Pros**: Blazing fast write speeds, perfectly suited for high-throughput streaming ingestion.
*   **Cons**: Slower query speeds, as the compute engine must execute complex merge logic during the read.

## Hudi vs. Iceberg and Delta Lake

Apache Hudi, [Apache Iceberg](/knowledge/apache-iceberg), and [Delta Lake](/knowledge/delta-lake) form the "Big Three" of modern open table formats.

*   **Iceberg** was designed primarily by Netflix to solve massive metadata scaling and query planning issues, utilizing a hierarchical tree of manifest files. It excels in decoupled architectures spanning millions of files.
*   **Hudi** was designed by Uber primarily to solve streaming ingestion and incremental processing. It excels in environments where the primary goal is quickly landing massive, continuous streams of database updates into the lake.

## Conclusion

Apache Hudi was a pioneer in the evolution of the [Data Lakehouse](/knowledge/data-lakehouse). By introducing native upserts, deletes, and incremental pulling to immutable object storage, it bridged the gap between the chaotic data lake and the structured data warehouse. For organizations dealing with heavy streaming workloads and complex Change Data Capture pipelines, Hudi remains one of the most powerful and mature table formats in the open-source ecosystem.
