# Towards Effective Orchestration of AI x DB Workloads

**ArXiv ID:** 2603.03772  
**Authors:** Naili Xing, Haotian Gao, Zhanhao Zhao, Shaofeng Cai, Zhaojing Luo, Yuncheng Wu, Zhongle Xie, Meihui Zhang, Beng Chin Ooi  
**Submitted:** March 4, 2026  
**Field:** Systems, Databases, Machine Learning Integration  

## Executive Summary

This paper addresses the emerging challenge of integrating artificial intelligence directly into database engines for efficient joint query processing and AI execution. The work proposes a framework for orchestrating AI×DB workloads—streams of queries that interleave relational processing with model inference—managing critical challenges including query optimization, execution scheduling, distributed execution coordination, and security enforcement. The significance lies in enabling seamless integration of AI operations within data systems, eliminating costly data export overhead while maintaining robustness and security guarantees.

## Problem Statement

Traditional AI-driven analytics pipelines export data from databases to external machine learning runtimes, incurring several critical limitations:
1. **High Overhead:** Data movement between systems introduces significant latency and bandwidth requirements
2. **Robustness Issues:** Stale data and model drift due to decoupling between training and inference pipelines
3. **Security Concerns:** Data exposure during export expands attack surface and complicates access control
4. **Management Complexity:** Coordinating between independent database and ML systems is error-prone

Recent trends pushing AI deeper into database engines require solving novel optimization problems: managing joint query processing and model execution, optimizing end-to-end latency under resource constraints, enforcing access control across heterogeneous components, and coordinating execution schedules when resources are contentious.

## Core Concepts & Theory

### AI×DB Workload Definition

An AI×DB workload is defined as a stream of AI×DB queries issued over a database instance, where:
- Each query interleaves relational processing (SQL) with AI execution (model inference, vector operations)
- Data flows between relational operators and ML models within unified execution context
- Reads and produces AI artifacts: model versions, embeddings, feature caches, intermediate embeddings

### Key Integration Challenges

**Query Processing Integration**
- Seamless composition of SQL operations with model inference steps
- Optimization of data passing between relational and ML components
- Memory-efficient execution of hybrid pipelines
- State management across different execution contexts

**Execution Scheduling**
- Coordination of heterogeneous compute resources (CPU, GPU, TPU) between database and ML components
- Batching strategies to amortize model inference costs
- Priority-based scheduling under resource constraints
- Dynamic adaptation to workload characteristics

**Distributed Execution**
- Partitioning queries across multiple machines
- Communication optimization between database nodes and ML accelerators
- Load balancing under heterogeneous node capabilities
- Fault tolerance and recovery mechanisms

**Security and Access Control**
- Fine-grained access control across AI and database layers
- Data lineage tracking for compliance requirements
- Model access restrictions and usage auditing
- Preventing information leakage through model outputs

### Architectural Considerations

**In-Database vs. External ML**
- Trade-offs between tight integration (reduced latency, memory efficiency) and modularity
- Unified storage vs. separate model repositories
- Unified scheduling vs. independent resource management

**Artifact Management**
- Model versioning and consistency across queries
- Embedding cache management and invalidation strategies
- Feature store integration with database engine
- Provenance tracking for reproducibility

## Main Ideas & Contributions

1. **Problem Formulation:** Systematic characterization of AI×DB workload challenges distinct from traditional database workloads
2. **Orchestration Framework:** Unified approach to managing query optimization, execution scheduling, and resource allocation
3. **Security Integration:** Access control mechanisms preserving both database and ML model privacy
4. **Experimental Insights:** Demonstrated benefits of coordinated scheduling over independent optimization
5. **Prototype Implementation:** Modified PostgreSQL system showing feasibility of integrated approach

### Novel Aspects

The paper identifies unique challenges arising from AI×DB integration that cannot be addressed by traditional database optimization alone:
- Model inference latency patterns differ fundamentally from traditional operations
- Resource sharing between CPU-intensive database operations and GPU-intensive model serving
- Correctness requirements across heterogeneous execution layers
- Semantic differences between relational algebra and neural computations

## Methodology & Implementation

### Experimental Setup

**System Configuration**
- Modified PostgreSQL prototype with integrated ML execution
- Support for model execution operators alongside traditional SQL operators
- Single-node and distributed deployment configurations

**Workload Characteristics**
- [Exact figures unavailable — see full paper for detailed workload specifications]
- Mix of relational and ML-heavy queries
- Varying model complexity (embeddings, classification, regression)
- Different data volumes and batch sizes

**Evaluation Metrics**
- End-to-end query latency
- Resource utilization (CPU, GPU, memory)
- Throughput under multiple concurrent queries
- Scheduling overhead and optimization effectiveness

### Key Implementation Details

**Query Optimization**
- Detection of AI×DB queries with ML operator identification
- Dependency analysis between relational and ML components
- Cost modeling incorporating both database and ML execution costs
- Orchestration decisions for batching, caching, and scheduling

**Execution Scheduling**
- Priority-aware scheduling respecting resource constraints
- Dynamic adaptation based on runtime characteristics
- Load balancing across heterogeneous compute devices
- Backpressure handling for resource-contrained scenarios

**Security Integration**
- Role-based access control extended to model artifacts
- Query-level isolation guarantees
- Audit logging for model access and inference
- Encryption support for sensitive AI artifacts

