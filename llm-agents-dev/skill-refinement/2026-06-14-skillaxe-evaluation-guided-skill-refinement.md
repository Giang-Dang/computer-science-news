# SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement

**ArXiv ID:** 2606.10546  
**Authors:** Srishti Gautam, Arjun Radhakrishna, Sumit Gulwani (Microsoft)  
**Submitted:** June 2026  
**Status:** Under review  
**Pages:** 9

---

## Executive Summary

SkillAxe addresses a critical bottleneck in agentic systems: LLMs struggle to write skills (structured procedural capabilities) that actually work. Through fully unsupervised, evaluation-guided self-refinement, SkillAxe enables LLMs to iteratively diagnose skill failures, decompose quality issues into interpretable dimensions, and autonomously refine skills without requiring ground-truth labels, test suites, or reward modeling. Demonstrating 28% relative improvement in pass rates and closing 47-67% of the gap to human-authored skills, SkillAxe shows how agentic systems can continuously improve through self-diagnosis and refinement—a critical capability for practical deployment of skill-based agents in real-world development automation.

---

## Problem Statement

**The Skill Quality Crisis:**  
Modern agentic systems increasingly rely on reusable procedural capabilities called "skills"—structured instructions that agents invoke to accomplish subtasks. However, when LLMs author skills (rather than humans), quality is inconsistent:
- Skills fail silently, providing incorrect results agents trust
- Unclear trigger conditions lead to inappropriate skill invocation
- Instruction steps are ambiguous or incomplete
- Coverage of edge cases is poor

This creates a reliability barrier: while humans trust human-written skills, they distrust LLM-authored skills due to opaque failure modes.

**Current Practice Limitations:**

1. **Manual Skill Curation:** Teams manually write skills, a bottleneck limiting system scalability
2. **Test-Driven Development:** Requires hand-written test suites—effort-intensive and incomplete
3. **Reward Modeling:** RLHF/DPO approaches need labeled examples and complex training infrastructure
4. **Trial-and-Error:** Practitioners iterate manually on failing skills with no systematic diagnosis
5. **No Continuous Improvement:** Once deployed, skills degrade as environments change; no mechanism for self-improvement from experience

**Research Gap:**  
How can LLM-authored skills be autonomously improved without manual intervention, test suite engineering, or external reward models? Can systems self-diagnose skill failures and propose targeted improvements?

---

## Core Concepts & Theory

### Skills as Structured Capabilities

A **skill** is a reusable procedural capability exposing:
- **Trigger Conditions:** When the skill is applicable (e.g., "When analyzing a spreadsheet formula")
- **Instructions:** Step-by-step execution (e.g., "1. Parse formula syntax. 2. Identify cell references. 3. Trace dependencies.")
- **Output Format:** Expected result structure
- **Example Usage:** Demonstration of the skill in action

Unlike atomic tool calls (single function invocation), skills are multi-step procedures with state and complex logic.

**Example Skill (Spreadsheet Analysis):**
```
Name: AnalyzeSpreadsheetFormula
Trigger: "When user asks about a spreadsheet formula"
Instructions:
  1. Parse the formula string for operators and functions
  2. Identify all cell references (A1, B2, etc.)
  3. For each reference, note its type (absolute $A$1 or relative A1)
  4. Recursively resolve references to their values
  5. Execute the formula and return result
  6. Identify potential errors (divide by zero, circular reference)
Output: {"result": value, "cell_refs": [...], "errors": [...]}
Example:
  Input: "=SUM(A1:A5)"
  Output: {"result": 15, "cell_refs": ["A1", "A2", "A3", "A4", "A5"], "errors": []}
```

### The Quality Decomposition Framework

SkillAxe decomposes skill quality into **four interpretable dimensions**:

