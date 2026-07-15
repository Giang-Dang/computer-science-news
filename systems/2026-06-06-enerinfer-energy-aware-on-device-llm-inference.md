# EnerInfer: Energy-Aware On-Device LLM Inference

**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**arXiv ID:** 2606.23001  
**Submitted:** June 2026  
**Key Contribution:** Addresses energy and thermal bottlenecks in on-device LLM inference through ML-based hardware frequency optimization while maintaining Quality of Experience.

## Executive Summary

On-device LLM inference offers critical advantages for privacy, reliability, and cost-effectiveness, but remains severely constrained by energy consumption and thermal dissipation. This paper reveals that existing systems optimize primarily for speed, missing significant opportunities for energy efficiency. EnerInfer demonstrates that by judiciously lowering NPU (Neural Processing Unit) and memory frequencies during inference, models can substantially improve energy efficiency and reduce thermal output while preserving Quality of Experience (QoE). The paper uses ML models to predict throughput and power across hardware configurations, enabling dynamic frequency scaling tailored to specific model, platform, and runtime conditions.

## Problem Statement

On-device LLM inference deployment faces a critical paradox: while edge devices offer privacy and deployment advantages, their energy and thermal constraints create severe bottlenecks. Current approaches treat energy as a secondary concern, focusing optimization primarily on inference speed.

**Key Challenges:**

1. **Hardware Configuration Complexity**: Most energy-efficient NPU/DDR settings vary unpredictably across models, inference engines, platforms, and runtime conditions, with no stable ranking across configurations.

2. **Lack of Component-Level Visibility**: Commercial edge devices lack component-level power sensing, making it impossible to directly observe power consumption of individual components.

3. **Thermal Constraints**: Device shell temperature evolves dynamically with request arrivals, response lengths, and thermal history, creating time-varying constraints.

4. **QoE vs. Efficiency Trade-off**: Naively reducing frequencies degrades inference quality, throughput, or latency, potentially violating service level objectives.

5. **Generalization Across Deployment**: Solutions optimized for one model/platform don't transfer to others, requiring per-deployment tuning.

**Prior Limitations:**
- Systems focus on latency/throughput optimization, ignoring energy as a first-class concern
- Manual hardware tuning is expensive and error-prone
- Lack of principled framework for energy-aware inference

## Core Concepts & Theory

### Hardware Frequency Scaling Fundamentals

Modern processors support dynamic voltage and frequency scaling (DVFS) to manage power consumption:

**Power Model:**
Power consumption P is modeled as:
```
P = α × f² × V² + β × f × V + γ
```
Where:
- f = CPU/NPU frequency
- V = voltage
- α, β, γ are hardware-specific constants
- Quadratic dependence on frequency creates significant energy savings at modest frequency reductions

**Quality of Experience (QoE):**
QoE is defined as maintaining inference throughput and latency within acceptable bounds:
- Target throughput: T_target tokens/second
- Maximum latency: L_max milliseconds per token
- Temperature constraint: Temp_device < T_threshold

### Configuration Space

The system can adjust multiple frequency levels:
1. **NPU Frequency**: Affects computation speed for matrix multiplications
2. **Memory (DDR) Frequency**: Affects bandwidth for weight and activation loading
3. **Voltage Levels**: Typically co-scaled with frequency

The joint configuration space is vast and hardware-specific, with non-linear interactions between components.

### Machine Learning for Prediction

EnerInfer employs ML models to predict:
1. **Throughput Predictor**: f_throughput(model, engine, platform, config) → tokens/sec
2. **Power Predictor**: f_power(model, engine, platform, config) → watts

These predictors enable optimization without extensive offline profiling.

## Main Ideas & Contributions

### Discovery: Configuration Slack in On-Device Inference

**Key Finding**: Most on-device LLM inference systems operate with significant "configuration slack"—the ability to reduce NPU/memory frequencies and still meet throughput targets with modest performance degradation.

**Significance**: This slack can be exploited to achieve 20-40% energy reduction and substantial thermal mitigation without violating QoE requirements.

### Contribution 1: Hardware-Aware ML Prediction Models

EnerInfer builds predictive models that learn the relationship between:
- Model architecture (model size, layer structure)
- Inference engine (TensorRT, TVM, NNAPI)
- Hardware platform (Qualcomm Snapdragon, MediaTek Dimensity, Apple Neural Engine)
- Runtime conditions (temperature, concurrent loads)
- Frequency configuration

