import json
import os

terms_file = 'scripts/terms.json'

new_terms = [
  {
    "term": "Data Quality",
    "category": "Data Governance",
    "keywords": ["accuracy", "completeness", "reliability", "trust"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Data Profiling",
    "category": "Data Engineering",
    "keywords": ["metadata", "statistics", "data analysis", "cleanliness"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "MLOps (Machine Learning Operations)",
    "category": "Artificial Intelligence",
    "keywords": ["deployment", "model lifecycle", "CI/CD", "monitoring"],
    "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"
  },
  {
    "term": "DataOps",
    "category": "Data Culture",
    "keywords": ["agile", "automation", "pipeline collaboration", "DevOps for data"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Model Drift",
    "category": "Artificial Intelligence",
    "keywords": ["data drift", "concept drift", "performance degradation", "retraining"],
    "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"
  },
  {
    "term": "Feature Store",
    "category": "Artificial Intelligence",
    "keywords": ["machine learning", "feature engineering", "model serving", "centralized data"],
    "target_cta": "https://www.amazon.com/AI-Ready-Data-Designing-Platforms-Agents/dp/B0GSN7GLH2/ref=sr_1_3"
  },
  {
    "term": "Data Lake vs Data Warehouse",
    "category": "Data Architecture",
    "keywords": ["structured vs unstructured", "cost comparison", "scalability", "lakehouse"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Snowflake Data Cloud",
    "category": "Data Architecture",
    "keywords": ["cloud data warehouse", "compute separation", "data sharing"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Databricks",
    "category": "Data Architecture",
    "keywords": ["unified analytics", "Apache Spark", "Delta Lake", "Lakehouse"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Data Virtualization",
    "category": "Data Architecture",
    "keywords": ["no data movement", "federation", "logical views", "Dremio"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Polyglot Persistence",
    "category": "Data Architecture",
    "keywords": ["multiple databases", "right tool for the job", "storage paradigms"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Kafka",
    "category": "Data Engineering",
    "keywords": ["event streaming", "publish-subscribe", "high throughput", "real-time"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Object Storage (S3, ADLS, GCS)",
    "category": "Data Lakehouse",
    "keywords": ["cloud storage", "durability", "scalability", "data lakes"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Storage Abstraction",
    "category": "Data Architecture",
    "keywords": ["decoupling", "cloud independence", "file systems", "HDFS"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Iceberg Copy-on-Write (CoW)",
    "category": "Data Engineering",
    "keywords": ["data updates", "file rewriting", "read optimized", "Apache Iceberg"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Iceberg Merge-on-Read (MoR)",
    "category": "Data Engineering",
    "keywords": ["delete files", "position deletes", "write optimized", "Apache Iceberg"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Row-Level Deletes",
    "category": "Data Engineering",
    "keywords": ["GDPR", "compliance", "upserts", "table formats"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Data Consistency",
    "category": "Data Engineering",
    "keywords": ["CAP theorem", "eventual consistency", "strong consistency", "ACID"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "ACID Compliance",
    "category": "Data Engineering",
    "keywords": ["databases", "transactions", "reliability", "data integrity"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Idempotent Data Pipelines",
    "category": "Data Engineering",
    "keywords": ["re-runnable", "safe retries", "data duplication", "robustness"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Backfilling Data",
    "category": "Data Engineering",
    "keywords": ["historical processing", "pipeline updates", "data correction", "reprocessing"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Upserts (Update and Insert)",
    "category": "Data Engineering",
    "keywords": ["merge operations", "CDC", "data synchronization", "lakehouse"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Unstructured Data",
    "category": "Data Formats",
    "keywords": ["text", "images", "audio", "AI training data"],
    "target_cta": "https://www.amazon.com/AI-Ready-Data-Designing-Platforms-Agents/dp/B0GSN7GLH2/ref=sr_1_3"
  },
  {
    "term": "Semi-Structured Data (JSON, XML)",
    "category": "Data Formats",
    "keywords": ["flexibility", "nested data", "NoSQL", "logs"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Open Table Formats",
    "category": "Data Lakehouse",
    "keywords": ["Iceberg", "Delta", "Hudi", "interoperability"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  }
]

if os.path.exists(terms_file):
    with open(terms_file, 'r') as f:
        existing_terms = json.load(f)
else:
    existing_terms = []

existing_terms.extend(new_terms)

with open(terms_file, 'w') as f:
    json.dump(existing_terms, f, indent=2)

print(f"Successfully added {len(new_terms)} terms. Total terms is now {len(existing_terms)}.")
