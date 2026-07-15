# UniToolCall: Unifying Tool-Use Representation, Data, and Evaluation for LLM Agents

## Executive Summary

UniToolCall presents a unified framework for standardizing tool-use representation, dataset construction, and evaluation metrics across diverse agent systems. By introducing the QAOA (Query-Action-Observation-Answer) paradigm and combining 10 existing benchmarks with 2,937 synthetic trajectories across 22,000+ tools and 390,000+ instances, the paper demonstrates that unified tool-use representation achieves 92.9% single-hop and 93.0% single-turn accuracy, exceeding performance of specialized models and enabling consistent evaluation across heterogeneous tool landscapes.

## Problem Statement

Current LLM agent tool-use research suffers from fundamental fragmentation:

1. **Representation Heterogeneity**: Each tool-use dataset (WebShop, API-Bank, ToolAlpaca) uses different formats for expressing tool interactions, making it impossible to train unified models and compare methods fairly.

2. **Limited Scope Coverage**: Most benchmarks focus on single-domain tool sets (e.g., shopping APIs or arithmetic functions), failing to capture the diversity agents encounter in real-world deployment.

3. **Evaluation Fragmentation**: Success metrics vary by dataset (task success vs. precision vs. F1), preventing meaningful comparison of agent capabilities across domains.

4. **Scalability Bottleneck**: Creating large-scale, diverse tool-use training data requires manual annotation—expensive and slow. Most datasets contain <50K instances.

5. **Incomplete Interaction Patterns**: Existing benchmarks rarely model:
   - Multi-hop tool chains (Tool A → Tool B → Tool C)
   - Parallel execution (calling multiple tools concurrently)
   - Multi-turn interactions (refining results through iterative calls)

The research gap is the lack of a unified data and evaluation framework that enables standardized tool-use agent development while supporting diverse interaction patterns.

## Core Concepts & Theory

### QAOA Framework: Unified Tool-Use Representation

UniToolCall introduces the **Query-Action-Observation-Answer (QAOA)** paradigm as a universal abstraction for tool use:

```
┌──────────────────────────────────────────────────────────┐
│                       QAOA Cycle                         │
└──────────────────────────────────────────────────────────┘

Query:       "What is the population of Tokyo?"
             ↓
Action:      execute_tool("search_api", 
                          query="Tokyo population",
                          filters={"type": "demographic"})
             ↓
Observation: {"result": "37.4M (2024)", 
              "source": "UN Statistics",
              "confidence": 0.98}
             ↓
Answer:      "Tokyo's population is approximately 37.4 million."
```

**Why QAOA?**

- **Universality**: Applies to API calls, code execution, database queries, web search, and custom tools
- **Composability**: Multiple QAOA cycles chain together for multi-hop reasoning
- **Schema Clarity**: Explicit separation of intent (Query) → action (Action) → feedback (Observation)
- **Executability**: Observation returned by tool is concrete feedback, not hallucination

### Tool Taxonomy

UniToolCall defines tools across 7 dimensions:

1. **Hop Complexity**: Single (one-step) vs. Multi-hop (chain reasoning)
2. **Turn Complexity**: Single-turn (query → action → answer) vs. Multi-turn (iterative refinement)
3. **Execution Pattern**: Serial (sequential calls) vs. Parallel (concurrent calls)
4. **Input Type**: Structured (JSON, SQL) vs. Unstructured (free text)
5. **Output Type**: Deterministic vs. Stochastic
6. **Domain**: API, Database, Search, Code, Math, Web, Knowledge Base, Custom
7. **Constraints**: Rate limiting, authentication, cost constraints

**Coverage in UniToolCall**:

```
Single-Hop / Single-Turn:     15,000+ tools (API queries, simple searches)
Single-Hop / Multi-Turn:       4,200+ tools (iterative refinement: "refine results")
Multi-Hop / Single-Turn:       2,100+ tools (chained queries: search → analyze → format)
Multi-Hop / Multi-Turn:          800+ tools (complex reasoning: explore → learn → decide)
```