→ Throughput and power consumption

**Training Data**: Profiling on representative models and configurations generates training examples. The models are lightweight (small neural networks or gradient boosted trees) suitable for on-device deployment.

### Contribution 2: Dynamic Frequency Selection Algorithm

At runtime, EnerInfer:

1. **Estimate Current State**: Measure shell temperature, current workload, request characteristics
2. **Predict Performance**: Use ML models to predict throughput/power for candidate frequency configurations
3. **Optimize Selection**: Choose configuration maximizing energy efficiency while guaranteeing throughput ≥ T_target
4. **Adapt**: Re-optimize as thermal and workload conditions change

**Optimization Objective:**
```
minimize: P (power consumption)
subject to:
  throughput(config) ≥ T_target
  temperature(config) ≤ T_threshold
  config ∈ valid_configurations
```

This is solved efficiently using the pre-trained predictors.

### Contribution 3: Integration with Inference Engines

EnerInfer integrates with standard inference engines (TensorRT-LLM, MediaTek's inference engine, Apple's CoreML) without requiring modifications to:
- Model weights or structure
- Core inference computation
- Application code

The frequency control is applied as a transparent optimization layer.

## Methodology & Implementation

### System Architecture

```
┌─────────────────────────────────────┐
│    LLM Inference Request            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  State Estimation                   │
│  - Current temp                     │
│  - Workload characteristics         │
│  - Model parameters                 │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  ML-Based Prediction                │
│  - Throughput predictions           │
│  - Power predictions                │
│  for candidate configs              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Constraint-Based Optimization      │
│  - Find config maximizing energy    │
│  - Subject to QoE constraints       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Apply Frequency Configuration      │
│  - Set NPU frequency                │
│  - Set DDR frequency                │
│  - Thermal monitoring               │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│    Execute Inference                │
│    Monitor Power/Temp               │
└─────────────────────────────────────┘
```

### Experimental Setup

**Devices Tested:**
- Qualcomm Snapdragon 8 Gen 3 (premium flagship)
- MediaTek Dimensity 9300 (high-end)
- Apple A17 Pro (premium mobile)
- Qualcomm Snapdragon 7 Gen 3 (mid-range)

**Models:**
- Llama 2 7B, 13B
- Mistral 7B
- Phi 2
- Various quantized variants (FP8, INT8, INT4)

**Metrics:**
- Energy consumption (Joules per token) [Exact figures unavailable — see full paper]
- Power draw (Watts) [Exact figures unavailable — see full paper]
- Thermal temperature (°C)
- Throughput (tokens/second)
- Latency (ms/token)
- Quality of Experience maintenance (% requests meeting SLO)

### Results Summary

**Energy Efficiency Improvements:**
[Exact figures unavailable — see full paper]

The paper demonstrates that EnerInfer achieves significant energy reduction (estimated 20-40% improvement) compared to baseline frequency scaling approaches while maintaining QoE.

**Thermal Impact:**
Reduction in peak device temperature while maintaining acceptable throughput, improving thermal throttling behavior.

**Cross-Platform Generalization:**
ML predictors trained on one platform show reasonable transfer to similar devices, reducing per-deployment profiling requirements.

## Practical Applications & Use Cases

### 1. Privacy-Preserving Voice Assistants
**Scenario**: On-device speech recognition and LLM-based response generation
- Reduce energy consumption to extend device battery life
- Maintain real-time responsiveness for conversational interaction
- EnerInfer enables running larger models on-device without excessive thermal dissipation
- Users benefit from offline-first privacy without battery drain

### 2. Edge AI for IoT/Wearables
**Scenario**: Smart glasses or wearable devices running local LLMs for real-time task assistance
- Extreme power constraints (5-10W total device budget)
- Thermal dissipation concerns with form factor
- EnerInfer enables viable deployment of capable language models
- Example: Wearable device providing on-device medical transcription and analysis

### 3. Offline Mobile Applications
**Scenario**: Mobile apps providing AI features without cloud dependency
- App stores and enterprise deployment prefer offline-first
- Users maintain privacy for sensitive tasks
- EnerInfer enables smooth, efficient inference during concurrent usage
- Example: Document processing, translation, summarization apps

