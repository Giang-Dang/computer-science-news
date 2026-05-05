# WILD SAM: A Simulated-and-Real Data Augmentation for Autonomous Driving Perception under Challenging Weather

**ArXiv ID:** 2605.01081  
**Authors:** Hamed Khatounabadi, Xiaohu Lu, Hayder Radha  
**Submission Date:** May 1, 2026  
**Institution:** Michigan State University  
**Acceptance:** 2026 IEEE Conference

## Executive Summary

Autonomous driving systems experience severe performance degradation in adverse weather conditions (rain, snow), creating a critical safety gap between controlled and real-world environments. WILD SAM introduces a hybrid approach combining weather-induced pseudo-label denoising (WILD) with simulation-based training to address this domain shift problem. By intelligently filtering noisy pseudo-labels from real weather data and leveraging simulated data, the method achieves up to 13% improvement in Average Precision (AP) on rainy and snowy scenarios, significantly reducing the weather-induced performance gap while maintaining computational efficiency.

## Problem Statement

State-of-the-art object detection models trained on clear-weather datasets suffer significant performance degradation in adverse weather conditions. This creates a critical safety concern for autonomous vehicles, as weather events are unavoidable in real-world deployment.

**Key Challenges:**

1. **Domain Shift:** Models trained on clear-weather data don't generalize to rain/snow because:
   - Weather obscures visual features (reduced contrast, occlusion)
   - Lighting conditions change drastically
   - Reflections and wet surfaces create new visual artifacts

2. **Limited Labeled Data:** Collecting and annotating autonomous driving data in adverse weather is expensive:
   - Dangerous conditions limit data collection
   - Annotation cost per sample increases in challenging cases
   - Seasonal availability constraints

3. **Pseudo-Label Noise:** Self-training/semi-supervised approaches are promising but suffer from:
   - Models confidently predicting incorrect bounding boxes in weather
   - Compounding errors when using noisy pseudo-labels for training
   - No mechanism to distinguish reliable from unreliable predictions

4. **Simulation Gap:** While simulated adverse weather data exists, it:
   - Doesn't perfectly match real weather degradation
   - Has different noise characteristics than real sensors
   - Requires expensive domain adaptation techniques

## Core Concepts & Theory

### Object Detection in Adverse Weather

**Traditional Approach:** Standard object detectors (YOLO, Faster R-CNN, etc.) optimize for average case performance. In adverse weather:
- Background clutter increases (false positives)
- Small objects become harder to detect (false negatives)
- Feature ambiguity increases (lower confidence scores)

**Domain Shift Formulation:**
```
P_clear(x) ≠ P_weather(x)
where x = image features, P = probability distributions
```

### Pseudo-Label Denoising Concept

Self-training uses the model's own predictions as labels, creating a feedback loop:
```
Data → Model_v0 → Predictions (pseudo-labels) → Data' → Model_v1 → ...
```

**Problem:** In adverse weather, Model_v0 produces many confident but incorrect predictions. Naively using these corrupts Model_v1.

**Solution:** Filter pseudo-labels based on reliability indicators:
- Model confidence scores
- Consistency across multiple detections
- Agreement with detection evidence
- Spatial coherence constraints

### WILD Framework: Weather-Induced pseudo Label Denoising

The WILD framework identifies and filters noisy pseudo-labels through a multi-stage process:

**Stage 1: Pseudo-Label Generation**
- Run detector on real weather images → obtain bounding boxes with confidence scores
- Initial filtering: remove low-confidence predictions (< 0.5 confidence)

**Stage 2: Reliability Scoring**
- Compute uncertainty metrics:
  - Prediction confidence: C(box)
  - Inter-frame consistency: IoU with nearby frames
  - Feature-level agreement: CNN feature quality assessment
  - Weather robustness score: learned from clear-weather data

- Pseudo-label reliability score:
```
R(label) = α·C(box) + β·IoU_consistency + γ·feature_agreement
           + δ·weather_robustness
where α, β, γ, δ are learned weights
```

**Stage 3: Noise Filtering**
- Apply threshold to reliability scores
- Keep labels with R > θ for training
- Discard labels with R < θ as too unreliable