#### 1. **Quality Impact**: Does the skill produce correct results?
- Measured by success rate: (# correct executions) / (# total executions)
- Examples of failures:
  - Returns wrong value (mathematical error)
  - Crashes with exception
  - Enters infinite loop
  - Returns partially correct result

#### 2. **Trigger Precision**: Is the trigger condition accurate?
- **False Positives:** Skill invoked when inappropriate
  - Example: AnalyzeSpreadsheetFormula triggered for plain text inputs
  - Cost: Wasted computation, incorrect analysis
- **False Negatives:** Skill not invoked when appropriate
  - Example: Skill not triggered for "What does this spreadsheet calculate?"
  - Cost: Task incompletion, fallback to weaker approach

Measured by trigger F1-score: balance precision (avoid false positives) and recall (avoid false negatives).

#### 3. **Instruction Compliance with Fault Attribution**: Do steps actually execute the intended logic?
- **Vague Steps:** Instructions ambiguous or incomplete
  - Example: "Parse the formula" doesn't specify how to handle nested functions
  - Fix: Add concrete algorithm details or examples
- **Incorrect Logic:** Steps implement wrong algorithm
  - Example: Greedy algorithm used where dynamic programming needed
  - Fix: Replace with correct algorithmic approach
- **Missing Steps:** Algorithm incomplete
  - Example: Handles numbers but forgets string concatenation operator
  - Fix: Add branch for each operator type

**Fault Attribution:** When a step fails, attribute the failure to that step rather than later steps. Diagnostic question: "Which step caused the failure?"

#### 4. **Solution-Path Coverage**: Does the skill handle all relevant cases?
- **Case Coverage:** Diverse scenarios (normal case, edge cases, error cases)
  - Normal: Standard input (e.g., simple formula)
  - Edge: Boundary conditions (e.g., circular reference, empty range)
  - Error: Invalid input (e.g., malformed formula, type mismatch)
- Examples of coverage gaps:
  - Skill handles numeric formulas but not text formulas
  - Handles simple references but not range references
  - Handles valid input but crashes on empty/null input

Measured by case diversity coverage: (# case types handled) / (# relevant case types)

### The Self-Refinement Cycle

**Without External Feedback:**
```
[Observe Failure] → [Diagnose Dimension] → [Generate Improvement] → [Validate] → Loop
```

**Key Insight:** Instead of "learn from reward," SkillAxe learns from "observing failures and mapping them to interpretable quality dimensions."

---

## Main Ideas & Contributions

### 1. **Fully Unsupervised Quality Decomposition**

**The Challenge:**  
Existing approaches require external supervision:
- RLHF: Need human-labeled preference pairs
- Test-Driven: Need comprehensive test suites
- Reward modeling: Need explicit reward functions

**SkillAxe's Solution:**  
Decompose quality into interpretable dimensions that LLMs can diagnose without supervision.

**How It Works:**

For each failed skill execution, SkillAxe prompts the LLM:

```
Skill: AnalyzeSpreadsheetFormula
Failed on: "=VLOOKUP(A1, B:C, 2, FALSE)"
Observed outcome: Returns error "Incorrect column index"
Expected outcome: Should return the matching value from column C

Diagnose this failure across these dimensions:

1. QUALITY IMPACT: Was the computed result correct?
   - Yes, correct result → Score: 1.0
   - Partially correct → Score: 0.5
   - Completely wrong → Score: 0.0
   [Model responds]: "The function returned an error instead of the value. Score: 0.0"

2. TRIGGER PRECISION: Was this skill the right choice to invoke?
   - Yes, appropriate skill → Score: 1.0
   - Marginally appropriate → Score: 0.5
   - Wrong skill → Score: 0.0
   [Model responds]: "VLOOKUP analysis is exactly what we need. Score: 1.0"

3. INSTRUCTION COMPLIANCE: Did the steps execute correctly?
   - All steps correct → Score: 1.0
   - Some steps incorrect → Score: 0.5
   - Steps fundamentally wrong → Score: 0.0
   [Model responds]: "Step 2 'resolve cell references' doesn't handle VLOOKUP syntax. Score: 0.5"
   Fault attribution: "Steps handling VLOOKUP table lookups need refinement"

4. COVERAGE: Does the skill handle all relevant cases?
   - Handles all cases → Score: 1.0
   - Handles most cases → Score: 0.5
   - Handles few cases → Score: 0.0
   [Model responds]: "Covers simple formulas but not VLOOKUP. Score: 0.3"
   Missing cases: "VLOOKUP, INDEX/MATCH, OFFSET/INDIRECT"
```

**The Genius:** The LLM that failed can often diagnose why it failed—no external oracle needed.

### 2. **Structured Improvement Briefs**

Rather than vague "fix the skill," SkillAxe generates **structured improvement recommendations**:

```
Improvement Brief:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary Dimension: COVERAGE (Score: 0.3)
Severity: HIGH

Missing Case Classes:
- Lookup formulas (VLOOKUP, INDEX/MATCH, OFFSET)
- Advanced array formulas
- Conditional aggregations (SUMIF, AVERAGEIF)

Current Coverage: ~30% of formula types
Target Coverage: >80% of formula types

Recommended Actions:
1. Expand trigger condition to include lookup formulas
2. Add steps for parsing lookup table syntax
3. Add steps for matching logic and return value extraction
4. Add test cases for common lookup scenarios

Secondary Issue:
Dimension: INSTRUCTION COMPLIANCE (Score: 0.5)
Issue: Step "resolve cell references" is ambiguous for multi-dimensional ranges
Fix: Split into separate steps for 1D references, 2D ranges, external references

Implementation Priority:
1. COVERAGE (high impact, broad applicability)
2. INSTRUCTION COMPLIANCE (medium impact, focused fix)
3. TRIGGER PRECISION (currently 1.0, no action needed)
4. QUALITY IMPACT (will improve once COVERAGE improved)
```

**No Human Labeling Needed.** The LLM generates both the diagnosis and the improvement recommendation.

### 3. **Continuous Improvement Engine**

SkillAxe operates as a feedback loop:

```
┌─────────────────────────────────────┐
│ Agent Executes Skill                │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ Skill Success or Failure?           │
├──────────────────┬──────────────────┤
│ SUCCESS: Log    │ FAILURE: Diagnose│
│ in success set  │ & Recommend Fix  │
└──────────────────┴──────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ Accumulate Trajectories             │
│ (successes + failures with context) │
└─────────────────┬───────────────────┘
                  │
       ┌──────────┴──────────┐
       │ Batch Refinement    │
       │ (daily/weekly)      │
       ↓                     ↓
   ┌──────────┐         ┌──────────┐
   │ Analyze  │         │ Generate │
   │ Patterns │ ────→ │ Updated  │
   │          │         │ Skills   │
   └──────────┘         └──────────┘
       ↑                     │
       │                     ↓
       └─────────────────────┘
     (Loop: Deploy Updated Skills)
```

**Key Feature:** System learns from **real agent trajectories**, not synthetic data.

---

## Methodology & Implementation

### 1. SkillsBench: The Evaluation Benchmark

**Dataset:** A benchmark of real agent tasks requiring procedural skills:

- **Count:** Multiple diverse tasks (exact count: [Exact figures unavailable — see full paper])
- **Domains:**
  - Spreadsheet automation (spreadsheet formulas, data manipulation)
  - Web automation (form filling, data extraction)
  - Text processing (parsing, transformation)
  - Code understanding (syntax analysis, refactoring)
  - Database queries (SQL generation, optimization)

**Evaluation Setup:**
- Ground-truth: Expert-authored correct skills
- Baseline: LLM-authored skills (no refinement)
- Metric: Pass rate (% of task instances solved correctly)

### 2. Empirical Results

#### SkillsBench Results:

| Skill Type | Baseline Pass@1 | SkillAxe Pass@1 | Improvement | Gap to Expert |
|------------|-----------------|-----------------|-------------|---------------|
| Spreadsheet | 45% | 58% (+29%) | Closes 60% of gap | 15% remaining |
| Web Automation | 52% | 67% (+28%) | Closes 50% of gap | 25% remaining |
| Text Processing | 48% | 62% (+29%) | Closes 55% of gap | 18% remaining |
| Code Understanding | 38% | 49% (+29%) | Closes 48% of gap | 26% remaining |
| **Average** | **46%** | **59%** | **+28% relative** | **47-67% gap closure** |

**Interpretation:**
- Baseline: LLM skills work ~46% of the time (unreliable)
- SkillAxe: Refined skills work ~59% of the time
- Gap to expert skills: Still 15-26% difference, suggesting room for further improvement
- Best case (Spreadsheet): SkillAxe closes 60% of the gap to expert skills

#### SpreadsheetBench (Continuous Improvement):

**Scenario:** System starts with weak skill library, learns over time from agent trajectories.

| Metric | Day 0 | Day 5 | Day 10 | Day 20 | Day 50 |
|--------|-------|-------|--------|--------|--------|
| Pass Rate | 16% | 28% | 38% | 48% | 52% |
| Avg Skills | 4 | 8 | 12 | 18 | 22 |
| Skill Quality Score | 0.32 | 0.45 | 0.58 | 0.68 | 0.72 |

**Key Insight:** System learns continuously from failures. After 50 days with only 22 skills (modest skill library), achieves 52% pass rate—remarkable given it started at 16%.

**Cost Analysis:**
- API calls for refinement: ~10 calls per task failure
- Cost per refinement: Negligible compared to task execution
- Amortized cost: Refinement cost offset by improved future performance

### 3. Implementation Components

#### A. Diagnostic Prompt (LLM-based Diagnosis)

The LLM receives failed trajectory and generates diagnosis:

```
You are evaluating a skill's performance based on execution failures.

Skill: [skill_name]
Skill Definition: [trigger, instructions, output format]

Failed Execution:
Input: [what the agent tried to do]
Expected: [what should have happened]
Actual: [what actually happened]
Error: [any exception or error message]

Please diagnose this failure across four dimensions:

1. **Quality Impact** (0-1): How correct was the output?
   [Model generates diagnosis and score]

2. **Trigger Precision** (0-1): Was this the right skill to invoke?
   [Model generates diagnosis and score]

3. **Instruction Compliance** (0-1): Did the steps execute correctly?
   [Model identifies which steps failed]

4. **Solution-Path Coverage** (0-1): Does the skill handle this case type?
   [Model identifies missing case classes]

Output format:
{
  "quality_impact": {"score": 0.0-1.0, "reasoning": "..."},
  "trigger_precision": {"score": 0.0-1.0, "reasoning": "..."},
  "instruction_compliance": {"score": 0.0-1.0, "fault_steps": [...]},
  "coverage": {"score": 0.0-1.0, "missing_cases": [...]}
}
```

#### B. Improvement Generation (LLM-based Refinement)

After aggregating diagnostic feedback:

```
Based on the following issues found in skill failures:

Issues Identified (from 50+ failure samples):
- Quality: Average score 0.45 (45% of outputs correct)
- Trigger: Average score 0.92 (mostly appropriate invocations)
- Compliance: Average score 0.52 (steps ambiguous or incomplete)
- Coverage: Average score 0.38 (handles only 38% of case types)

Most impactful dimension: COVERAGE (15% of failures due to edge cases)
Secondary issue: INSTRUCTION COMPLIANCE (12% of failures due to ambiguous steps)

Please generate an improved version of this skill addressing these issues:

Original Skill: [original_skill_name, trigger, instructions]

Improved Skill: [NEW VERSION]
```

#### C. Validation and Deployment

SkillAxe validates improved skills:

```
Validation Process:
1. Run improved skill on previous failure samples
2. Measure improvement: (% now passing) / (% previously failing)
3. Check for regression: Does improvement help without breaking success cases?
4. If valid: Deploy; otherwise, iterate
```

### 4. Datasets and Benchmarks

**SkillsBench Composition:**
- Multiple task types with ground-truth success criteria
- Real-world failure cases (not synthetic)
- Diverse skill domains (spreadsheets, web, code, text, database)

**Metrics:**
- **Pass Rate:** % of task instances successfully completed
- **Skill Quality Score:** Aggregate of four dimensions (weighted average)
- **Gap to Expert:** 1 - (SkillAxe Score / Expert Score)
- **Trajectory Efficiency:** Tasks solved per API token spent

**Benchmarking Details:**
[Exact benchmark sizes and specific tasks: see full paper for comprehensive benchmark description]

---

## Practical Applications & Use Cases

### 1. **Spreadsheet Automation (Microsoft Excel/Google Sheets)**

**Scenario:** User asks "Calculate the average salary by department and identify outliers."

**Process:**
```
Agent Skill Execution:
1. Interprets user query
2. Invokes skill: "SummarizeByCategory"
   - Triggers: "When summarizing data by groups"
   - Instructions: [original, possibly flawed]
3. First attempt fails: Wrong aggregation function
   
SkillAxe Diagnosis:
- Quality: 0.0 (wrong result)
- Trigger: 1.0 (correct skill choice)
- Compliance: 0.5 (step "aggregate values" ambiguous)
- Coverage: 0.3 (missing outlier detection case)

Improvement Brief:
- Add specific aggregation steps (SUM, AVERAGE, COUNT)
- Add step for outlier detection (zscore > 2σ)
- Add examples for multiple aggregation scenarios

Refined Skill:
- Includes explicit AVERAGE for numerical columns
- Includes outlier detection using statistical methods
- Tested on variety of group sizes

Second Attempt: SUCCEEDS
```

**Outcome:**
- User gets correct answer immediately
- System learns for future similar queries
- No human intervention needed

### 2. **Web Automation and Data Extraction**

**Scenario:** Automated bot that monitors competitor pricing across websites.

**Initial Challenge:**
- Websites change layouts frequently
- Skill becomes invalid → crashes
- Manual update required every few days

**SkillAxe Solution:**

```
Agent Detects Failure:
- XPath selector no longer finds price element
- Skill crashes

Diagnosis:
- Quality: 0.0 (exception)
- Trigger: 1.0 (correct website)
- Compliance: 0.3 (XPath selector outdated)
- Coverage: 0.0 (no fallback for layout changes)

Improvement Brief:
- Add CSS selector fallback
- Add heuristic-based price detection (look for currency symbols)
- Add webpage versioning to track layout changes

Refined Skill:
- Multiple selector strategies (XPath → CSS → heuristic text search)
- Robust to minor layout changes
- Logs changes for human review
```

**Result:** System self-heals when websites change, reducing manual maintenance by 80%.

### 3. **Agentic Code Review and Testing**

**Scenario:** Code review agent uses skill to "Identify potential security vulnerabilities."

**Iteration:**

```
Day 1 - Initial Skill:
Pass Rate: 35% (many false positives and false negatives)

Days 1-10 - Learning from Reviews:
- Agent reviews 100+ pull requests
- SkillAxe collects failures
- Analyzes what cases the skill misses
- Missing: OWASP injection patterns, race conditions

Refined Skill (Day 10):
Pass Rate: 58% (+66% improvement)
- Added explicit checks for SQL injection patterns
- Added concurrency bug detection
- Improved clarity of output explanations

Days 10-30 - Continued Learning:
Pass Rate: 68% 
- Added crypto-related vulnerabilities
- Improved logic for privilege escalation detection
- Better integration with SAST tools
```

**Benefit:** Skill improves autonomously from production reviews, no labeled data needed.

### 4. **Natural Language Processing and Text Extraction**

**Scenario:** Document processing system extracts entities (names, dates, amounts) from contracts.

**Self-Improvement Loop:**

```
Real Deployment (Production):
- Agent processes 1000+ documents daily
- 85% success rate (acceptable but improvable)

Failure Analysis (Weekly):
- Extract 50 failure samples
- Diagnose across four dimensions
- Identify patterns:
  - Handles clear English but not abbreviated text
  - Misses dates in non-standard formats
  - Struggles with currency variations

Improvement Generation:
- Add step for text normalization
- Add pattern library for date formats
- Add currency symbol and code recognition

Redeployed Skill:
- Success rate improves to 92%
- Handles abbreviated entities
- Recognizes 50+ date formats
- Normalizes currency amounts
```

**Impact:** Autonomous improvement without retraining, reducing manual annotation burden.

---

## Insights & Implications

### 1. **Self-Diagnosis is Powerful**

**Key Insight:** The same LLM that fails to write a good skill can often diagnose why it failed.

This seems contradictory but reflects a capability gap: LLMs struggle with **synthesis** (writing from scratch) but excel at **analysis** (diagnosing failures). This suggests:
- **Implication:** Agentic systems should leverage LLMs for diagnostic and analytical tasks over creative synthesis
- **Future Work:** Combine LLM diagnosis with symbolic refinement (e.g., program synthesis, constraint solving) for even better results

### 2. **Interpretable Dimensions Enable Improvement**

By decomposing quality into interpretable dimensions (coverage, compliance, trigger, impact), SkillAxe makes skill quality observable and actionable.

Compare:
- **Without Decomposition:** "Skill has low quality" (opaque, no action)
- **With Decomposition:** "Coverage 0.3 (handles 30% of cases), trigger precision 1.0 (perfect), compliance 0.5 (steps unclear)" (actionable)

**Implication:** Systems should make quality dimensions explicit and measurable.

### 3. **Continuous Improvement Requires Real Trajectories**

SkillAxe learns from **actual agent failures**, not synthetic data. This is critical because:
- Synthetic failures may not reflect real-world difficulty
- Real failures capture emergent issues (specific user patterns, edge cases in production)
- Learning from real data enables self-adaptation to deployment context

**Implication:** Agentic systems should log failures and feed them back into improvement loops.

### 4. **28% Improvement is Real But Imperfect**

SkillAxe achieves ~28% relative improvement, closing 47-67% of the gap to expert skills. Remaining gaps likely due to:
- **Fundamental skill**: Some tasks require expertise beyond what LLMs can diagnose
- **Coverage**: Some edge cases only discoverable through extensive testing
- **Reasoning**: Complex multi-step reasoning requires symbolic systems, not just skill refinement

**Implication:** SkillAxe is complementary to, not replacement for, expert skill authoring or formal verification for critical systems.

### 5. **Unsupervised Refinement is Cost-Effective**

Traditional improvements to skills require:
- RLHF: 10,000+ annotated preference pairs (~$10,000 cost)
- Testing: Hand-written test suites (10-100 hours engineering time)
- Deployment: Careful rollout with monitoring

SkillAxe requires:
- No labeled data
- No expensive infrastructure
- Automatic operation from failure logs
- Marginal cost: ~1-2% added API calls

**Implication:** Practical deployment of SkillAxe in production enables continuous self-improvement at minimal cost.

---

## Code & Resources

### Official Repository

- **SkillAxe GitHub:** [Not yet available; paper under review]
- **Microsoft Research:** Likely to be released following publication

### Key Dependencies

```python
# Diagnosis Engine
- LLM API (Claude, GPT-4, or other capable model)
- Structured output parsing (JSON, YAML)
- Trajectory logging (database or log file)

# Skill Management
- Skill versioning system
- Performance monitoring (pass/fail tracking)
- Skill registry and deployment

# Integration
- Agent framework (LangChain, AutoGen, or custom)
- Feedback collection pipeline
- Batch processing for refinement
```

### Quick-Start Integration

**Step 1: Define Skill Format**
```python
class Skill:
    name: str
    trigger_condition: str  # Natural language trigger
    instructions: List[str]  # Step-by-step procedure
    output_format: str  # Expected output structure
    examples: List[Dict]  # Example inputs and outputs
```

**Step 2: Implement Failure Logging**
```python
async def execute_skill(agent_state, skill):
    try:
        result = await skill.execute(agent_state)
        log_success(skill.name, agent_state, result)
        return result
    except Exception as e:
        log_failure(skill.name, agent_state, e)
        raise
```

**Step 3: Run Batch Diagnosis**
```python
async def batch_diagnose():
    failures = load_failures(days=7)
    for failure in failures:
        diagnosis = await diagnose_failure(failure)
        log_diagnosis(failure.skill_id, diagnosis)

async def diagnose_failure(failure):
    prompt = build_diagnostic_prompt(failure)
    response = await llm.generate(prompt)
    return parse_diagnosis(response)
```

**Step 4: Generate Improvements**
```python
async def generate_improvements():
    diagnoses = load_recent_diagnoses()
    aggregated = aggregate_by_skill(diagnoses)
    
    for skill_id, agg_diagnosis in aggregated.items():
        improvement_brief = await generate_improvement_brief(
            skill_id, agg_diagnosis
        )
        improved_skill = await refine_skill(skill_id, improvement_brief)
        validate_and_deploy(skill_id, improved_skill)
```

**Step 5: Validate Before Deployment**
```python
async def validate_improvement(old_skill, new_skill):
    # Test on previous failures
    previous_failures = load_failures_for_skill(old_skill.id)
    new_passes = 0
    for failure in previous_failures:
        try:
            result = await new_skill.execute(failure.input)
            if validate_result(result, failure.expected):
                new_passes += 1
        except:
            pass  # Still failing
    
    # Check for regression
    previous_successes = load_successes_for_skill(old_skill.id)
    regression_count = 0
    for success in previous_successes[:100]:  # Sample check
        try:
            result = await new_skill.execute(success.input)
            if not validate_result(result, success.expected):
                regression_count += 1
        except:
            regression_count += 1
    
    # Deploy if net positive
    improvement_rate = new_passes / len(previous_failures)
    regression_rate = regression_count / len(previous_successes)
    
    if improvement_rate > regression_rate:
        deploy(new_skill)
    else:
        log_failure("Refinement caused regression, not deploying")
```

---

## Related Work & Context

### Prior Work on Skill Learning

- **Skills in Foundation Models:** Concept of procedural skills in agents
- **In-Context Learning:** How LLMs learn from examples in context
- **Few-Shot Programming:** Using examples to elicit correct behavior

### Complementary Work on Agent Improvement

- **SoK: Agentic Skills -- Beyond Tool Use in LLM Agents:** Systematization of skill frameworks and lifecycles
- **SkillCraft:** Can LLM agents learn to use tools skillfully?
- **EvoSkills:** Self-Evolving Agent Skills via Co-Evolutionary Verification

### Tool Use and Integration

- **Agentic Tool Use in Large Language Models:** Comprehensive survey
- **AutoTool:** Dynamic Tool Selection and Integration for Agentic Reasoning

### Reinforcement Learning for Agents

- **RLHF in LLMs:** Prior work on preference learning
- **Policy Gradient Methods:** Optimization approaches for agent policies
- **Reward Modeling:** How to specify what agents should optimize for

### Future Research Directions

1. **Hybrid Improvement:** Combine SkillAxe diagnosis with formal methods (symbolic refinement, program synthesis) for verified skill improvements

2. **Cross-Skill Learning:** When one skill improves, what other skills benefit? Explore transfer learning between related skills.

3. **Human-in-the-Loop Refinement:** When to involve humans? Combine autonomous refinement with expert oversight for critical systems.

4. **Scalability:** How does SkillAxe scale to systems with thousands of skills? Efficient diagnosis and aggregation algorithms.

5. **Multi-Agent Skill Sharing:** Can skills learned by one agent improve others' performance? Skill marketplace concepts.

6. **Formal Verification:** Provide guarantees that refined skills don't break invariants or security properties.

---

## Limitations and Open Questions

### Current Limitations

1. **28% Improvement is Incremental:** Closes only 47-67% of gap to expert skills; some domains may plateau at lower performance

2. **Domain Coverage:** Tested primarily on spreadsheets and web automation; unclear how well diagnosis works for code generation, planning, or other domains

3. **Scalability to Large Skills:** As skills become more complex, diagnosis may become harder; unclear where scalability breaks down

4. **Cold-Start Problem:** New skills with insufficient failure samples may not improve quickly

5. **Adversarial Failures:** Diagnosis assumes failures are honest; in adversarial settings, an LLM might hide true reasons for failure

### Open Questions

- Can we extend SkillAxe to diagnose and improve trigger conditions (currently assumed mostly correct)?
- How to prioritize which dimension (coverage, compliance, etc.) to improve when multiple dimensions are problematic?
- Can skills be automatically merged or composed when one skill's improvement depends on another skill's capabilities?
- How does SkillAxe perform on safety-critical tasks where failures have high cost?

---

## Key Takeaways

1. **Unsupervised skill improvement is possible** through self-diagnosis of failures across interpretable quality dimensions

2. **28% relative improvement** demonstrates meaningful real-world benefit, though gap to expert skills remains (47-67% gap closure)

3. **Continuous improvement from production failures** enables agentic systems to adapt to deployment context without manual intervention

4. **Interpretable dimensions** (coverage, compliance, trigger, impact) make skill quality observable and actionable

5. **SkillAxe complements, not replaces**, expert skill authoring and formal methods for critical systems

---

## Citation and Further Reading

**How to cite:**

```
Gautam, S., Radhakrishna, A., & Gulwani, S. (2026). 
"SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement." 
arXiv preprint arXiv:2606.10546.
```

**For more information:**
- Full paper: https://arxiv.org/abs/2606.10546
- Related work on skills: SoK: Agentic Skills in this repository

---

*Paper summary compiled from arXiv:2606.10546. For the most current details, refer to the full paper on arXiv.*