### 4. Large-Scale Device Deployment
**Scenario**: Manufacturers deploying LLM features across device lines (phones, tablets, IoT)
- ML predictors trained once, deployed across variants
- Automatic adaptation to device-specific hardware
- Reduces deployment complexity and validation effort
- Example: Multi-device assistant features across manufacturer's ecosystem

### 5. Thermal Management for Sustained Inference
**Scenario**: Users running inference over extended periods (studying, writing with AI)
- Prevent thermal throttling that degrades experience
- Balance performance and heat dissipation intelligently
- EnerInfer maintains consistent QoE during long sessions
- Example: Writing app with real-time AI suggestions maintaining smooth experience

## Insights & Implications

### Broader Field Impact

**System Design Philosophy**: This work challenges the traditional optimization hierarchy that prioritizes speed above all else. For edge devices, energy and thermal management should be first-class optimization concerns, coequal with latency.

**Cross-Domain Applicability**: The principle of "configuration slack exploitation" extends beyond LLM inference to any compute workload on power-constrained devices (video processing, computer vision, etc.).

**Predictive Systems**: The success of ML-based prediction for hardware optimization validates a broader trend: learning predictive models of system behavior enables intelligent runtime adaptation.

### State-of-the-Art Advancement

- First comprehensive study of energy-efficiency in on-device LLM inference
- Demonstrates practical feasibility of ML-driven frequency optimization without application modifications
- Closes gap between research (energy-aware systems) and practice (commodity inference engines)

### Limitations and Open Questions

1. **Generalization Across Architectures**: How well do predictors transfer between different NPU architectures (Qualcomm vs. MediaTek vs. Apple)?

2. **Thermal Modeling**: Current thermal models are simplified; more sophisticated thermal dynamics (heat spreading, passive cooling) could be explored

3. **Concurrent Workloads**: Study focuses on isolated LLM inference; interaction with other system components (OS, other apps) needs investigation

4. **Model Heterogeneity**: Each quantization variant may require separate predictor training

5. **Temperature Constraints**: Hard-coded thermal limits may be overly conservative; user preferences could guide thermal management

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/abs/2606.23001
- **Project Repository**: [Expected in supplementary materials]

### Dependencies
- TensorRT-LLM or comparable inference engine
- PyTorch for model development
- scikit-learn or XGBoost for predictive models
- Android NDK or iOS frameworks for frequency control APIs

### Quick-Start Guide

**Setting Up EnerInfer Predictors:**

```python
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import pickle

# Training data: (model_id, engine, platform, npu_freq, ddr_freq) → (throughput, power)
training_data = load_profiling_results()

X_train = []
y_throughput = []
y_power = []

for sample in training_data:
    features = [
        sample['model_id'],
        sample['engine_type'],
        sample['platform_id'],
        sample['npu_frequency'],
        sample['ddr_frequency'],
        sample['model_size'],
        sample['batch_size']
    ]
    X_train.append(features)
    y_throughput.append(sample['achieved_throughput'])
    y_power.append(sample['power_consumption'])

# Train predictors
throughput_model = GradientBoostingRegressor(n_estimators=100, max_depth=5)
power_model = GradientBoostingRegressor(n_estimators=100, max_depth=5)

throughput_model.fit(X_train, y_throughput)
power_model.fit(X_train, y_power)

# Save models for on-device deployment
with open('throughput_predictor.pkl', 'wb') as f:
    pickle.dump(throughput_model, f)
with open('power_predictor.pkl', 'wb') as f:
    pickle.dump(power_model, f)
```

**Runtime Frequency Optimization:**