### Strict Precision Metric

Rather than task success rate (binary), UniToolCall proposes **Strict Precision**:

- **Single-Hop Strict Precision**: % of single tool calls returning exact/semantically correct results
- **Multi-Hop Strict Precision**: % of tool chains where all intermediate and final results are correct

This is stricter than prior metrics because intermediate errors compound, exposing weaknesses in chain reasoning.

### Data Generation Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│            UniToolCall Data Synthesis Pipeline               │
└──────────────────────────────────────────────────────────────┘

1. Seed Collection Phase
   ├─ Collect from 10 existing datasets (WebShop, API-Bank, etc.)
   ├─ Standardize to QAOA format
   └─ Result: 50,000 initial instances

2. Tool Augmentation Phase
   ├─ Catalog 22,000+ real-world tools (APIs, CLIs, libraries)
   ├─ Extract tool specifications (parameters, return types)
   └─ Create tool-query relevance mappings
   
3. Synthetic Trajectory Generation
   ├─ For each domain, generate ~150 queries
   ├─ Use LLM to compose tool chains (single/multi-hop)
   ├─ Execute chains against real tool APIs
   ├─ Collect observations (success or error)
   └─ Result: 340,000+ synthetic instances (2,937 diverse trajectories)

4. Quality Filtering
   ├─ Remove failed executions (tool API down, invalid parameters)
   ├─ Deduplicate semantically equivalent queries
   ├─ Balance across interaction patterns
   └─ Final: 390,000 high-quality instances
```

### Agent Topology for Tool-Use

UniToolCall enables standardized multi-agent patterns:

```
┌─────────────────────────────────────────────────┐
│              Query Planner Agent                │
│      (Determine which tools to call)            │
└────────────────────┬────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
    ┌─────▼──────┐       ┌─────▼──────┐
    │   Tool A   │       │   Tool B   │
    │  Executor  │   +   │  Executor  │  (Parallel Execution)
    └─────┬──────┘       └─────┬──────┘
          │                     │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   Observation       │
          │   Integration       │
          │   Agent             │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   Response          │
          │   Generation        │
          │   Agent             │
          └─────────────────────┘
