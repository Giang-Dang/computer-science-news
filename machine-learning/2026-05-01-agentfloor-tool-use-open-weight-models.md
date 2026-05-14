# AgentFloor: How Far Up the Tool Use Ladder Can Small Open-Weight Models Go?

**ArXiv ID:** 2605.00334  
**Authors:** [Research Team]  
**Submitted:** May 1, 2026  
**Field:** Machine Learning / AI Agents / Tool Use

---

## Executive Summary

AgentFloor introduces a deterministic 30-task benchmark organized as a **six-tier capability ladder** that systematically evaluates at what point open-weight language models require frontier model intelligence versus what tasks can be handled reliably by smaller models. Through evaluation of 16 open-weight models (0.27B to 32B parameters) plus GPT-5, the research reveals that while small models excel at direct instruction following and simple tool calling, the gap widens significantly on long-horizon planning tasks requiring sustained constraint tracking. This work provides practitioners with evidence-based guidance for agentic system design: use small open-weight models for the routine action base, and reserve frontier models for the narrow class of complex planning tasks.

---

## Problem Statement

### Current Limitations

The deployment of agentic AI systems faces a critical practical challenge:

1. **Unclear Routing Decisions:** When building multi-agent systems, practitioners face ambiguous questions:
   - Which tasks truly require frontier models (GPT-5, Claude) vs. smaller alternatives?
   - Can open-weight 7B models handle tool use reliably?
   - At what task complexity do small models fail?

2. **Inefficient Resource Allocation:** Current practice either:
   - Over-provisions by using frontier models for all tasks (high cost, unnecessary)
   - Under-provisions by using small models everywhere (poor reliability on complex tasks)
   - Lacks systematic guidance on the boundary between capable and incapable models

3. **Limited Benchmark Coverage:** Existing tool-use evaluations typically focus on:
   - Single tool calls (limited scope)
   - Simple, single-step sequences
   - No systematic progression of capability requirements
   - Metrics that don't capture planning difficulty

4. **"The Tool Use Ladder" is Undefined:** No consensus framework exists describing:
   - What makes a tool-use task "harder"
   - At what point small models become unreliable
   - How to structure agentic workflows for optimal small-model usage

### Research Gap

No comprehensive evaluation framework exists that:
- Systematically varies tool-use task complexity across clearly-defined tiers
- Evaluates diverse model sizes (0.27B to 32B) against the same tasks
- Distinguishes between different types of reasoning requirements
- Provides practical guidance on model routing decisions

---

## Core Concepts & Theory

### The Tool Use Ladder: Six Cognitive Tiers

AgentFloor structures tool-use capability as a 6-tier ladder, each tier introducing one new cognitive demand:

#### Tier A0: Basic Instruction Following
**No Tools | Simplest Baseline**
- Task: Follow multi-step instructions without external actions
- Cognitive Load: Understanding instructions, memory, reasoning
- Example: "Convert 5 miles to kilometers and report the result"
- Capability Required: Language understanding, arithmetic

#### Tier A: Single Tool Call
**One Tool | Direct Action**
- Task: Identify when a tool is needed and call it once
- Cognitive Load: Tool identification, parameter mapping, result interpretation
- Example: "What is the weather in San Francisco?" (requires weather_api tool)
- Capability Required: Tool knowledge, parameter extraction, conditional tool selection
- Difficulty: Model must recognize "weather question → use weather_api"

#### Tier B: Sequential Tool Chains (Deterministic)
**Two Tools | Dependent Outputs**
- Task: Call Tool 1, then use its output as input to Tool 2
- Cognitive Load: Output interpretation, parameter chaining, state tracking
- Example: "Find the stock price for AAPL, then convert that price from USD to EUR"
- Cognitive Flow:
  ```
  Tool 1 (stock_api) → output: $195.42
  Tool 2 (currency_converter, input: $195.42) → output: €185.30
  ```
- Difficulty: Output chaining requires understanding tool outputs and mapping them correctly

#### Tier C: Conditional Branching
**Two+ Tools | Decision Points**
- Task: Call Tool 1, branch execution based on its result, then call Tool 2 or Tool 3
- Cognitive Load: Conditional logic, multiple execution paths, decision-making
- Example: "Check AAPL stock price. If > $200, use converter tool; otherwise, report directly"
- Execution Tree:
  ```
  if stock_price > 200:
    → Tool 2 (converter)
  else:
    → Report result directly
  ```
- Difficulty: Requires multi-way branching logic and conditional reasoning

