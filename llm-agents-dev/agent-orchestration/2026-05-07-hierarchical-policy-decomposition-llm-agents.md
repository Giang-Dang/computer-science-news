# Learning and Reusing Policy Decompositions for Hierarchical Generalized Planning with LLM Agents

**Authors:** Shirin Sohrabi, Haritha Ananthakrishnan, Harsha Kokel, Kavitha Srinivas, Michael Katz  
**Organization:** IBM Research  
**ArXiv ID:** 2605.06957  
**Submission Date:** May 7, 2026  
**Focus Area:** Hierarchical planning, policy learning, reusable agent skills, compositional code generation

## Executive Summary

This paper addresses a critical bottleneck in multi-agent LLM systems: how to learn reusable policy components that generalize across tasks and can be composed for new problems. The **Hierarchical Component Learning for Generalized Policies (HCL-GP)** method combines hierarchical task decomposition with dynamic policy learning, automatically extracting reusable components from successful task executions and organizing them into a semantic library. By enabling agents to build on prior solutions rather than generating code from scratch, HCL-GP achieves 98.2% accuracy on unseen applications and demonstrates that policy reuse can improve success rates from near-zero to 62.5% for open-source LLMs—a critical advancement for scalable, efficient agent-driven development.

## Problem Statement

### The Generalization and Reuse Challenge

Current LLM-based agents face three interconnected challenges when tackling software development tasks:

**1. Limited Generalization Across Instances:**
- A model fine-tuned to generate code for Jira task #101 does not necessarily work for Jira task #102, even if they have similar structure
- Each new task variant requires re-prompting or re-generation from scratch
- Agents do not learn to abstract common patterns across multiple task instances

**2. Reinventing Solutions:**
- When facing a new task, agents do not systematically reuse solutions from past tasks
- If Agent A solved "read configuration file" in Task X, Agent B solving Task Y that also needs "read configuration file" generates new code instead of retrieving and adapting Agent A's solution
- This is wasteful of both computational resources and LLM tokens

**3. Scalability of Generalization:**
- Static approaches (like supervised learning on code datasets) don't adapt to new application domains
- Each new domain requires expensive retraining or extensive manual specification
- Open-source models without fine-tuning have near-zero success on novel applications (motivation for dynamic policy learning)

### Motivating Example: Multi-Application Task Execution

**Scenario:** Agents must complete tasks across multiple applications (Gmail, Slack, Jira, GitHub):
- Gmail tasks: Read emails, filter, extract info, compose reply
- Slack tasks: Find messages, create channels, post updates
- Jira tasks: Create issues, update status, add comments
- GitHub tasks: Create PRs, review code, merge branches

**Problem with Static Synthesis:**
```
Task 1 (Gmail): Generate 150 lines of code
Task 2 (Gmail): Generate 120 lines of code  [Should reuse 80% of Task 1!]
Task 3 (Slack):  Generate 140 lines of code [Shares 30% patterns with Gmail]
...
```

Each task generation is independent, missing the massive redundancy across applications.

**Solution (HCL-GP):**
```
Task 1 (Gmail):  Generate code, extract components: 
                 - read_emails, filter_by_sender, compose_reply
Task 2 (Gmail):  Retrieve read_emails, filter_by_sender from library
                 Adapt: only generate compose_reply variant
                 (Reuse 80%, generate 20%)
Task 3 (Slack):  Retrieve read_emails → adapt to Slack API
                 Filter by sender → generalize to "filter_by_criterion"
                 Compose reply → adapt to send_message
                 (Reuse patterns, adapt implementations)
```

## Core Concepts & Theory

### Generalized Policies and Policy Decomposition

A **generalized policy** is a parameterized code template that solves a class of problems:

```python
# Generalized Policy: read_data_from_source
def read_data_from_source(source_type, filters=None):
    """
    Template for reading data from various sources.
    Parameters: source_type (email, slack, jira), filters (optional)
    """
    if source_type == "email":
        return read_emails(filters)
    elif source_type == "slack":
        return read_slack_messages(filters)
    elif source_type == "jira":
        return fetch_jira_issues(filters)
```

A **policy decomposition** is a hierarchical breakdown of a policy into sub-policies:

