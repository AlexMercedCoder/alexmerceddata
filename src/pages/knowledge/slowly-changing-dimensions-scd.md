---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Slowly Changing Dimensions (SCD)"
description: "A comprehensive deep dive into Slowly Changing Dimensions (SCD), covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["data modeling", "historical data", "Kimball", "data warehousing"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Slowly Changing Dimensions

In the realm of Data Warehousing and Dimensional Modeling (popularized by Ralph Kimball), a "Dimension" is a table that contains descriptive attributes about a business entity—such as Customers, Products, or Employees. These attributes provide the context for the numerical facts (e.g., the Sales amount).

While facts happen instantaneously (a sale occurs on Tuesday at 2:00 PM), dimensional attributes change slowly and unpredictably over time. 
*   A customer gets married and changes their last name.
*   A product is moved from the "Electronics" category to the "Home Goods" category.
*   An employee is promoted from "Junior Analyst" to "Senior Analyst."

How a database handles these historical mutations is critical. If an employee was a Junior Analyst when they made a sale in 2024, but a Senior Analyst in 2026, how should a report attribute the 2024 sale? 

The methodologies used to track and store these historical changes are known as **Slowly Changing Dimensions (SCD)**. There are several strategies (Types) for handling SCDs, each with different architectural complexities and business implications.

## The Primary Types of SCD

While data architects have defined up to seven different types of SCDs, the vast majority of enterprise data pipelines rely on Type 1, Type 2, and occasionally Type 3.

### SCD Type 1: Overwrite (No History)
Type 1 is the simplest approach. When an attribute changes in the source system, the old value in the data warehouse is completely overwritten with the new value. No historical record is kept.

*   **Example**: John Smith updates his address from New York to London. The pipeline runs an `UPDATE` statement, replacing "New York" with "London" in John's row.
*   **Pros**: Incredibly simple to implement and maintain. Keeps the dimension table small and performant.
*   **Cons**: Total loss of historical truth. If you run a report on sales by region for last year, all of John's past purchases in New York will now falsely appear under London.
*   **Use Case**: Used for trivial data where history does not matter (e.g., fixing a typo in a customer's name, updating a phone number).

### SCD Type 2: Add New Row (Full History)
Type 2 is the gold standard for enterprise data warehousing. It preserves the complete, unbroken historical timeline of a dimension. Instead of overwriting data, a Type 2 pipeline inserts a completely new row for the updated entity.

To manage this, the dimension table requires three new metadata columns: `effective_date`, `expiration_date`, and a boolean `is_current` flag. Furthermore, the table cannot rely solely on the source system's ID (the Natural Key); it must generate a unique Surrogate Key for every row.

*   **Example**: John moves to London on May 1st.
    *   Row 1: Surrogate Key: 101, Name: John, City: New York, Effective: Jan 1, Expiration: April 30, Is_Current: False
    *   Row 2: Surrogate Key: 102, Name: John, City: London, Effective: May 1, Expiration: 9999-12-31, Is_Current: True
*   **Pros**: Absolute historical accuracy. Reports run exactly as the data existed at the time of the transaction.
*   **Cons**: Highly complex ETL/ELT logic required to manage the surrogate keys, date bounding, and flagging. The dimension table grows exponentially over time.
*   **Use Case**: Critical business dimensions like Employee Hierarchy, Product Categories, or Customer Demographics.

### SCD Type 3: Add New Column (Partial History)
Type 3 is a compromise. It tracks only the *previous* value of an attribute by adding a specific "previous_value" column to the existing row. It overwrites the "current_value" column.

*   **Example**: The table has columns `current_city` and `previous_city`. When John moves to London, `previous_city` becomes "New York" and `current_city` becomes "London".
*   **Pros**: Allows analysts to see the immediate past state without the massive table growth and complexity of Type 2.
*   **Cons**: It only tracks one step back. If John moves a third time to Paris, the "New York" record is permanently overwritten and lost.
*   **Use Case**: When the business explicitly only cares about the current state and the immediately preceding state (e.g., tracking a user's current subscription tier vs. previous tier).

## Implementing SCD Type 2 in the Data Lakehouse

Historically, managing SCD Type 2 on a Data Lake was nearly impossible because data lakes relied on immutable Parquet files. Updating the `expiration_date` on an old row meant rewriting the entire massive file.

Modern table formats like **Apache Iceberg** completely solved this. Because Iceberg supports ACID transactions and row-level `MERGE INTO` operations (Merge-on-Read), data engineers can now implement complex SCD Type 2 pipelines natively on S3.

Using a tool like **dbt (data build tool)** connected to a lakehouse engine (like Trino or Spark), engineers can define an "SCD Snapshot" configuration. Dbt will automatically detect changes in the source data, execute the complex Iceberg `MERGE` statements to expire the old records, and `INSERT` the new records, fully automating the SCD Type 2 lifecycle directly on the lake.

## Conclusion

Mastering Slowly Changing Dimensions is a rite of passage for data engineers. Choosing between overwriting data (Type 1) and preserving a pristine historical timeline (Type 2) dictates the analytical capabilities of the entire business. Thanks to the evolution of the Data Lakehouse and table formats like Apache Iceberg, implementing rigorous historical tracking at a petabyte scale is now more efficient and automated than ever before.