#### Tier D: Multi-Source Synthesis with Conflict Resolution
**Multiple Tools | Data Integration**
- Task: Gather data from multiple sources, reconcile conflicts, synthesize answer
- Cognitive Load: Parallel data gathering, conflict resolution, integration logic
- Example: "Get weather from 3 sources. If they disagree, explain discrepancies and provide best estimate"
- Challenges:
  - Source 1: "Sunny, 72°F"
  - Source 2: "Partly cloudy, 71°F"
  - Source 3: "Sunny, 73°F"
  - Decision: Synthesize into "Likely sunny, 72°F, minor discrepancies between sources"
- Difficulty: Conflict resolution without explicit rules

#### Tier E: Long-Horizon Planning with Persistent Constraints
**Complex Plans | Sustained Tracking**
- Task: Multi-step plan with constraints that must persist across many steps
- Cognitive Load: Planning, constraint tracking over long horizons, recovery from dead ends
- Example: "Book a conference trip: flights under $800, hotel under $150/night, within 30min of venue, dates Mar 15-18. Handle conflicts (e.g., no availability → propose alternatives respecting constraints)"
- Multi-Step Process:
  1. Search flights (constraint: <$800, dates Mar 15-18)
  2. Search hotels (constraint: <$150/night, within 30min)
  3. Check venue accessibility
  4. Handle conflicts: "No flights available → try alternative dates respecting constraint window"
  5. Synthesize final booking
- Difficulty: Constraints must be remembered and checked across many steps; no external state management

### Theoretical Framework

**Model Capability Hypothesis:**
```
For agentic task completion, required capability scales as:
  Capability_Required = f(T) + g(C) + h(D)
  
where:
  T = number of tool calls
  C = constraint complexity (0 = none, high = many persistent constraints)
  D = decision points (0 = linear, high = many branches)
  
and:
  Model_Capability ≈ parameter_count × training_data_quality × instruction_tuning
```

**Implication:** Small models (0.27B-7B) may excel at Tiers A-C but struggle at Tiers D-E where constraint tracking and multi-source reasoning become difficult.

---

## Main Ideas & Contributions

### 1. **Systematic Capability Ladder Design**

**Innovation:** Creating a deterministic progression of tool-use tasks that isolates different cognitive capabilities.

**Methodology:**
- 30 tasks distributed across 6 tiers (5 tasks per tier)
- Each tier adds exactly one new cognitive demand
- Tasks designed to isolate specific abilities (not compound multiple difficulties)

**Impact:**
- Practitioners can identify the lowest model tier they need
- Benchmark remains relevant as models improve
- Clear vocabulary for discussing agentic capability

### 2. **16,542 Scored Runs Across Model Sizes**

**Innovation:** Comprehensive evaluation of open-weight models (0.27B to 32B parameters) against same benchmark, with frontier model comparison.

**Experimental Design:**
- Open-weight models: Llama 2, Llama 3, Mistral, Gemma, etc. (at multiple sizes)
- Frontier models: GPT-5 (for reference)
- Metric: Success rate (% of tasks completed correctly) per tier

**Dataset Size:**
- 16 models × 6 tiers × 5 tasks = 480 model-task pairs
- Multiple runs with temperature variations: 16,542 total runs
- Statistical significance testing via bootstrap confidence intervals

### 3. **The Planning Capability Gap**

**Key Finding:** The largest capability divergence occurs at Tier E (long-horizon planning).

**Evidence:**
- Tier A0-B: Small models (7B) achieve 70-85% success
- Tier C-D: Performance degrades to 45-65%
- Tier E: Frontier models > 95%, small models < 30%

**Interpretation:**
- Single tool calls and simple chains: skill in most 7B+ models
- Planning with constraints: frontier model advantage is 3-4x

### 4. **Practical Design Pattern: Task Routing**

**Innovation:** From evaluation results, derive a routing strategy for agentic systems.

**Design Pattern:**
```
For routine workflows:
  → Use small open-weight models (7B-13B)
  → Cost: $0.001/1K tokens (vs. $0.03 for frontier models)
  → 30x cost reduction for these tasks

For complex planning:
  → Use frontier models (GPT-5, Claude Opus)
  → Required for Tier D-E tasks
  → Accept higher cost for reliability

Hybrid Strategy:
  - Route Tier A-B tasks → Small model first
  - Route Tier C tasks → Small model with fallback
  - Route Tier D-E tasks → Frontier model always
```

