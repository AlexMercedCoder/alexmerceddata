---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Apache Kafka"
description: "A comprehensive deep dive into Apache Kafka, covering architecture, concepts, and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["event streaming", "publish-subscribe", "high throughput", "real-time"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Apache Kafka

In the early 2010s, LinkedIn faced a massive infrastructure crisis. They needed to move massive amounts of data (user clicks, profile updates, server logs) between dozens of different internal systems. They built brittle, point-to-point connections: the Database sent data to the Search Index, the Web Server sent data to the Analytics engine, etc. As the company grew, this architecture devolved into an unmanageable "spaghetti" of network connections.

To solve this, Jay Kreps, Neha Narkhede, and Jun Rao created **Apache Kafka**.

Kafka is an open-source distributed event streaming platform. Instead of systems talking directly to each other, Kafka acts as a massive, high-speed, central nervous system for the enterprise. It completely decouples the systems that create data (Producers) from the systems that consume data (Consumers).

## How Kafka Works: The Distributed Commit Log

At its absolute core, Kafka is not a complex database; it is a remarkably simple, highly optimized mathematical structure called a **Distributed Commit Log**.

A Commit Log is simply an append-only file. 
When a Producer (e.g., the website's checkout service) sends a message to Kafka ("User Alex bought a coffee"), Kafka appends that message to the end of the log. It cannot be edited or deleted.

### Topics and Partitions
Kafka organizes these logs into categories called **Topics** (e.g., the `website_clicks` topic or the `financial_transactions` topic).

To handle petabytes of data, a single Topic is broken apart into multiple **Partitions**, and these partitions are distributed across a cluster of Kafka servers (Brokers). 
When a million users click on the website simultaneously, Kafka distributes those million messages evenly across 50 different partitions on 50 different servers. This allows Kafka to achieve blistering throughput, capable of processing millions of events per second with single-digit millisecond latency.

## The Publish-Subscribe (Pub/Sub) Model

Kafka operates on a Publisher/Subscriber model, which fundamentally changes how data engineering works.

1.  **The Producer (Publisher)**: The Checkout Service publishes an event to the `Purchases` topic. The Producer does not know (or care) who is going to read this data. It just drops it in the log and moves on.
2.  **The Consumers (Subscribers)**: Multiple independent systems can "subscribe" to the `Purchases` topic.
    *   The **Inventory System** reads the event and deducts 1 coffee bean.
    *   The **Fraud Detection AI** reads the *exact same event* a millisecond later to ensure the credit card isn't stolen.
    *   The **Data Lake Ingestion Pipeline** reads the event to write it into an [Apache Iceberg](/knowledge/apache-iceberg) table for long-term analytics.

Crucially, Kafka remembers the exact location (the **Offset**) where each Consumer stopped reading. If the Inventory System crashes and is offline for an hour, it doesn't lose any data. When it reboots, it simply asks Kafka for all the messages it missed since it died.

## Kafka vs. Traditional Message Queues

Before Kafka, systems used traditional message queues (like RabbitMQ or ActiveMQ). 
In a traditional queue, when a Consumer reads a message, the message is permanently deleted from the queue. If you want three different systems to read the same message, you have to duplicate the message three times.

In Kafka, reading a message does not delete it. The data remains persisted on the Kafka broker's hard drive for a configurable amount of time (e.g., 7 days, or even permanently). This allows organizations to "replay" historical streams of data to train new machine learning models or recover from catastrophic database failures.

## Conclusion

Apache Kafka is the undisputed backbone of real-time data architecture. By combining the ultra-fast, decoupled communication of a message broker with the durable storage of a database, Kafka allows organizations to transition from slow, overnight batch-processing to continuous, real-time event streaming. Whether you are hailing an Uber, swiping a credit card, or watching a Netflix movie, your actions are almost certainly generating data that is flowing through an Apache Kafka cluster.
