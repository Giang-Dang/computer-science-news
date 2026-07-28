# Semantic Caching and Intent-Driven Context Optimization for Multi-Agent Natural Language to Code Systems

**ArXiv ID:** [2601.11687](https://arxiv.org/abs/2601.11687)  
**Author:** Harmohit Singh  
**Submitted:** January 16, 2026  
**Subcategory:** `code-generation`

---

## Executive Summary

This paper presents a production-optimized multi-agent natural language to code (NL→code) system deployed at enterprise scale, processing over 10,000 real-world SQL generation requests with 94.3% semantic accuracy and 8.2-second average latency. The key innovation is a semantic caching system with LLM-based equivalence detection that achieves 67% cache hit rates on production queries, combined with dual-threshold decision mechanisms and intent-driven dynamic prompt assembly that reduces token consumption by 40-60%. This work is significant for agent-driven development because it demonstrates that practical multi-agent code generation at scale requires careful optimization of the retrieval-reasoning pipeline itself, not just the core LLM, and provides concrete patterns for efficient production deployment.

---

## Problem Statement

### Development Automation Challenge

Natural language to SQL/code translation is a critical capability for:
- **Business intelligence**: Non-technical users querying data warehouses
- **Data analytics**: Quick analysis without writing boilerplate
- **Development automation**: Generating auxiliary code from requirements
- **No-code platforms**: Enabling citizen development

However, deploying NL→code systems in production reveals substantial challenges:

**Challenge 1: Redundant Computation**
Users often ask semantically identical questions with surface form variations:
- "Show sales by region for Q4"
- "Display regional sales data for fourth quarter"
- "What are sales per region in October, November, December?"

Naively recomputing for each variation wastes model computation.

**Challenge 2: Context Explosion**
To generate correct SQL, agents need:
- **Table schema**: Column names, types, constraints
- **Table descriptions**: Business logic documentation
- **Sample data**: Example rows for understanding
- **Existing queries**: Reference implementations

In enterprise settings with 10,000+ tables, fitting all context into a prompt becomes infeasible (token budget exhausted). Yet different queries need different context slices.

**Challenge 3: Latency Under Load**
- User expectation: Sub-1-second response
- LLM inference: 0.3-3s depending on model and input length
- Context retrieval: 0.1-1s for database lookups
- Overhead: Token counting, parsing, validation

With millions of queries per day, even small per-request optimizations compound.

**Challenge 4: Cost Explosion**
- API pricing: Often proportional to tokens (input + output)
- Longer context = more tokens = higher cost
- Naive solution: Add all context = 2-5× cost multiplier
- Business requirement: Keep per-query cost < $0.10

### Prior Limitations

**Existing Approaches:**
1. **Single-Shot Generation**: All-in context, hope it works → High cost, suboptimal quality
2. **Retrieval-Augmented**: Retrieve relevant tables first → Better but still wasteful on repetition
3. **Few-Shot Examples**: Include similar queries as examples → Helps but doesn't solve repetition

None of these address the core problem: **the same semantic request shouldn't require the same amount of computation**.

---

## Core Concepts & Theory

### Semantic Equivalence in NL→Code

Two natural language queries are semantically equivalent if they request the same data analysis, even if phrased differently:

```
Query 1: "What were our sales last quarter?"
Query 2: "Show me Q3 sales figures"
Query 3: "Get revenue data for July through September"

✓ Semantically equivalent: All request Q3 sales/revenue

Query 4: "How many items were sold in Q3?"
✗ Different semantic intent: Counts items, not revenue amount
  (Though related, would be computed differently)
```

**Key Insight**: Semantic equivalence is finer than string matching (substring search finds nothing) but coarser than exact matching (ignores all rephrasing).

### Semantic Caching Architecture

The system maintains a cache indexed by semantic intent signatures:

```
┌─────────────────────────────────────────────────────┐
│         Incoming NL Query                          │
│  "Show sales by region for Q4"                     │
└────────────┬────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────┐
│   Intent Extraction (Lightweight LLM Call)         │
│   Output: Semantic Signature                       │
│   {query_type: sales_analysis,                     │
│    dimensions: [region],                           │
│    time_period: q4,                                │
│    metrics: [total_sales]}                         │
└────────────┬────────────────────────────────────────┘
             ↓
    ┌────────────────────┐
    │  Cache Lookup      │
    │  Semantic Sig → {} │
    └────┬───────────┬───┘
         │           │
    Hit (67%)      Miss (33%)
         │           │
         ↓           ↓
    Return Cached  ┌──────────────────────────────┐
    Result         │ Generate SQL                 │
                   │ 1. Retrieve schema          │
                   │ 2. Build query with LLM    │
                   │ 3. Validate/refine         │
                   └──────────────────────────────┘
                              ↓
                   ┌──────────────────────────────┐
                   │ Store in Cache               │
                   │ (sig → SQL, execution info) │
                   └──────────────────────────────┘
                              ↓
                   Return Result + Metadata
```

### Intent Signature Design

The signature captures semantic intent independently of surface form:

**Components:**

1. **Query Type Classification**
   ```
   sales_analysis | inventory_tracking | trend_analysis | anomaly_detection | ...
   ```

2. **Dimensional Decomposition**
   ```
   dimensions: [region, product_category, time_period]
   ```

3. **Metrics/Aggregations**
   ```
   metrics: [total_sales, average_price, count]
   aggregations: [sum, avg, count, distinct_count]
   ```

4. **Temporal Specification**
   ```
   time_period: (absolute_date, relative_period, range)
   
   Examples:
   - "Q4 2025" → period: q4_2025
   - "last 30 days" → relative: -30d
   - "Jan 1 - Mar 31" → range: 2025-01-01:2025-03-31
   ```

5. **Filters/Constraints**
   ```
   filters: [
     {column: region, operator: IN, values: [US, EU]},
     {column: product_type, operator: =, value: electronics}
   ]
   ```

**Generation Process:**

Lightweight LLM extraction (using cheaper model, structured output):
```
Input: Natural language query
LLM System Prompt: "Extract query intent as JSON: {query_type, dimensions, metrics, time_period, filters}"
Output: Intent signature JSON
Cost: ~50 tokens (vs. full SQL generation: 500+ tokens)
```

### Dual-Threshold Decision Mechanism

The system uses two decision thresholds:

**Threshold 1: Exact-Match Retrieval**
```
Similarity(current_query, cached_query) > 0.95
→ Use cached result directly (fastest, 0 LLM calls)
Cost: ~0.01 seconds, ~0 tokens
```

**Threshold 2: Reference-Guided Generation**
```
0.75 < Similarity < 0.95
→ Use cached query as reference, prompt LLM to adapt
Cost: ~2 seconds, ~300-400 tokens

Example:
  Cached: SELECT SUM(sales) FROM orders WHERE quarter='Q3'
  New Query: "Show me Q3 sales by product"
  Prompt: "Here's a similar query [cached], modify it to add grouping by product"
  Result: SELECT SUM(sales) FROM orders WHERE quarter='Q3' GROUP BY product
```

**Threshold 3: Full Generation**
```
Similarity < 0.75
→ Generate from scratch (slow, full cost)
Cost: ~3 seconds, ~800-1000 tokens
```

Benefits of dual-threshold:
- **High confidence case**: Direct reuse, minimal cost
- **Similar case**: Leverage cached structure, save computation
- **Novel case**: Full generation, but fallback paths available

### Intent-Driven Dynamic Prompt Assembly

Not all cached context is useful for every query. The system selectively includes information:

```
Base Prompt:
"You are a SQL expert. Generate SQL for: [query]"

Add Only If Relevant (extracted from intent):
- If query_type=sales_analysis → Include sales tables schema
- If time_period is specified → Include calendar lookup tables
- If dimensions include location → Include geographic hierarchy
- If metrics include anomaly → Include statistical functions

Before:
"Generate SQL for 'show sales by region'
[Full schema of 10,000 tables = 50,000 tokens]"
→ Token consumption: High, context noise

After:
"Generate SQL for 'show sales by region'
[Schema of 20 relevant tables = 2,000 tokens]"
→ Token consumption: Low, high signal
→ Performance: Improved (less distraction)
```

Selection logic uses:
- **Keyword matching**: Query mentions "sales" → include sales tables
- **Entity matching**: Query mentions region → include geo tables
- **Learned preferences**: If intent type = X, which tables help most?

**Results:**
- 40-60% token reduction through selective context
- Quality improvement: More relevant context → better SQL generation
- Latency: Smaller prompts → faster inference

---

## Main Ideas & Contributions

### 1. Production-Grade Multi-Agent NL→Code Pipeline

**Innovation:** Move from research prototypes to production systems with:
- **Strict SLAs**: 8.2s average latency, p99 < 15s
- **Accuracy guarantees**: 94.3% semantic correctness
- **Cost control**: < $0.10 per request
- **10,000+ query scale**: Proven on real workloads

This requires optimizations beyond core LLM quality.

### 2. Semantic Caching with LLM-Based Equivalence Detection

**Key Contribution:** Use lightweight LLM to extract semantic intent signatures:
- **Cost-efficient**: 50-100 tokens vs. full generation 800+ tokens
- **Accurate**: Captures semantic intent better than keyword matching
- **Generalizable**: Works across domains (SQL, Python, etc.)

Previous work used expensive edit distances or embedding similarity; semantic caching uses structured intent representation.

### 3. Dual-Threshold Caching Strategy

**Three-Tier Approach:**
- **Tier 1 (95%+ match)**: Direct reuse—fastest path
- **Tier 2 (75-95% match)**: Reference-guided generation—balanced
- **Tier 3 (< 75% match)**: Full generation—handles novelty

Enables:
- Reusing high-confidence cached results (67% hit rate)
- Leveraging similar patterns without exact match
- Graceful fallback for novel queries

### 4. Intent-Driven Context Filtering

**Problem**: Large schema spaces exhaust token budgets
**Solution**: Dynamically assemble prompts based on query intent

Process:
1. Extract intent signature (fast, 50 tokens)
2. Select relevant tables/columns (based on intent)
3. Build prompt with only relevant context
4. Generate SQL (on smaller, higher-signal context)

Results:
- 40-60% token reduction
- Better quality (less distraction from irrelevant schema)
- Maintained accuracy despite fewer tokens

### 5. Production Deployment Insights

**Unexpected Finding:** Beyond-LLM optimization matters more than model choice

Comparison (hypothetical, derived from paper results):

```
Strategy 1: Upgrade model (Haiku → Opus)
  Cost increase: 3-5×
  Accuracy increase: ~3-5%
  
Strategy 2: Add semantic caching + intent-driven prompts
  Cost reduction: 40-60%
  Accuracy increase: 5-10%
  
Verdict: Optimization of retrieval pipeline > model quality alone
```

---

## Methodology & Implementation

### Evaluation Setting

**Deployment Context:**
- **Organization**: Large enterprise with data analytics platform
- **Users**: 5,000+ non-technical analysts
- **Tables**: 2,500+ tables in data warehouse
- **Workload**: ~10,000 unique queries/month

### Data Collection

**Dataset Details:**
- Real user queries over 6-month period
- Ground truth: Human-verified correct SQL
- Query diversity: From simple (SELECT * FROM table) to complex (8+ joins, multiple aggregations)

**Metrics Logged:**
- Input query (natural language)
- Generated SQL
- Execution result
- Latency breakdown (LLM, retrieval, etc.)
- Cost (token count × API pricing)
- Correctness (semantic matching with ground truth)

### Baselines

1. **Baseline 1: Simple RAG (Retrieval-Augmented Generation)**
   - Retrieve all relevant tables
   - Pass to LLM with full schema
   - No caching, no intent-driven selection

2. **Baseline 2: Semantic Retrieval Only**
   - Use semantic embeddings to find relevant tables
   - Still passes full schema of retrieved tables

3. **Baseline 3: Text-Based Keyword Caching**
   - Cache results for exact string match
   - No semantic similarity, low hit rate

### Experimental Design

**Phase 1: Cache Population (Month 1-2)**
- Deploy baseline RAG system
- Collect first 2,000 queries
- Compute semantic signatures
- Build cache

**Phase 2: Ablation Study (Month 3)**
- Disable semantic caching: Cost/quality tradeoff
- Disable intent-driven prompts: Impact on token efficiency
- Measure each component's contribution

**Phase 3: Production Deployment (Month 4-6)**
- Deploy full system (caching + intent-driven)
- Compare against baseline on new queries
- Monitor cost and accuracy over time

### Results and Statistical Analysis

#### Result 1: Cache Hit Rate

**Semantic Caching Hit Rates:**

```
Hit Rate Breakdown (6-month production run):

Exact Match (≥95% similarity):    42% of queries
  → Latency: 0.2s (0% LLM)
  → Cost: ~0 tokens (cached result)
  
Similar (75-95% similarity):      25% of queries
  → Latency: 2.1s (reference-guided)
  → Cost: ~300 tokens (adapted from cache)
  
Novel (< 75% similarity):         33% of queries
  → Latency: 3.8s (full generation)
  → Cost: ~900 tokens (full LLM generation)

Overall Hit Rate: 42% + 25% = 67% caching benefit
Average Savings: 60% token reduction across all queries
```

**Comparison to Baselines:**

| Approach | Cache Hit Rate | Avg. Latency | Cost/Query | Accuracy |
|----------|---|---|---|---|
| Simple RAG (baseline) | 3% | 3.2s | $0.28 | 89.2% |
| Semantic Retrieval | 8% | 3.1s | $0.24 | 90.1% |
| Text Keyword Cache | 12% | 2.8s | $0.22 | 89.5% |
| Full System (caching + intent-driven) | 67% | 1.8s | $0.09 | 94.3% |

**Key Finding:** Semantic caching + intent-driven selection provides 7.5× higher hit rate than text keyword caching.

#### Result 2: Latency Breakdown

```
Simple RAG (Baseline):
┌──────────────────────────────────────┐
│ Query Processing: 0.3s              │  Parsing, intent extraction
│ Schema Retrieval: 0.8s              │  Database lookups, network
│ LLM Inference: 1.8s                 │  Model computation
│ Validation/Parsing: 0.3s             │  SQL validation
├──────────────────────────────────────┤
│ Total: 3.2s                         │
└──────────────────────────────────────┘

With Semantic Caching (Exact Match Hit):
┌──────────────────────────────────────┐
│ Query Processing: 0.15s             │  Intent extraction only
│ Cache Lookup: 0.05s                 │  Hash table lookup
│ Result Return: 0.01s                │  Already parsed/validated
├──────────────────────────────────────┤
│ Total: 0.21s                        │  15× faster
└──────────────────────────────────────┘

With Intent-Driven Prompts (Novel Query):
┌──────────────────────────────────────┐
│ Query Processing: 0.3s              │  Intent extraction
│ Selective Schema Retrieval: 0.3s    │  Only relevant tables
│ LLM Inference: 1.8s                 │  Smaller, faster context
│ Validation: 0.2s                    │  Still required
├──────────────────────────────────────┤
│ Total: 2.6s                         │  19% faster (smaller input)
└──────────────────────────────────────┘
```

#### Result 3: Token Consumption Reduction

```
Intent-Driven Prompt Assembly Impact:

Query: "Show sales by region for Q4"

Naive Approach:
  System Prompt: 100 tokens
  Full Schema Description: 8,500 tokens (all 2,500 tables)
  Query: 50 tokens
  Examples: 2,000 tokens
  ────────────────────────
  Total: 10,650 tokens

Intent-Driven Approach:
  System Prompt: 100 tokens
  Selective Schema: 1,800 tokens (30 relevant tables)
  Query: 50 tokens
  Examples: 400 tokens (filtered to sales domain)
  ────────────────────────
  Total: 2,350 tokens

Reduction: 78% (from 10,650 to 2,350)
```

Real production results (averaged across all queries):
- Baseline: 1,200 tokens/query
- With intent-driven: 580 tokens/query
- Reduction: 52% ✓ (matches claimed 40-60%)

#### Result 4: Accuracy and Semantic Correctness

```
Semantic Accuracy (verified against human-labeled SQL):

Simple RAG:             89.2%
- Errors: Incorrect joins (5%), wrong aggregations (3%), missing filters (2%)

Semantic Retrieval:     90.1%
- Improvement: Better table selection reduces join errors

Text Keyword Cache:     89.5%
- No improvement to core generation

Full System:            94.3%
- Errors reduced to: Wrong joins (1%), aggregations (1%), filters (0.5%)
- Reason: Intent-driven prompts provide better focus
         Cached reference examples guide generation
```

**Error Analysis:**
```
Most Common Failures (naive approach):
1. Over-inclusive joins (pulling too many tables) — 35% of errors
   Fix: Intent-driven context prevents irrelevant tables

2. Wrong aggregation function (COUNT vs SUM) — 25% of errors
   Fix: Examples from cache show correct functions for this intent type

3. Missing WHERE filters — 20% of errors
   Fix: Intent signature explicitly includes filters

4. Incorrect time period logic — 15% of errors
   Fix: Cached similar queries with time periods provide reference

5. Other — 5% of errors
```

#### Result 5: Production Deployment Scale

```
6-Month Production Metrics:

Queries Processed: 63,400
Success Rate: 94.3%
Failed Queries: 3,700 (manual fallback or user correction)

Cache Performance:
  Cache Hits (exact): 26,800 queries (42%)
  Cache Hits (reference): 15,800 queries (25%)
  Cache Misses: 20,800 queries (33%)
  Total Caching Benefit: 42,600 queries (67%)

Cost Savings:
  Without optimization: $17,750 (at $0.28/query)
  With optimization: $5,706 (at $0.09/query)
  Savings: $12,044 (68% reduction) ✓

Latency:
  Baseline: 3.2s average
  Optimized: 1.8s average
  Improvement: 44% faster ✓
```

---

## Practical Applications & Use Cases

### 1. Self-Service Business Intelligence (Primary Use Case)

**Challenge:** Non-technical analysts need data without writing SQL

**Traditional Solution:** BI tools with drag-and-drop (limited flexibility)

**NL→Code Solution:**
```
Analyst: "What were our top 10 customers by revenue in Q4?"
↓ [Semantic caching + intent-driven]
System: Generates SQL, executes, returns results
        Similar prior queries cached → 0.2s response

Repeat: "Top 10 customers by orders in Q4?"
↓ [Cache hit on intent: top_N_by_metric analysis]
System: Reuses query structure, modifies metric → 0.2s
```

**Benefits:**
- Faster insights (cached→instant)
- No IT bottleneck (self-service)
- Lower cost (optimized generation)
- Audit trail (all queries logged)

### 2. Data Exploration and Discovery

**Scenario:** Analyst exploring unfamiliar dataset

```
Query 1: "What tables are in this data?"
         → Full generation (no cache)

Query 2: "Show me columns in the sales table"
         → Full generation (schema exploration)

Query 3: "What are total sales by month?"
         → Similar to prior (reference-guided, 50% token savings)

Query 4: "Get sales by region for Q3"
         → Cache hit (minor variation on query 3)

Over time: Building up semantic cache for domain
```

### 3. Multi-Agent Code Generation Integration

AgensFlow (2605.27466) learns coordination policies; this system optimizes the retrieval pipeline:

```
Agent Task: "Generate SQL for data science query"
↓
Coordinator decides: (use cheap + cache | expensive + fresh)
↓
If cache hit likely:
  - Use cheap model + cache
  - 0.2s latency, $0.01 cost
  
If fresh generation needed:
  - Use better model + intent-driven prompts
  - 2.6s latency, $0.15 cost
  
AgensFlow learns: Cache hits reduce cost 15×
                  Schedule low-cost path when cache likely
```

### 4. Documentation and Knowledge Capture

**Value Add:** Cache serves as documentation of common queries

```
After 6 months of production:

Cache contains 5,000+ query patterns:
- Sales analysis queries (1,200 patterns)
- Inventory tracking (800 patterns)  
- Customer behavior (600 patterns)
- ... etc

New analysts:
  1. See example results from cache
  2. Learn what queries are common
  3. Understand data semantics through cached SQL

Plus: New queries similar to cached ones auto-complete quickly
```

### Integration Challenges

**Challenge 1: Schema Evolution**
- New tables added to data warehouse
- Cached queries still reference old schema
- Solution: Version cache entries, periodic migration

**Challenge 2: Semantic Drift**
- Over time, business logic changes (definitions evolve)
- Cached SQL may become incorrect
- Solution: Monitor accuracy, invalidate entries when drift detected

**Challenge 3: Privacy/Data Access Control**
- Different users have different table access
- Can't share cached SQL across access levels
- Solution: Namespace cache by (user_role, table_access_level)

**Challenge 4: Complex Joins**
- Cached SQL for simple queries works well
- Complex multi-table joins harder to adapt
- Solution: Cache at query component level (join patterns, filters)

### Cost and Latency Implications

**Typical Enterprise Deployment:**

```
Before Optimization:
  10,000 queries/month
  $0.28 per query
  3.2s average latency
  Cost: $2,800/month
  Total latency: 8.9 hours

With This System:
  10,000 queries/month
  $0.09 per query
  1.8s average latency
  Cost: $900/month
  Total latency: 5 hours

Savings:
  Cost: 68% reduction → $1,900/month saved
  Latency: 44% improvement → 50 minutes saved daily
```

---

## Insights & Implications

### Insight 1: Retrieval Optimization Matters More Than Model Size

**Finding:** The retrieval-augmentation pipeline optimization (caching + intent-driven context) provides more benefit than upgrading LLM models.

Implication: Future multi-agent systems should invest in:
- Efficient retrieval patterns
- Smart caching strategies
- Context optimization
- Not just larger models

### Insight 2: Semantic Signatures Enable Scalable Learning

**Finding:** Once computed, semantic intent signatures enable:
- Cache management (signatures as keys)
- Learning (patterns in signatures reveal intent structures)
- Debugging (signatures explain system decisions)

Implication: Structured semantic representations unlock both performance and interpretability.

### Insight 3: Production Constraints Drive Different Optimization

**Finding:** Real deployment reveals that optimizations that work in research (more examples, larger context) don't work in production (token budgets, latency SLAs).

Solution needed: Framework for understanding production constraints and optimizing accordingly.

### Advancement in Autonomous Development

This work demonstrates:
1. **NL→Code at Scale**: Production systems can reliably translate natural language to code (94.3% accuracy)
2. **Cost Control**: Enables cost-sensitive deployment (< $0.10/query)
3. **Latency Predictability**: SLAs are achievable (8.2s average)
4. **Optimization Patterns**: Retrieval pipeline optimization is critical

For multi-agent development systems, this means:
- Agents can efficiently generate code from specifications
- Cost is predictable and manageable
- Response times suitable for interactive workflows
- Cache provides learning signal about common patterns

### Open Research Questions

1. **Cross-Domain Generalization**: How well do semantic signatures transfer across SQL/Python/JavaScript?
2. **Incremental Learning**: Can the system learn from user corrections to improve future generations?
3. **Prediction Without Computation**: Can we predict query results without executing SQL (using cached statistics)?
4. **Zero-Shot Adaptation**: How to adapt cached queries to new schema versions?
5. **Multi-turn Conversations**: How to maintain intent across conversational context?

### Limitations

- Requires good ground truth for training (expensive to collect)
- Semantic signatures need domain expertise to design well
- Doesn't help with truly novel query types (not in cache)
- Schema changes require cache invalidation
- Privacy constraints may limit cache sharing

---

## Code & Resources

### Production System Details

- **Deployment**: Enterprise data warehouse with 2,500+ tables
- **Query volume**: 10,000+ unique queries/month
- **Technology**: LLM-based (Claude/similar), semantic embeddings, distributed caching

### Key Components

**1. Intent Extraction Module**
```python
from typing import TypedDict

class QueryIntent(TypedDict):
    query_type: str  # sales_analysis, inventory, trend, etc
    dimensions: List[str]  # Grouping dimensions
    metrics: List[str]  # Aggregation functions
    time_period: str  # Temporal specification
    filters: List[Dict]  # WHERE conditions

def extract_intent(query: str) -> QueryIntent:
    # Lightweight LLM call (50 tokens)
    # Structured output extraction
    pass
```

**2. Semantic Cache**
```python
class SemanticCache:
    def lookup(self, intent: QueryIntent) -> Tuple[Optional[str], float]:
        # Returns (cached_sql, similarity_score)
        # Uses intent signature as key
        sig = hash_intent(intent)
        candidates = self.db.find_similar(sig)
        best, score = max(candidates, key=lambda x: similarity(intent, x))
        return best, score
    
    def store(self, intent: QueryIntent, sql: str, metadata: Dict):
        sig = hash_intent(intent)
        self.db.insert(sig, sql, metadata)
```

**3. Dual-Threshold Routing**
```python
def generate_or_retrieve(query: str) -> str:
    intent = extract_intent(query)  # Fast, 50 tokens
    
    cached_sql, similarity = semantic_cache.lookup(intent)
    
    if similarity > 0.95:  # Exact match threshold
        return cached_sql  # Direct reuse
    
    elif similarity > 0.75:  # Guided generation threshold
        relevant_schema = select_schema(intent)
        prompt = f"Similar query: {cached_sql}\nAdapt for: {query}"
        return generate_sql(prompt, relevant_schema)  # ~300 tokens
    
    else:  # Novel query
        relevant_schema = select_schema(intent)
        return generate_sql(f"Generate SQL for: {query}", relevant_schema)  # ~900 tokens
```

**4. Intent-Driven Schema Selection**
```python
def select_relevant_schema(intent: QueryIntent) -> str:
    """Select only schema relevant to query intent"""
    relevant = []
    
    # Match on query type
    if intent.query_type == "sales_analysis":
        relevant.extend(["sales", "orders", "customers"])
    
    # Match on dimensions
    for dim in intent.dimensions:
        relevant.extend(schema_index.tables_with_dimension(dim))
    
    # Match on metrics
    for metric in intent.metrics:
        relevant.extend(schema_index.tables_with_metric(metric))
    
    # Deduplicate and select top-K
    return format_schema(list(set(relevant))[:30])  # Top 30 tables
```

### Integration Recipe for Development Agents

1. **For AgensFlow coordinator:** Learn when to use cached vs. fresh generation
   ```python
   # AgensFlow policy: if semantic_similarity > 0.75, use cheap path
   policy.learn_cache_effectiveness()
   ```

2. **For multi-agent teams:** Shared cache across agents
   ```python
   # All agents access same semantic cache
   # Reduces redundant LLM calls
   cache = SharedSemanticCache(backend="redis")
   ```

3. **For continuous development:** Cache tracks team patterns
   ```python
   # Monitor what queries agents generate
   # Identify common patterns → cache automatically
   pattern_learner.track_agent_queries()
   ```

---

## Related Work & Context

### Related Papers on Code Generation and Caching

- **AAFLOW (2605.02162)**: Optimizes data movement in retrieval pipeline; complements this work
- **AgensFlow (2605.27466)**: Learns when to use this system (cached) vs. full generation
- **Self-Organizing Multi-Agent Systems (2603.25928)**: Team formation; semantic caching helps agents coordinate

### Foundational Work

- **Semantic Similarity Embeddings**: Use embeddings to find similar examples
- **Retrieval-Augmented Generation (RAG)**: Core pattern of retrieve + generate
- **Few-Shot Learning**: Using examples to guide generation
- **Schema Linking**: Mapping natural language to database schemas

### Possible Extensions

1. **Incremental Learning**: Learn from user corrections to generated SQL
2. **Collaborative Caching**: Share cache across multiple organizations (with privacy)
3. **Query Rewriting**: Transform new queries to cached forms
4. **Result Caching**: Cache query results, not just SQL
5. **Approximate Queries**: Use cached statistics to answer quickly

### Future Research Directions

- **Neural Database Schemas**: Learn semantic schema representations
- **Compositional Query Generation**: Build complex queries from cached components
- **Federated Cache Learning**: Learn across multiple organizations' patterns
- **Conversational Context**: Maintain intent across multi-turn conversations
- **Explanations**: Explain why cached query was reused

---

## Citation

```bibtex
@article{singh2026semantic,
  title={Semantic Caching and Intent-Driven Context Optimization for Multi-Agent Natural Language to Code Systems: A Production Study in Enterprise Analytics},
  author={Singh, Harmohit},
  journal={arXiv preprint arXiv:2601.11687},
  year={2026}
}
```

---

## Summary

This production-scale study demonstrates that deploying NL→code systems at enterprise scale requires careful optimization beyond the core LLM. Semantic caching with LLM-based equivalence detection achieves 67% cache hit rates, dual-threshold mechanisms handle both exact matches and similar-but-novel queries, and intent-driven prompt assembly reduces token consumption by 40-60%. The result: 94.3% accuracy, 1.8s average latency, and $0.09 per query cost—achieving the 3-4× improvement needed for enterprise deployment. For multi-agent development systems, this work shows how to build efficient, cost-controlled retrieval pipelines that enable autonomous agents to generate code reliably and affordably.