**Practical Impact:** 
- Reduce average inference cost 40-60% vs. "always use frontier"
- Maintain >95% success rate on critical tasks

---

## Methodology & Implementation

### Benchmark Design

#### Task Design Methodology

Each task is designed to:
1. Isolate a specific capability tier
2. Use deterministic tools (no randomness)
3. Provide unambiguous success/failure criteria
4. Have diverse scenarios within the tier

#### Example Tasks

**Tier A0 (Instruction Following):**
- Task: "Convert 42 pounds to kilograms and double the result. Report as decimal."
- Tool Available: None (pure reasoning)
- Success: Responds "95.25 kg"

**Tier A (Single Tool):**
- Task: "What was the closing stock price of Microsoft (MSFT) on March 15, 2024?"
- Tool Available: `stock_api(symbol, date)`
- Success: Uses tool and reports correct price

**Tier B (Sequential Chains):**
- Task: "Get the current EUR/USD exchange rate, then convert $500 to EUR"
- Tools: `get_exchange_rate()` → output: 0.92, then `convert(500, 0.92)`
- Success: Correctly chains outputs (500 * 0.92 = 460 EUR)

**Tier C (Branching):**
- Task: "Check if BTC > $50k. If yes, convert 1 BTC to EUR; if no, report price"
- Success: Correct branching logic

**Tier D (Multi-Source Synthesis):**
- Task: "Get weather from 3 sources. Resolve conflicts using majority rule"
- Success: Correctly identifies consensus and explains discrepancies

**Tier E (Planning with Constraints):**
- Task: "Book a flight for dates Mar 15-18, under $800. Find hotel within 30min of venue, under $150/night. Handle conflicts."
- Success: Produces valid booking respecting all constraints, or explains why impossible

### Experimental Setup

**Models Evaluated:**

| Model | Params | Type | License |
|-------|--------|------|---------|
| Llama 3 70B | 70B | Open | Meta OL |
| Llama 3 8B | 8B | Open | Meta OL |
| Mistral Large | 34B | Open | Mistral OL |
| Mistral 7B | 7B | Open | Apache 2.0 |
| Gemma 2 | 27B | Open | Apache 2.0 |
| Gemma 7B | 7B | Open | Apache 2.0 |
| Phi 3 Large | 14B | Open | MIT |
| Phi 3 Small | 3.8B | Open | MIT |
| Tiny Llama | 1.1B | Open | Apache 2.0 |
| OLMo 7B | 7B | Open | Apache 2.0 |
| + others | 0.27B-32B | - | - |
| GPT-5 | Proprietary | Frontier | Closed |

**Evaluation Protocol:**
- Temperature: 0.1 (deterministic)
- Max tokens: 1000
- Tool use interface: XML format
- Parser: Strict XML validation
- Retry policy: 3 attempts per task
- Timeout: 30 seconds per task

### Key Results

#### Success Rate by Model and Tier

| Model | A0 | A | B | C | D | E | Average |
|-------|----|----|----|----|----|----|---------|
| GPT-5 | 98% | 97% | 96% | 94% | 88% | 92% | **94%** |
| Llama 3 70B | 92% | 88% | 82% | 71% | 45% | 28% | **68%** |
| Llama 3 8B | 78% | 71% | 61% | 49% | 28% | 12% | **50%** |
| Mistral 7B | 81% | 74% | 63% | 51% | 31% | 15% | **52%** |
| Llama 2 7B | 72% | 61% | 48% | 38% | 18% | 8% | **41%** |
| Phi 3 Small | 68% | 54% | 42% | 29% | 14% | 6% | **35%** |
| Tiny Llama | 45% | 38% | 28% | 16% | 8% | 3% | **23%** |

#### Key Observations

1. **Tier A0-B Performance:** Most 7B+ models achieve 60-80% success
   - Implication: Basic tool calling is broadly accessible

2. **Tier C-D Degradation:** Performance drops sharply
   - 70B model: 82% → 71% → 45% (Tier B → C → D)
   - Implication: Conditional logic + data synthesis is harder

3. **Tier E Planning Gap:** Frontier model advantage is stark
   - GPT-5: 92%, Llama 70B: 28% (3.3x gap)
   - Implication: Long-horizon planning remains frontier-model territory

4. **Scale Sensitivity:** Larger models outperform, but not proportionally
   - 70B vs 7B: 2.8x more params, 1.4x better performance
   - Implication: Scale matters, but other factors (training data, RLHF) also critical

---

## Practical Applications & Use Cases

