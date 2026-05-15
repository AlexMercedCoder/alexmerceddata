---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Data as Code"
description: "A comprehensive deep dive into Data as Code, covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["branching", "merging", "Nessie", "version control"]
cta_link: "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
---

## Introduction to Data as Code

For decades, software engineers have utilized **Version Control Systems** (like Git) to manage the lifecycle of their application code. Git allows thousands of developers to work on a codebase simultaneously by branching, testing code in isolation, committing changes, and merging them back into a main production branch via automated CI/CD pipelines. If a bug is deployed to production, it can be instantly reverted.

Data Engineering, conversely, has historically operated without these safety nets. When a data pipeline executes an `INSERT` or `UPDATE` against a production data warehouse, it is an immediate, live mutation. If the pipeline contains a logic error, the production table is instantly corrupted, downstream dashboards break, and the engineering team must scramble to write complex rollback scripts to recover the lost data.

**Data as Code** is the revolutionary paradigm that brings the rigorous, isolated, and reversible workflows of Git directly to massive datasets. It allows data engineers to treat petabyte-scale data lakes with the exact same version control mechanics used for software source code.

## The Mechanics of Data as Code

Data as Code is implemented through specialized [Data Catalogs](/knowledge/data-catalogs) (such as **[Project Nessie](/knowledge/project-nessie)** or **Dremio Arctic**) managing open table formats like **Apache Iceberg**.

Because Iceberg data files (Parquet) are immutable and table states are managed entirely by metadata pointers, catalogs like Nessie can track the entire history of a lakehouse as a sequence of atomic commits. This enables Git-like operations at the catalog level.

### 1. Branching
If a data engineer is tasked with overhauling the pipeline that builds the `gold_sales` table, they do not test their logic in production. Instead, they execute a command to create a branch:
`CREATE BRANCH dev_sales_overhaul FROM main;`

This creates a Zero-Copy Clone of the entire catalog state. The engineer can now run their new PySpark or dbt jobs against the `dev_sales_overhaul` branch. They can drop columns, overwrite data, and insert millions of rows. **None of these changes affect the `main` production branch.** Business users querying `main` will continue to see the pristine, original data.

### 2. Committing and Tagging
As the ETL job progresses on the branch, every transaction is recorded as an immutable commit. Data Scientists can also use **Tags** to permanently label specific commits. For example, a data scientist might tag the catalog state at the end of Q3 as `v_2026_Q3_Financials`. This guarantees that if they ever need to retrain a machine learning model against the exact data used in that quarter, that immutable reference point is permanently locked in.

### 3. Merging (Multi-Table Transactions)
The true power of Data as Code is realized during the Merge phase.
In a traditional data lake, if an ETL pipeline needs to update 5 different tables, it must do so sequentially. If the pipeline crashes on the 4th table, the first 3 tables are already updated, leaving the database in an inconsistent, corrupted state.

With Data as Code, the ETL job updates all 5 tables on the isolated branch. Once the job finishes, the engineer runs data quality tests (e.g., using [Great Expectations](/knowledge/great-expectations)) against the branch. 
If the tests pass, they execute a merge:
`MERGE BRANCH dev_sales_overhaul INTO main;`

The catalog atomically swaps the metadata pointers for all 5 tables simultaneously. The production environment transitions from the old state to the new state in a single millisecond. It guarantees absolute consistency. 

### 4. Reverting
If a catastrophic logic error is merged into production, there is no need to write reverse-ETL scripts or restore from tape backups. The administrator simply issues a revert command:
`REVERT main TO COMMIT a1b2c3d4;`
The entire lakehouse instantly time-travels back to the exact state it was in prior to the corrupted merge.

## Conclusion

Data as Code is the final step in the maturation of [DataOps](/knowledge/dataops). By lifting Git semantics from the application layer and applying them directly to the data catalog layer, organizations can achieve a level of data reliability, isolation, and agility that was previously impossible. It transforms the data lakehouse from a brittle, scary environment where changes are feared, into a robust engineering platform where data can be branched, tested, and shipped with absolute confidence.
