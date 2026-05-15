---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Project Nessie"
description: "A comprehensive deep dive into Project Nessie, covering architecture, concepts, and real-world usage in Data Catalogs."
date: "2026-05-14"
tags: ["git for data", "branching", "version control", "data catalog"]
cta_link: "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
---

## Introduction to Project Nessie

In software engineering, Git revolutionized how developers work. Before Git, multiple developers working on the same codebase frequently overwrote each other's changes, leading to broken code and lost work. Git solved this by introducing Branching and Merging: a developer can create an isolated "branch" of the codebase, make their changes, test them, and then atomically "merge" them back into the main production line.

For decades, Data Engineering completely lacked this capability. If two data engineers ran ETL pipelines against the same Data Lake simultaneously, they often corrupted the data. If a pipeline pushed bad data to production, the only way to fix it was to write complex SQL scripts to manually reverse the damage.

**Project Nessie** is the open-source solution to this problem. Often described as "Git for Data," Nessie is a transactional Data Catalog designed specifically for [Data Lakehouses](/knowledge/data-lakehouse) (specifically those using [Apache Iceberg](/knowledge/apache-iceberg)). It brings the exact same semantics of Git (Branching, Merging, Tagging, and Reverting) directly to petabyte-scale data tables.

## How Nessie Works

To understand Nessie, you must understand that it **does not store data**. It only stores metadata pointers.

When a massive Apache Iceberg table is written to [Amazon S3](/knowledge/amazon-s3), it consists of thousands of Parquet data files and a few JSON metadata files. 
Instead of the query engine (like [Dremio](/knowledge/dremio) or Spark) keeping track of these metadata files manually, it registers them with Nessie.

Nessie maintains a cryptographic, chronological log of every single change made to the metadata across the entire lakehouse. 

### 1. Zero-Copy Branching
When a data engineer wants to ingest a massive new dataset, they do not do it in production. They execute a command:
`CREATE BRANCH dev_ingestion FROM main;`
Nessie instantly creates a new pointer referencing the current state of the metadata. It takes milliseconds and consumes 0 bytes of extra storage. The engineer configures their [Apache Spark](/knowledge/apache-spark) job to write to the `dev_ingestion` branch.
As Spark writes new data, Nessie updates the `dev_ingestion` metadata. The `main` branch is completely unaffected. Business users querying `main` see the exact same pristine data they saw yesterday.

### 2. Multi-Table Transactions (Merging)
The most powerful feature of Nessie is the atomic merge.
If the ETL pipeline updates 10 different tables on the `dev_ingestion` branch, the data engineer can run data quality tests (like [Great Expectations](/knowledge/great-expectations)) against that branch. 
If the tests pass, they execute:
`MERGE BRANCH dev_ingestion INTO main;`
Nessie atomically updates the `main` pointer to point to the new metadata. In a single millisecond, all 10 tables in production are updated simultaneously. It is impossible for a user to query the system and see 5 tables updated and 5 tables outdated. 

### 3. Time Travel and Reverts
If a bug accidentally makes it into production, the data team no longer panics. Because Nessie maintains a permanent, immutable log of every commit, an administrator can simply run a command to revert the entire `main` branch to the exact state it was in one hour ago, instantly "time-traveling" the entire lakehouse back to a pristine state.

## Nessie vs. Traditional Metastores

Historically, the Hadoop ecosystem relied on the **Hive Metastore (HMS)** to track tables. 
The HMS is essentially a massive relational database (like MySQL) that stores table locations. It is highly rigid, struggles with extreme scale, and has absolutely no concept of version control, branching, or multi-table transactions. 
Nessie was built specifically to replace the aging HMS. By utilizing a modern, Git-like architecture optimized for immutable object storage and open table formats, Nessie provides the robust transactional guarantees required for the next generation of data engineering.

## Conclusion

Project Nessie fundamentally shifts the paradigm of [DataOps](/knowledge/dataops). By elevating data management to the same rigorous, version-controlled standard as software application code, it eliminates the fear of deploying changes to the [data lakehouse](/knowledge/data-lakehouse). It empowers data teams to experiment freely in isolated branches, test their data mathematically, and execute massive, instantaneous multi-table deployments with the absolute confidence that they can revert any mistake in milliseconds.
