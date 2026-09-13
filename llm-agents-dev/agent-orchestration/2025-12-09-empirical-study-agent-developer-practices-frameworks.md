# An Empirical Study of Agent Developer Practices in AI Agent Frameworks

**ArXiv ID:** [2512.01939](https://arxiv.org/abs/2512.01939)  
**Submitted:** December 9, 2025  
**Authors:** Yanlin Wang, Xinyi Xu, Jiachi Chen, Tingting Bi, Wenchao Gu, Zibin Zheng

## Executive Summary

This paper presents the first large-scale empirical study of LLM-based agent frameworks, analyzing real-world developer practices across 1,575 GitHub projects and 20,620 developer discussions involving ten representative frameworks. The study reveals critical insights about framework selection challenges, multi-framework adoption patterns, and dominant implementation challenges that inform both framework design and developer tool support for AI agent development. The research provides actionable guidance for developers choosing frameworks and for framework designers improving their offerings.

## Problem Statement

While LLM-based agent frameworks are rapidly proliferating in practice, little is known about how developers actually use these frameworks, what challenges they face, and how to design better frameworks to support agent development. The lack of empirical data on real-world agent development practices creates a significant gap between framework design (often driven by researchers) and actual developer needs. This problem is exacerbated by:

- **Framework Proliferation:** Multiple competing frameworks with overlapping functionality create confusion about which framework best serves specific use cases
- **Lack of Developer Guidance:** Developers struggle to make informed decisions about framework selection without empirical data
- **Unknown Pain Points:** The actual challenges developers face when building agents are underexplored, limiting targeted improvements
- **Unclear Adoption Patterns:** The degree to which real-world projects rely on single versus multiple frameworks remains unknown

## Core Concepts & Theory

### Multi-Agent Framework Ecosystem

LLM-based agent frameworks form an interconnected ecosystem serving different functional roles across the agent development lifecycle. The research organizes frameworks into four functional categories:

1. **Basic Orchestration:** Frameworks providing core agent communication and task orchestration primitives
2. **Multi-Agent Collaboration:** Specialized frameworks for coordinating multiple agents and managing agent interactions
3. **Data Processing:** Frameworks handling data pipelines and state management for agents
4. **Experimental Exploration:** Research frameworks for experimenting with novel agent architectures

### Developer-Centric Framework Evaluation

The study constructs a five-dimensional evaluation framework based on developer needs:

```
Framework Evaluation Dimensions:
├── Functionality (does it solve my use case?)
├── Usability (how easy is it to learn and use?)
├── Integration (does it work with my existing tools?)
├── Stability (is it reliable for production?)
└── Community (is there support and documentation?)
```

This framework captures the practical criteria developers apply when selecting and adopting frameworks, moving beyond academic metrics.

## Main Ideas & Contributions

### Key Finding #1: Multi-Framework Adoption is the Norm

The research found that **96% of top-starred projects use multiple frameworks**, contradicting the assumption that developers adopt a single framework per project. This indicates:

- No single framework comprehensively addresses all agent development needs
- Developers compose capabilities from multiple specialized frameworks
- Framework interoperability and standardization become critical challenges

### Key Finding #2: Framework Selection Paralysis

More than **80% of developers report significant difficulties in identifying frameworks matching their requirements**. This creates:

- High cognitive load when evaluating framework options
- Risk of suboptimal framework choices due to incomplete information
- Need for better framework discovery and comparison tools

### Key Finding #3: Developer-Reported Challenges

Developers identified three dominant categories of issues when working with agent frameworks:

```
Issue Category Breakdown:
├── Logic Failures: 33% (incorrect agent behavior, reasoning errors)
├── Tool Integration: 25.6% (difficulty connecting external APIs/tools)
├── Version Instability: 25% (breaking changes, compatibility issues)
└── Documentation: ~16% (unclear or outdated guidance)
```

Logic failures represent the most pressing challenge, suggesting developers need better debugging and reasoning validation tools.

### Key Finding #4: Application Domain Diversity

The ten analyzed frameworks are applied across ten distinct domains:

- Software Development (code generation, testing, refactoring)
- Data Analysis and Processing
- Business Process Automation
- Scientific Research Assistance
- Content Generation
- Customer Service Automation
- Knowledge Management
- Financial Analysis
- Healthcare Applications
- General-Purpose Reasoning

## Methodology & Implementation

### Data Collection

**GitHub Repository Analysis:**
- Analyzed 1,575 GitHub projects using agent frameworks
- Extracted framework usage patterns, version specifications, and integration strategies
- Analyzed project dependencies and multi-framework composition patterns

**Developer Discussion Mining:**
- Collected 20,620 discussions from developer forums, GitHub issues, and documentation
- Extracted and categorized developer-reported problems, solutions, and workarounds
- Analyzed sentiment and pain points expressed in real-time communications

**Framework Selection:**
- Selected ten representative LLM-based agent frameworks covering the full ecosystem
- Frameworks represent different architectural approaches and target use cases
- Covered both mature production frameworks and emerging research frameworks

### Analysis Methods

- **Descriptive Statistics:** Framework adoption rates, framework composition patterns, and issue prevalence
- **Thematic Analysis:** Qualitative coding of developer discussions to identify recurring themes
- **Network Analysis:** Multi-framework dependency patterns and composition topologies
- **Temporal Analysis:** Evolution of framework usage and problem emergence over time

### Evaluation Metrics

**Framework Adoption:**
- Number of projects using each framework
- Framework adoption trends over time
- Multi-framework co-adoption patterns

**Developer Experience:**
- Issue frequency and categorization
- Time-to-resolution for reported issues
- Community discussion volume

**Framework Maturity:**
- Release frequency and version stability
- Breaking change frequency
- Documentation completeness

## Practical Applications & Use Cases

### Use Case 1: Informed Framework Selection

Development teams can use the five-dimensional evaluation framework to:
- Systematically compare frameworks across usability, functionality, integration, stability, and community dimensions
- Identify frameworks addressing their specific requirements
- Anticipate integration challenges before framework adoption

### Use Case 2: Multi-Framework Architecture Design

Organizations can leverage multi-framework composition patterns to:
- Combine basic orchestration frameworks with specialized collaboration frameworks
- Integrate data processing capabilities without rebuilding pipelines
- Reduce development time through framework composition

### Use Case 3: Framework Vendor Roadmapping

Framework maintainers can use empirical findings to:
- Prioritize bug fixes targeting the three most common issue categories
- Improve documentation for frequently questioned features
- Enhance API stability to reduce version-related issues

### Use Case 4: Tool Support Development

IDE and developer tool vendors can:
- Build framework comparison and discovery tools
- Create debugging tools specifically for agent logic failures
- Provide integration assistants for tool connection workflows

## Insights & Implications

### Architectural Insight: Framework Fragmentation Reflects Specialization

The prevalence of multi-framework adoption reveals that agent development, like modern software engineering broadly, benefits from specialization. Rather than monolithic frameworks, the ecosystem has naturally evolved toward specialized frameworks, each optimizing for a specific aspect of agent development. This suggests:

- **Standardization Becomes Critical:** Common interfaces and communication protocols (like MCP) reduce friction between frameworks
- **Composition Tools Are Essential:** Better composition and orchestration tools are needed to manage multi-framework complexity
- **Documentation Must Emphasize Integration:** Framework documentation should focus on integration patterns with other frameworks

### Developer Experience Insight: Logic Failures Reflect Reasoning Complexity

The dominance of logic failures (33% of issues) indicates that developers struggle most with agent reasoning and behavior verification. This points to:

- **Need for Debugging Tools:** Specialized debuggers for tracing agent reasoning and decision-making are critical
- **Testing Framework Requirements:** Frameworks should provide built-in testing and validation capabilities
- **Explainability Matters:** Developers need insight into why agents make specific decisions

### Scalability Insight: Stability Concerns at Production Scale

Version instability issues affecting 25% of reported problems suggest frameworks are being deployed to production at scale but lack sufficient stability guarantees:

- **Semantic Versioning:** Frameworks must commit to backward compatibility policies
- **Deprecation Warnings:** Clear deprecation paths reduce surprise breaking changes
- **LTS Versions:** Long-term support branches can serve production systems

### Implication for Agent Framework Design

The research identifies several priorities for future framework development:

1. **Better Tool Integration:** Streamlined mechanisms for connecting external APIs and tools reduce a major source of friction
2. **Enhanced Debugging:** Built-in tools for tracing agent logic and validating reasoning reduce logic failure incidents
3. **Clear Composition Patterns:** Explicit support for multi-framework composition reduces integration complexity
4. **Stability Commitments:** Clear versioning policies and backward compatibility guarantees build developer confidence

## Code & Resources

### Official Framework Resources

The study analyzed these ten representative frameworks:

- **OpenAI Swarm:** Lightweight multi-agent orchestration
- **LangGraph:** Task graph composition and state management
- **AgentScope:** Academic framework for agent research
- **Dify:** No-code agent builder with visual interfaces
- **AutoGen:** Microsoft's multi-agent conversation framework
- **Semantic Kernel:** Microsoft's skill-based agent architecture
- **Crew AI:** Team-based multi-agent orchestration
- **Bee Framework:** Graph-based agent execution
- **LlamaIndex:** RAG-focused agent framework
- **Anthropic Claude SDK:** Official Anthropic agent tools

### Developer Resources

- [AgentScope Framework Docs](https://agentscope.io)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI Swarm GitHub](https://github.com/openai/swarm)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)

### Integration Patterns

The study identified these common multi-framework composition patterns:

1. **Orchestration + Collaboration:** Base orchestration framework + specialized multi-agent framework
2. **Orchestration + Data Processing:** Core framework + data pipeline and state management
3. **Specialized + Foundation:** Domain-specific framework + general-purpose foundation framework
4. **Experimental + Production:** Research framework for prototyping + production framework for deployment

## Related Work & Context

### Prior Work on Agent Frameworks

- **Survey of LLM Agents (2024):** Comprehensive taxonomy of agent architectures and design patterns
- **Agent Framework Benchmarking (2025):** Performance and usability comparison across frameworks
- **Developer Tool Support for Agents (2025):** IDE integration and debugging tools for agent development

### Foundational Work

- **Multi-Agent Systems Literature:** Classical coordination patterns and communication protocols
- **Software Engineering Tool Adoption:** Developer preferences and decision-making processes
- **API and Framework Design:** Best practices for developer-friendly system interfaces

### Future Research Directions

1. **Longitudinal Studies:** Track how framework preferences evolve as agent development matures
2. **Quantitative Benchmarking:** Develop standardized benchmarks comparing framework performance
3. **Tool Support Research:** Investigate how IDE plugins and debugging tools impact developer productivity
4. **Educational Study:** Examine how developers learn agent framework concepts
5. **Cross-Domain Analysis:** Assess whether framework preferences differ across application domains

## Relevance to Agent Systems and Development Automation

This paper provides critical empirical grounding for the agent development ecosystem:

- **Evidence-Based Design:** Framework designers now have data on actual developer needs and challenges
- **Community Insights:** The multi-framework adoption pattern validates the emerging MCP (Model Context Protocol) standardization initiative
- **Tool Development:** Results inform where developer tool investment has highest ROI (debugging, integration, discovery)
- **Scaling Considerations:** Findings about multi-framework composition inform how to architect large-scale agent systems

The research demonstrates that agent development has matured from academic research to production deployment, creating new demands on frameworks and tooling that extend beyond code generation to encompass reasoning validation, integration management, and production stability.

---

*Paper summary compiled from arXiv:2512.01939. For the most up-to-date results, please refer to the full paper on arXiv.*
