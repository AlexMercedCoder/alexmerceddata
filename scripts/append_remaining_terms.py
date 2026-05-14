import json
import os

terms_file = 'scripts/terms.json'

new_terms = [
  # Batch 5: Advanced Analytics & Streaming
  {"term": "Real-time Analytics", "category": "Data Analytics", "keywords": ["low latency", "dashboards", "event streams", "decision making"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Batch Processing vs Stream Processing", "category": "Data Engineering", "keywords": ["data processing", "latency", "throughput", "ETL"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Apache Druid", "category": "Query Engines", "keywords": ["OLAP", "time-series", "sub-second queries", "real-time"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "ClickHouse", "category": "Query Engines", "keywords": ["column-oriented", "analytical database", "high performance"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Business Intelligence (BI)", "category": "Data Analytics", "keywords": ["reporting", "KPIs", "dashboards", "data visualization"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Data Warehousing", "category": "Data Architecture", "keywords": ["EDW", "historical data", "structured data", "SQL"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Materialized Views", "category": "Data Architecture", "keywords": ["pre-computation", "query performance", "caching", "database optimization"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Apache Pinot", "category": "Query Engines", "keywords": ["OLAP", "real-time", "user-facing analytics", "distributed"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Mining", "category": "Data Analytics", "keywords": ["patterns", "statistics", "knowledge discovery", "machine learning"], "target_cta": "https://www.amazon.com/AI-Ready-Data-Designing-Platforms-Agents/dp/B0GSN7GLH2/ref=sr_1_3"},
  {"term": "Predictive Analytics", "category": "Data Analytics", "keywords": ["forecasting", "statistical modeling", "machine learning", "future trends"], "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"},
  {"term": "Prescriptive Analytics", "category": "Data Analytics", "keywords": ["optimization", "simulation", "decision support", "actionable insights"], "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"},
  {"term": "Dimensional Modeling", "category": "Data Architecture", "keywords": ["Ralph Kimball", "facts", "dimensions", "data warehouse"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Silos", "category": "Data Culture", "keywords": ["fragmentation", "isolation", "data integration", "lakehouse"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Customer Data Platform (CDP)", "category": "Data Architecture", "keywords": ["marketing", "unified profile", "segmentation", "analytics"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Apache Superset", "category": "Data Analytics", "keywords": ["data exploration", "visualization", "open source", "dashboards"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Tableau", "category": "Data Analytics", "keywords": ["BI tool", "visual analytics", "dashboards", "data sources"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Power BI", "category": "Data Analytics", "keywords": ["Microsoft", "business analytics", "DAX", "reporting"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Looker", "category": "Data Analytics", "keywords": ["LookML", "Google Cloud", "data modeling", "BI"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Data Lineage vs Data Provenance", "category": "Data Governance", "keywords": ["tracking", "origins", "transformations", "auditing"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Active Metadata", "category": "Data Governance", "keywords": ["automation", "data fabric", "machine learning", "metadata management"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Data Classification", "category": "Data Governance", "keywords": ["security", "PII", "sensitivity", "compliance"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Data Masking", "category": "Data Governance", "keywords": ["obfuscation", "security", "privacy", "testing"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Data Anonymization", "category": "Data Governance", "keywords": ["privacy", "de-identification", "compliance", "GDPR"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Master Data Management (MDM)", "category": "Data Governance", "keywords": ["single source of truth", "reference data", "consolidation", "quality"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Stewardship", "category": "Data Culture", "keywords": ["accountability", "data policies", "governance", "roles"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},

  # Batch 6: Generative AI, Models & Agents
  {"term": "Generative Pre-trained Transformer (GPT)", "category": "Artificial Intelligence", "keywords": ["OpenAI", "transformers", "LLMs", "NLP"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Attention Mechanism", "category": "Artificial Intelligence", "keywords": ["transformers", "neural networks", "sequence-to-sequence", "context"], "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"},
  {"term": "Low-Rank Adaptation (LoRA)", "category": "Artificial Intelligence", "keywords": ["fine-tuning", "parameter efficient", "LLMs", "weights"], "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"},
  {"term": "Reinforcement Learning from Human Feedback (RLHF)", "category": "Artificial Intelligence", "keywords": ["alignment", "reward model", "LLM training", "human-in-the-loop"], "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"},
  {"term": "Chain of Thought Prompting", "category": "Artificial Intelligence", "keywords": ["reasoning", "LLMs", "prompt engineering", "step-by-step"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Few-Shot Prompting", "category": "Artificial Intelligence", "keywords": ["in-context learning", "examples", "LLMs", "task adaptation"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Zero-Shot Prompting", "category": "Artificial Intelligence", "keywords": ["generalization", "LLMs", "no examples", "inference"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "LangChain", "category": "Artificial Intelligence", "keywords": ["framework", "agents", "LLM applications", "chains"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "LlamaIndex", "category": "Artificial Intelligence", "keywords": ["data framework", "RAG", "LLMs", "indexing"], "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"},
  {"term": "Vector Similarity Metrics", "category": "Artificial Intelligence", "keywords": ["cosine similarity", "euclidean distance", "dot product", "embeddings"], "target_cta": "https://www.amazon.com/Constructing-Context-Semantics-Agents-Embeddings/dp/B0GSHRZNZ5/ref=sr_1_21"},
  {"term": "Chunking Strategies for RAG", "category": "Artificial Intelligence", "keywords": ["document parsing", "context window", "embeddings", "information retrieval"], "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"},
  {"term": "Hybrid Search", "category": "Artificial Intelligence", "keywords": ["keyword search", "semantic search", "BM25", "vector search"], "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"},
  {"term": "Re-ranking Models", "category": "Artificial Intelligence", "keywords": ["Cross-encoders", "search optimization", "RAG", "relevance"], "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"},
  {"term": "Open-Source LLMs (Llama, Mistral)", "category": "Artificial Intelligence", "keywords": ["weights", "local deployment", "Hugging Face", "democratization"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Hugging Face", "category": "Artificial Intelligence", "keywords": ["model hub", "transformers", "open source", "machine learning"], "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"},
  {"term": "Model Quantization", "category": "Artificial Intelligence", "keywords": ["compression", "INT8", "memory optimization", "inference speed"], "target_cta": "https://www.amazon.com/Economics-AI-Latency-Infrastructure-Tradeoffs/dp/B0GSPGSKXC/ref=sr_1_36"},
  {"term": "Mixture of Experts (MoE)", "category": "Artificial Intelligence", "keywords": ["neural networks", "sparse activation", "scaling", "LLM architecture"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Hallucination in AI", "category": "Artificial Intelligence", "keywords": ["factual accuracy", "grounding", "LLMs", "reliability"], "target_cta": "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"},
  {"term": "AI Agent Tool Use (Function Calling)", "category": "Artificial Intelligence", "keywords": ["APIs", "action execution", "LLM extensions", "agentic workflows"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Autonomous Agents", "category": "Artificial Intelligence", "keywords": ["AutoGPT", "goal-driven", "planning", "execution"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Multi-Modal AI", "category": "Artificial Intelligence", "keywords": ["text", "images", "audio", "unified models"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Computer Vision", "category": "Artificial Intelligence", "keywords": ["image recognition", "CNNs", "object detection", "visual processing"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "Natural Language Processing (NLP)", "category": "Artificial Intelligence", "keywords": ["linguistics", "text analysis", "sentiment", "parsing"], "target_cta": "https://www.amazon.com/Building-Knowledge-Systems-AI-Context/dp/B0GSWFSSRC/ref=sr_1_27"},
  {"term": "Speech-to-Text (ASR)", "category": "Artificial Intelligence", "keywords": ["transcription", "audio processing", "voice assistants", "Whisper"], "target_cta": "https://www.amazon.com/dp/B0GQW7CTML"},
  {"term": "AI Ethics and Bias", "category": "Artificial Intelligence", "keywords": ["fairness", "safety", "alignment", "responsible AI"], "target_cta": "https://www.amazon.com/Governing-AI-Systems/dp/B0GSMVQ1TH/ref=sr_1_21"},

  # Batch 7: Distributed Systems & Advanced Engineering
  {"term": "Distributed Systems", "category": "Data Engineering", "keywords": ["networking", "concurrency", "fault tolerance", "scalability"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "CAP Theorem", "category": "Data Engineering", "keywords": ["consistency", "availability", "partition tolerance", "databases"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Eventual Consistency", "category": "Data Engineering", "keywords": ["BASE", "distributed databases", "latency", "sync"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Paxos and Raft Consensus", "category": "Data Engineering", "keywords": ["algorithms", "distributed state", "leader election", "replication"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "MapReduce", "category": "Data Engineering", "keywords": ["Hadoop", "batch processing", "distributed algorithms", "legacy data"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Serialization Formats (Protobuf, Thrift)", "category": "Data Formats", "keywords": ["RPC", "schema evolution", "binary encoding", "microservices"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Message Queues", "category": "Data Engineering", "keywords": ["RabbitMQ", "ActiveMQ", "asynchronous", "decoupling"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Log-Structured Merge-Tree (LSM)", "category": "Data Engineering", "keywords": ["databases", "write optimization", "SSTables", "compaction"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "B-Tree Indexing", "category": "Data Engineering", "keywords": ["databases", "read optimization", "search algorithms", "storage"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Data Partitioning and Sharding", "category": "Data Architecture", "keywords": ["horizontal scaling", "database design", "distributed storage", "performance"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Consistent Hashing", "category": "Data Engineering", "keywords": ["load balancing", "distributed caching", "node routing", "scalability"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Microservices Architecture", "category": "Software Architecture", "keywords": ["decoupling", "containers", "APIs", "scalability"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Serverless Computing", "category": "Cloud Architecture", "keywords": ["AWS Lambda", "event-driven", "auto-scaling", "functions"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Containerization (Docker)", "category": "DevOps", "keywords": ["isolation", "deployment", "environments", "microservices"], "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"},
  {"term": "Kubernetes", "category": "DevOps", "keywords": ["orchestration", "containers", "scaling", "cloud native"], "target_cta": "https://www.amazon.com/Shipping-AI-Prototype-Production-Systems/dp/B0GSR2GRZX/ref=sr_1_22"},
  {"term": "CI/CD for Data", "category": "DataOps", "keywords": ["automation", "testing", "deployment pipelines", "reliability"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Infrastructure as Code (IaC)", "category": "DevOps", "keywords": ["Terraform", "automation", "cloud provisioning", "reproducibility"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "GDPR and CCPA", "category": "Data Governance", "keywords": ["privacy laws", "compliance", "user rights", "data protection"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Personally Identifiable Information (PII)", "category": "Data Governance", "keywords": ["sensitive data", "privacy", "security", "masking"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Data Encryption (At Rest and In Transit)", "category": "Data Security", "keywords": ["cryptography", "TLS/SSL", "security", "protection"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Federated Learning", "category": "Artificial Intelligence", "keywords": ["decentralized AI", "privacy-preserving", "edge devices", "model training"], "target_cta": "https://www.amazon.com/Governing-AI-Systems/dp/B0GSMVQ1TH/ref=sr_1_21"},
  {"term": "Homomorphic Encryption", "category": "Data Security", "keywords": ["cryptography", "secure computation", "privacy", "cloud security"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Differential Privacy", "category": "Data Privacy", "keywords": ["statistical noise", "anonymization", "data analysis", "security"], "target_cta": "https://www.amazon.com/Governing-AI-Systems/dp/B0GSMVQ1TH/ref=sr_1_21"},
  {"term": "Zero Trust Architecture", "category": "Data Security", "keywords": ["authentication", "authorization", "network security", "identity"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Threat Modeling", "category": "Data Security", "keywords": ["risk assessment", "vulnerabilities", "security lifecycle", "mitigation"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},

  # Batch 8: Ecosystem & Strategy
  {"term": "The Apache Software Foundation", "category": "Open Source", "keywords": ["governance", "community", "open source", "incubator"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Apache Hadoop", "category": "Data Engineering", "keywords": ["HDFS", "MapReduce", "big data", "legacy ecosystems"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Apache Hive", "category": "Data Engineering", "keywords": ["data warehouse", "Hadoop", "metastore", "SQL"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Hive Metastore (HMS)", "category": "Data Catalogs", "keywords": ["metadata", "legacy catalogs", "Hadoop ecosystem", "Iceberg migration"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "AWS Glue", "category": "Data Catalogs", "keywords": ["managed service", "serverless", "ETL", "AWS"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Amazon S3", "category": "Cloud Architecture", "keywords": ["object storage", "AWS", "data lakes", "durability"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Azure Data Lake Storage (ADLS)", "category": "Cloud Architecture", "keywords": ["Microsoft Azure", "hierarchical namespace", "object storage", "analytics"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Google Cloud Storage (GCS)", "category": "Cloud Architecture", "keywords": ["GCP", "object storage", "global infrastructure", "analytics"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Engineering Lifecycle", "category": "Data Engineering", "keywords": ["generation", "storage", "ingestion", "transformation", "serving"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Strategy", "category": "Data Culture", "keywords": ["business alignment", "value creation", "roadmap", "leadership"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Data Literacy", "category": "Data Culture", "keywords": ["education", "understanding data", "decision making", "organizational culture"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Chief Data Officer (CDO)", "category": "Data Culture", "keywords": ["leadership", "executive", "data governance", "strategy"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Data-Driven Decision Making", "category": "Data Culture", "keywords": ["analytics", "metrics", "business value", "KPIs"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Monetization", "category": "Data Strategy", "keywords": ["revenue streams", "data products", "value extraction", "business models"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Data Privacy by Design", "category": "Data Governance", "keywords": ["frameworks", "proactive privacy", "engineering", "compliance"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Data Security Posture Management (DSPM)", "category": "Data Security", "keywords": ["cloud security", "risk management", "visibility", "compliance"], "target_cta": "https://hello.dremio.com/wp-apache-polaris-guide-reg.html"},
  {"term": "Open-Source Software (OSS)", "category": "Data Culture", "keywords": ["community", "collaboration", "transparency", "licensing"], "target_cta": "https://hello.dremio.com/wp-apache-iceberg-the-definitive-guide-reg.html"},
  {"term": "Vendor Lock-in", "category": "Data Strategy", "keywords": ["proprietary systems", "migration costs", "open formats", "cloud independence"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "Total Cost of Ownership (TCO) in Data", "category": "Data Strategy", "keywords": ["compute costs", "storage costs", "maintenance", "ROI"], "target_cta": "https://www.amazon.com/Economics-AI-Latency-Infrastructure-Tradeoffs/dp/B0GSPGSKXC/ref=sr_1_36"},
  {"term": "FinOps for Data", "category": "Data Strategy", "keywords": ["cloud spend", "cost optimization", "financial accountability", "efficiency"], "target_cta": "https://www.amazon.com/Economics-AI-Latency-Infrastructure-Tradeoffs/dp/B0GSPGSKXC/ref=sr_1_36"},
  {"term": "Return on Investment (ROI) for AI", "category": "Data Strategy", "keywords": ["business cases", "value realization", "metrics", "AI investments"], "target_cta": "https://www.amazon.com/Economics-AI-Latency-Infrastructure-Tradeoffs/dp/B0GSPGSKXC/ref=sr_1_36"},
  {"term": "Change Management in Data Initiatives", "category": "Data Culture", "keywords": ["adoption", "training", "organizational alignment", "processes"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Center of Excellence (CoE)", "category": "Data Culture", "keywords": ["best practices", "leadership", "innovation", "support"], "target_cta": "https://www.amazon.com/Agentic-Enterprise-Deploying-Agents-Organization/dp/B0GSN3NNS5/ref=sr_1_16"},
  {"term": "Data Product Manager", "category": "Data Culture", "keywords": ["product lifecycle", "user needs", "data as a product", "agile"], "target_cta": "https://www.manning.com/books/architecting-an-apache-iceberg-lakehouse"},
  {"term": "The Future of the Data Lakehouse", "category": "Data Strategy", "keywords": ["convergence", "AI integration", "real-time", "trends"], "target_cta": "https://www.amazon.com/Open-Source-Lakehouse-Architecting-Analytical-ebook/dp/B0D46P3VB7/ref=sr_1_17"}
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
