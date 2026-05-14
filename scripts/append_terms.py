import json
import os

terms_file = 'scripts/terms.json'

new_terms = [
  {
    "term": "Apache Arrow",
    "category": "Data Formats",
    "keywords": ["in-memory", "columnar format", "zero-copy", "performance"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Arrow Flight SQL",
    "category": "Data Connectivity",
    "keywords": ["database connectivity", "high throughput", "JDBC", "ODBC"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Vector Search Indexes",
    "category": "Artificial Intelligence",
    "keywords": ["ANN", "HNSW", "Faiss", "embeddings"],
    "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"
  },
  {
    "term": "Data Lineage",
    "category": "Data Governance",
    "keywords": ["provenance", "impact analysis", "compliance", "tracing"],
    "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
  },
  {
    "term": "Data Observability",
    "category": "Data Engineering",
    "keywords": ["monitoring", "data quality", "anomaly detection", "reliability"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Zero-Copy Cloning",
    "category": "Data Architecture",
    "keywords": ["snapshots", "storage optimization", "branching", "Apache Iceberg"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Data as Code",
    "category": "Data Engineering",
    "keywords": ["branching", "merging", "Nessie", "version control"],
    "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
  },
  {
    "term": "Prompt Engineering",
    "category": "Artificial Intelligence",
    "keywords": ["LLMs", "context framing", "few-shot learning", "reasoning"],
    "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"
  },
  {
    "term": "Fine-Tuning LLMs",
    "category": "Artificial Intelligence",
    "keywords": ["LoRA", "PEFT", "model adaptation", "domain specific"],
    "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"
  },
  {
    "term": "Data Contracts",
    "category": "Data Engineering",
    "keywords": ["API", "schema registry", "data producers", "quality guarantees"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Reverse ETL",
    "category": "Data Engineering",
    "keywords": ["operational analytics", "data activation", "CRM sync", "lakehouse"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Data Vault Architecture",
    "category": "Data Architecture",
    "keywords": ["hubs", "links", "satellites", "agile data warehouse"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Star Schema",
    "category": "Data Architecture",
    "keywords": ["dimensional modeling", "facts", "dimensions", "Kimball"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Slowly Changing Dimensions (SCD)",
    "category": "Data Architecture",
    "keywords": ["historical data", "Type 2 SCD", "data warehouse", "upserts"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Lambda Architecture",
    "category": "Data Architecture",
    "keywords": ["batch layer", "speed layer", "streaming", "data consolidation"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Kappa Architecture",
    "category": "Data Architecture",
    "keywords": ["streaming first", "event logs", "Kafka", "simplified pipelines"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Hudi",
    "category": "Data Formats",
    "keywords": ["table formats", "upserts", "incremental processing", "lakehouse"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Delta Lake",
    "category": "Data Formats",
    "keywords": ["transaction log", "Databricks", "Z-Ordering", "open formats"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Compute Pushdown",
    "category": "Data Engineering",
    "keywords": ["query optimization", "data source", "filtering", "performance"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Predicate Pushdown",
    "category": "Data Engineering",
    "keywords": ["file pruning", "min-max stats", "Parquet", "query execution"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Bloom Filters",
    "category": "Data Engineering",
    "keywords": ["probabilistic data structures", "file skipping", "query speed", "indexing"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Z-Ordering",
    "category": "Data Engineering",
    "keywords": ["space-filling curves", "data clustering", "multi-dimensional queries", "file pruning"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Event Sourcing",
    "category": "Data Architecture",
    "keywords": ["state changes", "event log", "immutable data", "microservices"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Micro-Batches",
    "category": "Data Engineering",
    "keywords": ["Spark Streaming", "near real-time", "latency", "ETL"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Multi-Agent Systems",
    "category": "Artificial Intelligence",
    "keywords": ["collaboration", "autonomous agents", "GenAI workflows", "distributed AI"],
    "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"
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
