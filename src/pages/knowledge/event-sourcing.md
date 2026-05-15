---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Event Sourcing"
description: "A comprehensive deep dive into Event Sourcing, covering architecture, concepts, and real-world usage in Data Architecture."
date: "2026-05-14"
tags: ["state changes", "event log", "immutable data", "microservices"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Event Sourcing

In a traditional relational database architecture, the database stores the *current state* of an entity. 

If a customer has $100 in their bank account, the database table row reads: `Balance: $100`. If they withdraw $20, the application runs a SQL `UPDATE` statement. The old value is permanently erased, and the row now reads: `Balance: $80`.

While simple, this "state-based" architecture loses crucial information. If a business needs to know *why* the balance is $80, or exactly what time it changed, or if a bug accidentally subtracted the money twice, the database cannot answer. The history has been destroyed. 

**Event Sourcing** is a software architecture pattern that fundamentally reverses this dynamic. Instead of storing the final, current state of an entity, Event Sourcing stores every single change to that entity as an immutable, sequential log of events. The current state is then calculated dynamically by replaying the events.

## How Event Sourcing Works

In an Event Sourcing architecture (often paired with systems like [Apache Kafka](/knowledge/apache-kafka)), the database is essentially an append-only log.

### The Immutable Event Log
When a user interacts with the application, they generate "Events." An event is a record of something that has definitively happened in the past. Events are immutable; once written, they can never be altered or deleted.

Instead of updating a row, the banking application appends a sequence of events to the log:
1.  `AccountCreatedEvent { account_id: 123, initial_deposit: 100 }`
2.  `MoneyWithdrawnEvent { account_id: 123, amount: 20, timestamp: "14:00" }`
3.  `AddressChangedEvent { account_id: 123, new_city: "London" }`

### Calculating the Current State (Projection)
If the application needs to show the user their current balance on their mobile app, it does not query a `balance` column. Instead, a process reads the event log for `account_id: 123` from the beginning, sequentially adding and subtracting the values in memory until it arrives at the final state ($80). 

Because recalculating a 10-year event history for a high-volume account is slow, production systems use **Snapshots**. Every night, the system might calculate the state, save a snapshot (e.g., `Balance on Jan 1: $80`), and the next day's queries only replay the events that occurred *after* the snapshot.

## The Synergy with CQRS

Event Sourcing is almost universally paired with **CQRS (Command Query Responsibility Segregation)**.

CQRS is an architectural pattern that separates the infrastructure used for writing data (Commands) from the infrastructure used for reading data (Queries).

In a high-throughput microservices environment:
1.  **The Write Side**: The application writes the raw, immutable events instantly to the Event Store (e.g., Kafka). This is incredibly fast because it is purely an append-only operation with no table locks.
2.  **The Read Side**: Background processors listen to the Event Store. As new events arrive, these processors calculate the new state and write it into specialized read-optimized databases (like Elasticsearch for searching, or a PostgreSQL [Star Schema](/knowledge/star-schema) for BI dashboards).

## Why Event Sourcing is Powerful

Despite its complexity, Event Sourcing is adopted heavily in domains requiring absolute auditability, such as finance, logistics, and e-commerce.

### 1. Absolute Auditability and Compliance
Because history is never erased, an Event Sourced system is a perfect audit log. Regulators can see every exact mutation a financial record underwent. There is no such thing as an undocumented `UPDATE`.

### 2. Time Travel and Debugging
If a software bug corrupts a user's dashboard, engineers can instantly roll back the system to any specific point in time by simply replaying the event log up to a specific timestamp, ignoring the corrupted events. 

### 3. Business Intelligence Flexibility
In a traditional system, if you decide you want to track a new metric (e.g., "How many times did users change their address last year?"), you cannot answer the question because the old addresses were overwritten. In an Event Sourced system, the history is perfectly preserved in the log. You can write a new projection algorithm today, run it against the 5-year historical event log, and instantly generate a dashboard showing 5 years of historical address change trends.

## Conclusion

Event Sourcing shifts the perspective of software design from managing static state to recording dynamic behavior. By capturing the complete, immutable narrative of every action a system takes, it provides unmatched auditability, resilience, and analytical flexibility. While it introduces significant complexities around eventual consistency and event versioning, for mission-critical enterprise applications, the guarantee of a perfect, unalterable historical record is an invaluable architectural asset.
