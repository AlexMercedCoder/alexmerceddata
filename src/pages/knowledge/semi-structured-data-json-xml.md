---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Semi-Structured Data (JSON, XML)"
description: "A comprehensive deep dive into Semi-Structured Data, covering concepts and real-world usage in Data Formats."
date: "2026-05-14"
tags: ["flexibility", "nested data", "NoSQL", "logs"]
cta_link: "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
---

## Introduction to Semi-Structured Data

In data architecture, data generally falls into two extremes. **Structured Data** is highly rigid, perfectly organized into relational rows and columns. **[Unstructured Data](/knowledge/unstructured-data)** is completely chaotic, like a raw text file or a JPEG image.

**Semi-Structured Data** occupies the middle ground. It does not obey the strict rules of a relational database (there are no predefined tables or columns), but it is not chaotic. It utilizes internal tags or markers to separate semantic elements and enforce a hierarchy of records and fields. 

It is the language of the modern web. Every time an application talks to an API, every time a web browser renders a page, and every time a microservice logs an error, the data is transmitted in a semi-structured format.

## The Dominant Formats: XML and JSON

Historically, there have been two primary formats for semi-structured data.

### XML (eXtensible Markup Language)
Popularized in the late 1990s and 2000s, XML relies on heavy, verbose tags to structure data (similar to HTML).
```xml
<Customer>
    <ID>123</ID>
    <Name>Alex</Name>
    <Address>
        <City>Orlando</City>
    </Address>
</Customer>
```
While XML is extremely rigid and excellent for strict enterprise data exchange (like banking protocols), its verbosity makes files massive and slow to transmit over the internet.

### JSON (JavaScript Object Notation)
Created as a lightweight alternative to XML, JSON completely took over the internet. It uses simple key-value pairs and arrays, making it incredibly easy for both humans and computers to read.
```json
{
  "customer_id": 123,
  "name": "Alex",
  "address": {
    "city": "Orlando"
  }
}
```
JSON is the undisputed standard for REST APIs, web application configurations, and NoSQL databases.

## The Superpower: Schema Evolution and Nesting

The primary reason software engineers love Semi-Structured data is **flexibility**. 

If you use a relational database, adding a `phone_number` field requires executing an `ALTER TABLE` command. This locks the database, risks downtime, and takes time.

If you use a JSON document in a NoSQL database (like MongoDB), you simply add the `"phone_number": "555-1234"` key to the next document you save. The database doesn't care. It accepts it instantly. This schema-less nature allows rapid, agile software development.

Furthermore, Semi-Structured data allows for **Nesting**. A relational database cannot store a list of items inside a single cell; you must create a separate table and use a `JOIN`. In JSON, you simply create an array within the document: `"purchases": ["Laptop", "Mouse"]`. 

## The Analytical Challenge: The "Shredding" Problem

While JSON is a dream for software engineers building web apps, it is a nightmare for data analysts. 

Data warehouses (like Snowflake or BigQuery) are designed to run fast aggregations over flat columns. If a data engineer dumps a massive JSON string containing deeply nested arrays into a single database column, the analyst cannot easily query it using standard SQL. 

Historically, data engineers had to build brutal ETL pipelines to "shred" or "flatten" the JSON. They wrote Python code to extract the nested `city` field from the JSON and map it to a flat `city` column in a relational table. 

## Modern Solutions in the Lakehouse

Modern Data Lakehouse engines have largely solved the JSON problem.

1.  **Native JSON Support**: Engines like [Dremio](/knowledge/dremio), Trino, and Snowflake now feature native functions to query JSON directly. An analyst can write SQL like `SELECT raw_data:address.city FROM logs` to instantly extract the deeply nested value without flattening it.
2.  **Columnar JSON**: Because standard JSON text files are terrible for analytical scanning, tools often convert JSON into **[Apache Parquet](/knowledge/apache-parquet)**. Parquet is capable of preserving the nested, semi-structured hierarchy of the JSON while applying columnar compression to it, providing the flexibility of JSON with the analytical speed of a relational database.

## Conclusion

Semi-Structured data represents the inevitable compromise between the rigidity required by analytical databases and the flexibility required by agile software development. While it introduces complexity into the data engineering pipeline, modern lakehouse architectures and advanced SQL dialects have made it possible to ingest, query, and analyze massive volumes of JSON seamlessly, bridging the gap between operational applications and enterprise analytics.
