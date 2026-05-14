---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Pinot"
description: "A comprehensive deep dive into Apache Pinot, covering architecture, concepts, and real-world usage in Query Engines."
date: "2026-05-14"
tags: ["OLAP", "real-time", "user-facing analytics", "distributed"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Apache Pinot

Imagine opening the LinkedIn app on your phone and clicking on the "Who Viewed Your Profile" dashboard. You instantly see a chart showing that 500 people from Dremio and 200 people from Microsoft viewed your profile in the last 90 days. 

To generate that simple chart, a database somewhere had to scan billions of web-click events, filter them specifically for your user ID, aggregate the companies, and return the answer in less than 50 milliseconds. If it took 5 seconds, you would close the app. 

Traditional Data Warehouses (like Snowflake) cannot do this. They are built to answer a few heavy queries for internal executives, not millions of simultaneous, lightweight queries for external users.

LinkedIn created **Apache Pinot** to solve this exact problem. Pinot is a real-time, distributed OLAP datastore purpose-built to deliver ultra-low latency queries for **User-Facing Analytics**.

## The Architecture of Pinot

Pinot achieves its blistering speeds through a combination of columnar storage, aggressive indexing, and a highly distributed scatter-gather query architecture.

### 1. Ingestion (Real-time and Offline)
Pinot ingests data in two ways simultaneously:
*   **Real-time Nodes**: These nodes connect directly to a message broker (like Apache Kafka). They ingest streaming events and store them entirely in RAM. This ensures that the moment an event occurs, it is instantly queryable.
*   **Offline Nodes**: Periodically, the Real-time nodes flush their RAM and convert the data into highly compressed, columnar chunks (called Segments) and store them on disk (or in cloud storage like S3). 

### 2. The Scatter-Gather Query Execution
When a user clicks "Who Viewed My Profile," the query hits a **Pinot Broker**. 
The Broker knows exactly which Segments (both Real-time and Offline) contain the relevant data. It breaks the query into tiny pieces and *scatters* them to dozens of Pinot Servers simultaneously. Each server calculates its tiny piece of the answer in milliseconds and returns it to the Broker. The Broker *gathers* the partial answers, merges them, and returns the final chart to the user.

## The Secret Weapon: Aggressive Indexing

What makes Pinot unique is its fanatical approach to indexing. In a Data Lakehouse, you might scan an entire Parquet file. In Pinot, you almost never scan.

Pinot automatically builds multiple indexes for every segment:
1.  **Inverted Index**: Similar to a search engine. If you query `WHERE company = 'Dremio'`, Pinot uses the inverted index to instantly locate the exact row numbers, bypassing a full table scan.
2.  **Star-Tree Index**: This is Pinot's crowning achievement. It is essentially a dynamic, intelligent Materialized View. If you frequently query aggregations (like "Total Views by Day"), the Star-Tree pre-calculates and stores these aggregations across different dimension hierarchies. This allows Pinot to return massive aggregations in single-digit milliseconds, regardless of how much underlying data exists.

## Apache Pinot vs. Apache Druid vs. ClickHouse

Pinot exists in the same architectural space as Druid and ClickHouse (Real-Time OLAP). 
*   **ClickHouse** is often the fastest for brute-force scanning of massive, wide tables without indexes.
*   **Druid** is excellent for log analytics and high-cardinality time-series data.
*   **Pinot** is widely considered the best choice when dealing with incredibly high concurrency (e.g., 100,000 external users clicking a dashboard simultaneously) because its Star-Tree index guarantees predictable, sub-second latency regardless of user load.

## Conclusion

Apache Pinot is a highly specialized engine. It is difficult to configure and expensive to run because it relies heavily on keeping massive amounts of data in RAM and fast SSDs. However, for companies building applications where analytics *are* the product (like Uber Eats restaurant dashboards or LinkedIn profile metrics), Pinot provides the architectural foundation necessary to deliver real-time data at consumer scale.