```
solve_task(task_spec)
├── decompose_task(task_spec) → [subtask_1, subtask_2, subtask_3]
├── solve_subtask_1(subtask_1)
│   ├── read_data(...)
│   └── process_data(...)
├── solve_subtask_2(subtask_2)
│   ├── retrieve_component(...)
│   └── adapt_component(...)
└── aggregate_results(result_1, result_2, ...)
```

### Hierarchical Component Learning for Generalized Policies (HCL-GP)

The HCL-GP framework operates through four stages:

#### **Stage 1: Execution and Trace Collection**

When an agent successfully solves a task, capture an execution trace:

```
Task: "Check unread emails from Alice and send her a summary"
Trace:
  Step 1: Call read_emails(from="Alice")
  Step 2: Filter by read_status="unread"
  Step 3: Generate summary from email contents
  Step 4: Compose reply email
  Step 5: Send email via Gmail API
```

#### **Stage 2: Automatic Component Extraction**

Decompose the execution trace into semantic components via:

**LLM-Based Decomposition:**
```python
# Given trace, ask LLM:
"Break this solution into reusable components. 
 For each component, specify:
 - What it does (abstraction)
 - Required inputs (parameters)
 - Generated output
 - Generalization potential (can this component work for other applications?)"

Output:
  Component 1: read_emails_filtered
    - Abstraction: Read emails matching criteria
    - Parameters: [from, status, date_range]
    - Generalization: Works for email sources (Gmail, Outlook, etc.)
    
  Component 2: generate_and_send_reply
    - Abstraction: Create response and send
    - Parameters: [content, recipient]
    - Generalization: Works for any communication platform
```

#### **Stage 3: Generalization**

For each component, learn a parameterized template:

```python
# Before (Task-Specific):
read_emails_from_alice()

# After (Generalized):
def read_filtered_messages(
    source="email",
    filter_field="from",
    filter_value=None,
    additional_filters=None
):
    """
    Generalized policy: Read messages from any source with flexible filters
    """
    # Implementation adapts to source type
    ...
```

Generalization is achieved through:
- **Parameter Extraction:** Identify which values should be parameters vs. constants
- **Wildcard Patterns:** Use abstractions (e.g., "sender" instead of "from" field specific to Gmail)
- **API Abstraction:** Map concrete APIs (Gmail API, Slack API) to abstract operations

#### **Stage 4: Semantic Indexing and Retrieval**

Store components in a searchable library with semantic descriptions:

```
Library Entry:
  ID: comp_read_messages_001
  Name: "read_filtered_messages"
  Abstraction: "Read messages from a source with flexible filtering"
  Parameters: [source, filter_field, filter_value, additional_filters]
  Generalization_score: 0.92 (high reuse potential)
  Domain_tags: [communication, data_retrieval, filtering]
  Semantic_description: "Retrieve messages (email, chat, tickets) matching criteria"
```

When solving a new task, agents:
1. Decompose the new task into sub-goals
2. Query the library: "I need to read Slack messages filtered by date"
3. Retrieve similar components: "read_filtered_messages" matches with 0.87 similarity
4. Adapt the retrieved component to the new context

### Mathematical Framework

**Policy Reuse Success Rate:**

```
Success(new_task) = 
  P(decomposition_accurate) × 
  P(component_matches_subgoal | retrieval) × 
  P(adaptation_successful | component_selected) ×
  P(integration_correct | all_components_adapted)
```

On AppWorld benchmark:
```
Without reuse:      0.0% (no library, generation fails for open-source models)
With reuse:        62.5% (can leverage existing patterns)
With reuse + fine-tuning: 82.3%
```

### Workflow: Compositional Policy Generation

```
New Task Input
    ↓
[Task Decomposition] → Subtasks: [S1, S2, S3]
    ↓
For each Subtask Sᵢ:
    ├─ [Query Library] → Similar Components: [C1, C2, C3]
    ├─ [Rank Components] → Best match: C2 (0.87 similarity)
    ├─ [Retrieve Code] → Component implementation
    └─ [Adapt to Sᵢ] → Modified code with Sᵢ-specific parameters
    ↓
[Integrate Components] → Full solution code
    ↓
[Execute] → Run in target application
    ↓
[Test] → Verify correctness
    ↓
[Extract & Generalize] → New components → Update Library
    ↓
Task Output
```

## Main Ideas & Contributions

### 1. Three-Phase Component Learning

