---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Compute Pushdown"
description: "A comprehensive deep dive into Compute Pushdown, covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["query optimization", "data source", "filtering", "performance"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Compute Pushdown

In modern decoupled data architectures, data is often stored far away from the engine executing the query. For example, a business analyst might run a massive SQL aggregation using a federated query engine (like Dremio or Trino), but the actual data resides inside a proprietary operational database (like Oracle), a cloud data warehouse (like Snowflake), or even an external REST API.

If the analyst executes the query:
`SELECT region, SUM(sales) FROM oracle_db.sales_data WHERE region = 'EMEA' GROUP BY region`

The naive, brute-force way to execute this query is for the federated engine to pull *every single row* from the Oracle database over the network, load the massive dataset into its own RAM, filter out the non-EMEA rows, calculate the sum, and return the answer. If the table has 10 billion rows, this network transfer will take hours and crash the system.

**Compute Pushdown** (often called Query Pushdown) is the fundamental optimization technique that prevents this disaster.

Compute Pushdown is the process where a high-level query engine intelligently delegates (pushes down) portions of the SQL computation directly to the underlying data source, allowing the source system to perform the heavy lifting before any data is transferred over the network.

## The Mechanics of Compute Pushdown

Compute pushdown relies on a sophisticated component within the query engine called the **Query Planner** or **Cost-Based Optimizer (CBO)**.

When the query engine receives a SQL statement, the optimizer analyzes the capabilities of the underlying storage system.

### 1. Filter Pushdown (Predicate Pushdown)
This is the most common form of pushdown. In the example above, the query contains a `WHERE region = 'EMEA'` clause.
Instead of downloading all 10 billion rows, the Trino/Dremio engine rewrites the query and sends the exact SQL string `SELECT * FROM sales_data WHERE region = 'EMEA'` directly to the Oracle database. 
Oracle, which is highly optimized for its own storage, executes the filter natively. It only returns the 5 million rows that belong to EMEA over the network. Network I/O is reduced by 99.9%.

### 2. Projection Pushdown (Column Pruning)
If a table has 100 columns, but the user's `SELECT` statement only asks for 2 columns (`region` and `sales`), the query engine pushes down a projection constraint. It instructs the source database (or the Parquet file reader) to completely ignore the other 98 columns, extracting and transmitting only the required data.

### 3. Aggregation Pushdown
Modern query engines can push down complex mathematical operations. 
In our example, the engine can push the entire `SUM()` and `GROUP BY` operation down to Snowflake or Oracle. The source database calculates the final answer natively and returns a single row containing the result: `[EMEA, $500,000]`. The federated engine does virtually zero processing and transfers only a few bytes over the network.

## Compute Pushdown in the Lakehouse (Iceberg/Parquet)

While pushdown is conceptually easy to understand when querying another relational database, it becomes slightly more complex—and vastly more important—when querying flat files in a Data Lakehouse.

Object storage (like Amazon S3) has no native compute capabilities; S3 cannot execute a SQL `SUM()`. Therefore, compute pushdown in a lakehouse refers to pushing the logic down into the *file reader* processes (the low-level software libraries scanning the Parquet files).

**Apache Iceberg** and **Apache Parquet** are designed explicitly to support aggressive pushdown:
1.  **Metadata Level (Iceberg)**: When Dremio evaluates `WHERE date = '2026-01-01'`, it pushes that filter into the Iceberg manifest files. Iceberg instantly identifies that 9,000 out of 10,000 Parquet files do not contain data for that date, and Dremio completely skips downloading them.
2.  **File Level (Parquet)**: For the 1,000 files Dremio does download, the Parquet reader uses the file's footer statistics (min/max values) to skip irrelevant chunks of data (Row Groups) within the file itself.

## The Importance in Data Virtualization

Compute Pushdown is the primary enabling technology for **Data Virtualization** and the **Data Mesh**. 

Without robust pushdown capabilities, organizations are forced to use brittle ETL pipelines to physically copy data from operational databases into a central data warehouse just to achieve decent query performance. 
With advanced Compute Pushdown, an engine like Dremio can execute a SQL join between an Oracle database and a Snowflake database in real-time. By pushing the heavy filtering and aggregations down to the respective source systems simultaneously, the virtualized query returns in seconds without ever permanently moving or duplicating the underlying data.

## Conclusion

In the era of distributed data, network bandwidth is the ultimate bottleneck. Compute Pushdown is the architectural strategy that honors a fundamental law of big data: *Move the compute to the data, do not move the data to the compute.* By intelligently delegating SQL operations to the source systems and storage layers, modern query engines deliver blazing-fast federated analytics across highly fragmented enterprise infrastructures.
