---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Open Table Formats"
description: "A comprehensive deep dive into Open Table Formats, covering architecture, concepts, and real-world usage in the Data Lakehouse."
date: "2026-05-14"
tags: ["Iceberg", "Delta", "Hudi", "interoperability"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Open Table Formats

To understand the monumental importance of Open Table Formats, you must understand the two major flaws of the previous data generation.

1.  **The Data Warehouse Lock-in**: If you loaded data into a proprietary warehouse (like Oracle or Teradata), they converted your data into a secret, proprietary file format. If you wanted to leave Oracle, or use a different tool to analyze that data, you couldn't. Your data was held hostage by the vendor.
2.  **The Data Lake Chaos**: To escape lock-in, companies dumped their data as open-source Parquet files into [Amazon S3](/knowledge/amazon-s3) (the Data Lake). But S3 is just a hard drive. It has no transactional guarantees. If two people tried to write a file at the same time, the data corrupted. You couldn't run a SQL `UPDATE` or `DELETE` command. 

The industry needed a solution that provided the transactional perfection of a Data Warehouse, but kept the data stored in open, vendor-neutral files on cheap cloud storage.

This solution is the **Open Table Format**. It is the architectural foundation of the modern **[Data Lakehouse](/knowledge/data-lakehouse)**.

## What is an Open Table Format?

An Open Table Format (like [Apache Iceberg](/knowledge/apache-iceberg), [Delta Lake](/knowledge/delta-lake), or [Apache Hudi](/knowledge/apache-hudi)) is not a query engine, and it is not a storage platform. It is a **Metadata Abstraction Layer**.

When you write an Iceberg table, two things are saved to your [Amazon S3](/knowledge/amazon-s3) bucket:
1.  **The Data Files**: Standard, open-source [Apache Parquet](/knowledge/apache-parquet) files.
2.  **The Metadata Files**: A collection of JSON and Avro files that explicitly map out exactly which Parquet files belong to the table.

### How it Solves the Problem
When an engine (like [Dremio](/knowledge/dremio), Spark, or Snowflake) wants to query the table, it doesn't blindly scan S3. It reads the Iceberg Metadata.

*   **ACID Transactions**: Because Iceberg controls the metadata, it can guarantee transactions. If an engine writes 100 new Parquet files, they are invisible. Only when the write is 100% complete does Iceberg instantly update the metadata pointer to include the new files.
*   **Row-Level Updates/Deletes**: If an analyst runs a `DELETE` command, Iceberg handles the complex mechanics of rewriting the specific Parquet file or logging a delete file, allowing the Data Lake to behave exactly like a relational database.
*   **Time Travel**: Because the metadata keeps a historical log of every single change, an analyst can query the table exactly as it existed 30 days ago.

## The Big Three: Iceberg, Delta, and Hudi

The Open Table Format wars began in the late 2010s, dominated by three major open-source projects.

1.  **Apache Iceberg**: Originally developed at Netflix. It is widely considered the most truly "open" standard, boasting the largest ecosystem of native integrations across AWS, Google Cloud, Snowflake, [Dremio](/knowledge/dremio), and open-source engines. It was designed from the ground up for massive, petabyte-scale table metadata management.
2.  **[Delta Lake](/knowledge/delta-lake)**: Developed by [Databricks](/knowledge/databricks). It is heavily tied to the [Apache Spark](/knowledge/apache-spark) ecosystem and optimized for the [Databricks](/knowledge/databricks) platform. It is exceptionally popular due to its seamless developer experience within [Databricks](/knowledge/databricks).
3.  **[Apache Hudi](/knowledge/apache-hudi)**: Originally developed at Uber. Hudi (Hadoop Upserts Deletes and Incrementals) was explicitly designed for massive streaming workloads and heavy real-time Upserts.

## The Promise of Interoperability

The defining characteristic of these formats is the word **Open**. 

Because the specifications for Iceberg are public and open-source, any vendor can build an engine to read and write it. 
An organization can use [Apache Flink](/knowledge/apache-flink) to ingest streaming data into an Iceberg table, use [Apache Spark](/knowledge/apache-spark) to run a massive batch transformation on that table, use Snowflake to run a highly secure executive dashboard on it, and use Dremio to federate it—all without moving or copying a single byte of data.

## Conclusion

Open Table Formats represent the final decoupling of compute from storage. By providing a standardized, vendor-neutral layer of metadata on top of cloud object storage, they stripped proprietary Data Warehouses of their core advantage. They transformed the chaotic Data Lake into the highly reliable Data Lakehouse, ensuring that enterprises permanently retain ownership, flexibility, and control over their most valuable data assets.