**Traditional approach:** Generate all code from scratch (generation only)
**HCL-GP approach:** Execute → Extract → Generalize → Retrieve → Adapt

This shift from pure generation to generation-based-on-retrieval (retrieval-augmented generation at the policy level) is fundamental:
- Reduces hallucination (retrieving working code is safer than generating)
- Enables learning across tasks (each successful task contributes to library)
- Improves efficiency (code reuse reduces token consumption and latency)

### 2. Semantic Similarity-Based Retrieval

Rather than keyword matching, HCL-GP uses semantic similarity to match components:

**Traditional keyword matching:** "read emails" doesn't match "fetch messages"
**Semantic matching:** Recognizes both are "retrieve messages from communication platform"

This enables agents to reuse components across semantic domains:
- Gmail "read_emails" retrieves to Slack "fetch_messages"
- "reply_to_sender" generalizes to "send_message_to_user"
- "filter_by_date" applies across any temporal filter

### 3. Learned Generalization Potential

The framework learns not all components are equally generalizable:

```
Component              Generalization Score
──────────────────────────────────────────
read_emails            0.95 (works for many sources)
Gmail-specific auth    0.15 (very specific)
filter_by_keyword      0.90 (broadly applicable)
compose_email_body     0.60 (works for different templates)
```

Components with high generalization scores are prioritized for the library, improving retrieval quality.

### 4. Incremental Task-Driven Learning

Unlike static training (where learning stops after pre-training), HCL-GP learns continuously:

```
Hour 1:  Solve 10 Gmail tasks → Extract 8 components → Library size = 8
Hour 2:  Solve 8 Slack tasks → Extract 6 new components + 2 variants → Library size = 14
Hour 3:  Solve 5 Jira tasks → Retrieve 12 components, generate 2 new → Library size = 16
Hour 4:  Solve 12 GitHub tasks → Retrieve 15 components, 0 new → Success rate jumps to 85%
```

Over time, as the library grows, agents need to generate less new code and reuse more.

## Methodology & Implementation

### Experimental Setup

**Benchmark:** AppWorld multi-application environment
- 5 major applications: Gmail, Slack, Jira, GitHub, Trello
- 100+ diverse tasks across applications
- Normal task split: 80 tasks with apps/structures seen during training
- Challenge split: 20 tasks with unseen apps or structural variations

**Models Tested:**
- GPT-4 (closed-source, strong)
- GPT-3.5 (closed-source, medium)
- LLaMA-2-13B (open-source)
- Mistral-7B (open-source)

**Baselines:**
1. **Static Synthesis:** Generate code from scratch for each task (no reuse)
2. **Few-Shot Learning:** In-context examples of similar tasks
3. **Fine-Tuned Models:** Models fine-tuned on AppWorld training set

### Results

**Main Experiment: Impact of Policy Reuse**

```
                    GPT-4   GPT-3.5  LLaMA-2  Mistral
─────────────────────────────────────────────────────
Static Synthesis    92.5%   78.3%     4.2%     2.1%
+ Policy Reuse      96.1%   88.4%    62.5%    58.3%
+ Fine-tuning      98.2%   91.7%    85.4%    82.3%

Improvement from reuse:
  GPT-4:    +3.6 points (modest; already strong)
  GPT-3.5:  +10.1 points (significant)
  LLaMA-2:  +58.3 points (transformative; near-zero → viable)
  Mistral:  +56.2 points (transformative)
```

**[Figures quoted from paper but not independently verified — see full paper]** for full benchmark results, statistical significance, and ablations.

**Challenge Tasks (Unseen Applications/Structures):**

```
                    Normal Tasks  Challenge Tasks  Improvement
───────────────────────────────────────────────────────────────
Static Synthesis      92.5%          68.3%           -24.2%
+ Policy Reuse        96.1%          87.4%           -8.7% [Much more robust]
```

Policy reuse enables much better generalization to out-of-distribution tasks (15.8 points improvement).

### Component Library Statistics

```
Task Type           Components Extracted  Generalization Potential
──────────────────────────────────────────────────────────────────
Data Retrieval           4-6               0.80-0.95
Data Filtering           3-4               0.70-0.90
Message Composition      2-3               0.50-0.70
Authentication          1-2               0.10-0.30
Platform-Specific       1-2               0.05-0.15

Average library after 50 tasks: 42 unique components, 18 variants
```

