# Securing Retrieval-Augmented Generation: A Taxonomy of Attacks, Defenses, and Future Directions

**ArXiv ID:** [2604.08304](https://arxiv.org/abs/2604.08304)  
**Authors:** Yuming Xu, Mingtao Zhang, Zhuohan Ge, Haoyang Li, Nicole Hu, Jason Chen Zhang, Qing Li, Lei Chen  
**Institutions:** The Hong Kong Polytechnic University; The Hong Kong University of Science and Technology (Guangzhou)  
**Submitted:** April 9, 2026  
**Field:** Systems Security / LLM Security / Retrieval-Augmented Generation

---

## Executive Summary

Retrieval-Augmented Generation (RAG) has become the dominant architecture for deploying LLMs in production, enabling knowledge grounding without expensive fine-tuning. However, RAG's reliance on an **external knowledge pipeline** introduces a distinct attack surface that is neither purely an LLM problem nor a classical database security problem. This paper presents the first systematic security taxonomy for RAG systems, abstracting the workflow into 6 stages, identifying 3 trust boundaries and 4 primary security surfaces, and cataloguing known attacks and defenses across each. The finding that current defenses remain **reactive and fragmented** — patching individual vulnerabilities rather than addressing structural RAG-specific risks — makes this a critical reference for anyone deploying RAG in production.

---

## Problem Statement

### RAG's Security Blind Spot

RAG systems augment LLM responses by retrieving relevant documents from an external knowledge base at query time. A typical RAG pipeline involves:
1. User submits a query
2. An embedding model encodes the query
3. A vector database retrieves top-K relevant chunks
4. Retrieved chunks are injected into the LLM context
5. The LLM generates a response conditioned on both query and retrieved context

While much work has addressed LLM safety (jailbreaks, harmful content), RAG introduces **new attack vectors** through the retrieval mechanism that existing LLM safety work largely ignores:
- An attacker can poison the knowledge base *before* queries arrive
- Retrieval can be manipulated to inject adversarial content even for benign prompts
- Private documents in the knowledge base may be extractable via carefully crafted queries

### The Boundary Problem

A fundamental ambiguity in the field: which vulnerabilities are *inherent LLM flaws* (e.g., hallucination, instruction-following failures) versus *RAG-specific or RAG-amplified risks* (e.g., knowledge poisoning, retrieval manipulation)?

Prior work conflates these two categories, leading to:
- Inflated attack surface estimates (attributing LLM flaws to RAG)
- Misdirected defenses (applying LLM guardrails where retrieval-level interventions are needed)
- No clear operational boundary for RAG system security engineering

The paper's core contribution is establishing this **operational boundary** and building a taxonomy around it.

---

## Core Concepts & Theory

### RAG System Architecture

A RAG system can be decomposed into the following 6 stages:

```
[Indexing] → [Query Processing] → [Retrieval] → [Augmentation] → [Generation] → [Post-processing]
    ↑                                                                                      ↓
[Knowledge Base]                                                              [User Response]
```

**Stage 1 — Indexing:** Raw documents are chunked, embedded, and stored in a vector database. Attack surface: document injection, chunk manipulation.

**Stage 2 — Query Processing:** User query is preprocessed, potentially rewritten or expanded. Attack surface: query injection, adversarial query crafting.

**Stage 3 — Retrieval:** Top-K documents retrieved via embedding similarity. Attack surface: retrieval manipulation, embedding space attacks.

**Stage 4 — Augmentation:** Retrieved documents are formatted and inserted into the LLM prompt. Attack surface: context injection, format manipulation.

**Stage 5 — Generation:** LLM generates response conditioned on augmented context. Attack surface: prompt injection via retrieved content, context exploitation.

**Stage 6 — Post-processing:** Response filtering, citation extraction, output formatting. Attack surface: output poisoning, filtering bypass.

### Trust Boundaries

The paper identifies 3 fundamental trust boundaries in RAG systems:

**Boundary 1 — Knowledge Provider Trust:** Does the system trust the source of documents added to the knowledge base? (Internal documents: high trust; Web-scraped documents: low trust)

**Boundary 2 — User Trust:** Does the system treat user queries as potentially adversarial? (Consumer apps: zero trust; Enterprise internal: moderate trust)

**Boundary 3 — Model Trust:** Does the system trust the LLM's ability to ignore adversarial content in retrieved documents? (No current LLM can be unconditionally trusted here)

### The Four Security Surfaces

| Security Surface | Threat Stage | Example Attack |
|-----------------|--------------|----------------|
| Pre-retrieval knowledge corruption | Indexing | Poison documents to alter future responses |
| Retrieval-time access manipulation | Retrieval | Craft queries to retrieve target documents |
| Downstream context exploitation | Augmentation/Generation | Inject instructions via retrieved content |
| Knowledge exfiltration | Query/Generation | Extract private knowledge base contents |

---

## Main Ideas & Key Contributions

### 1. Operational Boundary Definition

The paper's most fundamental contribution: **secure RAG is about securing the external knowledge-access pipeline**, not about securing the LLM itself. This clean separation enables targeted security engineering.

Formally: a vulnerability is a *RAG-specific risk* if and only if it does not exist (or is substantially less severe) in a RAG-free LLM deployment with the same query and generation policy.

### 2. Attack Taxonomy

**Knowledge Poisoning Attacks (Pre-retrieval):**
- *Passive poisoning:* Inject malicious documents into the knowledge base directly
- *Active poisoning:* Craft documents that rank highly for target queries while appearing benign
- *Trigger-based poisoning:* Documents that only activate when specific keywords appear in the query (backdoor-style)

**Retrieval Manipulation Attacks:**
- *Embedding space attacks:* Craft documents whose embeddings are close to many query embeddings (denial of service via retrieval flooding)
- *Ranking manipulation:* Exploit the reranker model's vulnerabilities to elevate adversarial documents

**Context Exploitation Attacks (Prompt Injection via RAG):**
- *Direct injection:* Hide instructions in documents that override the system prompt when retrieved (e.g., "Ignore all previous instructions...")
- *Indirect injection:* Instructions are embedded in content that appears semantically relevant to benign queries
- *Cross-context attacks:* Use retrieved content to exfiltrate information from the LLM's other context windows

**Knowledge Exfiltration:**
- *Reconstruction attacks:* Query the RAG system with diverse queries to reconstruct the knowledge base
- *Membership inference:* Determine whether specific documents are in the knowledge base
- *Attribute inference:* Extract sensitive attributes from private documents via carefully crafted queries

### 3. Defense Taxonomy

**Input/Query Defenses:**
- Query sanitization, intent classification, rate limiting
- Effectiveness: high for obvious attack patterns, low for semantically sophisticated attacks

**Knowledge Base Defenses:**
- Document provenance tracking, anomaly detection for newly indexed content
- Access control lists for document retrieval
- Effectiveness: good for passive poisoning, limited for active/trigger-based poisoning

**Retrieval Defenses:**
- Certified robustness for embedding models
- Reranker anomaly detection
- Multi-source retrieval with majority voting
- Effectiveness: moderate, computationally expensive

**Generation-time Defenses:**
- Context-aware prompt injection detection
- Retrieved context quarantine (treat retrieved content as untrusted user input)
- Attribution-based filtering (require LLM to cite sources; flag uncited factual claims)
- Effectiveness: best current defense, but adds 20–40% latency

### 4. Gap Analysis: Reactive vs. Proactive Defenses

The paper's most impactful finding: current RAG defenses are **reactive** (responding to known attack patterns) rather than **proactive** (providing structural guarantees). No current defense provides:
- Formal security guarantees against adaptive adversaries
- Protection against all four security surfaces simultaneously
- Deployable defense with acceptable performance overhead

---

## Methodology & Implementation

### Survey Scope

- **Papers reviewed:** ~200 papers on RAG, LLM security, knowledge poisoning, and adversarial NLP (2022–2026)
- **Attacks documented:** 34 distinct attack types across the 4 security surfaces
- **Defenses documented:** 28 defense mechanisms
- **Benchmarks surveyed:** RAG-Attack-Bench, PoisonedRAG, AdvRAG, BEIR-Security

### Threat Model Formalization

Each attack is characterized along:
- **Attacker capability:** Read/write access to knowledge base? Query access only?
- **Attacker knowledge:** White-box (knows model and embedding function)? Black-box?
- **Attack goal:** Targeted (specific query → specific wrong answer) or untargeted (degrade quality generally)?
- **Stealthiness requirement:** Must the attack evade detection?

### Benchmark Summary

| Benchmark | Attack Types | Metrics | Key Finding |
|-----------|--------------|---------|-------------|
| PoisonedRAG | Knowledge poisoning | ASR, BLEU | 5 injected docs can achieve >80% ASR |
| AdvRAG | Retrieval manipulation | Recall@K change | Embedding attacks reduce Recall@10 by 47% |
| RAG-Attack-Bench | Context injection | Detection rate | Current LLMs detect <60% of injections |

### Key Empirical Results

- **Poisoning efficiency:** As few as **5 adversarial documents** (in a 10K-document corpus) achieve >80% targeted attack success rate on GPT-4-based RAG systems
- **Injection detectability:** State-of-the-art injection detectors miss 40%+ of sophisticated indirect injection attacks
- **Exfiltration feasibility:** ~500 queries suffice to reconstruct 60% of a 1,000-document knowledge base

---

## Practical Applications & Real-World Use Cases

### 1. Enterprise RAG Deployment

Companies deploying internal RAG systems (HR chatbots, document Q&A, code assistants) face insider threats via knowledge base poisoning. This paper provides:
- A risk assessment framework for the specific attack surface
- Prioritized defense recommendations based on trust boundary analysis
- Architectural guidance for high-security deployments (multi-source retrieval, provenance tracking)

### 2. Customer-Facing RAG Products

Consumer-facing RAG products (search engines, shopping assistants, news summarizers) that index public web content are most vulnerable to active poisoning, since adversaries can publish crafted web pages. The paper's analysis of web-scraped knowledge bases guides:
- Source trust scoring
- Anomaly detection for newly indexed content
- Rate limiting for queries that retrieve from recently added documents

### 3. Healthcare and Legal RAG

High-stakes domains where a wrong AI-generated answer has serious consequences require the strongest defenses. The paper's taxonomy enables compliance teams to systematically audit their RAG systems against each attack surface.

### 4. Security Tool Development

The taxonomy provides a roadmap for building RAG-specific security tools:
- **RAG firewall:** Input sanitization + retrieval monitoring + output filtering
- **Knowledge base integrity monitor:** Detects anomalous document injection
- **Adversarial query detector:** Flags queries that appear designed to trigger retrieval of target documents

### Implementation Challenges

- **Latency overhead:** Defense layers add 20–100% latency, unacceptable for real-time applications
- **False positive cost:** Aggressive filtering blocks legitimate queries
- **Adaptive attackers:** Defenses trained on known attack patterns are vulnerable to novel attack variants
- **Encrypted knowledge bases:** Privacy-preserving retrieval (via private information retrieval) has not yet been integrated with RAG at scale

---

## Insights & Implications

### RAG Security is a Systems Problem

The paper establishes that RAG security cannot be solved by improving the LLM alone. It requires **defense-in-depth across the full pipeline**: secure knowledge ingestion, robust retrieval, generation-time context quarantine, and output auditing. This has architectural implications for AI infrastructure teams.

### The Attacker Has Structural Advantages

In RAG systems, the attacker can act *before* queries are made (via knowledge poisoning) and in *real time* (via query injection). Defenders must protect against both temporal modes simultaneously, creating an asymmetric security game.

### Standardization Needed

The lack of standardized threat models and benchmarks has hindered progress. The paper calls for:
- A standard RAG security benchmark covering all 4 surfaces
- Formal definitions of "RAG-secure" systems (analogous to cryptographic security definitions)
- Responsible disclosure frameworks for RAG vulnerabilities

### Limitations

1. **Dynamic knowledge bases:** Most analysis assumes a static knowledge base; continuous indexing creates additional attack windows
2. **Multimodal RAG:** Image/audio retrieval introduces new attack surfaces not covered
3. **Multi-hop RAG:** Iterative retrieval systems have compounding attack surfaces not fully analyzed

### Open Questions

- Can we achieve provably secure retrieval with acceptable performance?
- How do RAG security properties degrade as the knowledge base scales to billions of documents?
- Are there RAG architectures that are structurally more secure (e.g., verified retrieval with cryptographic proofs)?

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2604.08304](https://arxiv.org/abs/2604.08304)
- **HTML Full Text:** [https://arxiv.org/html/2604.08304v1](https://arxiv.org/html/2604.08304v1)

### Referenced Attack Implementations

| Attack | Repository |
|--------|-----------|
| PoisonedRAG | [https://github.com/sleeepeer/PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG) |
| Phantom (Indirect Injection) | [https://github.com/BerkeleyRiskRL/Phantom](https://github.com/BerkeleyRiskRL/Phantom) |
| RAG-Jailbreak | Check arXiv for release |

### Quick Security Assessment Checklist

```
□ Is the knowledge base access-controlled? (Who can add documents?)
□ Are newly indexed documents reviewed before becoming retrievable?
□ Is retrieved context treated as untrusted input by the LLM prompt?
□ Is there rate limiting on queries to prevent reconstruction attacks?
□ Is there anomaly detection on retrieval patterns?
□ Are there output filters for detected injection patterns?
```

---

## Related Work & Context

### Building On

- **Lewis et al. (2020):** Original RAG paper — dense retrieval + seq2seq generation
- **Zou et al. (2023):** Universal adversarial suffixes for LLMs (injection primitives)
- **Perez & Ribeiro (2022):** Prompt injection as a formal attack class
- **PoisonedRAG (Zou et al., 2024):** First systematic study of knowledge poisoning in RAG

### Concurrent Work

- **MCP Security (2604.07551):** Extends security analysis to Model Context Protocol — similar taxonomy approach for tool-use pipelines
- **Adaptive Defense Orchestration for RAG (2604.20932):** Proposes a Sentinel-Strategist architecture for adaptive multi-vector attack defense
- **Secure RAG via Distance-Preserving Encryption (2601.12331):** Privacy-preserving retrieval approach

### Where This Leads

1. **Formal RAG security:** Cryptographically verifiable retrieval with integrity guarantees
2. **Adversarially robust embeddings:** Embedding models certified against embedding space attacks
3. **Differentially private RAG:** Provable privacy guarantees against knowledge exfiltration
4. **RAG security standards:** Industry standards analogous to OWASP for web applications, tailored to LLM+RAG systems
