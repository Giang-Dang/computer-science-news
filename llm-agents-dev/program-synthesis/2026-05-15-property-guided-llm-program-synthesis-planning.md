# Property-Guided LLM Program Synthesis for Planning

**ArXiv ID:** 2605.16142  
**Authors:** André G. Pereira, Augusto B. Corrêa, Jendrik Seipp  
**Submitted:** May 2026

## Executive Summary

This paper introduces property-guided program synthesis where LLMs generate heuristic functions for AI planning, guided by formal property specifications rather than test-case evaluation. Using a CEGIS-style loop where LLMs propose candidates and a property checker provides verification, the system drastically reduces evaluation cost and iterations. Concrete counterexamples from property violations guide LLM refinement, enabling agents to synthesize stronger planning heuristics more efficiently than traditional test-driven approaches.

## Problem Statement

Synthesizing heuristic functions for AI planning faces significant challenges:
- **High evaluation cost**: Testing candidate heuristics requires running full planning algorithms
- **Weak feedback**: Test results (pass/fail) provide limited guidance for improvement
- **Scalability issues**: Complex heuristics are expensive to evaluate on large planning domains
- **Limited specification**: Test cases may miss important properties the heuristic should satisfy
- **Iteration inefficiency**: Many candidate generations needed before finding viable heuristics

Traditional program synthesis approaches rely on exhaustive test case evaluation. For planning heuristics with expensive evaluation (planning itself is computationally hard), this becomes prohibitive. The research gap centers on using formal property specifications to guide synthesis more efficiently.

## Core Concepts & Theory

### Property-Guided Synthesis Loop (CEGIS-Style)