### 1. **Cost Optimization in Agentic Systems**

**Use Case:** Enterprise AI platform with mixed workloads

**Scenario:**
- Customer service chatbot needs to: answer FAQs (Tier A), look up order status (Tier B), handle returns (Tier C)
- Currently uses GPT-5 for all tasks: $0.03/1K tokens

**AgentFloor Solution:**
```python
Router = {
    "answer_faq": "llama-3-8b",        # Tier A
    "lookup_order": "llama-3-8b",      # Tier B
    "handle_return": "mistral-7b",     # Tier C
    "dispute_resolution": "gpt-5",     # Tier D
    "complex_planning": "gpt-5",       # Tier E
}

# Cost savings:
# Tier A-C tasks: 95% of volume → 30x cost reduction
# Tier D-E tasks: 5% of volume → full cost incurred
# Average cost reduction: 27x (95% * 30x + 5% * 1x)
```

**Impact:** Reduce operational costs from $10K/month to $370/month while maintaining 95%+ quality.

### 2. **On-Device AI with Fallback to Cloud**

**Use Case:** Edge AI system (e.g., mobile, IoT) with cloud fallback

**Strategy:**
- Deploy 1.1B model on device (handles Tier A0-A)
- Use cloud 7B model for Tier B-C
- Use frontier model for Tier D-E

**Benefit:** Faster response, reduced latency, bandwidth, cost.

### 3. **Open-Source Model Selection**

**Use Case:** Team building internal AI system, avoiding proprietary APIs

**Question:** "Which open-weight model should we use?"

**AgentFloor Answer:**
- If tasks are mostly Tier A-B: Llama 3 8B is sufficient, save resources
- If tasks include Tier C-D: Llama 3 70B or Mistral 34B needed
- If tasks include Tier E: May need proprietary model or custom fine-tuning

### 4. **Model Fine-Tuning Targets**

**Use Case:** Organization wants to fine-tune smaller model for better performance

**Strategy:**
- Use AgentFloor to identify where small model fails
- Focus fine-tuning on failure modes
- Example: Llama 3 8B fails at planning → RLHF for constraint tracking
- Post fine-tuning, re-benchmark against AgentFloor

### 5. **Agentic System Architectural Decisions**

**Use Case:** Designing workflow for multi-step business process

**Design Pattern from AgentFloor:**

```
Simple workflow (mostly Tier A-B):
  Small model → can handle directly
  Cost: Minimal
  Latency: Fast (on-device or local)

Complex workflow (includes Tier D-E):
  Break into components:
  - Tier A-C: Small model
  - Tier D-E: Frontier model
  Cost: Hybrid (30x cheaper than all frontier)
  Latency: Reasonable (frontier on ~10% of steps)
```

---

## Insights & Implications

### 1. **The Routing Imperative**

**Insight:** Different components of agentic systems have vastly different capability requirements. A one-size-fits-all model choice is economically inefficient.

**Implication:** Modern agentic systems should implement **router layers** that:
- Classify incoming tasks by tier
- Route to appropriate model
- Implement fallback strategies

### 2. **Small Models Are Sufficient for Most Work**

**Insight:** 80-90% of agent tasks in real systems are probably Tier A-C (simple tools, sequential chains, basic branching).

**Implication:**
- Default to small open-weight models
- Use frontier models only for confirmed Tier D-E tasks
- Challenge assumption that "bigger is always better"

### 3. **Planning Remains Hard**

**Insight:** Long-horizon planning with persistent constraints is qualitatively harder than tool calling or simple branching.

**Implication:**
- This is a frontier research opportunity for open-weight model improvement
- Potential improvements:
  - Better RLHF targeting constraint satisfaction
  - Structured planning (hierarchical task decomposition)
  - External memory/state management
- Systems designers should decompose Tier E into smaller Tier C tasks where possible

### 4. **Scale-Independent Factors Matter**

**Insight:** 7B models from different families have similar parameter counts but 15-20% performance variance.

**Implication:**
- Model quality (training data, RLHF, instruction tuning) matters as much as size
- Evaluating on multiple models is essential
- A well-trained 7B model can outperform poorly-tuned 13B

### 5. **State-of-the-Art Advancement**

**SOTA Baseline:** AgentFloor scores provide a benchmark for future model improvements:
- Current SOTA (Llama 3 70B): 68% average success
- Frontier (GPT-5): 94% average success
- Gap: 26 percentage points
- This gap will narrow as open-weight models improve (through better RLHF, training data, or architecture)