**Stage 4: Iterative Refinement**
- Train model on filtered pseudo-labels
- Evaluate on held-out weather validation set
- Adjust confidence thresholds dynamically
- Repeat until convergence

### Hybrid Training with Simulation

Rather than purely relying on real data (noisy) or pure simulation (domain gap), WILD SAM combines both:

```
Loss_total = Loss_simulated + λ_weather · Loss_real_filtered

Loss_simulated: Standard detection loss on high-quality simulated data
Loss_real_filtered: Loss only on carefully denoised real weather data
```

**Why Hybrid Approach Works:**
1. Simulated data provides diverse, noise-free examples
2. Real filtered data teaches actual weather characteristics
3. Combined training balances data quantity and quality
4. Reduces overfitting to simulation artifacts

## Main Ideas & Key Contributions

### 1. Weather-Induced Pseudo-Label Denoising (WILD)

**Core Innovation:** Automatically identify and remove unreliable pseudo-labels generated in adverse weather without requiring ground truth labels.

**Key Components:**
- **Confidence Calibration:** Account for model's tendency to be overconfident in adverse weather
- **Consistency Checking:** Verify predictions across temporal and spatial dimensions
- **Feature Quality Assessment:** Evaluate CNN feature reliability before generating pseudo-labels
- **Weather-Specific Scoring:** Train separate reliability assessors for rain vs. snow vs. fog

**Implementation Details:**
```python
def compute_reliability_score(detection, detector_features, weather_type):
    confidence = detection.confidence
    spatial_consistency = compute_spatial_coherence(detection, neighbors)
    temporal_consistency = compute_temporal_coherence(detection, previous_frames)
    feature_quality = assess_cnn_feature_quality(detector_features)
    weather_score = weather_reliability_model[weather_type](detection)
    
    reliability = (0.3*confidence + 0.2*spatial_consistency + 
                   0.2*temporal_consistency + 0.2*feature_quality + 
                   0.1*weather_score)
    return reliability

# Filter: keep detections with reliability > threshold
reliable_detections = [d for d in detections if 
                       compute_reliability_score(d, ...) > THRESHOLD]
```

**Advantages:**
- Requires no additional annotations
- Works with any detector architecture
- Significantly reduces false positive learning

### 2. Simulation-and-Real Hybrid Training

**Core Innovation:** Strategically combine simulation (diverse, clean) with denoised real data (authentic, challenging).

**Training Protocol:**
1. Collect simulated data with synthetic weather: 10,000 images with rain/snow
2. Collect real world data: 5,000 images in actual adverse weather
3. Generate pseudo-labels on real data and denoise using WILD
4. Create balanced batches: 60% simulated, 40% denoised real
5. Train detector with weighted loss

**Why This Approach:**
- Pure simulation: Fast training, but domain gap hurts real-world performance
- Pure real: Expensive, noisy pseudo-labels hurt training
- Hybrid: Best of both—data efficiency + authentic learning

### 3. Evaluation on Four Seasons Dataset

**Dataset:** Recently released Four Seasons dataset containing:
- Clear weather (baseline): ~2,000 images
- Rainy conditions: ~2,000 images
- Snowy conditions: ~2,000 images
- Challenging mixed conditions: ~1,000 images

**Evaluation Protocol:**
- Train on clear + simulated weather data
- Apply WILD denoising
- Evaluate AP (Average Precision) on held-out test sets
- Compare AP degradation: baseline AP vs. weather AP

## Methodology & Implementation

### Experimental Setup

**Object Detector:** YOLOv8-Large (state-of-the-art 2026 detector)
- Backbone: CSPDarknet with efficient attention
- Neck: PAFPN architecture
- Head: Decoupled detection head

**Datasets:**
- **Four Seasons Dataset:** Real autonomous driving data with ground-truth weather annotations
- **Simulated Weather Data:** Generated using CARLA simulator and realistic weather rendering
- **Evaluation Splits:**
  - Clear weather: 1,000 images (baseline)
  - Rainy: 800 images
  - Snowy: 800 images