```

## Main Ideas & Contributions

### 1. QAOA: Universal Tool-Use Abstraction

The paper argues that tool use across domains (API → database → code → search) follows the same cognitive pattern:

1. **Formulate intent** (Query)
2. **Select and invoke tool** (Action)
3. **Receive feedback** (Observation)
4. **Synthesize response** (Answer)

By standardizing this representation, researchers can:
- Train single models for all tool-use tasks
- Transfer learning from one domain to another
- Evaluate fairly across domains

### 2. Massive Unified Dataset (390K+ Instances)

Combining:
- **10 Existing Benchmarks**: WebShop, API-Bank, ToolAlpaca, AutoAct, APIBank, ToolBench, M³Tool, API-Rank, InfiniteTool, ToolE
- **Synthetic Trajectories**: 2,937 LLM-generated tool chains covering diverse patterns
- **22,000+ Real Tools**: APIs, libraries, CLIs with authentic specifications

Result: Largest unified tool-use dataset enabling robust model training.

### 3. Comprehensive Evaluation Framework

**Strict Precision metrics** reveal model capabilities more accurately:

- **Single-Hop Strict Precision**: Does the model select the right tool and invoke it correctly?
- **Multi-Hop Strict Precision**: Can the model chain tools logically without intermediate failures?
- **Parallel Execution Precision**: Can the model invoke multiple tools concurrently and integrate results?

These metrics expose weaknesses standard benchmarks miss.

### 4. Interaction Pattern Support

Unlike prior work, UniToolCall supports:

- **Single-hop single-turn**: Simple API lookup (e.g., "search for restaurants")
- **Single-hop multi-turn**: Iterative refinement (e.g., "refine results by rating")
- **Multi-hop single-turn**: Planning then executing (e.g., "get weather for the city with highest tourism")
- **Multi-hop multi-turn**: Adaptive reasoning (e.g., "search → analyze → ask clarifying question → refine search → answer")

## Methodology & Implementation

### Experimental Setup

**Model Comparison**:
- Baseline Models: GPT-4, Claude 3.5 Sonnet, Qwen 3-32B, Gemini 3 Flash Preview, Llama 3.1
- Specialized Tool Models: ToolLLaMA, ChatGPT-Function-Calling
- Closed-Source APIs: OpenAI Assistants, Anthropic Tool Use

**Evaluation Protocol**:
1. Sample 500 instances from each interaction-pattern category
2. Generate tool calls using each model
3. Execute against real tool APIs (or simulators for unavailable tools)
4. Score based on Strict Precision
5. Analyze failure modes by category

### Key Results

**Overall Performance (Strict Precision)**:

```
Model                          Single-Hop    Multi-Hop    Average
─────────────────────────────────────────────────────────────────
GPT-4 Turbo                      91.2%        78.3%       84.8%
Claude 3.5 Sonnet                92.9%        81.6%       87.3%
Qwen 3-32B                       89.4%        74.1%       81.8%
Gemini 3 Flash Preview           88.7%        72.5%       80.6%
Llama 3.1 70B                    85.3%        68.9%       77.1%
─────────────────────────────────────────────────────────────────
ToolLLaMA (Baseline)             76.2%        54.3%       65.3%
ChatGPT Function Call            82.1%        61.4%       71.8%
```

**Single-Turn Single-Hop (Most Reliable)**:
- Claude 3.5: 92.9% (errors mainly in parameter type mismatches)
- GPT-4: 91.2% (errors in required field detection)

**Multi-Turn Multi-Hop (Most Challenging)**:
- Claude 3.5: 68.3% (error propagation through chains)
- GPT-4: 71.4% (occasional tool sequencing errors)

**Error Analysis**:

| Error Category                    | Frequency |
|:--|:--|
| Incorrect parameter type          | 18.2%     |
| Missing required field            | 14.7%     |
| Tool selection error              | 12.3%     |
| Parameter value out of range      | 11.8%     |
| Logical sequencing error          | 10.9%     |
| Parallel execution conflict       | 8.5%      |
| Authentication/permission error   | 7.2%      |
| Result integration error          | 6.8%      |
| Other                             | 9.6%      |

### Architecture for Implementation

**Unified Tool-Call Pipeline**:

```python
class UniToolCallAgent:
    def process_query(self, query: str) -> Answer:
        # Step 1: Query understanding
        intent = self.parse_query(query)
        
        # Step 2: Tool planning (which tools, in what order)
        plan = self.plan_tool_chain(
            intent=intent,
            available_tools=self.tools,
            interaction_pattern="auto"  # Auto-detect
        )
        
        # Step 3: Execute tool calls
        if plan.execution_type == "parallel":
            observations = parallel([
                self.execute_action(action) for action in plan.actions
            ])
        else:
            observations = []
            for action in plan.actions:
                obs = self.execute_action(action)
                observations.append(obs)
        
        # Step 4: Integrate observations
        integrated = self.integrate_observations(observations)
        
        # Step 5: Generate answer
        return self.generate_answer(integrated, intent)
    
    def execute_action(self, action: Action) -> Observation:
        tool = self.tools[action.tool_name]
        params = self.validate_params(action.parameters, tool.schema)
        result = tool.call(**params)
        return Observation(result=result, source=action.tool_name)
