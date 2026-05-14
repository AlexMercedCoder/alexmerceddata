import json
import os

terms_file = 'scripts/terms.json'

new_terms = [
  {
    "term": "Data Serialization",
    "category": "Data Engineering",
    "keywords": ["encoding", "binary formats", "RPC", "data transport"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Avro",
    "category": "Data Formats",
    "keywords": ["row-based", "schema evolution", "JSON schema", "streaming"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Trino (PrestoSQL)",
    "category": "Query Engines",
    "keywords": ["distributed SQL", "MPP", "federated queries", "interactive analytics"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Flink",
    "category": "Query Engines",
    "keywords": ["stream processing", "stateful computations", "event-driven", "real-time"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Spark",
    "category": "Query Engines",
    "keywords": ["batch processing", "in-memory computing", "distributed data", "ETL"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Query Planner",
    "category": "Data Engineering",
    "keywords": ["SQL parsing", "execution plan", "logical plan", "physical plan"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Cost-Based Optimizer (CBO)",
    "category": "Data Engineering",
    "keywords": ["statistics", "execution paths", "query performance", "joins"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Vectorized Execution",
    "category": "Data Engineering",
    "keywords": ["SIMD", "CPU cache", "columnar processing", "query engines"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Data Democratization",
    "category": "Data Culture",
    "keywords": ["accessibility", "data literacy", "empowerment", "analytics for everyone"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Self-Service Analytics",
    "category": "Data Culture",
    "keywords": ["business intelligence", "dashboards", "ad-hoc queries", "agile data"],
    "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
  },
  {
    "term": "Extract, Load, Transform (ELT)",
    "category": "Data Engineering",
    "keywords": ["cloud data warehouses", "dbt", "data transformations", "modern data stack"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Data Orchestration",
    "category": "Data Engineering",
    "keywords": ["DAGs", "scheduling", "workflow management", "dependencies"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Apache Airflow",
    "category": "Data Engineering",
    "keywords": ["Python", "orchestration", "DAGs", "data pipelines"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Project Nessie",
    "category": "Data Catalogs",
    "keywords": ["git for data", "branching", "version control", "data catalog"],
    "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
  },
  {
    "term": "Dremio Sonar",
    "category": "Query Engines",
    "keywords": ["SQL engine", "lakehouse platform", "Arrow Flight", "data virtualization"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Semantic Layer",
    "category": "Data Architecture",
    "keywords": ["business logic", "metrics", "unified interface", "data abstraction"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Virtual Data Warehouse",
    "category": "Data Architecture",
    "keywords": ["data federation", "no data movement", "logical data warehouse"],
    "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"
  },
  {
    "term": "Zero-ETL",
    "category": "Data Engineering",
    "keywords": ["direct queries", "real-time sync", "operational data", "lakehouse"],
    "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"
  },
  {
    "term": "Multi-Cloud Architecture",
    "category": "Data Architecture",
    "keywords": ["vendor lock-in", "AWS", "Azure", "GCP", "hybrid cloud"],
    "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"
  },
  {
    "term": "Knowledge Graphs",
    "category": "Artificial Intelligence",
    "keywords": ["ontologies", "relationships", "graph databases", "semantic context"],
    "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"
  },
  {
    "term": "Graph Neural Networks (GNNs)",
    "category": "Artificial Intelligence",
    "keywords": ["deep learning", "node embeddings", "network analysis", "machine learning"],
    "target_cta": "https://www.amazon.com/Constructing-Context-Semantics-Agents-Embeddings/dp/B0GSHRZNZ5/ref=sr_1_21"
  },
  {
    "term": "Zero-Shot Learning",
    "category": "Artificial Intelligence",
    "keywords": ["LLMs", "prompting", "generalization", "inference"],
    "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"
  },
  {
    "term": "Tokenization in LLMs",
    "category": "Artificial Intelligence",
    "keywords": ["subwords", "BPE", "vocabulary", "text processing"],
    "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"
  },
  {
    "term": "Temperature in Generative AI",
    "category": "Artificial Intelligence",
    "keywords": ["creativity", "randomness", "LLM parameters", "logits"],
    "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"
  },
  {
    "term": "Hardware Acceleration (GPUs/TPUs) for AI",
    "category": "Artificial Intelligence",
    "keywords": ["parallel processing", "tensor cores", "model training", "inference"],
    "target_cta": "https://www.amazon.com/Economics-AI-Latency-Infrastructure-Tradeoffs/dp/B0GSPGSKXC/ref=sr_1_36"
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