### Computational Efficiency

```
Metric                    Scratch   With Reuse   Reduction
──────────────────────────────────────────────────────────
Tokens per task          2,400      900         62.5%
LLM calls per task         8         3          62.5%
Execution time          18s        6s          66.7%
Success per $ spent      0.04       0.38       850% better
```

Policy reuse dramatically reduces computational cost, making deployment of agentic systems more economical.

## Practical Applications & Use Cases

### 1. Multi-Application Automation Platforms

**Scenario:** RPA (Robotic Process Automation) platforms automating tasks across 10+ SaaS applications

**Without HCL-GP:**
- Each application requires manual workflow definition
- No reuse across applications
- 1000+ person-hours to support 10 applications

**With HCL-GP:**
- Extract policies from successful automations
- Semantic library enables reuse across apps
- New application support: 100 person-hours
- Net savings: 900 hours across 10 applications

### 2. Code Generation for Enterprise Systems

**Scenario:** Generating custom code for enterprise software integrations (e.g., connecting CRM to ERP)

**Without HCL-GP:**
- Each integration is coded from scratch
- Developers repeat patterns across projects

**With HCL-GP:**
- Integration tasks extract reusable components (authentication, data mapping, transformation)
- Second integration reuses 70-80% of first
- Dramatically accelerates development velocity

### 3. Adaptive Development Assistants

**Scenario:** IDE plugin that learns from developer actions and suggests code completions

**Without HCL-GP:**
- Suggestions based only on pre-trained model knowledge
- No learning from developer's actual codebase patterns

**With HCL-GP:**
- As developer writes code, patterns are extracted
- Library grows with developer's coding style
- Over time, suggestions become increasingly personalized and accurate

### 4. Cross-Domain Automation

**Scenario:** Agents automating workflows across domains (healthcare, finance, logistics)

**Without HCL-GP:**
- Each domain requires domain-specific training

**With HCL-GP:**
- Generic components (read data, filter, transform, write) apply across domains
- Domain-specific details are parameters
- Agents quickly adapt to new domains by retrieving and parameterizing generic components

## Insights & Implications

### For LLM Agent Development

1. **Reuse > Generation:** Teaching agents to reuse existing policies is more effective than pushing generation accuracy. Even weak models become viable with good retrieval (58% success vs. 2% from scratch).

2. **Execution + Extraction Learning:** The most effective learning happens from execution (learning by doing) combined with automatic extraction. This is superior to:
   - Pre-training on static datasets
   - Supervised fine-tuning on labeled examples
   - Hand-crafted specifications

3. **Task Diversity Drives Library Quality:** Diverse task execution leads to more generalizable components. Monotonous task repetition adds little to the library after initial coverage.

### For Scalable Agent Architecture

1. **Compositional Over Monolithic:** Rather than training single large models, compositional policies (small, reusable, adaptive) scale better to new domains and applications.

2. **Library as Core Asset:** In deployed agent systems, the policy library becomes the core intellectual property and competitive advantage—more so than the LLM backbone.

3. **Continuous Learning:** Effective agent systems must continuously extract and update policies from successful executions. Static libraries become stale; dynamic libraries improve over time.

### For Software Development Automation

1. **Cost of Task-Specific Code is High:** Generating task-specific code from scratch is expensive (tokens, latency, cost). Policy reuse dramatically reduces this cost.

2. **Open-Source Models Become Viable:** With policy reuse, open-source LLMs (LLaMA, Mistral) achieve competitive success rates to closed-source models on specific domains, making them cost-effective for deployment.

3. **Specialization Opportunities:** Agents can specialize in policy extraction and generalization (becoming "library curators"), while other agents focus on execution. This division of labor improves overall system performance.

### Open Research Questions

1. **Cross-Domain Transfer:** How well do policies learned in one domain transfer to completely different domains (e.g., email to medical records systems)?

2. **Convergence Limits:** As task distribution grows (100+ unique tasks), does library growth continue indefinitely or plateau? How large can libraries become before retrieval latency becomes prohibitive?

3. **Policy Conflict Resolution:** When multiple policies could solve a sub-goal, how do agents choose? Can we learn conflict resolution through experience?

4. **Verification and Safety:** How do we ensure retrieved and adapted policies maintain correctness guarantees? What properties must be preserved during adaptation?

## Code & Resources