```

## Practical Applications & Use Cases

### 1. Multi-Service Integration (E-commerce)

**Scenario**: E-commerce agent helping customer find and purchase product.

**Tool Chain**:
1. Search tool → find matching products
2. Price-comparison tool → check alternative vendors (parallel)
3. Inventory tool → verify stock
4. Review-aggregation tool → check ratings
5. Payment tool → process purchase

**Benefit**: UniToolCall enables agents to reliably execute 5-step chains with >85% accuracy, vs. ~45% with unstructured tool calling.

### 2. Data Intelligence Pipeline

**Scenario**: Business intelligence agent querying database, processing data, generating insights.

**Tool Chain**:
1. SQL executor → query data warehouse
2. Statistical analysis tool → compute metrics
3. Visualization tool → create charts (parallel to 2)
4. Report generator → format findings

**Result**: With unified representation, agents consistently handle multi-turn refinement ("try larger date range", "show confidence intervals").

### 3. Software Development Assistance

**Scenario**: Coding agent using IDE tools, debuggers, package managers.

**Tool Chain**:
1. Code search → find relevant functions
2. Package manager → check dependencies
3. Compiler → validate syntax
4. Debugger → trace execution (conditional)
5. Documentation retriever → provide context

**Benefit**: Unified representation enables agents to handle ~2.5x longer tool chains with same error rate.

### 4. Research Question Answering

**Scenario**: Academic agent answering complex research questions requiring multi-source information.

**Tool Chain**:
1. Literature search (multi-hop: broad search → narrow by relevance → deep read)
2. Data extraction
3. Synthesis and insight generation
4. Citation formatting

**Result**: Multi-turn capability enables adaptive queries ("these sources don't match—try different terms").

## Insights & Implications

### 1. Tool Standardization is Foundation for Scale

The gap between single-hop (92.9%) and multi-hop (81.6%) performance reveals the challenge: **as complexity increases, unified representation becomes critical** to prevent information loss.

Traditional, domain-specific approaches can't scale because each domain requires re-engineering. UniToolCall shows that abstract QAOA representation enables generalization.

### 2. Multi-Hop is the Frontier

Single-hop tool use is largely solved (>90% accuracy). The bottleneck is **multi-hop chains and error recovery**:
- 11.4 percentage-point drop from single-hop to multi-hop
- Main failure mode: error propagation (tool output doesn't match next tool's input)

Future work should focus on:
- Robust error detection and recovery
- Constraint propagation (checking feasibility before executing chains)
- Adaptive tool selection based on previous results

### 3. Parallel Execution Needs Explicit Modeling

8.5% of errors involve parallel tool conflicts. Current models don't explicitly model:
- Tool dependencies (Tool A must complete before B)
- Resource conflicts (two tools accessing same resource)
- Result integration complexity (combining parallel results)

UniToolCall reveals that explicit patterns support this; generative models struggle.

### 4. Real-World Deployment Requires Authentic Tools

590K synthetic instances accelerate research, but 10x variation between test-set and real-world tools. The paper includes tool specifications for 22,000+ real tools—crucial for deployment.

### Open Research Directions

1. **Tool Discovery**: How can agents discover new tools beyond the training set?
2. **Tool Composition**: Can agents learn to combine tools creatively (e.g., using output type mismatch as input)?
3. **Constraint Satisfaction**: Explicitly modeling tool constraints and dependencies
4. **Cost/Latency Optimization**: Tool-aware planning considering execution cost and latency
5. **Tool Versioning**: Handling tool API evolution (breaking changes, deprecations)

## Code & Resources

### Official Implementation

**Framework**: huggingface/unitoolcall
- GitHub: https://github.com/unitoolcall/unitoolcall
- Hugging Face: https://huggingface.co/datasets/unitoolcall/UniToolCall-v1

**Dataset Structure**:
```
{
  "query": "Find restaurants in Tokyo with rating > 4.5",
  "action": {
    "tool": "search_restaurants",
    "parameters": {
      "location": "Tokyo",
      "rating_min": 4.5
    }
  },
  "observation": {
    "results": [...],
    "count": 237,
    "success": true
  },
  "answer": "Found 237 highly-rated restaurants in Tokyo..."
}
```

### Integration with Existing Frameworks

**LangChain Integration**:
```python
from unitoolcall import UniToolCallAgent, QAOA_ToolRegistry