## Practical Applications & Use Cases

### Recommendation Systems
- Real-time personalized recommendations combining database queries with collaborative filtering models
- User preference prediction from behavioral data stored in database
- Dynamic model serving avoiding cold-start problems

### Financial Services
- Fraud detection combining transaction data with ML models
- Real-time credit risk assessment merging customer history with predictive models
- Portfolio optimization based on market data and ML predictions

### Healthcare Systems
- Patient risk prediction using medical history and diagnostic models
- Drug interaction detection from pharmacological databases and ML models
- Resource allocation optimization for hospital operations

### E-Commerce Platforms
- Dynamic pricing combining inventory data with demand models
- Search ranking integrating catalog with learning-to-rank models
- Supply chain optimization using predictive models and inventory data

### Manufacturing and Industry 4.0
- Predictive maintenance combining sensor data with anomaly detection models
- Quality control integrating production parameters with defect prediction
- Process optimization using historical data and performance models

### Geospatial and Environmental Systems
- Climate modeling integrating sensor networks with ML predictions
- Urban planning combining demographic data with traffic prediction models
- Resource management optimizing allocation with learned demand patterns

## Insights & Implications

### Field Impact

The work establishes AI×DB integration as a critical architectural pattern for modern data-driven applications. Key implications:

1. **System Design Philosophy:** Future database engines must natively support AI operations rather than treating them as external concerns
2. **Performance Optimization:** Database optimization techniques and ML serving techniques must be co-optimized rather than treated independently
3. **Security Model Evolution:** Traditional database access control must extend to encompass AI artifacts and inference operations
4. **Resource Management:** Unified scheduling under heterogeneous compute resources becomes essential for efficient execution

### Architectural Trends

- Migration from extract-transform-load (ETL) plus external ML to integrated end-to-end execution
- Tighter coupling between data storage and compute through co-location of databases and ML services
- Evolution toward polyglot execution supporting multiple computational paradigms within unified systems
- Increased importance of intermediate representations (embeddings, feature vectors) in database design

### Research Implications

1. **Query Optimization:** Traditional cardinality and cost estimation techniques insufficient; must incorporate ML operation characteristics
2. **Resource Management:** New scheduling and allocation algorithms needed for hybrid CPU-GPU workloads
3. **Correctness and Verification:** Techniques for ensuring correctness across relational and probabilistic components
4. **Fault Tolerance:** Recovery mechanisms must handle failures in both database and ML components

### Limitations and Open Questions

- **Scalability:** How does overhead scale with model complexity and data volume?
- **Heterogeneity:** Supporting diverse ML frameworks and hardware efficiently
- **Consistency:** Balancing consistency requirements with latency constraints
- **Debugging:** Observability and debugging of failures spanning database and ML layers
- **Multi-Tenancy:** Isolation and resource sharing guarantees in shared environments

## Code & Resources

### System Components
- **Query Parser:** Extended SQL grammar for ML operations
- **Optimizer:** Cost-based planning for AI×DB queries
- **Executor:** Coordinated execution of relational and ML components
- **Scheduler:** Resource-aware scheduling for heterogeneous workloads

### Dependencies and Requirements

**Software:**
- PostgreSQL 14+ (modified version with AI integration)
- PyTorch or TensorFlow for model execution
- ONNX runtime for model serving
- Python 3.9+ for integration layer

**Hardware:**
- CPU: 4+ cores for relational processing
- GPU: NVIDIA GPU with CUDA 11.8+ (recommended for model inference)
- Memory: 16+ GB for realistic workloads
- Storage: SSDs for database and model caches

### Integration Example

```sql
-- AI×DB Query Example
SELECT u.user_id, u.name, 
       predict_preference(u.profile, item_embedding(i.item_id)) AS score
FROM users u, items i
WHERE i.category = 'electronics'
AND u.region = 'US'
ORDER BY score DESC
LIMIT 10;
```

## Related Work & Context

### Prior Work Foundations

**Database Systems**
- Volcano optimizer model for cost-based query planning
- Columnar databases and vectorized execution engines
- Distributed query processing and federated databases

**Machine Learning Systems**
- Feature stores for centralized feature management
- Model serving systems (TFServing, MLflow, Seldon)
- Distributed training and inference frameworks

**Hybrid Approaches**
- Materialized views for caching computed results
- Approximate query processing for interactive analytics
- Stream processing and continuous analytics

### Related Recent Papers

- **In-Database ML:** SystemML, MADlib integration of ML into databases
- **ML Serving:** Model-serving systems optimizing inference latency and throughput
- **Query Optimization:** Advanced optimization techniques for complex analytics workloads
- **Data Management for AI:** Feature engineering, data quality, and lineage tracking

### Future Research Directions

1. **Automated System Design:** Techniques for automatically optimizing database-ML system architectures
2. **Cross-Layer Optimization:** Joint optimization of database execution and model inference
3. **Unified Cost Models:** Comprehensive cost estimation spanning SQL and ML operations
4. **Adaptive Execution:** Dynamic optimization and re-planning based on runtime characteristics
5. **Privacy-Preserving Integration:** Techniques for AI×DB workloads with differential privacy and secure computation

---

**Paper Link:** [arXiv:2603.03772](https://arxiv.org/abs/2603.03772)
