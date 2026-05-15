---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Data Classification"
description: "A comprehensive deep dive into Data Classification, covering concepts and real-world usage in Data Governance."
date: "2026-05-14"
tags: ["security", "PII", "sensitivity", "compliance"]
cta_link: "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
---

## Introduction to Data Classification

In a massive enterprise Data Lakehouse containing petabytes of data, not all rows and columns are created equal. 

If a hacker steals a table containing `website_click_coordinates`, it is a minor nuisance. If a hacker steals a table containing `customer_credit_card_numbers`, the company will face catastrophic lawsuits, regulatory fines, and permanent brand damage. Furthermore, internal employees (like junior data analysts) should have free access to the click data, but should be strictly blocked from viewing the credit card data.

**Data Classification** is the foundational governance process of scanning an organization's entire data estate, identifying the specific types of data being stored, and assigning a standardized "Tag" or "Label" to that data based on its business value, legal requirements, and sensitivity.

## The Classification Levels

Organizations typically implement a strict hierarchical classification taxonomy. While the specific names vary by company, a standard taxonomy looks like this:

### 1. Public Data
Data that is freely available to the world and carries zero risk if exposed. 
*   *Examples*: Press releases, public product catalogs, open job listings. 
*   *Access*: Unrestricted.

### 2. Internal / Business General
Data that is not public, but would cause minimal damage if leaked. It is standard operational data used by employees daily.
*   *Examples*: Internal corporate memos, aggregate sales dashboards, unreleased product roadmaps.
*   *Access*: Available to all authenticated employees.

### 3. Confidential
Data that is highly sensitive and would cause significant financial or reputational harm to the company or its partners if exposed.
*   *Examples*: Unreleased financial earnings reports, M&A strategy documents, vendor contracts, proprietary source code.
*   *Access*: Restricted to specific departments (e.g., Legal, Finance) on a strict "Need to Know" basis.

### 4. Restricted / Highly Confidential (PII, PHI, PCI)
The most dangerous data in the enterprise. Exposure of this data violates federal or international laws (like GDPR, HIPAA, or PCI-DSS).
*   **PII (Personally Identifiable Information)**: Social Security Numbers, exact dates of birth, home addresses.
*   **PHI (Protected Health Information)**: Medical diagnoses, prescription records.
*   **PCI (Payment Card Industry)**: Credit card numbers, bank account routing numbers.
*   *Access*: Severely restricted. Even database administrators are often blocked from viewing this data in plaintext.

## Automation and the Data Catalog

Historically, Data Classification was an impossible manual task. A data steward had to look at every single table in a 10,000-table database and manually type "Confidential" next to the columns.

Today, classification is heavily automated using **[Active Metadata](/knowledge/active-metadata)** platforms and AI.
Tools like BigID, Securiti.ai, or Collibra actively scan the Apache Iceberg tables in [Amazon S3](/knowledge/amazon-s3). They use Machine Learning and Regular Expressions to analyze the actual data in the columns. 
If the ML model detects a column filled with 16-digit numbers that pass the Luhn algorithm (the mathematical formula for credit cards), it autonomously applies the `PCI_RESTRICTED` tag to that column in the centralized Data Catalog.

## Driving Policy (Tag-Based Security)

Classification is useless if it doesn't drive security. 
Modern architectures (like [Dremio](/knowledge/dremio) or Snowflake) use **Tag-Based Security**. 

Instead of an administrator writing 500 different SQL rules saying "Bob cannot see Table A, Table B, Table C...", the administrator writes a single policy: *"No employee below the rank of VP can view any column tagged `PCI_RESTRICTED`."* 

Because the AI automatically classified the columns, the security is enforced globally and instantly across the entire enterprise, eliminating human error.

## Conclusion

Data Classification is the absolute prerequisite for enterprise data security and regulatory compliance. You cannot protect what you do not know you have. By utilizing automated ML scanning and standardized taxonomies to map the exact locations of toxic data, organizations can safely open their data lakehouses to analysts while mathematically guaranteeing that sensitive information remains locked down.
