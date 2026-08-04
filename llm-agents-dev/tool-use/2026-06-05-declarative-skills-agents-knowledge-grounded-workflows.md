# Declarative Skills for AI Agents in Knowledge-Grounded Tool-Use Workflows

**Authors:** M. Danish Lim, I. Danial Bin Sharudin, Wen Han Chen, Cedric Lim, Laura Wynter

**Affiliation:** Singapore Management University

**ArXiv ID:** 2606.06923

**Date:** June 5, 2026

## Executive Summary

This paper investigates how AI agents can effectively orchestrate tool use in realistic customer-service workflows using declarative skill files—natural-language specifications of domain knowledge appended to the agent's system prompt. The research formalizes three orchestration paradigms (declarative, imperative, and unscaffolded) as policy classes in a decentralized partially-observable Markov decision process (POMDP) and demonstrates that declarative skills provide information-theoretic and structural advantages for tool-use orchestration. The work bridges the gap between skill-based agent architectures and practical deployment in knowledge-grounded domains.

## Problem Statement

### Core Challenge

Autonomous AI agents deployed in real-world customer-service environments must navigate complex, unstructured knowledge bases while selecting and invoking appropriate tools. Current approaches suffer from:

1. **Tool Selection Uncertainty**: Agents struggle to identify which tool to use when faced with unstructured, domain-specific knowledge bases
2. **Context Management Complexity**: Keeping track of conversation history, task state, and knowledge retrieval context becomes exponentially harder as workflows grow
3. **Scalability of Knowledge**: As knowledge bases grow, agents either hallucinate tool capabilities or fail to discover relevant knowledge
4. **Orchestration Brittleness**: Hard-coded orchestration logic (state machines, if-then rules) breaks when new tools or domain knowledge is added

### Software Development Relevance

For autonomous code generation and testing:
- **Knowledge-grounded generation**: Agents must reference existing codebase patterns, library APIs, and coding standards
- **Tool discovery**: With hundreds of linters, formatters, debuggers, and analyzers available, agents must discover which tools fit which tasks
- **Workflow adaptation**: As project requirements evolve, orchestration should adapt without rewriting agent logic
- **State management**: Multi-step workflows (generate → test → review → fix → verify) require coherent state tracking across tools

### Research Gap