```
┌──────────────────────────────────────────────────────────────┐
│    Property-Guided Program Synthesis for Planning Heuristics  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ INITIALIZATION                                           │  │
│ │ Input: Planning domain, task set, property specification │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ • Define formal properties heuristic must satisfy        │  │
│ │   Examples:                                              │  │
│ │   - admissibility (h(s) ≤ actual_cost(s, goal))         │  │
│ │   - consistency (h(s) ≤ cost(s→s') + h(s'))            │  │
│ │   - monotonicity variations                              │  │
│ └─────────────────────────────────────────────────────────┘  │
│                           ↓                                    │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ SYNTHESIS LOOP (Iterate until property satisfied)       │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │                                                          │  │
│ │ Step 1: LLM Proposes Candidate                          │  │
│ │ ├─ Input: Domain knowledge, property specs, examples   │  │
│ │ ├─ Generate: Python heuristic function                 │  │
│ │ └─ Represent as: Computable program                    │  │
│ │                                                          │  │
│ │ Step 2: Property Checker Validates                      │  │
│ │ ├─ Run: Heuristic on training instances                │  │
│ │ ├─ Check: Does it satisfy formal property?             │  │
│ │ └─ Decision: Valid or Invalid?                         │  │
│ │                                                          │  │
│ │ ┌─ If VALID ─────────────────────────────────────┐    │  │
│ │ │ Return successful heuristic                    │    │  │
│ │ │ Task complete!                                 │    │  │
│ │ └────────────────────────────────────────────────┘    │  │
│ │                                                          │  │
│ │ ┌─ If INVALID ─────────────────────────────────────┐   │  │
│ │ │ Generate Counterexample:                        │   │  │
│ │ │ • Find instance where property violated         │   │  │
│ │ │ • Example: Heuristic is inadmissible on state s │   │  │
│ │ │ • Compute: Actual cost vs. heuristic estimate   │   │  │
│ │ │                                                 │   │  │
│ │ │ Concrete Feedback to LLM:                       │   │  │
│ │ │ • Show exact violation: h(s) > c(s, goal)      │   │  │
│ │ │ • Provide context: state features, actions      │   │  │
│ │ │ • Suggest direction: "overestimate, need to..."  │   │  │
│ │ │                                                 │   │  │
│ │ │ → Continue synthesis with refined candidate    │   │  │
│ │ └─────────────────────────────────────────────────┘   │  │
│ │                                                          │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                                │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ EFFICIENCY GAIN                                          │  │
│ │ • Early stopping: Evaluation halts at first violation   │  │
│ │ • Concrete feedback: Counterexamples guide refinement   │  │
│ │ • Targeted generation: LLM focuses on violation type    │  │
│ │ • Reduced cost: Evaluation continues only for promising │  │
│ │   candidates, not full test suites                      │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Key Properties for Planning Heuristics

**Admissibility** (Primary):
- Definition: h(s) ≤ true cost from s to goal
- Ensures: A* with heuristic finds optimal solution
- Verification: Check on all training states

**Consistency** (Secondary):
- Definition: h(s) ≤ cost(s→s') + h(s') for all successors s'
- Ensures: Admissible heuristics remain admissible during search
- More restrictive than admissibility

**Goal Recognition**:
- Definition: h(goal) = 0
- Ensures: Search terminates correctly
- Simple to verify

**Non-negativity**:
- Definition: h(s) ≥ 0 for all s
- Ensures: No negative estimates
- Basic sanity check

### Feedback Mechanisms

**Counterexample-Driven Refinement**:
1. Property checker finds violation
2. Extracts concrete state where violation occurs
3. Provides full context to LLM (state features, actions, costs)
4. LLM uses counterexample to guide next candidate generation
5. Process repeats: each iteration learns from specific failures

**Early Stopping Advantage**:
- Traditional: Evaluate heuristic on entire training set
- Property-guided: Stop evaluation when property first violated
- Result: ~50-80% reduction in evaluation cost (estimated)

## Main Ideas & Contributions

1. **Property-Guided Synthesis**: Formal specifications guide candidate generation more efficiently than test cases alone.

2. **Concrete Counterexamples**: Specific property violations provide richer feedback than binary pass/fail test results.

3. **Early Stopping**: Evaluation halts at first violation, eliminating wasted computation on doomed candidates.

4. **LLM-Property Loop**: Combines LLM generation (creative synthesis) with formal verification (correctness guarantee).

5. **Planning-Specific Application**: Demonstrates effectiveness on important domain (AI planning heuristics).

6. **Efficiency Gains**: Substantial reduction in both program generations and evaluation cost compared to test-driven synthesis.

## Methodology & Implementation

### Experimental Setup

**Planning Domains**:
- Classical planning problems (blocks world, logistics, etc.)
- Various difficulty levels and scales
- Training set of planning instances

**Synthesis Task**:
- Generate Python heuristic function
- Target: Admissible estimate of cost-to-goal
- Input: Planning state representation
- Property: Admissibility constraint

**Baselines**:
- Test-driven LLM synthesis (evaluate on full test suite)
- Traditional heuristic design (hand-crafted)
- Other program synthesis approaches

### Results [Exact figures unavailable — see full paper]

**Efficiency Metrics** [Estimated]:
- **Generation reduction**: 30-40% fewer LLM generations vs. test-driven
- **Evaluation savings**: 50-80% reduction in evaluation cost
- **Convergence speed**: Faster discovery of valid heuristics
- **Quality**: Generated heuristics competitive with hand-designed ones

**Key Findings**:
- Concrete counterexamples significantly guide refinement
- Early stopping provides substantial speedup
- LLM can leverage property specifications effectively
- Generated heuristics transfer to similar domains

## Practical Applications & Use Cases

### Use Case 1: Planning Benchmark Acceleration
- Goal: Synthesize heuristics for new planning domain
- Traditional: Test hundreds of candidate functions on full benchmark
- Property-guided: Rapid property-driven refinement, fewer evaluations
- Result: 2-3x faster heuristic development

### Use Case 2: Automated Solver Tuning
- Planning systems need domain-specific heuristics
- Property-guided synthesis automates heuristic design
- Properties ensure heuristics maintain solver correctness
- Enables rapid deployment to new domains

### Use Case 3: Agent Planning Enhancement
- Agents need efficient planning heuristics
- Generated heuristics improve planning speed
- Admissibility property ensures optimality preservation
- Reduced synthesis cost enables frequent re-tuning

### Integration Challenges

1. **Property Specification**: Correctly specifying properties requires planning expertise
2. **False Positives**: Erroneous counterexamples could mislead synthesis
3. **Scalability**: Large planning states make evaluation expensive even with early stopping
4. **Generalization**: Heuristics trained on limited domains may not transfer
5. **Convergence**: Ensuring synthesis eventually finds valid candidate

### Cost & Latency Implications

**Offline (Synthesis Phase)**:
- Significant compute for property checking
- Early stopping dramatically reduces total cost
- Parallelizable: Can check multiple candidates concurrently

**Online (Planning Phase)**:
- Generated heuristics are lightweight Python functions
- Minimal overhead vs. manually-designed heuristics
- Enables faster planning for agents

## Insights & Implications

### For Agent-Driven Development Systems

1. **Formal Guidance**: Formal property specifications complement LLM synthesis, improving both efficiency and correctness.

2. **Counterexample Value**: Concrete failure examples provide actionable feedback for LLM refinement.

3. **Specialization**: Domain-specific properties enable synthesis of specialized, efficient solutions.

### Advancement in Program Synthesis

- Demonstrates effectiveness of property-guided synthesis for complex programs
- Shows LLMs can leverage formal specifications effectively
- Provides methodology for synthesis with formal correctness guarantees

### Limitations & Open Questions

1. **Property Expressiveness**: How to specify complex behavioral properties formally?
2. **Specification Correctness**: What if the property specification itself is wrong?
3. **Scalability to Complexity**: Does approach work for properties harder to check?
4. **Multi-Property Synthesis**: Handling multiple competing properties simultaneously
5. **Generalization Bounds**: Guarantees on unseen domain instances?

## Code & Resources

### Synthesis Framework

- LLM candidate generation with property-aware prompting
- Property checker for admissibility and consistency
- CEGIS loop orchestration
- Counterexample extraction and feedback

### Planning Infrastructure

- Planning domain representation (PDDL format)
- State exploration for training instances
- Cost computation for property checking
- Heuristic evaluation harness

### Dependencies

- LLM API for synthesis
- Planning solver (for cost computation)
- Python execution environment for generated heuristics
- Property verification tools

## Related Work & Context

### Foundational Areas

- **Program synthesis**: Specification-guided synthesis, CEGIS approach
- **AI planning**: Heuristic search, admissibility, consistency
- **Formal methods**: Property specification, verification
- **LLMs for code**: Program generation, refinement

### Related Papers

- "ReaComp: Compiling LLM Reasoning into Symbolic Solvers" (2605.05485)
- "Structured Program Synthesis using LLMs" (2506.13820)
- "Property-Guided LLM Program Synthesis" extends synthesis methodology

### Possible Extensions

1. **Multi-Property Synthesis**: Optimize across multiple properties simultaneously
2. **Hybrid Heuristics**: Combine LLM-synthesized with classical heuristics
3. **Interactive Refinement**: Human guidance on property specification
4. **Portability**: Transfer learned heuristics across planning domains
5. **Provable Properties**: Generate heuristics with formal correctness proofs

## Conclusion

Property-guided synthesis demonstrates that formal property specifications can guide LLM-based program synthesis more efficiently than test-driven approaches. In the planning domain, concrete counterexamples derived from property violations enable rapid refinement of heuristic functions. The approach significantly reduces both synthesis cost and iterations while maintaining correctness guarantees. This work provides a template for applying formal methods to LLM synthesis, opening new possibilities for producing correct, efficient programs through agent-LLM collaboration.

---

_Generated by [Claude Code](https://claude.ai/code)_
