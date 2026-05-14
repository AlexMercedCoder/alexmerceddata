---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Change Data Capture (CDC)"
description: "A comprehensive deep dive into Change Data Capture (CDC), covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["streaming", "database logs", "Debezium", "incremental updates"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Change Data Capture (CDC)

In modern enterprise data architectures, keeping the analytical data lakehouse synchronized with the operational databases (the systems running the actual applications) is a foundational challenge. 

Historically, data engineers solved this using **Batch ETL (Extract, Transform, Load)**. Every night at 2:00 AM, a script would wake up, query the operational database for all records modified in the last 24 hours (e.g., `SELECT * FROM orders WHERE updated_at > yesterday`), and dump the results into the data warehouse. 

This batch approach has two fatal flaws:
1.  **Stale Data**: Business analysts are always looking at data that is up to 24 hours old.
2.  **Performance Impact**: Running massive analytical queries against an operational database (like PostgreSQL or MySQL) consumes heavy CPU and I/O, often slowing down the actual application for end-users.

**Change Data Capture (CDC)** is the modern, real-time solution to this problem. Instead of querying the database for changes, a CDC system silently listens to the database's internal transaction logs and instantly streams every single `INSERT`, `UPDATE`, and `DELETE` event to the data lakehouse as it happens.

## How CDC Works

Nearly all robust relational databases (PostgreSQL, MySQL, Oracle, SQL Server) maintain an internal transaction log (like the Write-Ahead Log or WAL in Postgres, or the binlog in MySQL). These logs record every single mutation applied to the database to ensure crash recovery. 

CDC tools exploit these logs to extract data without ever executing a SQL query against the database engine.

### The Debezium Architecture
The open-source industry standard for CDC is **Debezium**. Debezium operates as a connector, typically deployed alongside Apache Kafka.

1.  **Log Reading**: Debezium connects directly to the PostgreSQL WAL. It reads the raw byte-stream of the transaction log. Because it reads the log file from disk (or via replication protocols) rather than executing `SELECT` queries, the performance impact on the operational database is near zero.
2.  **Event Generation**: When an application updates a customer's address, the database writes this to the WAL. Debezium instantly detects the write, parses it, and transforms it into a structured JSON or Avro event. 
    *   The event payload contains the *before* state of the row, the *after* state of the row, and the type of operation (`u` for update, `i` for insert, `d` for delete).
3.  **Streaming**: Debezium publishes this event to an Apache Kafka topic (e.g., `customer_db.public.users`). 
4.  **Ingestion**: A downstream streaming engine (like Apache Flink or Kafka Connect) consumes the Kafka topic and immediately applies the changes to the analytical table in the data lakehouse.

## Applying CDC to the Data Lakehouse

Streaming CDC events into a traditional data lake was historically very difficult. Because data lakes consisted of immutable Parquet files, applying a single `UPDATE` or `DELETE` event required rewriting the entire Parquet file, which was disastrous for performance.

**Apache Iceberg** solved this problem by introducing **Row-Level Deletes** (specifically Merge-on-Read).

When a CDC event arrives indicating that Row ID `123` was updated, the ingestion engine (e.g., Flink) does not rewrite the existing data files. Instead, it:
1.  Writes the new, updated row into a new data file.
2.  Writes a **Delete File** (a positional or equality delete) that instructs the query engine to ignore the old version of Row ID `123` during read time.

This allows the lakehouse to ingest a continuous, high-throughput stream of CDC updates and deletes with sub-second latency, without burning compute resources rewriting massive files. Background maintenance tasks (Compaction) will later asynchronously clean up the delete files to maintain peak read performance.

## Challenges of CDC

While CDC is incredibly powerful, it introduces distributed systems complexity:

1.  **Schema Evolution**: If a developer drops a column in the operational PostgreSQL database, the CDC event stream will instantly reflect that change. The downstream data lakehouse table (Iceberg) must be configured to seamlessly handle this schema evolution without crashing the ingestion pipeline.
2.  **Ordering Guarantees**: Network issues can cause events to arrive out of order. If an `UPDATE` event arrives before the `INSERT` event for the same row, the pipeline must have logic to buffer, reorder, or handle the state correctly.
3.  **Initial Snapshotting**: When you first turn on a CDC pipeline for a database that already has 500 million rows, Debezium must perform an initial "snapshot" to copy the existing data before it begins streaming the log. Managing this massive initial load without locking the database is a complex engineering task.

## Conclusion

Change Data Capture is the critical bridge connecting operational systems to analytical lakehouses. By replacing sluggish, resource-heavy batch queries with lightweight, real-time log tailing, CDC ensures that the data lakehouse is a live, accurate reflection of the business. When combined with modern table formats like Apache Iceberg, organizations can finally achieve real-time analytics at a fraction of the cost of legacy data warehouses.
