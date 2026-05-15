---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Object Storage (S3, ADLS, GCS)"
description: "A comprehensive deep dive into Object Storage, covering architecture, concepts, and real-world usage in Data Architecture."
date: "2026-05-14"
tags: ["cloud storage", "scalability", "blob storage", "data lake"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Object Storage

In the era of on-premises computing, data was stored in two primary ways:
1.  **Block Storage**: The raw hard drives plugged into a server (like the C: drive on your laptop). Extremely fast, but severely limited in size.
2.  **File Storage**: Systems that organize data into rigid, hierarchical folders and sub-folders (like a Network Attached Storage drive). Great for humans organizing documents, but terrible at scaling. If you put 10 million files into a single folder, the operating system grinds to a halt trying to traverse the file tree.

As the internet exploded, companies needed to store billions of photos, videos, and log files. File and Block storage architectures simply broke at that scale.

The solution was **Object Storage**, commercialized most famously by Amazon Web Services in 2006 as **[Amazon S3](/knowledge/amazon-s3)** (Simple Storage Service). Object Storage completely abandoned the concept of folders and hard drives, creating an infinitely scalable, flat repository that became the foundational bedrock of the entire cloud computing revolution.

## The Architecture of Object Storage

In an Object Storage system (like Amazon S3, Azure Data Lake Storage [ADLS], or Google Cloud Storage [GCS]), there is no folder hierarchy. The system is entirely flat. 

Every piece of data is treated as a discrete **Object**.

An Object consists of three things:
1.  **The Data (The Payload)**: The actual sequence of bytes (a JPEG image, an [Apache Parquet](/knowledge/apache-parquet) file, a JSON document).
2.  **The Metadata**: Highly customizable tags attached directly to the object. Instead of relying on a folder name to provide context, you can tag an object with `{"author": "Alex", "project": "Lakehouse", "retention_days": "365"}`.
3.  **A Globally Unique Identifier (URI/Key)**: A long, unique string used to retrieve the object.

Because the system is flat, it scales infinitely. Adding the 1-Billionth object is mathematically just as fast and easy as adding the 1st object. There is no file tree to traverse.

## How the "Folders" Trick Works

If you log into the Amazon S3 console, it *looks* like there are folders. This is an illusion created by the user interface.

If you upload a file named `sales/2026/january/report.pdf`, S3 does not create a `sales` folder, put a `2026` folder inside it, and so on. 
The entire string `sales/2026/january/report.pdf` is simply the flat, Unique Identifier (the Key) for that single object. The UI just parses the slashes (`/`) and draws pictures of folders on your screen to make it easier for human brains to comprehend.

## Object Storage and the Data Lakehouse

Object storage was originally designed for serving static website assets (images and CSS files) and archiving backups. However, due to its infinite scalability and incredibly cheap cost (pennies per gigabyte), it became the physical foundation for the entire **Data Lake** movement.

Instead of buying a $5 Million Teradata appliance, organizations realized they could simply dump massive Parquet files into S3 for a fraction of the cost.

However, Object Storage has a major limitation for databases: **It is immutable.** You cannot open a 1GB Parquet file in S3, change a single row, and save it. You must overwrite the entire 1GB file. This is why building databases directly on S3 was historically impossible.

The **Open Data Lakehouse** (powered by Apache Iceberg) solved this. Iceberg acts as an intelligent abstraction layer. When a user runs a SQL `UPDATE` command, Iceberg handles the complex mechanics of rewriting the necessary Parquet files and managing the metadata, allowing high-performance query engines (like Dremio) to treat raw, immutable Object Storage exactly like a transactional relational database.

## Conclusion

Object Storage is the unsung hero of the modern internet and the modern data stack. By abandoning the limitations of legacy file systems in favor of a flat, highly distributed architecture, services like S3, ADLS, and GCS provided the infinite, cheap storage capacity required to unleash the Big Data and Artificial Intelligence revolutions.
