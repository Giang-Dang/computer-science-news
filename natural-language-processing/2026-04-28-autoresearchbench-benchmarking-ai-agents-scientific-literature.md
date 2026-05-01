# AutoResearchBench: Benchmarking AI Agents on Complex Scientific Literature Discovery

**Paper**: [arXiv:2604.25256](https://arxiv.org/abs/2604.25256)  
**Authors**: Lei Xiong and 16 co-authors  
**GitHub**: [https://github.com/CherYou/AutoResearchBench](https://github.com/CherYou/AutoResearchBench)  
**Submitted**: April 28, 2026  
**Field**: Natural Language Processing / AI Agents / Benchmarking  

---

## Executive Summary

AutoResearchBench is a rigorous benchmark designed to measure how well AI agents can autonomously navigate the scientific literature — finding specific target papers (Deep Research) and comprehensively collecting papers satisfying specified conditions (Wide Research). Built from 1,000 expert-verified problems spanning 8 core computer science areas, and grounded in a controlled environment of over 3 million arXiv papers with full-text access, AutoResearchBench reveals a stark capability gap: **even the most powerful frontier LLMs, which have largely solved general web-browsing benchmarks, achieve only ~9% accuracy on these tasks**. This benchmark exposes that scientific literature discovery is a fundamentally harder, qualitatively different challenge from general web search — and it defines a new frontier for agentic AI research.

---

## Problem Statement

### The Gap Between Agentic Web Browsing and Scientific Research

Recent agentic benchmarks like **BrowseComp** (OpenAI) have shown that frontier LLMs have become remarkably capable at general web-browsing tasks — finding factual information, navigating multi-page workflows, answering obscure trivia. Many frontier models now achieve 70%+ accuracy on such benchmarks.

However, *scientific literature discovery* has fundamentally different requirements:

1. **Deep comprehension of scientific concepts**: Finding a paper is not about matching keywords — it requires understanding what methodology a paper uses, what problem it solves, how its results compare to others, and whether it satisfies a complex set of research criteria.

2. **Fine-grained utilization of detailed content**: The relevant information often lives in tables, figures, equation blocks, appendices, or reference lists — not in the abstract. An agent must reason about content buried deep within full papers.

3. **Open-endedness**: Unlike factual queries (which have single correct answers), scientific literature queries may have zero, one, or many qualifying papers. The agent must reason about *completeness* — knowing when it has found all qualifying papers, not just some.

4. **Multi-hop chaining**: Finding papers often requires chains of reasoning: identifying a concept in one paper, following its citations, finding related work that the first paper compares against, and locating the specific paper that introduced a particular technique three citation hops away.

### Why Existing Benchmarks Fall Short

| Benchmark | Focus | Why It Doesn't Capture Scientific Discovery |
|---|---|---|
| BrowseComp | General web search | Tasks have single unambiguous answers; content is in surface-accessible web pages |
| WebArena | Web navigation | Action space is UI interaction, not deep text comprehension |
| GAIA | Multi-step reasoning | Questions are answerable from general knowledge, not specific paper content |
| SWE-Bench | Code generation | Software tasks, not literature tasks |
| SciFact | Scientific claim verification | Verification of claims, not discovery of papers |
| PaperQA | Question answering over papers | Given papers as input; doesn't require finding papers |

**AutoResearchBench fills this gap**: it requires agents to autonomously search, retrieve, read, and reason about scientific papers to satisfy complex discovery criteria.

---

## Core Concepts & Theory

### The Two Task Types

**Task Type 1: Deep Research**

*Definition*: Given a natural language description of a target paper (describing its topic, methodology, key results, or context), the agent must identify the specific paper being described.

*Why it's hard*: The description may use different terminology than the paper's title or abstract. Identifying the correct paper requires:
- Understanding the described methodology deeply enough to map it to a specific algorithmic contribution
- Distinguishing the target from many similar papers that partially match the description
- Following multi-hop chains (e.g., "the paper that introduced the technique used in paper X's ablation study")

*Evaluation metric*: **Binary accuracy** — either the agent identifies the correct paper or it doesn't.

*Difficulty*: Even frontier LLMs achieve only **9.39% accuracy**.

**Task Type 2: Wide Research**

*Definition*: Given a set of conditions (e.g., "find all papers that use Transformer architectures for time series forecasting and were published in 2023"), the agent must comprehensively collect all qualifying papers.

*Why it's hard*: 
- The number of qualifying papers is unknown — the agent must decide when to stop searching.
- Recall is as important as precision — missing qualifying papers is penalized.
- The conditions may require understanding experimental details not stated in abstracts.

*Evaluation metric*: **Intersection over Union (IoU)** between the agent's retrieved set and the ground truth set.

*Difficulty*: Frontier LLMs achieve only **9.31% IoU**.

### The 3D Distinguishing Framework

AutoResearchBench is distinguished from prior benchmarks along three dimensions:

```
Research-Oriented
      │
      │  Tasks demand in-depth understanding of scientific
      │  concepts, not shallow keyword matching or common-
      │  sense reasoning. An agent must understand WHY a
      │  paper is relevant, not just THAT it appears relevant.
      │
Literature-Focused
      │
      │  Critical clues come from fine-grained paper content:
      │  tables, figures, equations, appendices, and reference
      │  lists. Surface-level abstracts are often insufficient.
      │
Open-Ended
      │
      │  The number of qualifying papers is unknown. The agent
      │  must reason about completeness and know when to stop.
      │  Sometimes zero papers satisfy the conditions.
```

### Controlled Evaluation Environment

To ensure reproducibility and prevent data contamination:

- A controlled environment is built over **3+ million arXiv papers** with up-to-date full-text extraction.
- The environment provides agents with standardized search tools:
  - **Keyword search**: BM25-based retrieval over paper titles, abstracts, and full text
  - **Semantic search**: Dense retrieval using embeddings
  - **Citation graph navigation**: Follow references and citations between papers
  - **Full text access**: Read complete paper content including tables, figures (OCR'd), and appendices
- Agents interact with this environment through a standardized action API.
- The environment is isolated from the open internet to prevent agents from exploiting external hints.

---

## Main Ideas & Key Contributions

### Contribution 1: The AutoResearchBench Dataset

**Scale**: 1,000 problems spanning 8 core CS areas:

| Area | # Problems |
|---|---|
| Machine Learning | ~200 |
| Computer Vision | ~150 |
| Natural Language Processing | ~150 |
| Algorithms & Theory | ~100 |
| Systems | ~100 |
| Human-Computer Interaction | ~100 |
| Robotics | ~100 |
| Security | ~100 |

**Construction methodology**: A "full-text-first human-machine pipeline":

1. **Automated candidate generation**: An LLM-assisted pipeline reads full papers and generates problem candidates — descriptions of papers designed to be challenging for retrieval.
2. **Human expert verification**: Domain experts verify that (a) each problem has a definitive answer, (b) the description is unambiguous, (c) the problem is appropriately difficult, and (d) the answer requires reading full paper content, not just abstracts.
3. **Adversarial filtering**: Problems that frontier LLMs can solve using only title/abstract information are removed, ensuring all problems require deep content engagement.

**Quality assurance**: Each problem is verified by at least 2 independent experts. Problems with expert disagreement are discarded.

### Contribution 2: Rigorous Baseline Evaluation

The paper evaluates a comprehensive set of baselines:

- **Frontier LLMs**: GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash, and comparable models
- **Reasoning-enhanced models**: o1, o3, Claude 3.7 Sonnet (extended thinking)
- **Search-augmented systems**: RAG pipelines with various retrieval strategies
- **Specialized research assistants**: Semantic Scholar API-based agents, PaperQA-style systems

**Key finding**: Even the best performing system (frontier LLMs with extended thinking) achieves only ~9-10% on both task types, while many strong baselines score below 5%.

### Contribution 3: Revealing the Research Discovery Gap

By exposing this gap between general web-browsing capability (~70%+ on BrowseComp) and scientific literature discovery (~9%), AutoResearchBench defines a new challenge frontier for the community. The gap suggests that:
- Scientific discovery is qualitatively harder than general web browsing
- Specialized capabilities (deep paper reading, citation chain reasoning) are needed
- Simply scaling LLMs may not be sufficient — new architectural or training approaches are needed

### Contribution 4: Open Evaluation Infrastructure

The benchmark, evaluation pipeline, and controlled environment are publicly released, enabling the community to:
- Develop new agents and track progress
- Conduct controlled ablation studies on retrieval vs. reasoning components
- Build specialized tools for scientific literature navigation

---

## Methodology & Implementation

### Benchmark Construction Pipeline in Detail

**Step 1: Seed Paper Selection**

Papers from arXiv (primarily 2020-2025) are sampled with stratified sampling across the 8 CS areas. Both highly-cited papers and newer, less-cited papers are included to ensure the benchmark tests true discovery ability, not just recall of famous papers.

**Step 2: Problem Generation**

For Deep Research tasks: An LLM reads the full paper and generates a description that:
- Omits the paper's title and author names
- References the methodology, key results, or specific contributions
- May reference the paper's relationship to other papers (requiring multi-hop reasoning)

For Wide Research tasks: A domain expert defines a set of conditions (topic + time period + methodological constraints) and manually identifies all qualifying papers in the controlled environment.

**Step 3: Difficulty Calibration**

Problems are tested against a baseline retrieval system. Problems that the baseline solves are removed. This ensures all retained problems require genuine agentic reasoning beyond simple keyword lookup.

**Step 4: Expert Validation**

Domain experts verify the answer and confirm the problem requires full-text engagement. The validation process includes:
- Confirming the target paper exists and is in the environment
- Confirming the description is unambiguous
- Confirming the necessary information is available in the full text

### Evaluation Protocol

**For Deep Research**:
```
Accuracy = (# correctly identified papers) / (total problems)
```
An agent's answer is correct if it returns the exact target paper (by arXiv ID).

**For Wide Research**:
```
IoU = |Retrieved ∩ Ground Truth| / |Retrieved ∪ Ground Truth|
```
This measures both precision (not returning non-qualifying papers) and recall (not missing qualifying papers).

**Agent interface**: Agents interact through a Python API:
```python
# Available tools
env.search_keyword(query, top_k=10)    # BM25 keyword search
env.search_semantic(query, top_k=10)   # Dense semantic search
env.get_paper_content(paper_id)        # Full text access
env.get_citations(paper_id)            # Papers this paper cites
env.get_cited_by(paper_id)            # Papers that cite this paper
env.submit_answer(paper_ids)           # Final answer submission
```

### Key Results

| System | Deep Research Accuracy | Wide Research IoU |
|---|---|---|
| BM25 retrieval (no LLM) | <2% | <3% |
| GPT-4o (no tools) | ~3% | ~2% |
| GPT-4o + search tools | ~6% | ~5% |
| Claude 3.5 Sonnet + search | ~7% | ~6% |
| Best frontier model + extended thinking | ~9.4% | ~9.3% |
| Human expert | ~85%+ | ~70%+ |

The human-AI gap is dramatic: human experts with the same tools achieve 85%+ accuracy, while the best AI systems reach only ~9%.

---

## Practical Applications & Real-World Use Cases

### 1. Autonomous Literature Review

A fully capable AutoResearchBench agent would be able to:
- Conduct comprehensive literature reviews for research papers
- Identify all relevant prior work given a research problem statement
- Track the provenance of specific techniques through the citation graph

### 2. Research Novelty Assessment

Before submitting a paper, researchers could use a capable agent to verify their claimed novelty — finding any existing work that substantially overlaps with their contributions.

### 3. Patent and IP Discovery

Patent searches require finding prior art — a task structurally similar to Deep Research. Improving agents on AutoResearchBench would directly benefit patent search quality.

### 4. Systematic Review Automation

Medical and scientific systematic reviews require finding *all* papers satisfying specific criteria — exactly the Wide Research task. Capable agents could dramatically accelerate systematic review workflows.

### 5. Academic Grant Writing Assistance

Grant proposals require demonstrating awareness of the state of the art and identifying gaps. An agent capable of comprehensive scientific literature discovery could assist grant writers in ensuring their proposals are grounded in complete knowledge of existing work.

### Implementation Challenges

- **Full-text processing cost**: Reading millions of papers in full is computationally expensive. Efficient retrieval that identifies candidate papers before committing to full reads is essential.
- **Citation graph reasoning**: Multi-hop citation chaining requires maintaining complex state across many paper reads.
- **Ambiguity resolution**: When a description matches multiple papers, the agent must gather more evidence to disambiguate — requiring sophisticated follow-up strategies.

---

## Insights & Implications

### Broader Implications for the Field

AutoResearchBench delivers a crucial reality check on the state of agentic AI:

1. **General capabilities do not transfer to specialized domains**: Despite near-human performance on general web tasks, the best AI systems fail dramatically on scientific literature discovery. Domain-specific benchmarks are essential for tracking real-world progress.

2. **Reading comprehension at the research level is unsolved**: The benchmark isolates reading comprehension as a key bottleneck — agents can retrieve candidate papers but fail to correctly parse complex methodological descriptions to identify the correct one.

3. **Completeness reasoning is a new frontier**: The Wide Research task challenges agents to know when they've found all qualifying items — a form of meta-reasoning about the completeness of their search that current LLMs handle poorly.

4. **Tool use and reasoning must be deeply integrated**: Simple RAG (retrieve-then-read) pipelines perform only marginally better than pure LLM approaches. Genuine improvement requires iterative, hypothesis-driven search strategies where reasoning informs retrieval and retrieval informs further reasoning.

### How This Advances State-of-the-Art

- Defines a new benchmark category: *autonomous scientific discovery*
- Provides a reproducible, controlled evaluation environment over a realistic document corpus (3M+ papers)
- Quantifies the gap between current AI capability and human expert performance on realistic research tasks

### Limitations

- **Static snapshot**: The benchmark is built from a snapshot of the arXiv corpus. As new papers are published, the ground truth may change (though the controlled environment remains static).
- **English-language only**: ArXiv papers are predominantly English; the benchmark does not test multilingual scientific discovery.
- **CS-focused**: While CS is a rich testbed, extending to other scientific domains (biology, physics, medicine) is left for future work.
- **Closed domain**: The controlled environment isolates agents from the open internet; real-world research also involves book chapters, conference proceedings, and closed-access journals.

### Open Questions

- What architectural components are most responsible for the human-AI performance gap?
- Do specialized training approaches (fine-tuning on scientific papers) significantly close the gap?
- Can mixture-of-agents approaches (different agents for retrieval, reading, and synthesis) outperform single-agent pipelines?

---

## Code & Resources

- **Official GitHub**: [https://github.com/CherYou/AutoResearchBench](https://github.com/CherYou/AutoResearchBench)
- **ArXiv Paper**: [https://arxiv.org/abs/2604.25256](https://arxiv.org/abs/2604.25256)
- **Dataset**: Released with the paper (see GitHub for access instructions)

### Quick Start

```python
from autoresearchbench import AutoResearchEnv, Evaluator

# Initialize the controlled environment
env = AutoResearchEnv(
    corpus_path="/path/to/arxiv-corpus",    # 3M+ papers, full text
    task_type="deep_research"               # or "wide_research"
)

# Load a benchmark problem
problem = env.load_problem(problem_id=42)
print(problem.description)  # Natural language description of target paper

# Agent interaction loop
while not env.done:
    # Agent searches and reads papers
    results = env.search_keyword("transformer time series forecasting")
    paper = env.get_paper_content(results[0].paper_id)
    # ... agent reasoning ...
    env.submit_answer([target_paper_id])

# Evaluate
score = Evaluator.score(env.agent_answer, problem.ground_truth)
```

### Computational Requirements

- **Storage**: ~2TB for the full arXiv corpus with extracted full text
- **Index**: ~50GB for BM25 and semantic search indices
- **Inference**: Standard GPU resources for LLM-based agents; the environment itself is CPU-bound

---

## Related Work & Context

### Builds Upon

- **BrowseComp** (OpenAI, 2025): The web-browsing benchmark that AutoResearchBench explicitly contrasts with; establishes that scientific discovery is harder than general web browsing.
- **PaperQA** (Lala et al., 2023): A system for answering questions about a given set of papers; AutoResearchBench tests the harder problem of finding the papers first.
- **SciAgent, ResearchAgent** (various, 2024-2025): Agents designed for scientific tasks; AutoResearchBench provides rigorous evaluation infrastructure for such systems.
- **GAIA Benchmark** (Mialon et al., 2023): Multi-step reasoning benchmark; AutoResearchBench focuses on the scientific literature subset of challenges GAIA raises.

### Related Contemporary Work

- **DeepResearch Bench** (arXiv:2506.11763, June 2026): A subsequent benchmark with broader scope (generates research reports rather than identifying specific papers); AutoResearchBench focuses on cleaner, more precisely evaluable discovery tasks.
- **AutoResearch-RL** (arXiv:2603.07300, March 2026): Explores reinforcement learning for autonomous research task execution; AutoResearchBench provides evaluation infrastructure for such systems.
- **CoSearch** (already in this repo, April 2026): Explores joint training of reasoning and document ranking; AutoResearchBench's findings on the limitations of retrieval-then-read pipelines motivate the joint training approach CoSearch explores.

### Where This Research Leads

- **Closed-loop research assistants**: AI systems that can autonomously conduct literature reviews, identify gaps, and suggest research directions.
- **Specialized scientific retrieval models**: Fine-tuned retrievers and readers trained on scientific paper content with research-oriented objectives.
- **Agentic research workflows**: Integration with experiment tracking, code execution, and writing tools to enable end-to-end autonomous research pipelines.
- **Cross-domain benchmarks**: Extensions to biology, chemistry, physics, and medicine to test whether scientific discovery capability generalizes across domains.
