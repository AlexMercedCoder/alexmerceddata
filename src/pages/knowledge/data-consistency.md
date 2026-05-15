---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Data Consistency"
description: "A comprehensive deep dive into Data Consistency, covering concepts and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["CAP theorem", "eventual consistency", "strong consistency", "ACID"]
cta_link: "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
---

## Introduction to Data Consistency

When a user deposits $100 into their bank account via a mobile app, they expect to instantly see their balance increase by $100 when they refresh the screen. If they refresh the screen and the balance hasn't changed, they will panic, assuming the bank lost their money.

In a single, monolithic database running on a single computer, this is trivial to guarantee. When the transaction hits the hard drive, the data is updated.

However, in modern distributed systems, databases are spread across hundreds of servers globally. If the user's deposit is processed by Server A in New York, it takes physical time (milliseconds to seconds) for Server A to copy that new data to Server B in London and Server C in Tokyo. 
**Data Consistency** is the mathematical discipline of managing what happens if a user connects to Server B *before* the data finishes copying. 

## The CAP Theorem

Discussions around consistency in distributed systems are strictly governed by the **[CAP Theorem](/knowledge/cap-theorem)** (Brewer's Theorem). It states that a distributed data store can only guarantee two out of the following three properties simultaneously:

1.  **Consistency (C)**: Every read receives the most recent write, or an error. If Server A is updated, you cannot read from Server B until Server B is identical to A.
2.  **Availability (A)**: Every request receives a non-error response, without the guarantee that it contains the most recent write. The system will always answer you, even if the answer is slightly outdated.
3.  **Partition Tolerance (P)**: The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes (e.g., the internet cable between NY and London is cut).

Because network partitions (P) are an unavoidable reality of physics, distributed systems must choose between prioritizing Consistency (CP architectures) or Availability (AP architectures).

## Strong vs. Eventual Consistency

This forced choice leads to two distinct database paradigms.

### Strong Consistency (CP)
In a Strongly Consistent system (like traditional Relational Databases or Google Spanner), the database prioritizes accuracy above all else. 
If the network connection between NY and London breaks during a transaction, the database will completely lock up and refuse to answer read requests in London. It returns an error rather than risk showing the user an outdated bank balance. 
*   **Pros**: Absolute mathematical perfection. Required for financial ledgers and inventory management (you can't sell the same seat on an airplane twice).
*   **Cons**: Slower performance (you have to wait for global replication locks) and lower availability during network outages.

### Eventual Consistency (AP)
In an Eventually Consistent system (like Apache Cassandra or Amazon DynamoDB), the database prioritizes uptime and speed.
If the NY server updates a profile picture, it immediately tells the user "Success!" and tries to sync with London in the background. If a user in London checks the profile a millisecond later, the London server will happily return the *old* profile picture. It prioritizes giving an answer immediately. The system guarantees that, eventually, if no new updates are made, all servers will converge on the correct data.
*   **Pros**: Blistering speed and 100% uptime. Required for social media (it doesn't matter if you see a "Like" on a post 2 seconds later than someone else).
*   **Cons**: Developers must write complex defensive code to handle the chaos of reading stale data.

## Consistency in the Data Lakehouse

Historically, [Amazon S3](/knowledge/amazon-s3) (the foundation of the Data Lake) was only *Eventually Consistent*. If you wrote a massive file to S3 and immediately tried to list the files in the bucket, S3 might not show you the new file. This made building transactional databases on S3 nearly impossible.

In late 2020, AWS upgraded S3 to provide **Strong Read-After-Write Consistency**. This monumental physical upgrade, combined with the ACID guarantees provided by [Open Table Formats](/knowledge/open-table-formats) like **Apache Iceberg**, finally allowed the Data Lakehouse to provide the Strong Consistency of a traditional Data Warehouse, ensuring that business analysts never accidentally query a half-written, corrupted dataset.

## Conclusion

Data Consistency is the ultimate architectural tradeoff in distributed computing. Engineers must carefully evaluate the business use case before selecting a database. Building a banking app on an Eventually Consistent database will result in catastrophic financial errors, while building a global social media feed on a Strongly Consistent database will result in agonizing load times. Understanding where a system falls on the CAP spectrum is essential for designing reliable data infrastructure.
