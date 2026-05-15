---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Log-Structured Merge-Tree (LSM)"
description: "A comprehensive deep dive into Log-Structured Merge-Trees (LSM), covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["databases", "write optimization", "SSTables", "compaction"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to LSM Trees

In traditional databases (like PostgreSQL), data is stored in B-Trees. B-Trees are incredibly fast for reading data. However, they are terribly slow at writing data. 
Every time you insert a new record into a B-Tree, the database has to physically search the hard drive, find the exact correct block in the middle of the file, and overwrite it. This is called **Random I/O**. Hard drives (especially mechanical ones) hate Random I/O. If you try to insert 100,000 records per second, the hard drive will bottleneck and the database will crash.

The **Log-Structured Merge-Tree (LSM Tree)** was invented to solve the "write bottleneck." 
It is the underlying data structure powering almost all modern, high-throughput distributed databases (like Apache Cassandra, RocksDB, LevelDB, and DynamoDB).

## How LSM Trees Work: The Write Optimization

LSM Trees completely abandon Random I/O. They embrace **Sequential I/O**. Instead of searching for the correct place to put data, they just blindly append data to the end of a log.

### Step 1: The MemTable (RAM)
When a user writes a new record (`ID=42, Name=Alex`), the LSM tree does *not* write it to the hard drive immediately. It writes it to a sorted tree structure sitting in the computer's **Memory (RAM)**, called the MemTable. Writing to RAM is instantaneous.

### Step 2: The Flush (SSTable)
Eventually, the MemTable fills up (e.g., reaching 64MB). The database freezes that MemTable and "flushes" it to the physical hard drive as a brand new, immutable file called an **SSTable** (Sorted String Table). 
Because the database is just dumping 64MB of pre-sorted data sequentially onto the disk in one massive block, the hard drive writes it at maximum speed. 

### Step 3: Compaction
Over time, the hard drive fills up with hundreds of these 64MB SSTable files. 
If a user updates `ID=42` three different times on three different days, that record exists in three different SSTables.
To fix this, a background process called **Compaction** wakes up. It reads the hundreds of small SSTables, merges them together, deletes the old versions of `ID=42`, and writes a single, massive, perfectly sorted new SSTable. 

## The Read Penalty

There is no free lunch in computer science. By optimizing the database for extreme write speeds, the LSM Tree sacrifices read speed.

If a user runs `SELECT * FROM table WHERE ID=42`, the database has to check multiple places:
1.  First, it checks the active MemTable in RAM.
2.  If it doesn't find it, it checks the newest SSTable on the hard drive.
3.  If it doesn't find it, it checks the next oldest SSTable, and the next, and the next.

Searching 50 different files to find one record is slow. To mitigate this "Read Penalty," LSM trees use **[Bloom Filters](/knowledge/bloom-filters)**—a highly efficient mathematical algorithm that can instantly tell the database, *"Do not check SSTable #4, I mathematically guarantee ID=42 is not in there."*

## Conclusion

The Log-Structured Merge-Tree is the architectural engine of the Big Data era. Traditional B-Trees could never handle the massive, unrelenting write-heavy workloads of IoT sensors or social media feeds. By utilizing RAM as a buffer and forcing all disk writes to be purely sequential, LSM Trees allow modern databases to ingest millions of records per second without breaking a sweat, deferring the heavy lifting of sorting and merging to background compaction processes.