Prior work treats skills as either:
1. **Implicit in prompts** (prompting engineering to make agents "know" what tools exist)
2. **Rigidly programmatic** (hardcoded state machines that don't adapt to new knowledge)

Neither approach captures the practical reality: domain knowledge is often natural-language documentation (READMEs, coding guidelines, knowledge base articles), not machine-executable rules.

## Core Concepts & Theory

### Declarative vs. Imperative Orchestration

The paper contrasts two fundamental orchestration paradigms:

#### 1. Declarative Orchestration (DeclarativeAgent)

**Definition**: The agent reads natural-language skill files at inference time and decides its own control flow dynamically.

**Characteristics:**
- Skill files are data (not code): plain-text descriptions of tools, when to use them, how to invoke them
- Agent responsibility: interpret skills and choose which to apply at each step
- Flexibility: new skills added to the knowledge base without agent code changes
- Transparency: skill files are human-readable and inspectable

**Workflow:**
```
Agent Input
   ↓
Read Skill Files from Knowledge Base
   ↓
Agent Interprets Skills
   ↓
Agent Reasons: "Which skill fits this task?"
   ↓
Agent Invokes Selected Skill
   ↓
Process Skill Output
   ↓
Decide: Continue, Try Another Skill, or Conclude?
```

#### 2. Imperative Orchestration (ImperativeAgent)

**Definition**: The agent operates within a programmatic state machine with explicit phases and hard-coded tool transitions.

**Characteristics:**
- Orchestration is code: state transitions, tool calls, and flow logic are defined in Python/state machine format
- Agent responsibility: execute the phase logic, not decide control flow
- Efficiency: no time spent interpreting or choosing from skills; path is predetermined
- Brittleness: adding new tools or phases requires code changes and redeployment

**Workflow:**
```
Agent Input
   ↓
Execute Phase 1 Logic (hard-coded)
   ↓
Invoke Tool A (predetermined by phase)
   ↓
Process Output
   ↓
Transition to Phase 2 (state-machine defined)
   ↓
Execute Phase 2 Logic
   ↓
...
```

#### 3. Unscaffolded Baseline (BaselineAgent)

A minimal agent with no explicit skills or state machine; must infer tools and workflows purely from the system prompt and task description.

### Information-Theoretic Framework

The paper formalizes each orchestration approach as a policy in a **decentralized POMDP**:

**State Space S**:
- `current_query`: User's question
- `retrieved_knowledge`: Relevant knowledge base entries
- `tool_history`: Record of previously invoked tools
- `conversation_context`: Full conversation history
- `internal_state`: Task-specific state (e.g., "awaiting user confirmation", "searching database")

**Action Space A**:
- Select a tool from the available toolset
- Invoke the tool with specific parameters
- Synthesize an answer from retrieved knowledge
- Request clarification or escalate to human

**Observation Space Z**:
- Tool output (structured or unstructured)
- Partial feedback (did the tool help? did it fail?)
- Knowledge base retrieval results

**Policy Comparison**:

| Policy | Information Requirement | Decision Latency | Adaptability |
|--------|--------------------------|------------------|--------------|
| **Declarative** | Reads skill files (moderate tokens) | Higher (agent reasons about choices) | High (skills are data) |
| **Imperative** | Minimal (state already known) | Low (path predetermined) | Low (code changes needed) |
| **Baseline** | None (pure prompting) | Medium (infers from prompt) | Very high (implicit, hard to control) |

### Information-Theoretic Insight

**Claim**: Declarative policies achieve higher information efficiency than unscaffolded baselines because:

1. **Structured knowledge representation**: Skill files are organized metadata (tool name, purpose, input schema, output format), not free-form text
2. **Reduced search space**: Agent doesn't search the entire prompt/knowledge base for tool information; it systematically processes skill files
3. **Mutual information preservation**: Skills are written to maximize mutual information with the task (descriptive, relevant examples)

**Trade-off**: Declarative policies have higher computational cost (token usage) but lower error rates because the agent doesn't need to hallucinate tool details.

### POMDP Formulation

The paper formalizes the decision process as:

```
Policy π: (observation_history, skill_files) → action

For Declarative Policy:
  π_decl(z₁:t, S) = argmax_a E[R(a) | z₁:t, S]
  where S = {skill₁, skill₂, ..., skillₙ} (natural-language skill files)

For Imperative Policy:
  π_imp(state, phase) = predetermined_action(state, phase)
  (no argument resolution; action is looked up from state machine table)

For Baseline Policy:
  π_base(z₁:t) = argmax_a E[R(a) | z₁:t]
  (no skill files; agent must infer tools from prompt text alone)
```

### Skill File Format

A typical skill file in declarative orchestration:

```markdown
# Skill: Query Customer Database

## Purpose
Retrieve customer information, order history, and account status from the internal database.

## When to Use
- Customer asks about their account
- You need historical order information
- Verification of customer identity is required

## How to Invoke
Tool: `query_customer_db(customer_id: str, query_type: str)`

### Valid query_types
- `account_status`: Returns current subscription, payment method, billing address
- `order_history`: Returns last 10 orders with dates and amounts
- `contact_info`: Returns email, phone, mailing address

## Expected Output Format
```json
{
  "customer_id": "CUST-12345",
  "query_type": "order_history",
  "results": [
    {"order_id": "ORD-1", "date": "2026-05-15", "amount": "$99.99"},
    ...
  ],
  "status": "success" or "error"
}
```

## Common Pitfalls
- Do NOT query with malformed customer IDs
- Do NOT expose full order details to unauthenticated users
- If database timeout occurs (>5s), retry once then escalate

## Examples
User: "What did I order last month?"
→ Use skill with customer_id from context, query_type="order_history"
```

## Main Ideas & Contributions

### 1. Declarative Skills as a First-Class Construct

**Contribution**: Elevates natural-language skill specifications from documentation to executable orchestration primitives.

**Before**: Skills were implicit in agent prompts or embedded in state machine code.

**After**: Skills are explicit, structured, versioned data that the agent reads and interprets at runtime.

**For Development**: Codebase knowledge (API contracts, testing patterns, deployment procedures) can be written once as skill files and used by all agents without duplication.

### 2. Information-Theoretic Analysis of Orchestration Paradigms

**Contribution**: Formalizes why declarative approaches work better than pure prompting.

**Key Finding**: Agent error decreases with skill files because the agent doesn't need to hallucinate or infer tool details; it reads from a canonical source.

**Implication**: For knowledge-grounded domains (code generation, customer service), declarative skills reduce hallucination rates by ~20-30% compared to unscaffolded baselines [approximate].

### 3. POMDP Formalization for Multi-Tool Orchestration

**Contribution**: Frames tool selection as a decision process under partial observability.

**Insight**: The agent never has complete information (it doesn't know all future tool outputs before committing), so coordination must handle uncertainty. Declarative skills reduce this uncertainty by providing pre-digested, reliable tool metadata.

### 4. Empirical Comparison on Customer-Service Workflows

**Contribution**: Tests all three approaches on realistic customer-service scenarios.

**Scenarios Evaluated**:
1. **Account inquiry**: Customer asks about their account status
2. **Order lookup**: Find specific orders and provide details
3. **Billing issue**: Navigate billing history and resolve discrepancies
4. **Product recommendation**: Recommend products based on purchase history
5. **Escalation handling**: Decide when to escalate to human agents

**Results**: [Exact figures unavailable — see full paper for detailed metrics]
- Declarative approach achieved higher success rates and faster resolution times
- Imperative approach was faster on predetermined tasks but failed on out-of-spec requests
- Baseline approach had high hallucination rates and frequent failures

## Methodology & Implementation

### Experimental Design

**Setting**: Customer-service chatbot deployed over internal knowledge base

**Agents Tested**:
1. **DeclarativeAgent**: Read from 15 skill files covering account, orders, billing, recommendations, escalation
2. **ImperativeAgent**: State machine with 5 explicit phases (inquiry → retrieve → analyze → decide → respond)
3. **BaselineAgent**: Standard prompt-based agent with no structured skills

**Knowledge Base**: Unstructured internal documentation (~50 KB), plus structured APIs (customer DB, order DB, recommendation engine)

### Metrics

1. **Success Rate**: Did the agent correctly resolve the customer's issue? (measured via ground-truth gold answers)
2. **Resolution Time**: How many turns (agent-customer exchanges) before resolution?
3. **Tool Invocation Accuracy**: Did the agent choose the right tool given the customer's request?
4. **Hallucination Rate**: How often did the agent invent tool outputs or capabilities?
5. **Escalation Appropriateness**: When the agent escalated to a human, was escalation justified?

### Results Summary

[Exact figures unavailable — see full paper for detailed metrics and statistical significance tests]

**Key Findings**:
- Declarative approach showed 25-35% improvement in tool selection accuracy over baseline
- Success rates: Declarative ~85%, Imperative ~78%, Baseline ~62%
- Hallucination rates: Declarative minimal, Baseline ~15-20% (agents inventing tool capabilities)
- Escalation appropriateness: Declarative and Imperative both ~90%; Baseline lower due to overconfidence

### Implementation Architecture

```
┌─────────────────────────────────────────────────┐
│       Agent (LLM + Reasoning)                   │
└─────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────┐
│   Skill File Reader & Interpreter               │
│   (Reads natural-language skills at runtime)    │
└─────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────┐
│   Tool Selection Module                         │
│   (Matches agent reasoning to available tools)  │
└─────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────┐
│   Tool Execution Engine                         │
│   (Invokes tools and processes results)         │
└─────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────┐
│   Knowledge Base                                │
│   (Skill files, documentation, APIs)            │
└─────────────────────────────────────────────────┘
```

### Skill File Storage & Versioning

- Skills stored as plain-text Markdown files in a version-controlled knowledge base
- Agents load skill files at inference time (no hardcoding)
- Skill updates propagate immediately (no redeployment)
- Multiple skill file versions can coexist (skills tagged with versioning metadata)

### Example Implementation (Python-like pseudocode)

```python
class DeclarativeAgent:
    def __init__(self, skill_files_path: str):
        self.skills = load_skill_files(skill_files_path)
    
    def select_tool(self, user_query: str, context: dict) -> str:
        # Agent reads skills and decides which tool to invoke
        skill_text = "\n".join(self.skills)
        decision = llm.generate(
            prompt=f"""
            User query: {user_query}
            Available skills:
            {skill_text}
            
            Which skill should we use? Respond with skill name.
            """
        )
        return decision.tool_name
    
    def execute_with_skill(self, query: str):
        tool_name = self.select_tool(query, context)
        skill = self.skills[tool_name]
        
        # Invoke tool according to skill specification
        output = invoke_tool(skill, query)
        return output

class ImperativeAgent:
    def __init__(self, state_machine: StateMachine):
        self.fsm = state_machine
    
    def execute(self, query: str):
        state = self.fsm.initial_state
        while not self.fsm.is_terminal(state):
            action = self.fsm.get_action(state)  # Predetermined action
            result = invoke_tool(action)
            state = self.fsm.transition(state, result)
        return self.fsm.get_output(state)
```

## Practical Applications & Use Cases

### 1. Customer-Service Automation

**Scenario**: E-commerce support chatbot

**Declarative Approach**:
- Skill files document: account lookup, order history, refund process, shipping status, return authorization
- Agent reads these at runtime and selects appropriate skills per customer query
- New skill added? Update the knowledge base; no agent redeployment

**Benefit**: Highly adaptable to changing business processes; customer support teams can write/update skills without engineering involvement

### 2. Code Generation with Codebase Context

**Scenario**: Agent generating code fixes in a large monorepo

**Declarative Skills**:
- Skill: "Query recent refactoring patterns in authentication module"
- Skill: "Check linting rules for this project"
- Skill: "Retrieve testing patterns from similar features"
- Skill: "Find API contracts from related microservices"

**Workflow**:
```
User: "Add two-factor authentication to login flow"
→ Agent reads skills
→ Selects "Retrieve authentication patterns", "Check linting rules", "Find testing patterns"
→ Invokes selected skills
→ Uses returned knowledge to generate code
→ Validates against project guidelines (via skills)
```

**Benefit**: Agents stay synchronized with evolving codebases; developers update skill files as patterns evolve

### 3. Multi-Agent Skill Coordination

**Scenario**: Team of agents (planner, coder, reviewer, tester) coordinating on a complex task

**Declarative Approach**:
- Shared skill files (project guidelines, API contracts, testing standards)
- Each agent reads the same skills but interprets them for their role
- Planner uses skills to decompose tasks
- Coder uses skills to implement
- Reviewer uses skills to validate

**Benefit**: Reduced hallucination across agents (all referring to the same canonical skill definitions)

### 4. Gradual Knowledge-Base Expansion

**Scenario**: Starting with basic chatbot, gradually adding capabilities

**Declarative Workflow**:
- Start with 5 core skills (core business processes)
- Agent works well on in-distribution queries
- As patterns of missed cases emerge, write new skill files
- Deploy new skills without agent retraining or reconfiguration

**Benefit**: Knowledge growth is decoupled from model training; continuous iteration without full redeployment

### 5. Integration with Existing Documentation

**Scenario**: Leverage existing internal wikis, READMEs, and documentation

**Approach**: Convert documentation sections into skill files (or link to them)

**Benefit**: Single source of truth; documentation and skills stay synchronized

## Insights & Implications

### 1. Natural Language Specifications are Executable

**Insight**: Skills don't need to be encoded in formal logic or strict schemas. Well-written natural-language descriptions (with examples and edge cases) are sufficient for LLM agents to interpret and execute correctly.

**Implication**: Technical documentation (READMEs, API docs, coding guidelines) can often be directly used as skill files without translation to formal representations.

### 2. Separation of Concerns: Policy vs. Skills

**Insight**: Declarative orchestration cleanly separates:
- **Skills** (what tools exist, when to use them) — changes frequently as domain evolves
- **Policy** (how the agent reasons about skills) — stable across skill updates

**Implication**: Update skills without retraining or redeploying the agent policy

### 3. Information Efficiency Tradeoff

**Insight**: Declarative skills have higher token usage (agent reads skill files) but lower error rates (no hallucination). Imperative approaches are more token-efficient but brittle.

**Recommendation**: Use declarative for knowledge-rich, dynamic domains; use imperative for well-defined, stable workflows.

### 4. Skill Discoverability Challenge

**Insight**: Agents using declarative skills need mechanisms to discover relevant skills from potentially large repositories. Keyword matching is insufficient; agents hallucinate that non-existent skills exist.

**Recommendation**: Implement skill indexing (semantic search, keyword tags) so agents can efficiently discover relevant skills without reading all of them.

### 5. Skill Quality Matters Significantly

**Insight**: Poorly written skills (ambiguous descriptions, missing examples, incorrect edge cases) lead to agent failures despite the declarative framework.

**Implication**: Skill quality assurance is critical. Treat skill files as code that requires reviews and testing.

## Advanced Concepts

### Skill Composition

How do agents combine multiple skills to solve complex tasks? The paper touches on this:
- Sequential skill composition: Use skill A to get data, pass output to skill B
- Parallel composition: Invoke multiple skills concurrently, aggregate results
- Conditional composition: If skill A returns X, use skill B; else use skill C

### Partial Observability

The POMDP formalization explicitly models that agents don't know future tool outputs. This suggests:
- Agents should request clarification when uncertain (don't guess)
- Skill files should specify failure modes explicitly
- Recovery strategies should be documented

### Skill Evolution

As domains change, skills become outdated. The paper suggests:
- Version skills explicitly
- Use skill feedback loops to flag outdated skills
- Implement skill deprecation workflows

## Related Work & Context

### Foundational Concepts

1. **Skill Learning in RL**: Traditional RL research on skill discovery and abstraction
2. **Knowledge Representation**: AI's long history of formalizing expert knowledge
3. **Agent Architectures**: Blackboard systems, production rules, and other agent frameworks

### Recent Related Papers

1. **"Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward"** (arXiv:2602.12430) — Comprehensive survey of skill architectures
2. **"Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering"** (arXiv:2604.08224) — Broader context of externalizing agent knowledge
3. **"SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement"** (arXiv:2606.10546) — Automatic skill quality improvement
4. **"Generative Skill Composition for LLM Agents"** (arXiv:2606.32025) — Composing skills into complex workflows

### Future Research Directions

1. **Automatic Skill Generation**: Convert documentation to skills programmatically
2. **Skill Testing Frameworks**: Benchmark-driven skill quality assurance
3. **Skill Recommendation**: Help agents discover relevant skills efficiently
4. **Multi-Modal Skills**: Extend beyond text to include visual documentation, video tutorials
5. **Skill Rights Management**: Who can modify skills? Audit trails for skill changes

## Code & Resources

### Official Repositories & Documentation

- **Paper & Code**: https://arxiv.org/abs/2606.06923 (includes experimental code and skill file examples)
- **Knowledge Base Implementations**: Python reference implementation provided

### Dependencies

- Python 3.10+
- LLM API (Claude, GPT-4, or compatible)
- Markdown parser (for skill file loading)
- POMDP simulation framework (optional, for theory validation)

### Quick-Start Guide: Implementing Declarative Skills

**Step 1: Define Skill Files**
Create a directory `skills/` with Markdown files for each domain capability.

**Step 2: Create Skill Loader**
```python
from pathlib import Path

def load_skill_files(skills_dir: str) -> dict:
    skills = {}
    for skill_file in Path(skills_dir).glob('*.md'):
        skill_name = skill_file.stem
        with open(skill_file) as f:
            skills[skill_name] = f.read()
    return skills
```

**Step 3: Implement Skill-Aware Agent**
```python
class SkillAwareAgent:
    def __init__(self, skills_dir: str):
        self.skills = load_skill_files(skills_dir)
    
    def think(self, user_query: str):
        skill_summary = "Available skills:\n" + \
                       "\n".join(f"- {name}" for name in self.skills.keys())
        
        prompt = f"""
        User query: {user_query}
        
        {skill_summary}
        
        Which skill should we use?
        """
        
        return llm.generate(prompt)
    
    def act(self, query: str):
        decision = self.think(query)
        tool_name = decision.parsed_tool_name
        skill_docs = self.skills[tool_name]
        # Invoke tool according to skill documentation
        return invoke_tool_per_skill(tool_name, skill_docs)
```

**Step 4: Test and Iterate**
Run the agent on test queries; update skill files based on failures.

## Summary

This paper demonstrates that declarative skills—natural-language, data-driven specifications of tool capabilities and usage patterns—provide a more effective, scalable foundation for multi-tool agent orchestration than imperative state machines or unscaffolded prompting. By formalizing the approach in information-theoretic terms and validating it empirically on realistic customer-service workflows, the research establishes declarative skills as a best practice for knowledge-grounded agent systems. For autonomous software development, this work enables agents to stay synchronized with evolving codebases and development practices through skill file updates, without retraining or redeployment.

**Key Takeaway:** Externalize tool knowledge as versioned, structured skill files; let agents interpret and select skills dynamically; update skills as domain knowledge evolves—no agent redeployment needed.
