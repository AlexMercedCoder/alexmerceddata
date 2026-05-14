---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Data Vault Architecture"
description: "A comprehensive deep dive into Data Vault Architecture, covering concepts and real-world usage in Data Architecture."
date: "2026-05-14"
tags: ["hubs", "links", "satellites", "agile data warehouse"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Data Vault Architecture

In the landscape of Enterprise Data Warehousing, two architectural paradigms have historically dominated: Ralph Kimball's Dimensional Modeling (Star Schemas) and Bill Inmon's Corporate Information Factory (3NF normalization). 

While both are effective, they struggle with extreme agility. If a massive global enterprise undergoes a corporate merger and suddenly needs to ingest 50 new, fundamentally different operational databases into their existing data warehouse, modifying a rigidly structured Star Schema or heavily normalized 3NF database is a grueling, multi-month engineering effort that often breaks existing ETL pipelines.

**Data Vault 2.0**, invented by Dan Linstedt, is a hybrid data modeling methodology designed explicitly for extreme agility, auditability, and massive scale. It is mathematically designed so that adding new data sources requires zero refactoring of the existing architecture.

## The Core Components of a Data Vault

Data Vault Abandons traditional tables in favor of a strictly defined, three-component structure: **Hubs**, **Links**, and **Satellites**.

### 1. Hubs (The Core Business Keys)
A Hub represents a core business entity (like a Customer, Product, or Store). 
Hubs contain *no descriptive attributes* (no names, no addresses). They exist solely to track the unique, immutable business identifier (the Natural Key) across the entire enterprise.
*   **Columns in a Hub**: Surrogate Hash Key (the primary key), the Natural Business Key (e.g., `Customer_ID`), the Load Timestamp (when it was first seen), and the Record Source (where it came from).
*   *Why?* If a customer exists in both Salesforce and a legacy AS400 system, they share the same Hub row. The Hub is the anchor.

### 2. Links (The Intersections)
A Link represents a transaction or a relationship between two or more Hubs. 
Like Hubs, Links contain no descriptive attributes. They only contain the Surrogate Hash Keys of the Hubs they connect.
*   **Example**: A `Link_Order` table connects the `Hub_Customer`, `Hub_Product`, and `Hub_Store` tables.
*   *Why?* This heavily decoupled structure means many-to-many relationships are trivial to track and modify without altering table schemas.

### 3. Satellites (The Descriptive Context)
Satellites contain the actual descriptive data (the context) that traditional dimension tables hold. They are always attached to either a Hub or a Link.
Crucially, Satellites are **insert-only**. They inherently track historical changes (SCD Type 2) because every time an attribute changes in the source system, a new row is appended to the Satellite with a new timestamp.
*   **Example**: A `Sat_Customer_Demographics` table attached to the `Hub_Customer`, containing Name, Age, and Address. 
*   *Why separate them?* If you acquire a new company that tracks "Customer Shoe Size," you don't alter the existing `Sat_Customer_Demographics` table. You simply create a brand new `Sat_Customer_Shoe_Size` table and attach it to the existing `Hub_Customer`. Zero refactoring required.

## The Raw Vault vs. The Business Vault

Data Vault strictly separates raw data ingestion from business logic transformation.

### The Raw Vault
The Raw Vault is an unadulterated, 100% historically accurate copy of the source data, modeled into Hubs, Links, and Satellites. No business logic (like standardizing currency or fixing typos) is allowed in the Raw Vault. It serves as an auditable system of record. If a data scientist needs raw, untouched data for a machine learning model, they query the Raw Vault.

### The Business Vault
The Business Vault sits on top of the Raw Vault. Here, data engineers apply complex business rules, aggregations, and data cleansing. The outputs are often materialized as new "Business Satellites" or "Computed Links."

## Bridging the Gap: The Information Delivery Layer

While a Data Vault is incredibly agile for data engineers to build and maintain, it is an absolute nightmare for a business analyst to query. A simple query might require joining 12 different Hub, Link, and Satellite tables.

Therefore, Data Vault architecture dictates the creation of an **Information Delivery Layer** (often known as Data Marts). 
Data Engineers write SQL views (often running on massive MPP engines like Dremio or Snowflake) that sit on top of the Data Vault. These views automatically join the Hubs, Links, and Satellites together and project them outwards as a beautiful, simple **Star Schema**. 

The business analyst connects Tableau to the Star Schema views, completely unaware of the complex Data Vault machinery churning beneath the surface.

## Conclusion

Data Vault is not for small startups or simple reporting. It is a heavy-duty, enterprise-grade architecture designed for massive complexity, frequent corporate acquisitions, and rigorous audit requirements. By hyper-normalizing data into Hubs, Links, and Satellites, Data Vault ensures that the data warehouse can dynamically absorb any new data source without ever breaking existing pipelines, achieving true architectural agility.
