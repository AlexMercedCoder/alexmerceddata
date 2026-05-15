---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Upserts (Update and Insert)"
description: "A comprehensive deep dive into Upserts, covering concepts and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["merge operations", "CDC", "data synchronization", "lakehouse"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Upserts

In the world of data ingestion, moving data from an operational database (like PostgreSQL) into an analytical data warehouse (like Snowflake or an Iceberg Lakehouse) presents a complex logic problem. 

If you receive a file containing 10,000 user records from the operational database, you cannot simply `INSERT` them into the data warehouse. What if 5,000 of those users already exist in the warehouse? If you `INSERT` them, you will create duplicates. 

To prevent this, legacy ETL pipelines had to execute complex logic:
1. Query the warehouse to see if User ID `123` exists.
2. If it does exist, execute an `UPDATE` command to modify their email address.
3. If it does not exist, execute an `INSERT` command to add the new user.

Writing this `IF/ELSE` logic for billions of rows is computationally agonizing and highly prone to error.

The solution is the **Upsert** (a portmanteau of "Update" and "Insert"). An Upsert is a single, atomic database operation that automatically figures out whether a record should be updated or inserted based on a primary key.

## The SQL Implementation: MERGE INTO

In modern SQL databases and [Open Table Formats](/knowledge/open-table-formats), the Upsert logic is executed using the standard `MERGE INTO` statement. 

Instead of writing Python logic to check for existence, the data engineer simply hands the 10,000 new records (the Source) to the database (the Target) and writes:

```sql
MERGE INTO lakehouse.users AS target
USING incoming_kafka_stream AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN
  UPDATE SET target.email = source.email, target.last_login = source.last_login
WHEN NOT MATCHED THEN
  INSERT (user_id, email, last_login) VALUES (source.user_id, source.email, source.last_login)
```

The database engine handles the complexity internally. It executes an incredibly fast join between the Source and the Target, instantly resolving the logic and applying the mutations in a single, ACID-compliant transaction.

## The Role of Upserts in CDC

Upserts are the absolute foundational mechanism for **Change Data Capture (CDC)** architectures. 

In a CDC pipeline, a tool like Debezium constantly watches an operational database for changes. Whenever a row changes, it publishes a tiny JSON event to [Apache Kafka](/knowledge/apache-kafka): `{"operation": "update", "user_id": 123, "email": "new@email.com"}`. 

A streaming engine (like [Apache Flink](/knowledge/apache-flink) or Spark Structured Streaming) reads these thousands of events per second from Kafka. Because events arrive continuously, and because networks can duplicate messages, the streaming engine relies entirely on Upserts. By executing continuous `MERGE INTO` operations against the [Apache Iceberg](/knowledge/apache-iceberg) table, the engine guarantees that no matter how many times an update arrives, the final Iceberg table remains perfectly synchronized with the upstream operational database.

## Upserts in the Data Lakehouse

Historically, executing an Upsert against a Data Lake (Hadoop/S3) was impossible because Parquet files are immutable. You couldn't update a row; you had to rewrite the entire file.

The invention of **Apache Iceberg**, **[Delta Lake](/knowledge/delta-lake)**, and **[Apache Hudi](/knowledge/apache-hudi)** explicitly solved this. These formats provide the metadata layer required to execute massive `MERGE INTO` operations against cloud object storage. 

Depending on the configuration, they handle the Upsert in two ways:
1.  **Copy-on-Write**: It copies the affected Parquet file, applies the Upserts in memory, and writes a new file to S3.
2.  **Merge-on-Read**: It simply writes a tiny "Delete File" (to neutralize the old version of the row) and inserts the new version into a new data file, allowing Upserts to happen in milliseconds.

## Conclusion

The Upsert is the most important data mutation command in modern analytics. By abstracting the complex existence-checking logic away from the developer and pushing it deep into the database engine, Upserts enable resilient, idempotent data pipelines. They are the engine that powers real-time database replication, ensuring the [Data Lakehouse](/knowledge/data-lakehouse) remains an exact, mathematically perfect reflection of the operational business.