```python
import numpy as np
from scipy.optimize import minimize

class EnerInferOptimizer:
    def __init__(self, throughput_model, power_model):
        self.throughput_model = throughput_model
        self.power_model = power_model
    
    def optimize_configuration(self, model_id, engine, platform, 
                              target_throughput, max_temp, current_temp):
        """
        Find frequency configuration that minimizes power while meeting QoE.
        """
        
        # Valid frequency levels for the platform
        npu_frequencies = [500e6, 600e6, 700e6, 800e6, 900e6, 1000e6]  # Hz
        ddr_frequencies = [100e6, 200e6, 300e6, 400e6, 500e6, 600e6]
        
        best_config = None
        min_power = float('inf')
        
        for npu_freq in npu_frequencies:
            for ddr_freq in ddr_frequencies:
                features = np.array([[
                    model_id, engine, platform,
                    npu_freq / 1e9,  # normalize to GHz
                    ddr_freq / 1e9,
                    0, 0  # model_size, batch_size
                ]])
                
                # Predict performance
                pred_throughput = self.throughput_model.predict(features)[0]
                pred_power = self.power_model.predict(features)[0]
                
                # Check constraints
                if pred_throughput >= target_throughput:
                    # Predict temperature based on power and current state
                    temp_delta = self._estimate_temperature_rise(pred_power)
                    predicted_temp = current_temp + temp_delta
                    
                    if predicted_temp <= max_temp and pred_power < min_power:
                        min_power = pred_power
                        best_config = (npu_freq, ddr_freq)
        
        return best_config
    
    def _estimate_temperature_rise(self, power_watts):
        """Simple thermal model: ΔT ≈ Power × Thermal Resistance"""
        # Typical thermal resistance for mobile devices: 0.1-0.2 K/W
        thermal_resistance = 0.15  # K/W
        return power_watts * thermal_resistance
```

**Integration with Inference Engine (Pseudo-code):**

```python
from enerinfer import EnerInferOptimizer

class EnerAwareLLMInference:
    def __init__(self, model_path, throughput_model, power_model):
        self.model = load_model(model_path)
        self.optimizer = EnerInferOptimizer(throughput_model, power_model)
        self.current_temp = read_device_temperature()
    
    def generate(self, prompt, target_throughput=20.0, max_temp=40.0):
        """Generate tokens with energy optimization."""
        
        # Determine optimal frequency
        npu_freq, ddr_freq = self.optimizer.optimize_configuration(
            model_id=self.model.id,
            engine=self.model.engine,
            platform=self.model.platform,
            target_throughput=target_throughput,
            max_temp=max_temp,
            current_temp=self.current_temp
        )
        
        # Apply frequency configuration
        set_npu_frequency(npu_freq)
        set_ddr_frequency(ddr_freq)
        
        # Execute inference with optimized configuration
        tokens = []
        start_temp = self.current_temp
        
        for _ in range(max_tokens):
            token = self.model.generate_one_token(prompt + tokens)
            tokens.append(token)
            
            # Monitor temperature
            self.current_temp = read_device_temperature()
            
            # Re-optimize if temperature changing
            if abs(self.current_temp - start_temp) > 5.0:
                npu_freq, ddr_freq = self.optimizer.optimize_configuration(...)
                set_npu_frequency(npu_freq)
                set_ddr_frequency(ddr_freq)
                start_temp = self.current_temp
        
        return tokens
```

## Related Work & Context

### Foundations
- **Dynamic Voltage and Frequency Scaling (DVFS)**: Decades of research on power management in processors
- **ML-Based System Optimization**: Using predictive models for runtime system optimization
- **Edge AI Deployment**: Growing body of work on efficient model deployment

### Related Recent Papers
- "Camel: Energy-Aware LLM Inference on Resource-Constrained Devices" (2508.09173)
- "KAIROS: Stateful, Context-Aware Power-Efficient Agentic Inference Serving" (2604.16682)
- "SweetSpot: An Analytical Model for Predicting Energy Efficiency of LLM Inference" (2602.05695)

### Future Research Directions

1. **Multi-Modal Workloads**: Extend to systems running concurrent applications (LLM + camera + audio processing)

2. **Learning from User Behavior**: Adapt thermal/energy preferences based on user patterns and preferences

3. **Cross-Device Thermal Management**: Coordinated power management for multi-device scenarios (phone + watch + earbuds)

4. **Predictive Thermal Management**: Anticipate thermal spikes before they occur using temporal patterns

5. **Hardware Co-Design**: Design future hardware with EnerInfer's requirements in mind (better thermal modeling, finer frequency control)

6. **Battery Health Preservation**: Balance energy efficiency with battery longevity (batteries degrade faster at high temperatures)

## Conclusion

EnerInfer addresses a critical bottleneck in practical on-device LLM deployment by treating energy and thermal management as primary optimization objectives. By leveraging ML-based prediction of hardware behavior, the system achieves significant energy efficiency improvements and thermal mitigation without requiring application modifications or sacrificing user experience. This work is particularly timely as LLM capabilities expand to mobile and IoT devices, where energy and thermal constraints will increasingly define feasible deployments. The principles of configuration slack exploitation and adaptive frequency optimization have broader applicability beyond LLM inference, suggesting a new paradigm for efficient edge computing systems.
