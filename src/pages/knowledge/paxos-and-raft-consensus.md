---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Paxos and Raft Consensus"
description: "A comprehensive deep dive into Paxos and Raft Consensus, covering algorithms and real-world usage in Data Engineering."
date: "2026-05-14"
tags: ["algorithms", "distributed state", "leader election", "replication"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Distributed Consensus

Imagine an army with 5 different generals, all camped on different hills surrounding an enemy city. They can only communicate by sending messengers running between the hills. 
To win the battle, all 5 generals must attack at the exact same time. If only 2 generals attack, they will lose. They must reach a **Consensus**. 

However, messengers can be killed (Network Packet Loss). A general might be a traitor (Byzantine Fault). A general might fall asleep (Server Crash). How do the generals mathematically guarantee they all agree on the attack time, despite the chaos?

This is the fundamental problem of [Distributed Systems](/knowledge/distributed-systems). If you have a database cluster of 5 servers, and a user tries to change their password, how do you mathematically guarantee that all 5 servers agree on the new password, even if a router crashes during the transaction?

To solve this, computer science relies on **Consensus Algorithms**.

## Paxos: The Unintelligible Pioneer

Published in 1989 by Leslie Lamport (and largely ignored until he republished it in 1998), **Paxos** was the first mathematically proven algorithm to achieve consensus in a distributed network with unreliable communication.

Paxos operates on a complex system of "Proposers," "Acceptors," and "Learners." It requires multiple phases of voting and message passing to ensure that once a majority (a Quorum) of nodes accepts a value, that value is permanently locked in and cannot be changed, regardless of network failures.

*   **The Problem with Paxos**: While mathematically flawless, Paxos is notoriously, terrifyingly difficult to understand and even harder to code in the real world. As one famous paper noted: *"The dirty little secret of the NSDI community is that at most five people really, truly understand every part of Paxos."* Every company that implemented Paxos ended up building a custom, modified version that was prone to devastating bugs.

## Raft: Consensus for Humans

Because Paxos was so difficult to implement, researchers at Stanford University published the **Raft** consensus algorithm in 2014. 

Raft's explicit, stated goal was **Understandability**. It mathematically provides the exact same safety guarantees as Paxos, but is structured in a way that software engineers can easily comprehend and build.

Raft simplifies consensus by heavily relying on **Leader Election**:
1.  **The Leader**: In a 5-node cluster, Raft holds an election. One node becomes the Leader. The other 4 become Followers.
2.  **The Dictatorship**: All writes MUST go to the Leader. If a user wants to change a password, they tell the Leader.
3.  **The Log Replication**: The Leader does not immediately save the password. It sends a message to the 4 Followers: *"I propose changing the password to '123'."*
4.  **The Quorum**: The Leader waits. Once a majority of the Followers (at least 2 out of 4) reply *"Acknowledged"*, the Leader permanently saves (commits) the password, and orders the Followers to do the same.

If the Leader catches fire, the Followers detect the silence via a heartbeat timeout. They immediately hold a new election, pick a new Leader, and normal operations resume within milliseconds.

## Real-World Implementations

Consensus algorithms are not used for everything (they are too slow for massive data storage). They are used for the "Brain" of the distributed system—storing critical metadata and managing cluster state.

*   **Apache ZooKeeper**: Uses a Paxos-like algorithm (ZAB) to manage configuration for Hadoop and Kafka clusters.
*   **etcd**: Uses the **Raft** algorithm. It is the critical "brain" that stores the entire state of every [Kubernetes](/knowledge/kubernetes) cluster in the world.
*   **HashiCorp Consul**: Uses **Raft** for service discovery and configuration.

## Conclusion

Paxos and Raft are the mathematical bedrock of distributed computing. Without these algorithms, the concept of a multi-server database would be impossible, as the servers would instantly fall out of sync at the first sign of a network hiccup. While Paxos proved that consensus was mathematically possible, Raft democratized it, allowing the open-source community to build the robust, self-healing architectures that power the modern cloud.
