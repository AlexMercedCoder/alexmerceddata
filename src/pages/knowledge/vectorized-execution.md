---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Vectorized Execution"
description: "A comprehensive deep dive into Vectorized Execution, covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["SIMD", "CPU cache", "columnar processing", "query engines"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Vectorized Execution

In the continuous quest to make databases faster, software engineers spent decades optimizing hard drives, memory management, and network I/O. However, as data architectures shifted from spinning hard drives to high-speed NVMe SSDs and entirely in-memory processing (like [Apache Spark](/knowledge/apache-spark)), a new, unexpected bottleneck emerged: **The CPU itself.**

Traditional relational databases (like PostgreSQL or MySQL) execute queries using a "Volcano" or "Row-at-a-Time" processing model. 
If an analyst runs `SELECT SUM(salary) FROM employees`, the database engine reads Row 1, extracts the salary, adds it to a running total. Then it calls a function to read Row 2, extracts the salary, adds it to the total. This continues for every single row. 

While this sounds logical, it is disastrously inefficient for modern CPUs. The overhead of calling the "read row" function 100 million times consumes more processing power than the actual mathematical addition. 

**Vectorized Execution** is the modern software architecture designed to fix this. It abandons row-by-row processing, processing data in massive, contiguous blocks (vectors), completely revolutionizing the speed of analytical query engines.

## The Mechanics of Vectorization

To understand Vectorized Execution, we must look at how modern CPUs interact with memory.

### The CPU Cache Bottleneck
CPUs are incredibly fast, but RAM is relatively slow. To bridge the gap, CPUs have tiny amounts of ultra-fast memory called L1/L2 Cache. When a CPU asks for data, it pulls a chunk of data from RAM into the Cache. 

In a traditional row-based database, a row contains mixed data types (e.g., `[String: John, Int: 35, String: NY]`). If the CPU only wants to sum the ages, it pulls the entire row into its tiny cache, wasting 80% of the cache space on irrelevant strings. It does the math, flushes the cache, and pulls the next row. This constant flushing and reloading is called a **Cache Miss**, and it destroys performance.

### Columnar Memory and Vectors
Vectorized Execution engines (like [Dremio](/knowledge/dremio), Snowflake, or [ClickHouse](/knowledge/clickhouse)) never use row-based memory. They use **Columnar Memory** (specifically, the **[Apache Arrow](/knowledge/apache-arrow)** format). 

In Arrow, all the `salary` integers are stored perfectly next to each other in RAM. 
Instead of processing one row at a time, a Vectorized engine grabs a "Vector" (a contiguous batch of, say, 4,096 salaries) and loads it into the CPU cache in one single swoop. Because the data is uniform, there is zero wasted cache space.

### SIMD (Single Instruction, Multiple Data)
Once the vector of 4,096 integers is sitting in the CPU cache, the query engine utilizes a specific hardware capability present in all modern Intel and AMD processors called **SIMD**.

Normally, a CPU executes one instruction on one piece of data (`Add A to B`).
SIMD allows the CPU to execute *one instruction on multiple pieces of data simultaneously*. The engine issues a single CPU command: `"Add these 4,096 numbers together."` The CPU executes the addition across the entire vector in a single clock cycle.

By eliminating 4,095 function calls and perfectly utilizing the CPU cache, Vectorized Execution can accelerate analytical queries by 10x to 100x compared to legacy row-based databases.

## Impact on the Data Ecosystem

Vectorized execution is the invisible technology that makes the modern [Data Lakehouse](/knowledge/data-lakehouse) viable.

1.  **Synergy with Parquet**: [Apache Parquet](/knowledge/apache-parquet) is a columnar storage format on disk. When a Vectorized engine reads a Parquet file, it does not need to parse the data into rows. It simply copies the column straight from the disk into a vectorized [Apache Arrow](/knowledge/apache-arrow) memory buffer and immediately executes SIMD mathematics on it. The synergy between columnar storage and vectorized compute is the core of modern performance.
2.  **Engine Evolution**: Legacy Hadoop engines (like [Apache Hive](/knowledge/apache-hive)) originally used row-at-a-time processing, which is why they were so slow. Modern engines like Trino, [Dremio](/knowledge/dremio), and [Apache Spark](/knowledge/apache-spark) (via its Photon engine or DataFusion) have completely rebuilt their internal architectures around Vectorized Execution.
3.  **Data Science Acceleration**: The transition from legacy Python libraries (which process data row-by-row) to modern libraries like **Polars** (which uses [Apache Arrow](/knowledge/apache-arrow) and vectorized Rust execution) has brought this exact same 100x speed increase to laptops and local data science workflows.

## Conclusion

Vectorized Execution is a masterclass in hardware-aware software engineering. By acknowledging that modern CPUs are starved for data, vectorized engines abandon the intuitive row-by-row processing model in favor of dense, columnar batches. By maximizing CPU cache efficiency and unlocking the power of SIMD instructions, vectorization provides the raw computational horsepower required to analyze petabyte-scale datasets at the speed of thought.
