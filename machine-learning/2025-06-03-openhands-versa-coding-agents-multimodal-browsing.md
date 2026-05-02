# Coding Agents with Multimodal Browsing are Generalist Problem Solvers

**ArXiv ID**: [2506.03011](https://arxiv.org/abs/2506.03011)  
**Authors**: Aditya Bharat Soni, Boxuan Li, Xingyao Wang, Valerie Chen, Graham Neubig  
**Institution**: Carnegie Mellon University  
**Published**: June 3, 2025  
**Venue**: EACL 2026 Findings  
**Field**: Machine Learning, AI Agents, Software Engineering

---

## Executive Summary

OpenHands-Versa challenges the prevailing trend of building narrowly specialized AI agents by demonstrating that a compact, general-purpose toolkit—code editing and execution, web search, and multimodal web browsing—is sufficient to simultaneously outperform the best specialized agents on three diverse and challenging benchmarks: SWE-Bench Multimodal (software engineering), GAIA (knowledge tasks), and The Agent Company (workplace automation). The work provides both a practical high-performing open-source agent and a theoretical insight: generality and specialization are not necessarily at odds when the right tools are chosen.

---

## Problem Statement

### The Specialization Trap

The AI agent landscape in 2025 is dominated by *specialized agents*: systems engineered and tuned for a single domain. SWE-agents are optimized for repository-level code editing; web agents are designed for browser interaction and form-filling; workflow agents handle structured enterprise processes. Each achieves strong performance in its niche, but:

1. **Cross-domain failure**: A state-of-the-art SWE-agent, given a knowledge retrieval task, falls far below even a basic browser-equipped agent.
2. **Benchmark overfitting**: Specialized agents often incorporate benchmark-specific tricks (e.g., custom repository navigation heuristics) that don't generalize.
3. **Deployment complexity**: Maintaining multiple specialized agents for different use cases incurs significant engineering overhead.

### The Research Question

> *What is the minimal, domain-agnostic set of tools that enables a single agent to perform at or above the state-of-the-art across a diverse range of tasks?*

### Limitations of Prior Generalist Attempts

Previous attempts at generalist agents either:
- Provided **too many tools** (causing the agent to be confused about which tool to use for a given context)
- Relied on **task-specific scaffolding** embedded in the agent's system prompt
- Used **text-only browsing** (capturing web content as plain text), losing visual layout, charts, UI screenshots, and other visual information critical for many tasks

---

## Core Concepts & Theory

### 1. The OpenHands Agent Framework

OpenHands-Versa is built on **OpenHands** (v0.28.1), an open-source agent framework with the following architecture:

```
┌─────────────────────────────────────────┐
│              LLM Backend                │
│    (e.g., Claude, GPT-4o, Gemini)       │
└────────────────────┬────────────────────┘
                     │  Action requests
                     ▼
┌─────────────────────────────────────────┐
│          Event Stream Controller        │
│  - Maintains conversation history       │
│  - Routes tool calls                    │
│  - Manages context window               │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐    ┌──────────────────────┐
│  Sandboxed      │    │  Browser Environment  │
│  Runtime        │    │  (Playwright-based)   │
│  - Bash shell   │    │  - Navigate URLs      │
│  - File system  │    │  - Click/fill forms   │
│  - Code exec    │    │  - Screenshot capture │
└─────────────────┘    └──────────────────────┘
```

The **event stream architecture** ensures that all agent actions and observations are logged as structured events, enabling reproducibility and debugging.

### 2. The Four General Tools

OpenHands-Versa equips the agent with exactly four tool categories:

| Tool | Description | Why It's General |
|------|-------------|------------------|
| **Code editing** | Read/write/diff files, navigate repos | Most knowledge work involves structured documents |
| **Code execution** | Run scripts, test code, call APIs | Enables computation, verification, and automation |
| **Web search** | Query search engines, retrieve documents | Access to current knowledge and documentation |
| **Multimodal web browsing** | Navigate browsers, capture screenshots | Access to visual content, forms, interactive UIs |

The key addition over previous agents is **multimodal browsing**: rather than scraping web pages to plain text, the agent renders pages and captures screenshots, which it passes to a vision-capable LLM. This enables the agent to:
- Read charts, graphs, and tables that don't render well as text
- Interact with visual UIs (clicking buttons, filling forms from visual context)
- Navigate web applications that require visual understanding

### 3. Context Condensation for Long Browsing Sessions

A challenge with browser-based agents is that web pages produce large observations. A single page might generate thousands of tokens of DOM/screenshot data. To manage context length:

```
Browsing History: [page₁, page₂, page₃, ..., pageₙ]
                                              ↓  (condensation)
[placeholder, placeholder, ..., pageₙ₋ₖ, ..., pageₙ]
```

The **browsing condenser** retains only the `k` most recent browsing observations, replacing older ones with a fixed placeholder message. This:
- Prevents context overflow during long web sessions
- Keeps the most relevant recent context
- Reduces LLM inference cost on long tasks

### 4. Domain-Aware Tool Selection

A core finding of the paper is that OpenHands-Versa exhibits **domain-aware tool selection**: given a software engineering task, it predominantly uses code tools; given a knowledge retrieval task, it predominantly uses browser tools. This emergent specialization arises without any task-type classification logic—it comes entirely from the LLM's ability to interpret the task description and choose appropriate tools.

---

## Main Ideas & Key Contributions

### Contribution 1: The Minimal General Toolkit Hypothesis

The paper makes a bold empirical claim: code + web_search + multimodal_browser is a **near-complete general toolkit** for knowledge work. The evidence:
- It suffices for software engineering tasks (SWE-Bench Multimodal)
- It suffices for general factual/reasoning tasks (GAIA)
- It suffices for enterprise workflow tasks (The Agent Company)

This suggests that most knowledge work can be decomposed into: *retrieving information* (search + browsing), *processing information* (code execution), and *creating/modifying artifacts* (code editing).

### Contribution 2: Multimodal Browsing as a Key Differentiator

Ablation experiments show that removing multimodal browsing (falling back to text-only web scraping) causes a meaningful performance drop, particularly on tasks involving:
- Reading charts and graphs from documentation
- Interacting with visual interfaces
- Tasks from the GAIA benchmark that require visual reasoning about web content

### Contribution 3: Cross-Benchmark SOTA Without Specialization

Previously, achieving SOTA on *one* of these benchmarks typically required architectural choices that hurt performance on the others. OpenHands-Versa achieves:
- **SWE-Bench Multimodal**: +9.1 percentage points over previous published SOTA
- **GAIA**: +1.3 percentage points over previous published SOTA  
- **The Agent Company**: +9.1 percentage points over previous published SOTA

### Contribution 4: Open-Source Implementation Merged Upstream

The methodology has been merged into the main OpenHands repository, making it immediately available to the community. This is practically significant: OpenHands-Versa is not just a research artifact but a production-ready open-source agent.

---

## Methodology & Implementation

### Benchmark Descriptions

| Benchmark | Type | Description | # Tasks |
|-----------|------|-------------|----------|
| **SWE-Bench Multimodal** | Software Engineering | Fix GitHub issues with visual context (screenshots, diagrams) | ~300 instances |
| **GAIA** | General AI | Multi-step reasoning tasks requiring tool use and web search | ~450 tasks |
| **The Agent Company** | Workplace Automation | Enterprise tasks: code review, document creation, data analysis | ~175 tasks |

### Evaluation Protocol

- **SWE-Bench Multimodal**: Automated test suite evaluation—patches are applied and test suites run
- **GAIA**: Exact-match evaluation on final answers
- **The Agent Company**: Task completion scoring by automated graders

### Experimental Configuration

```yaml
Base Framework: OpenHands v0.28.1
LLM Backend: claude-3-7-sonnet (Anthropic) # Primary experiments
Browser Engine: Playwright with Chromium
Context Condensation: k=5 most recent browsing observations
Max Steps: 50 per task (to control compute)
```

### Ablation Studies

The paper systematically evaluates tool subsets:

| Configuration | SWE-Bench MM | GAIA | Agent Company |
|---------------|--------------|------|---------------|
| Code only | High | Low | Medium |
| Code + Text browser | Medium | Medium | Medium |
| Code + Multimodal browser | Higher | Higher | Higher |
| Code + Web search + MM browser | **Best** | **Best** | **Best** |

### Tool Usage Analysis

A unique contribution is quantitative analysis of *how* tools are used:
- **SWE-Bench tasks**: ~70% of actions involve code tools, ~20% browser, ~10% search
- **GAIA tasks**: ~55% browser, ~30% search, ~15% code
- **Agent Company tasks**: ~50% code, ~30% browser, ~20% search

This domain-aware distribution emerges from the LLM's reasoning, not explicit routing logic.

---

## Practical Applications & Real-World Use Cases

### 1. Software Development Assistance

The SWE-Bench results directly translate to real-world code assistance:
- **Bug fixing with visual context**: Issues that include screenshots of UI bugs or error dialogs (increasingly common in modern software development)
- **Documentation-driven development**: Reading visual API documentation to implement features
- **Code review automation**: Browsing PR diffs and CI dashboards visually

### 2. Research Assistance

GAIA-style tasks map to research workflows:
- Synthesizing information from multiple web sources
- Reading and reasoning about figures in papers or reports
- Fact-checking claims against web sources

### 3. Enterprise Automation

The Agent Company results demonstrate applicability to:
- Internal tool navigation (wikis, issue trackers, project management systems)
- Data gathering and report generation
- Code and process review workflows

### 4. Personal Productivity

A single OpenHands-Versa deployment could handle:
- Researching and summarizing topics from the web
- Writing and testing code
- Filling out forms, interacting with web apps
- Managing files and documents

### Implementation Challenges

- **Cost**: Multimodal LLM calls with screenshot inputs are more expensive than text-only calls. Long tasks with many browser screenshots can incur significant API costs.
- **Sandboxing**: The sandboxed runtime requires careful configuration to prevent the agent from making unintended system changes.
- **Browser reliability**: Real-world web pages are often poorly structured, use heavy JavaScript, or have anti-bot measures that complicate browser automation.
- **Context management**: Despite the browsing condenser, very long tasks can still exhaust context windows. Better long-context summarization remains an open problem.

---

## Insights & Implications

### Rethinking the Specialization Paradigm

The dominant narrative in agent development has been: *better performance requires more specialization*. OpenHands-Versa challenges this by showing that:

1. **The bottleneck is often the toolkit, not the model**: A capable LLM with the right tools can generalize without domain-specific scaffolding.
2. **Emergent specialization**: LLMs are capable of selecting appropriate tools for different task types without explicit routing rules.
3. **Multimodal perception is a general capability**: Visual browsing benefits all task types, not just those that seem visually oriented.

### The "Minimum Viable Toolkit" as a Research Primitive

This work implicitly introduces a new research question: *what is the minimum viable toolkit for [domain X]?* This could be applied to scientific research agents, customer service agents, or data analysis agents.

### Limitations

- **LLM-dependent**: Performance is tightly coupled to the capability of the underlying LLM. Weaker models may not exhibit the same domain-aware tool selection.
- **Single-session assumption**: The agent maintains no long-term memory between sessions. Persistent agents may need additional memory mechanisms.
- **Cost efficiency**: The multimodal approach is more expensive per task than text-only approaches; cost/performance tradeoffs may matter in high-volume deployments.
- **Safety and access control**: An agent with code execution + web browsing + file access has significant capabilities; deployment in sensitive environments requires careful sandboxing.

### Broader Impact

The merger of the approach into the mainline OpenHands repository means millions of developers can immediately use a SOTA generalist agent. This accelerates the practical adoption of agent-based automation and raises the bar for future specialized agent research (which must now justify why specialization is needed).

---

## Code & Resources

- **Research Repository**: [https://github.com/adityasoni9998/OpenHands-Versa](https://github.com/adityasoni9998/OpenHands-Versa)
- **Upstream OpenHands** (recommended for production use): [https://github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- **ArXiv Paper**: [https://arxiv.org/abs/2506.03011](https://arxiv.org/abs/2506.03011)
- **EACL 2026 Proceedings**: [https://aclanthology.org/2026.findings-eacl.318](https://aclanthology.org/2026.findings-eacl.318)

### Quick Start

```bash
# Install OpenHands (includes Versa capabilities upstream)
pip install openhands-ai

# Or via Docker (recommended for sandboxed code execution)
docker pull ghcr.io/all-hands-ai/runtime:0.28-nikolaik

# Set up API key
export ANTHROPIC_API_KEY=your_key_here

# Run an agent task
python -m openhands.core.main \
  --task "Fix the bug described in this GitHub issue: [issue URL]" \
  --model claude-3-7-sonnet-20250219
```

### Computational Requirements

- **API-based**: No local GPU required; relies on LLM API
- **Browser**: Chromium (installed via Playwright)
- **Docker**: Recommended for sandboxed execution environment
- **Cost estimate**: GAIA tasks ~$0.50–2.00 each; SWE-Bench tasks ~$1.00–5.00 each depending on complexity

---

## Related Work & Context

### Foundational Agent Frameworks

| System | Approach | Limitation Addressed by OpenHands-Versa |
|--------|----------|------------------------------------------|
| **SWE-agent** (Yang et al., 2024) | Specialized bash + editor for code tasks | Text-only, fails on visual/general tasks |
| **AutoGPT** | LLM with web + code tools | Poor tool selection, hallucination-prone |
| **WebArena** agents | Browser-focused, text scraping | No code execution, text-only browsing |
| **OpenHands (base)** | Code + text browser | Lacks multimodal browsing |

### Key Related Papers

- **GAIA: A Benchmark for General AI Assistants** (Mialon et al., 2023): The benchmark that most directly motivated this research.
- **SWE-Bench Verified** (Chowdhury et al., 2024): The code-focused benchmark lineage.
- **The Agent Company** (Xu et al., 2024): Enterprise automation benchmark.
- **Multimodal Web Agents** (various, 2024–2025): The body of work on visual browser automation.

### Where This Research May Lead

1. **Cost-optimized generalist agents**: Can distillation or smaller models achieve similar generality at lower cost?
2. **Long-horizon generalist tasks**: Current evaluations max at ~50 steps. Multi-day, multi-session tasks remain an open frontier.
3. **Collaborative multi-agent pipelines**: Could multiple OpenHands-Versa instances collaborate on subtasks?
4. **Safety and alignment for powerful agents**: As agents become more capable and general, sandboxing, permission scoping, and monitoring become increasingly critical.
5. **Adaptive context condensation**: Smarter summarization of browsing history beyond the simple recency-based condenser.