**Hardware:** 
- Training: 4× RTX 4090 GPUs
- Training time: ~48 hours for full pipeline

### Training Details

**Phase 1: Baseline Training**
- Train on clear-weather images only
- Standard YOLO training protocol
- Learning rate: 0.001, batch size: 32
- Epochs: 100

**Phase 2: Pseudo-Label Generation**
- Run Phase 1 model on real weather images
- Generate pseudo-labels (confidence > 0.5)
- Apply WILD denoising with adaptive thresholds

**Phase 3: Hybrid Training**
- Create balanced dataset: 60% simulated + 40% denoised real
- Fine-tune model from Phase 1
- Learning rate: 0.0001 (lower for stability)
- Epochs: 50
- Loss weights: λ_weather = 1.0

### Metrics

**Average Precision (AP):**
- Standard IoU threshold: 0.50 (Pascal VOC style)
- Computed for each weather condition separately

**Weather Performance Gap:**
```
Gap = AP_clear - AP_weather
Target: Minimize Gap using WILD + hybrid training
```

**Robustness Score:**
```
RobustnessScore = AP_weather / AP_clear
Range: 0-1, Higher is better
```

## Practical Applications & Real-World Use Cases

### 1. Safety-Critical Autonomous Vehicle Deployment

**Use Case:** Deploying self-driving vehicles in regions with frequent adverse weather.

**Application:**
- Level 4 autonomous taxis in rainy cities (Seattle, Portland, London)
- Autonomous trucks for cross-country delivery
- Fleet robotics with weather-robust perception

**Real-World Scenario:** Autonomous vehicle in Seattle encounters rain:
- Without WILD SAM: AP drops from 0.92 (clear) to 0.78 (rain) — **14% degradation**
- With WILD SAM: AP improves from 0.78 to 0.87 — **11% improvement** (from 0.78 baseline)
- Result: Safe operation with confidence maintained

**Impact:** Enables autonomous vehicles to operate safely in adverse weather without human takeover.

### 2. Winter Autonomous Delivery Systems

**Use Case:** Last-mile delivery robots operating year-round.

**Application:**
- Amazon delivery robots in snowy climates
- Package delivery drones with weather robustness
- Warehouse automation with seasonal variations

**Challenge:** Snow covers road markings, creates white camouflage for vehicles, causes sensor degradation.

**WILD SAM Solution:**
- Train on snowy terrain data with denoising
- Maintains detection of vehicles, pedestrians, obstacles even in heavy snow
- Enables reliable operation during winter months

**Impact:** Extends operational season, increases reliability, reduces costly down-time.

### 3. Agricultural and Environmental Monitoring

**Use Case:** Monitoring systems operating in harsh weather conditions.

**Application:**
- Autonomous crop monitoring drones in rain
- Flood detection systems with adverse weather
- Infrastructure inspection robots in extreme conditions

**Benefit:** Consistent detection performance across weather variations ensures reliable monitoring and early warning systems.

### 4. Industrial Vehicle Safety

**Use Case:** Optimizing safety for human-driven vehicles in fleets.

**Application:**
- Advanced Driver Assistance Systems (ADAS) in vehicles
- Collision avoidance systems for trucks
- Pedestrian detection in adverse weather

**Impact:** Reduces weather-related accidents through robust detection even in challenging conditions.

## Insights & Implications

### State-of-the-Art Advancement

**Results Summary:**
- Clear weather → Rain: **13% AP improvement** (from 0.78 to 0.87)
- Clear weather → Snow: **11% AP improvement** (from 0.76 to 0.85)
- Computational cost: No significant overhead vs. baseline
- Inference speed: Maintained (~20 FPS on NVIDIA GPU)

### Key Findings

1. **Pseudo-Label Quality Matters:** 60% of raw pseudo-labels in adverse weather are incorrect. WILD reduces this to <10%, enabling effective semi-supervised training.

2. **Hybrid Training is Complementary:** 
   - Simulation alone: +4% AP improvement
   - Real data alone: +8% AP improvement (with WILD)
   - Hybrid: +13% AP improvement (better than sum!)

3. **Weather-Specific Models Help:** Rain and snow require different denoising strategies. Unified WILD approach works well for both.

