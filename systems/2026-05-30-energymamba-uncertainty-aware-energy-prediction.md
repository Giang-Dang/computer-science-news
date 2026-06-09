# EnergyMamba: An Uncertainty-Aware Graph-Enhanced Selective State Space Model for Energy Consumption Prediction

**Authors:** Lei Zhou, Shiyu Wang, and collaborators

**arXiv ID:** 2606.00506

**Submitted:** May 30, 2026

## Executive Summary

EnergyMamba proposes a novel Graph-Enhanced Selective State Space Model (GE-Mamba) that combines graph neural networks with state space models to enable accurate and reliable energy consumption prediction. By integrating spatial context from grid topology with temporal dynamics and providing uncertainty estimates, the framework achieves approximately 5% improvement in prediction accuracy and 6% improvement in uncertainty quantification over existing baselines, with practical applications for grid management and extreme weather scenarios.

## Problem Statement

Energy consumption prediction is critical for power grid operations, demand forecasting, and renewable energy integration. However, existing approaches face several limitations:

- **Spatial Isolation:** Most methods treat energy prediction as a purely time-series problem without explicitly modeling spatial dependencies among different regions in the power grid
- **Lack of Uncertainty:** Traditional models fail to provide reliable uncertainty estimates, making them unreliable during abnormal situations such as extreme weather events or grid faults
- **Scalability:** Current approaches struggle to scale to large-scale real-world grid topologies with thousands of measurement points
- **Temporal-Spatial Coupling:** Disentangling temporal dynamics from spatial correlations remains a challenging problem in coupled spatiotemporal systems

## Core Concepts & Theory

### Graph-Enhanced Selective State Space Models

EnergyMamba extends the Mamba architecture—a selective state space model with subquadratic complexity—by incorporating graph structure:

1. **Spatial Component:** Uses graph neural networks to model dependencies between grid nodes based on actual power grid topology
2. **Temporal Component:** Employs selective state space models to capture temporal dynamics with linear complexity
3. **Integration:** Injects spatial context learned from the grid topology into the temporal dynamics for coupled spatiotemporal modeling

### Mathematical Foundation

State space models operate on the principle: h(t) = A h(t-1) + B x(t)

The selective mechanism allows different sequence positions to selectively update state, improving expressivity while maintaining efficiency.

### Uncertainty Quantification

**Adaptive Sequential Conformalized Quantile Regression (AS-CQR):**
- Generates prediction intervals with coverage guarantees
- Features locally adaptive normalization to handle non-stationary energy distributions
- Includes online feedback mechanism that adjusts to changing patterns in real-time

## Main Ideas & Contributions

### Novel Technical Contributions

1. **GE-Mamba Architecture:** First integration of graph structure into selective state space models, enabling explicit spatial-temporal coupling
2. **Uncertainty-Aware Framework:** AS-CQR module provides statistically sound confidence intervals, not just point predictions
3. **Adaptive Learning:** Online feedback mechanism allows the model to adapt to regime changes (e.g., seasonal variations, extreme weather)
4. **Practical Relevance:** Addresses real challenges faced by grid operators including peak demand prediction and anomaly detection

### Key Innovations

- Spatial context injection without increasing computational complexity
- Uncertainty quantification with formal coverage guarantees
- Linear-complexity temporal modeling enabling efficient inference on long sequences
- Explicitly handles abnormal situations through adaptive quantile regression

## Methodology & Implementation

### Datasets

Evaluation conducted on four large-scale real-world energy consumption datasets:
- **Florida:** Power grid consumption data with regional granularity
- **New York:** Urban power demand with high temporal variability
- **California:** Grid-scale data with renewable energy integration challenges
- Additional datasets capturing diverse geographic and operational contexts

### Experimental Setup

**Model Architecture:**
- GE-Mamba with Selective Scan Mechanism
- Graph encoder for spatial dependencies
- Selective State Space Layers for temporal modeling
- AS-CQR prediction head for uncertainty estimation

**Baselines:** Compared against 15 state-of-the-art methods including:
- Traditional time series models (ARIMA, Prophet)
- Deep learning approaches (LSTM, Transformer, Temporal Convolution Networks)
- Graph-based methods (Graph Convolution Networks, Graph Attention Networks)
- Recent state space models

### Evaluation Metrics

**Point Prediction:**
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)

**Uncertainty Quantification:**
- Prediction Interval Coverage Probability (PICP)
- Mean Prediction Interval Width (MPIW)
- Sharpe Ratio for risk-adjusted predictions

### Results

