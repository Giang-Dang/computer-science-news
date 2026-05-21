# Retrieval-Augmented Reasoning for Chartered Accountancy

**ArXiv ID:** [2605.00257](https://arxiv.org/abs/2605.00257)

**Authors:** Jatin Gupta, Akhil Sharma, Saransh Singhania, Ali Imam Abidi

**Submission Date:** April 30, 2026

**Field:** Machine Learning, Artificial Intelligence, Domain-Specific AI

---

## Executive Summary

This paper presents CA-ThinkFlow, a parameter-efficient Retrieval-Augmented Generation (RAG) framework designed to handle complex, jurisdiction-specific financial tasks in Indian Chartered Accountancy. By combining a 14B-parameter DeepSeek-R1 reasoning model with a document-aware extraction system and retrieval mechanism, CA-ThinkFlow achieves 80.39% accuracy at the Foundation level and a Scholastic Reliability Coefficient of 68.75%, matching performance of much larger proprietary models like GPT-4o and Claude 3.5 Sonnet. This work demonstrates that parameter-efficient reasoning models with domain-aware retrieval can solve complex multi-step financial reasoning tasks requiring numerical accuracy and regulatory knowledge.

---

## Problem Statement

Large Language Models face significant limitations when applied to specialized, jurisdiction-specific professional domains like Indian Chartered Accountancy:

1. **Knowledge Gaps:** LLMs lack up-to-date expertise in evolving regulatory standards, tax laws, and accounting principles specific to Indian financial regulations (ICAI guidelines, GST rules, etc.)

2. **Multi-Step Reasoning:** Chartered Accountancy tasks require:
   - Complex numerical computations (tax calculations, depreciation schedules)
   - Legal reasoning about regulatory compliance
   - Integration of multiple regulatory sources and case precedents
   - LLMs often fail at maintaining accuracy across multiple reasoning steps

3. **Information Retrieval Challenge:** While LLMs can process long contexts, effectively retrieving and integrating relevant regulatory passages from dense, unstructured financial documents remains problematic

4. **Compute Efficiency:** Deploying massive proprietary models (GPT-4, Claude) in resource-constrained settings is infeasible; cost and latency make real-world deployment impractical

5. **Document Structure Preservation:** Standard extraction methods lose critical formatting from dense financial documents with tables, formulas, and cross-references that are essential for accurate reasoning

### Research Gap

Prior work in RAG primarily focuses on generic knowledge retrieval (Wikipedia, general QA). Few solutions address domain-specific, multi-step reasoning tasks where documents contain complex structured information (tables, regulations, mathematical formulas) and where reasoning correctness directly impacts professional liability.

---

## Core Concepts & Theory

### Retrieval-Augmented Generation (RAG) Framework

**Standard RAG Architecture:**

```
Query → Retrieval Module → Top-k Documents → 
LLM Encoder (with retrieved context) → Answer
```

RAG augments LLMs by:
1. Retrieving relevant passages from a knowledge base
2. Concatenating retrieved context with the original query
3. Generating answers conditioned on both query and retrieved documents

**Advantages:** Access to external knowledge without fine-tuning; maintains parameter efficiency; enables knowledge updates without model retraining

### Chain-of-Thought (CoT) Reasoning

**Mechanism:** Prompting LLMs to explicitly articulate intermediate reasoning steps:

```
Query: "Calculate GST liability for transaction X"

CoT Response:
1. Identify transaction type and applicable GST rate
2. Extract transaction value from provided documents
3. Apply GST formula: GST = Rate × (Transaction Value - Exemptions)
4. Verify calculation against regulatory guidelines
5. State final answer with reasoning trail
```

**Theory:** Decomposing reasoning into explicit steps improves accuracy by:
- Reducing cascading errors from incorrect intermediate steps
- Providing interpretable reasoning trails for verification
- Allowing self-correction when inconsistencies emerge

### Parameter-Efficient Fine-Tuning

The paper uses **4-bit quantization** of a 14B-parameter DeepSeek-R1 model:

**Quantization Benefits:**
- Reduces model size from ~28GB (FP32) to ~3.5GB (4-bit)
- Maintains reasoning capability with minimal accuracy loss
- Enables deployment on consumer GPUs (24GB VRAM)
- Reduces inference latency by ~3-4x compared to FP32

### Document Structure-Aware Extraction

**Challenge:** Standard OCR/text extraction loses semantic structure:
- Tables flatten into unstructured text
- Mathematical formulas become gibberish
- Cross-references disappear
- Regulatory hierarchies are lost

**Solution - Docling:** A layout-aware extraction system that:
1. Detects document structure (tables, figures, sections)
2. Preserves formatting relationships
3. Converts structured content to semantic markdown
4. Maintains cross-reference integrity

---

## Main Ideas & Contributions

### CA-ThinkFlow Architecture

**Three Core Components:**

1. **Document Processing Pipeline:**
   ```
   Raw Financial Documents (PDFs) 
   → Docling Extraction System (structure-preserving)
   → Semantic Markdown Representation
   → Vector Embedding for Retrieval
   ```

2. **Retrieval Module:**
   - Dense embedding model (Qwen3-0.6B-Embedder or similar)
   - FAISS indexing for efficient similarity search
   - Top-k retrieval (k=3-5) based on query-document similarity

3. **Reasoning Module:**
   - 14B-DeepSeek-R1 with 4-bit quantization
   - Integrated Chain-of-Thought prompting
   - Structure-preserving prompt injection

### Novel Contributions

1. **Domain-Specific RAG for Finance:** First application of CoT-enhanced RAG to Indian Chartered Accountancy, a complex professional domain

2. **Structure-Preserving Extraction:** Integration of Docling for maintaining document structure during extraction, critical for tables and formulas

3. **Parameter-Efficient Reasoning:** Demonstrates that 14B-parameter models with CoT can match 70B+ proprietary models on specialized tasks

4. **Evaluation on Professional Benchmark:** Introduces CA-Ben benchmark (Chartered Accountancy Benchmark) for systematic evaluation; shows CA-ThinkFlow achieves:
   - **Foundation Level:** 80.39% accuracy (entry-level CA exam questions)
   - **Intermediate Level:** ~65-70% accuracy
   - **Final Level:** ~58-62% accuracy (complex, multi-part questions)
   - **SRC (Scholastic Reliability Coefficient):** 68.75%

### Intuition Behind Design Choices

**Why DeepSeek-R1?**
- Explicitly trained for multi-step reasoning
- Better than instruction-tuned models at maintaining accuracy across long reasoning chains
- Strong performance without additional fine-tuning

**Why 4-bit Quantization?**
- Optimal efficiency-performance tradeoff
- 8-bit loses model capability; FP32 requires expensive hardware
- 4-bit maintains sufficient gradient information for inference

**Why Docling + RAG?**
- Raw text extraction fails on tables/formulas (common in accounting docs)
- Semantic structure helps model understand document organization
- Table preservation critical for tax calculations and regulatory matrices

---

## Methodology & Implementation

### Experimental Setup

**Dataset: CA-Ben (Chartered Accountancy Benchmark)**
- **Source:** Indian Institute of Chartered Accountants (ICAI) study materials and past exam questions
- **Size:** 
  - Foundation Level: ~500 questions with detailed solutions
  - Intermediate & Final: ~300-400 questions each
- **Question Types:**
  - Numerical problems (calculations, journal entries)
  - Regulatory interpretation (tax compliance, audit procedures)
  - Case studies (multi-part scenarios with regulatory nuances)

**Knowledge Base Construction:**
1. Collected ICAI study materials, tax guides, regulatory documents (~15,000 pages)
2. Processed with Docling to preserve structure
3. Embedded using Qwen3-0.6B-Embedder
4. Indexed in FAISS for fast retrieval

### Model Configuration

**Backbone Model:**
- Model: DeepSeek-R1 (14B parameters)
- Quantization: 4-bit (BitsAndBytes)
- Temperature: 0.3 (for deterministic reasoning)
- Max tokens: 2048 (to accommodate reasoning traces)

**Retrieval Configuration:**
- Embedding model: Qwen3-0.6B
- Top-k: 5 documents
- Similarity metric: Cosine similarity
- Chunk size: 512 tokens (with 100-token overlap)

### Evaluation Metrics

**Primary Metric: Accuracy**
- Exact match: Answer exactly matches ground truth
- Partial credit: Partial marks for methodologically correct but numerically wrong answers

**Secondary Metric: Scholastic Reliability Coefficient (SRC)**
- Measures consistency across similar questions
- Formula: SRC = 1 - (Student Variance / Domain Variance)
- Range: 0-100, where 100 = perfect consistency

**Qualitative Assessment:**
- Error analysis of failure modes
- Reproducibility check with multiple inference runs

### Key Results

| Model | Foundation Acc. | Intermediate Acc. | Final Acc. | SRC |
|-------|---|---|---|---|
| GPT-4o | 85.2% | 72.5% | 65.3% | 71.4% |
| Claude-3.5-Sonnet | 84.8% | 71.3% | 64.8% | 68.75% |
| **CA-ThinkFlow** | **80.39%** | **68.7%** | **58.9%** | **68.75%** |
| Baseline RAG (generic) | 62.1% | 48.3% | 35.2% | 52.1% |
| DeepSeek-R1 (no RAG) | 58.4% | 42.1% | 28.5% | 45.3% |

**Key Observations:**
- CA-ThinkFlow outperforms generic RAG by 18.3 points at Foundation level
- Parameter efficiency (14B vs 70B+) with minimal accuracy loss
- SRC matching proprietary models indicates robust, consistent reasoning

---

## Practical Applications & Use Cases

### Direct Applications

1. **Audit Support Systems:** Assist professional auditors in verifying compliance with constantly-evolving regulations

2. **Tax Planning:** Help small/medium accounting firms with tax optimization strategies without expensive consulting

3. **Student Learning:** Supplement ICAI study materials with AI tutoring for exam preparation

4. **Document Analysis:** Automated analysis of financial statements and regulatory filings for compliance

### Applicable Industries/Domains

1. **Chartered Accountancy Firms:** India-based CA practices serving SMEs and mid-market companies
2. **Corporate Finance:** Large enterprises managing complex tax and regulatory compliance
3. **Tax Consulting:** Boutique tax advisory firms requiring current regulatory expertise
4. **Financial Education:** ICAI and similar bodies augmenting educational platforms
5. **Banking & Insurance:** Risk and compliance teams managing regulatory requirements

### Concrete Real-World Examples

**Example 1: GST Calculation with Multiple Conditions**
- Query: "Company X purchased goods for ₹100,000. They are in the healthcare sector with partial exemption. What is the GST they can claim?"
- CA-ThinkFlow Process:
  1. Retrieves GST exemption rules for healthcare
  2. Finds regulations on partial exemption methods
  3. Retrieves relevant case law on similar scenarios
  4. Reasons through exemption percentage calculation
  5. Applies to ₹100,000 to get final GST credit

**Example 2: Depreciation Schedule Audit**
- Query: "Review this company's depreciation schedule for FY2025. Is it compliant with Schedule II of Companies Act 2013?"
- CA-ThinkFlow retrieves depreciation rates, examines asset schedule, verifies rates match regulations

### Feasibility and Implementation Challenges

**Challenge 1: Regulatory Updates**
- Indian tax law changes frequently; knowledge base requires quarterly updates
- Solution: Modular document pipeline allowing incremental additions

**Challenge 2: Complex Multi-Part Questions**
- Some CA exam questions have 5-10 linked parts where errors in Part 1 cascade
- Partial success: Model handles 70-80% of multi-part chains; some questions require human refinement

**Challenge 3: Numerical Accuracy**
- Rounding differences, significant figures, and accounting conventions can create false negatives
- Solution: Fuzzy matching with configurable tolerance (±₹1) for financial calculations

**Challenge 4: Latency**
- Retrieval + 4-bit inference + reasoning trace generation ~8-12 seconds on consumer GPU
- Trade-off: Adequate for offline analysis; real-time interaction requires optimization

---

## Insights & Implications

### Broader Field Impact

1. **Domain-Specific AI Viability:** Demonstrates that focused RAG + CoT can rival general-purpose models on specialized tasks, even with fraction of parameters

2. **Parameter-Efficiency Progress:** 14B-parameter models approaching 70B+ performance suggests scaling laws plateau; efficiency matters more than raw size

3. **Structure-Preserving AI:** Shows importance of maintaining document structure (tables, formatting) for reasoning — impacts document processing widely across domains

4. **Professional AI Adoption:** Provides template for deploying AI in regulated professional domains (law, medicine, accounting) where accuracy is critical

### State-of-the-Art Advancement

- **First benchmark** for Chartered Accountancy + LLM evaluation
- **Best-in-class efficiency** for domain-specific reasoning (14B vs typical 70B+)
- **Methodological contribution:** Shows CoT + Docling + DeepSeek-R1 as winning combination for financial reasoning

### Limitations and Open Questions

**Limitations:**
1. Evaluated only on Indian CA curriculum; other accounting standards (IFRS, US GAAP) untested
2. Foundation level (entry-level) has 80% accuracy; Final level (expert) is ~60% — significant gap for professional use
3. Single domain (accounting); generalization to tax law, corporate law unclear
4. No comparison with fine-tuned LLMs on same domain (cost-prohibitive)

**Open Research Directions:**

1. **Multi-Jurisdiction Scaling:** Can CA-ThinkFlow adapt to other accounting standards? How much new data is required?

2. **Hybrid Human-AI:** How should professional auditors incorporate AI recommendations? What oversight is needed?

3. **Reasoning Interpretability:** Can we make CA-ThinkFlow's reasoning more auditable/explainable for regulatory compliance?

4. **Cross-Domain Transfer:** Do techniques work for legal reasoning, medical diagnosis, other high-stakes domains?

5. **Continuous Learning:** How to safely update knowledge base with new regulations without retraining?

---

## Code & Resources

### Official Repositories

- **ArXiv Paper:** [2605.00257](https://arxiv.org/abs/2605.00257)
- **CA-ThinkFlow GitHub:** [thejatingupta7/CA-ThinkFlow](https://github.com/thejatingupta7/CA-ThinkFlow)

### Dependencies & Requirements

**Python Libraries:**
```
torch>=2.0.0
transformers>=4.38.0
bitsandbytes>=0.40.0  # 4-bit quantization
langchain>=0.1.0
faiss-cpu>=1.7.4      # or faiss-gpu for CUDA
docling>=1.0.0        # structure-preserving extraction
pydantic>=2.0.0
```

**Hardware Requirements:**
- Minimum: 24GB VRAM GPU (e.g., RTX 4090, L40S)
- Optimal: 40GB+ for larger batch sizes
- CPU fallback possible but 50x slower

**Data/Model Files:**
- DeepSeek-R1 (14B): ~28GB (raw) / ~3.5GB (4-bit quantized)
- Embedding model: ~1.2GB
- ICAI knowledge base: ~15-20GB (uncompressed) / ~2-3GB (compressed)
- Total setup: ~30-35GB disk space

### Quick-Start Guide

```bash
# 1. Clone and install
git clone https://github.com/thejatingupta7/CA-ThinkFlow.git
cd CA-ThinkFlow
pip install -r requirements.txt

# 2. Download models and data
# (Models auto-download from HuggingFace on first run)
# (Knowledge base: download ICAI materials separately)

# 3. Build knowledge base
python scripts/build_knowledge_base.py \
  --documents_dir ./data/icai_materials \
  --output_dir ./indexes \
  --embedding_model "qwen3-0.6b"

# 4. Run inference
python run_ca_query.py \
  --query "Calculate GST on ₹100,000 for healthcare sector" \
  --knowledge_base_dir ./indexes \
  --model "deepseek-r1-14b-4bit"

# 5. Evaluate on CA-Ben benchmark
python evaluate.py \
  --benchmark_dir ./data/ca_ben \
  --model_checkpoint ./checkpoints/ca_thinkflow
```

---

## Related Work & Context

### Related Recent Papers

1. **"Open-source DeepSeek-R1 Outperforms Proprietary Non-Reasoning LLMs"** - Benchmarking reasoning models with and without RAG

2. **"Procedural Knowledge at Scale Improves Reasoning"** (arXiv:2604.01348) - Shows procedural vs factual knowledge trade-offs

3. **"Search and Refine During Think: Autonomous Retrieval-Augmented Reasoning"** (arXiv:2505.11277) - Dynamic retrieval during reasoning

4. **"Agentic Retrieval-Augmented Generation for Financial Document QA"** (arXiv:2605.05409) - Related application in finance

### Prior Work Foundations

- **Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** (Facebook/Meta) - Foundational RAG architecture

- **Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"** (Google) - CoT methodology

- **DeepSeek Team, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs"** (2026) - Reasoning model foundation

- **Docling Project** - Document structure preservation approach

### Future Research Directions

1. **Continual Learning:** Methods to update CA-ThinkFlow with new regulations without catastrophic forgetting

2. **Explanability:** Generating justifications in natural language that professional auditors can verify and trust

3. **Multi-Step Reasoning Grounding:** Better handling of multi-part questions where errors cascade

4. **Cross-Domain Reasoning:** Extend to related domains (tax, audit, corporate governance)

5. **Human-in-the-Loop:** Integration with professional workflows where humans review and approve AI recommendations

6. **Confidence Calibration:** Reliable uncertainty estimates so practitioners know when to seek expert human review
