---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Separation of Compute and Storage"
description: "A comprehensive deep dive into the Separation of Compute and Storage, covering architecture, concepts, and real-world usage in the Data Lakehouse."
date: "2026-05-14"
tags: ["scalability", "cloud architecture", "cost optimization"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Compute and Storage Separation

For decades, the dominant paradigm in data architecture was the monolithic, tightly-coupled system. Traditional on-premises relational databases (RDBMS) and early big data platforms like [Apache Hadoop](/knowledge/apache-hadoop) (HDFS) operated under the assumption that the disks storing the data and the CPUs processing the data must exist within the exact same physical server node. 

While this architecture maximized local I/O speeds over slower legacy networks, it created a fundamental problem: **inflexible scaling**. If your storage filled up, you had to buy a new server (adding compute you didn't need). If your processing demands spiked, you had to buy a new server (adding storage you didn't need).

The **Separation of Compute and Storage** is the foundational architectural shift that enabled the modern cloud data ecosystem. By decoupling the layer that holds the data from the layer that queries it, organizations unlocked infinite scalability, elasticity, and massive cost optimizations. This principle is the bedrock upon which the entire [Data Lakehouse](/knowledge/data-lakehouse) architecture is built.

## How Decoupling Works

In a decoupled architecture, the system is split across two independent cloud services connected by high-speed cloud networks.

### The Storage Layer (Object Storage)
The storage layer is delegated to highly durable, infinitely scalable, and incredibly cheap cloud object stores such as [Amazon S3](/knowledge/amazon-s3), Azure Data Lake Storage (ADLS), or Google Cloud Storage (GCS). 
*   **Characteristics**: You pay only for the exact gigabytes you consume. The storage layer has no awareness of SQL, query execution, or data processing. It simply stores and retrieves binary objects (e.g., Parquet files).

### The Compute Layer (Query Engines)
The compute layer consists of elastic, ephemeral clusters of servers running query engines like [Apache Spark](/knowledge/apache-spark), Trino, [Dremio](/knowledge/dremio), or Snowflake virtual warehouses.
*   **Characteristics**: You pay only for the compute time you use. Clusters can be spun up in seconds to execute a heavy query and completely shut down (scaling to zero) when idle. 

When a query is executed, the compute nodes request the necessary byte-ranges directly from the object store over the network.

## The Strategic Advantages

The separation of compute and storage provides several transformative benefits for enterprise data platforms.

### 1. Independent and Elastic Scalability
Workloads are rarely symmetric. An organization might have 10 Petabytes of compliance log data that is rarely queried. In a coupled architecture (like Hadoop), storing 10PB requires a massive cluster of servers, burning power and CPU cycles 24/7 just to keep the disks alive. 

In a decoupled architecture, you simply dump the 10PB into S3 for a low monthly fee. When an auditor occasionally needs to query it, you spin up a massive 100-node Trino cluster for exactly 20 minutes, run the query, and shut it down. You scaled storage infinitely without paying for idle compute.

### 2. Multi-Engine Interoperability
Because the data lives in a passive, centralized object store rather than being locked inside a proprietary database engine, the data is "democratized." 
*   Data Engineers can use [Apache Spark](/knowledge/apache-spark) to write ETL pipelines to the S3 bucket.
*   Data Scientists can use Python/Pandas or Ray to read the exact same files for machine learning.
*   Business Analysts can use [Dremio](/knowledge/dremio) to execute real-time BI dashboards against the same data.

There is no need to copy or move the data. The single source of truth remains in storage, while specialized compute engines are brought to the data.

### 3. Workload Isolation
In legacy databases, a heavy ETL job could monopolize the CPU, causing CEO dashboards to time out. In a decoupled environment, you can provision separate, isolated compute clusters for different teams that point to the same storage bucket.
*   **Cluster A (ETL)**: Runs heavy batch processing jobs at night.
*   **Cluster B (Marketing)**: Runs ad-hoc analytical queries.
*   **Cluster C (Executives)**: A dedicated, highly-available cluster for BI tools.

Because the compute nodes do not share CPU or RAM, there is zero resource contention. 

## The Challenge: The Network Bottleneck and Metadata

The obvious drawback to decoupling is the network. Fetching data from S3 is physically slower than reading it from a local NVMe drive. Early attempts at decoupling suffered from severe latency issues.

The industry solved this through two major innovations:
1.  **Columnar Formats ([Apache Parquet](/knowledge/apache-parquet))**: Instead of downloading entire rows of data, Parquet allows the compute engine to use HTTP Range requests to download only the specific columns needed for a query.
2.  **Advanced Metadata ([Apache Iceberg](/knowledge/apache-iceberg))**: As discussed in the Iceberg Manifest Lists architecture, Iceberg tracks data at the file and partition level. Before the compute engine ever reaches out to S3, it reads the Iceberg metadata to prune 99% of the files. The compute engine only requests the exact files containing relevant data over the network.

Furthermore, modern compute engines like Dremio utilize sophisticated local caching (e.g., C3 - Columnar Cloud Cache) on NVMe drives. If a file is fetched from S3, it is cached locally on the compute node. If a subsequent query needs the same file, it is read at local NVMe speeds, achieving the performance of a coupled architecture with all the flexibility of a decoupled one.

## Conclusion

The separation of compute and storage is not merely a feature—it is the prerequisite for the modern data era. It breaks the tyranny of monolithic scaling, ends resource contention, and fosters an open ecosystem where data is an independent asset that can be seamlessly activated by any engine. This decoupling, paired with table formats like Apache Iceberg, forms the true definition of the Open Data Lakehouse.