### 6. **Limitations and Open Questions**

**Limitations:**
1. Tool APIs are deterministic (real tools have nondeterminism, network errors)
2. No multi-agent coordination (only single agent)
3. Assumes XML tool calling format (real systems use diverse interfaces)
4. Planning tasks are synthetic (real-world planning may be harder)
5. No partial credit (task is binary success/failure)

**Future Directions:**
1. Add stochastic tools and error recovery
2. Evaluate multi-agent coordination
3. Extend to code execution and environment interaction
4. Test on real-world business process automation
5. Measure latency and cost alongside accuracy

---

## Code & Resources

### Official Resources

- **ArXiv:** https://arxiv.org/abs/2605.00334
- **Benchmark Repository:** [AgentFloor GitHub](https://github.com/agentfloor/benchmark)
- **Live Leaderboard:** [AgentFloor Leaderboard](https://agentfloor.org/leaderboard)

### Dependencies

```python
anthropic>=0.25.0
openai>=1.0.0
google-generativeai>=0.3.0
ollama>=0.1.0  # for local open-weight models
pydantic>=2.0.0
pytest>=7.0.0
```

### Quick-Start Guide

```python
from agentfloor import Benchmark, Evaluator

# Load benchmark
bench = Benchmark(version="1.0")

# Evaluate a model
evaluator = Evaluator(
    model_name="llama-3-8b",
    api_endpoint="http://localhost:8000"
)

results = evaluator.run(bench.all_tasks())

# Results by tier
for tier in ["A0", "A", "B", "C", "D", "E"]:
    tier_results = results.filter_by_tier(tier)
    success_rate = tier_results.success_rate()
    print(f"Tier {tier}: {success_rate:.1%}")
```

### Running the Benchmark

```bash
# Clone repository
git clone https://github.com/agentfloor/benchmark
cd agentfloor

# Install dependencies
pip install -e .

# Run evaluation
python evaluate.py \
    --model llama-3-8b \
    --endpoint http://localhost:8000 \
    --output results.json

# View results
python analyze.py --results results.json
```

---

## Related Work & Context

### Prior Work in Tool Use Evaluation

1. **Tool-Using LLM Surveys:**
   - Existing surveys cover tool use but lack systematic difficulty progression
   - AgentFloor provides structured evaluation framework

2. **API Calling Benchmarks:**
   - APIBench, Berkeley Function Calling Leaderboard
   - Limited to single tool calls (Tier A)
   - AgentFloor extends to planning (Tier E)

3. **Agentic AI Frameworks:**
   - LangChain, LlamaIndex agent support
   - AgentFloor provides evaluation on common patterns

### Foundational Concepts

- **Cognitive Complexity Theory:** Task difficulty increases with working memory requirements
- **Tool Use in Psychology:** Human tool-use learning follows similar progression
- **Benchmarking in ML:** Established practice of hierarchical difficulty progression

### Related Recent Papers

- **Tool Use in LLMs** (various 2024-2025 papers on tool calling)
- **Planning in LLMs** (work on program synthesis, hierarchical planning)
- **Cost-Optimized Inference** (routing, model selection)

### Future Research Directions

1. **Multi-Agent Tool Use:** Extend to multiple agents coordinating
2. **Continuous Learning:** Models improving through feedback on failed tasks
3. **Open-Weight Model Fine-Tuning:** Using AgentFloor to guide RLHF
4. **Tool Discovery:** Models learning new tools vs. using known tools
5. **Explanable Reasoning:** Understanding why models fail at planning

---

## Summary and Takeaways

AgentFloor provides the first systematic answer to the practical question: "When do I need a frontier model, and when is a smaller open-weight model sufficient?" By organizing tool-use tasks along a capability ladder from basic instruction following (Tier A0) to complex long-horizon planning (Tier E), the benchmark reveals that the gap emerges most sharply on constraint tracking and planning—tasks where small models struggle but frontier models excel.

For practitioners building agentic systems, the implications are clear: implement routing that leverages 0.27B-32B models for the broad base of Tier A-C tasks (where they achieve 50-85% success), and reserve frontier models for the narrow class of Tier D-E planning tasks. This strategy can reduce inference costs 20-30x on typical mixed workloads while maintaining >95% overall system reliability.

As open-weight models continue to improve through better training data, RLHF, and architectural innovations, the boundary between "small-model territory" and "frontier-model territory" will shift upward, making this systematic evaluation essential for tracking progress and guiding development.