registry = QAOA_ToolRegistry.load_from_huggingface()
agent = UniToolCallAgent(tool_registry=registry)
result = agent.invoke("Find flights to Tokyo under $500")
```

**LlamaIndex Integration**:
```python
from llamaindex.tools import UniToolCallToolSpec

tool_spec = UniToolCallToolSpec()
agent = ReActAgent.from_tools(tool_spec.tools)
```

### Setup Instructions

```bash
# Install
pip install unitoolcall-sdk

# Load dataset
from unitoolcall import load_dataset
train, val, test = load_dataset("v1.0", split="all")

# Evaluate your agent
from unitoolcall.eval import evaluate
results = evaluate(your_agent, test)
print(f"Single-hop precision: {results.single_hop_precision}")
```

### Tool Specification Format

```yaml
tool_name: "search_restaurants"
description: "Search for restaurants by location, cuisine, rating"
parameters:
  location:
    type: "string"
    required: true
    description: "City or address"
  cuisine:
    type: "string"
    required: false
    enum: ["Italian", "Japanese", "French", ...]
  rating_min:
    type: "float"
    required: false
    min: 1.0
    max: 5.0
returns:
  type: "object"
  properties:
    results:
      type: "array"
      items:
        type: "object"
        properties:
          name: { type: "string" }
          address: { type: "string" }
          rating: { type: "number" }
          cuisines: { type: "array" }
    count: { type: "integer" }
    success: { type: "boolean" }
```

## Related Work & Context

### Prior Tool-Use Benchmarks

- **APIBench (2024)**: Focused on API calling; limited to single-hop
- **ToolBench (2024)**: 16K tools but non-unified representation
- **ToolAlpaca (2024)**: Tool instruction-tuning; limited interaction patterns
- **M³Tool (2024)**: Multi-modal but smaller scale (~10K instances)

**UniToolCall Advances**: Unified across all, 40x larger, supports multi-hop and multi-turn.

### Related Frameworks

- **Tool-Use in ReAct (Yao et al., 2023)**: Implicit tool reasoning; UniToolCall makes explicit
- **Gorilla (Sharan et al., 2024)**: Tool retrieval from large catalogs; complements UniToolCall
- **OpenAPI Spec Standardization**: UniToolCall applies OpenAPI concepts to LLM tool-use

### Complementary Research

- **Tool Learning** (Qin et al., 2024): Teaching agents to use new tools; benefits from UniToolCall data
- **Tool Grounding** (Schoop et al., 2024): Connecting language to tool semantics; benefits from QAOA clarity
- **Constrained Tool Selection** (Gao et al., 2024): Tool selection with constraints; gains leverage from QAOA

## Future Directions & Extensions

1. **Dynamic Tool Availability**: Real-world tools appear/disappear; how to handle API changes?
2. **Tool Domain Adaptation**: Transfer tool-use from one domain to vastly different domain?
3. **Adversarial Tool-Use**: Tool-use security—detecting and preventing tool-based attacks?
4. **Cost-Aware Tool Planning**: Considering financial cost and latency in tool chains?
5. **Human-in-the-Loop Tool-Use**: Requesting clarification when uncertain about tool selection?

---

**Paper Details**:
- **ArXiv ID**: 2604.11557
- **Published**: April 2026
- **Authors**: Yijuan Liang, Xinghao Chen, Yifan Ge, Ziyi Wu, Hao Wu, Changyu Zeng, Wei Xing, Xiaoyu Shen
- **Affiliations**: USTC, Ningbo Institute of Technology, Hong Kong Polytechnic University
- **GitHub**: https://github.com/unitoolcall/unitoolcall
- **Dataset**: https://huggingface.co/datasets/unitoolcall/UniToolCall-v1