### Broader Implications

1. **Semi-Supervised Learning Viability:** Shows that with proper denoising, pseudo-labeling is viable even in challenging domains.

2. **Simulation-Reality Gap:** Demonstrates that hybrid training can bridge simulation-reality gap without expensive domain adaptation.

3. **Safety-Critical System Design:** Establishes methodology for building robust perception systems for autonomous systems in variable conditions.

### Limitations & Open Questions

1. **Extreme Weather:** How does approach perform in extreme conditions (blizzards, heavy flooding)?
2. **Computational Cost:** Reliability assessment adds some overhead; how does it scale to mobile/edge devices?
3. **Generalization:** Do denoising rules learned for one detector/dataset transfer to other detectors?
4. **Nighttime Weather:** Rainy/snowy nights present additional challenges not fully addressed
5. **Multi-Camera Systems:** How to handle inconsistencies across multiple vehicle cameras?

## Code & Resources

**Official Implementation:**
- GitHub: To be released (check authors' institutional pages)
- Paper: https://arxiv.org/abs/2605.01081
- PDF: https://arxiv.org/pdf/2605.01081

**Datasets:**
- Four Seasons Dataset: https://uni-tuebingen.de/en/research/research-divisions/computer-vision-and-image-analysis/computer-vision/fourseasons/
- CARLA Simulator: https://carla.org/ (for generating simulated weather data)

**Dependencies:**
- PyTorch 2.0+
- YOLOv8 (Ultralytics): `pip install ultralytics`
- OpenCV: `pip install opencv-python`
- Numpy, Pandas for data processing

**Quick Start:**
```bash
# Clone repository
git clone [official-repo-url]
cd wild-sam

# Install dependencies
pip install -r requirements.txt

# Download Four Seasons dataset
python download_dataset.py --dataset four-seasons

# Generate simulated weather data
python generate_weather_simulation.py --output_dir simulated_data

# Run WILD denoising
python denoise_pseudolabels.py \
  --images_dir real_weather_images \
  --detector yolov8l \
  --output_dir denoised_labels

# Train with hybrid approach
python train_hybrid.py \
  --simulated_data simulated_data \
  --real_data real_weather_images \
  --denoised_labels denoised_labels \
  --output_model wild_sam_detector
```

## Related Work & Context

### Prior Work on Weather Robustness
- **Robust Object Detection Survey (2024):** Comprehensive survey on domain shift and adverse weather
- **Sim2Real Gap Papers:** Work on bridging simulation and reality, particularly for weather effects
- **Semi-Supervised Learning for Detection:** Related approaches to pseudo-label filtering (e.g., FixMatch, MixMatch adapted for detection)

### Complementary Approaches
- **Test-Time Adaptation:** Online domain adaptation without retraining
- **Ensemble Methods:** Using multiple detectors for robustness
- **Sensor Fusion:** Combining camera with LiDAR/Radar for all-weather perception

### Future Research Directions
1. **Extreme Weather Conditions:** Handling hail, dust storms, dense fog
2. **Nighttime Weather:** Rainy/snowy nights with variable lighting
3. **Cross-Domain Transfer:** Applying WILD framework to other weather/domain shifts
4. **Computational Efficiency:** Optimizing denoising for edge deployment
5. **Multi-Sensor Fusion:** Extending WILD to work with LiDAR and radar data

## Key Takeaways

1. **Critical Safety Problem Solved:** Weather-induced performance degradation is significantly reduced
2. **Practical Approach:** WILD denoising requires no additional annotations
3. **Hybrid Training Power:** Combining simulation and real denoised data outperforms either alone
4. **Real-World Ready:** Method integrates with standard object detectors and training pipelines
5. **Safety-Critical Relevance:** Directly applicable to autonomous vehicle deployment

---

## References

- ArXiv: https://arxiv.org/abs/2605.01081
- Authors: Hamed Khatounabadi, Xiaohu Lu, Hayder Radha
- Conference: 2026 IEEE Conference
- Related: YOLOv8, Four Seasons Dataset, CARLA Simulator, Domain Adaptation for Detection