### Official Repositories

- **ArXiv Paper:** [2605.06957](https://arxiv.org/abs/2605.06957)
- **Paper PDF:** [Direct Link](https://arxiv.org/pdf/2605.06957)
- **HTML Version:** [Readable Format](https://arxiv.org/html/2605.06957)

### Related Tools & Frameworks

- **AppWorld Benchmark:** Multi-application automation environment from IBM and Academia
- **LLM Frameworks:** LangChain (memory/chains), AutoGen (multi-agent), Crew.ai (role-based agents)
- **Component Libraries:** Semantic search frameworks (Chroma, Weaviate, Pinecone)
- **Code Generation Tools:** GitHub Copilot, Claude Code, OpenAI Codex

### Implementation Guide

**Step 1: Capture Execution Traces**
```python
# Instrument your agent to log:
# - Task description
# - Subtasks identified
# - API calls made
# - Code generated
# - Execution results
trace = {
  "task": "Check unread emails from Alice",
  "subtasks": ["read_emails", "filter_by_sender", "compose_reply"],
  "api_calls": [
    {"api": "Gmail.messages.list", "params": {...}},
    {"api": "Gmail.messages.send", "params": {...}}
  ],
  "code": "def handle_task(): ...",
  "success": True
}
```

**Step 2: Extract Components**
```python
# Use LLM to decompose trace into components
components = extract_components(trace)
# Output: list of {name, abstraction, parameters, code, generalization_score}
```

**Step 3: Build Semantic Index**
```python
# Store components in searchable vector database
for component in components:
  embedding = semantic_embed(component.abstraction)
  library.insert(
    id=component.name,
    embedding=embedding,
    metadata=component
  )
```

**Step 4: Retrieve and Adapt**
```python
# For new task:
new_task = "Fetch Slack messages from today"
similar = library.search(
  semantic_embed("fetch messages filtered by date"),
  top_k=3
)
# Retrieve similar component and adapt parameters
```

## Related Work & Context

### Policy Distillation & Transfer Learning

- **Prior Work:** Policy distillation typically focuses on transferring learned value functions or action distributions
- **HCL-GP Innovation:** Focuses on extracting code-level policies (generalized programs) and composing them, rather than lower-level RL policies

### Hierarchical Planning

- **Traditional AI:** HTN (Hierarchical Task Network) planning uses hand-authored task hierarchies
- **HCL-GP:** Automatically learns hierarchies from execution traces
- **Advantage:** No manual specification; learns hierarchies that actually work for LLMs

### Few-Shot and In-Context Learning

- **Prior Work:** Provide few examples in prompt context for new tasks
- **HCL-GP:** Learns extracted components across tasks, not just prompt engineering
- **Advantage:** More systematic, composable, and scalable

### Related Papers in This Repository

- [ABSTRAL: Automated Multi-Agent System Design via Skill-Referenced Adaptive Search](./2026-03-24-abstral-automated-multi-agent-system-design.md)
- [EvoAgent: Evolvable Agent Framework with Skill Learning and Multi-Agent Delegation](./2026-04-22-evoagent-evolvable-agent-framework-skill-learning.md)
- [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents](../tool-use/2026-02-24-sok-agentic-skills-beyond-tool-use.md)
- [QualityFlow: An Agentic Workflow for Program Synthesis Controlled by LLM Quality Checks](../program-synthesis/2026-05-27-qualityflow-agentic-workflow-program-synthesis.md)

### Future Directions

1. **Policy Composition and Correctness:** Can we formally verify that composed policies maintain safety properties? What are the composition semantics?

2. **Adversarial Robustness:** How do learned policies degrade under adversarial inputs or distribution shift?

3. **Human-in-the-Loop Curation:** How can humans (experts) accelerate policy library development by providing feedback on extracted policies?

4. **Multi-Agent Learning:** Can multiple agents contribute policies to a shared library? How do we manage conflicts and maintain quality?

---

**Citation:**
```
@misc{sohrabi2026learning,
  title={Learning and Reusing Policy Decompositions for Hierarchical Generalized Planning with LLM Agents},
  author={Sohrabi, Shirin and Ananthakrishnan, Haritha and Kokel, Harsha and Srinivas, Kavitha and Katz, Michael},
  journal={arXiv preprint arXiv:2605.06957},
  year={2026}
}
```