**Accuracy Improvements:**
- ~5% improvement in RMSE over best baseline
- Consistent improvements across all four datasets
- Particularly strong performance on peak demand forecasting

**Uncertainty Quantification:**
- ~6% improvement in uncertainty quality metrics
- Maintains theoretical coverage guarantees
- Superior performance during extreme weather events

**Computational Efficiency:**
- Linear complexity in sequence length (O(n) vs O(n²) for attention)
- Practical inference times suitable for real-time grid operations
- Efficient training with reduced memory requirements

## Practical Applications & Use Cases

### Grid Operations & Demand Forecasting

- **Peak Demand Prediction:** Enables utilities to maintain adequate generation capacity
- **Load Balancing:** Helps distribute demand across regions and time periods
- **Reserve Planning:** Informs decisions about spinning reserve requirements

### Renewable Energy Integration

- **Wind/Solar Variability:** Predicts intermittency patterns for variable renewable resources
- **Grid Stability:** Enables proactive balancing when renewable output fluctuates
- **Market Operations:** Supports day-ahead and real-time market clearing

### Extreme Weather Response

- **Outage Preparation:** Early detection of demand spikes during storms or heat waves
- **Risk Management:** Provides uncertainty estimates for contingency planning
- **Disaster Recovery:** Supports rapid restoration prioritization

### Smart Grid Applications

- **Demand Response:** Identifies optimal times for load shifting and conservation
- **Pricing Signals:** Enables dynamic pricing based on accurate supply-demand forecasts
- **Distributed Generation:** Coordinates residential and commercial solar/battery systems

### Regional Grid Operators

Applicable to:
- Independent System Operators (ISOs) in deregulated markets
- Vertically integrated utilities in regulated markets
- Microgrid operators managing distributed resources

## Insights & Implications

### Theoretical Contributions

1. **Spatial-Temporal Decoupling:** Demonstrates that explicit graph structure integration outperforms implicit spatial learning
2. **Selective Mechanisms:** Validates that selective attention to sequences is more efficient than global attention for grid data
3. **Uncertainty as Feature:** Shows that uncertainty estimates are learnable and improve with spatial context

### Field Impact

- **Paradigm Shift:** Moves energy prediction from time-series to spatiotemporal graph learning
- **Safety Critical Systems:** Demonstrates that formal uncertainty quantification enables deployment in critical infrastructure
- **Climate Resilience:** Provides tools for grid operators to handle increasingly extreme weather

### Limitations & Open Questions

1. **Generalization:** Performance on grids with different topology structures requires further investigation
2. **Explainability:** Graph attention weights could be analyzed for grid planning insights
3. **Scalability:** Extension to continental-scale grids with thousands of nodes needs validation
4. **Real-Time Adaptation:** Online learning mechanisms could be strengthened for rapid environment changes

## Code & Resources

**Repository:** Code and data appear to be available on arXiv supplementary materials

**Dependencies:**
- PyTorch for model training
- Graph neural network libraries (PyGeometric or similar)
- Time series libraries for baseline comparisons
- CUDA for GPU acceleration

**Computing Requirements:**
- GPU memory: ~8-16GB for large-scale datasets
- Training time: Hours to days depending on dataset size
- Inference: Real-time capable on standard server hardware

**Quick Start:**
1. Install dependencies: PyTorch, PyGeometric
2. Load one of the provided datasets
3. Initialize GE-Mamba architecture with grid topology
4. Train with adaptive loss including uncertainty regularization
5. Evaluate on held-out test set with coverage guarantees

## Related Work & Context

### Related Recent Papers

- **State Space Models:** Mamba and variants for sequential modeling
- **Graph Neural Networks:** GCN, GAT for spatial dependency learning
- **Uncertainty Quantification:** Conformalized prediction methods
- **Energy Forecasting:** Recent deep learning approaches for demand prediction
- **Spatiotemporal Models:** Traffic flow, weather prediction, and other grid-structured data

### Prior Work Foundations

- Classical time series methods: ARIMA, exponential smoothing
- First generation neural approaches: LSTM-based energy prediction
- Graph learning for energy: Early GNN applications to power systems
- State space models: From signal processing to deep learning

### Future Research Directions

1. **Multi-Step Forecasting:** Extension to longer-horizon predictions with uncertainty bounds
2. **Causal Discovery:** Learning causal relationships between grid nodes
3. **Transfer Learning:** Pre-training on large public datasets for improved generalization
4. **Adversarial Robustness:** Uncertainty-aware defenses against adversarial perturbations
5. **Climate Integration:** Incorporating climate models for long-term grid planning
6. **Decentralized Operation:** Distributed versions for peer-to-peer grid operations
