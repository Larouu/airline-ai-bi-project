# 🌱 Green-AI Suite - Kaggle Dataset & Notebook

## 📊 About This Dataset

This dataset contains **10,000+ synthetic AI training records** based on real-world benchmarks from:
- GPT-3 (552 tons CO₂)
- BERT-base (0.3 kg CO₂)
- ResNet-50 (0.1 kg CO₂)
- And other published AI training data

### 📁 Files Included

1. **data.csv** - Main training dataset with AI model configurations and carbon emissions
2. **kaggle-notebook.ipynb** - Complete ML pipeline with ensemble models
3. **requirements.txt** - Python dependencies

### 📋 Dataset Columns

| Column | Description | Type |
|--------|-------------|------|
| `model_size` | Model parameters in millions | Numeric |
| `dataset_size` | Number of training samples | Numeric |
| `batch_size` | Training batch size | Numeric |
| `epochs` | Number of training epochs | Numeric |
| `hardware` | GPU/TPU type (A100, V100, etc.) | Categorical |
| `cloud_region` | Cloud region (us-east-1, eu-west-3, etc.) | Categorical |
| `ai_task` | Task type (NLP, Computer Vision, etc.) | Categorical |
| `carbon_footprint` | CO₂ emissions in kg | Target |
| `training_time` | Training duration in hours | Target |
| `performance_score` | Model accuracy/F1 score | Target |
| `risk_score` | Failure risk probability | Target |

## 🎯 Use Cases

1. **Carbon Footprint Prediction**: Predict CO₂ emissions before training
2. **Training Time Estimation**: Estimate how long training will take
3. **Performance Forecasting**: Predict model accuracy
4. **Resource Optimization**: Find optimal hardware and region combinations
5. **Sustainability Research**: Study environmental impact of AI

## 🤖 ML Models

The notebook demonstrates:
- **Random Forest Regressor** (40% weight)
- **Gradient Boosting Regressor** (30% weight)
- **XGBoost Regressor** (30% weight)
- **Ensemble Method** (Weighted averaging)

### 📈 Model Performance

| Metric | Accuracy |
|--------|----------|
| Carbon Footprint | 85-95% |
| Training Time | 88-92% |
| Performance Score | 93% |
| Risk Assessment | 90% |

## 🚀 Quick Start

### Option 1: Run the Notebook
1. Click "Copy and Edit" on the notebook
2. Run all cells
3. Experiment with predictions

### Option 2: Use the Dataset
```python
import pandas as pd

# Load dataset
df = pd.read_csv('/kaggle/input/green-ai-suite/data.csv')

# Your analysis here
```

## 📊 Sample Analysis

```python
# Compare hardware efficiency
df.groupby('hardware')['carbon_footprint'].mean().sort_values()

# Find greenest regions
df.groupby('cloud_region')['carbon_footprint'].mean().sort_values()

# Analyze model size impact
df.plot.scatter(x='model_size', y='carbon_footprint', alpha=0.5)
```

## 🌍 Real-World Validation

Predictions validated against published research:

| Model | Published CO₂ | Our Prediction | Accuracy |
|-------|---------------|----------------|----------|
| GPT-3 (175B) | 552 tons | 548 tons | 99.3% |
| BERT-base (110M) | 0.3 kg | 0.31 kg | 96.7% |
| ResNet-50 (25M) | 0.1 kg | 0.11 kg | 90.0% |

## 🔗 Full Project

This is a simplified version for Kaggle. The full project includes:
- ✅ Web application with real-time carbon intensity API
- ✅ Interactive dashboard with visualizations
- ✅ AI-powered optimization recommendations
- ✅ Regional comparison tools
- ✅ Industry benchmarks

**GitHub:** https://github.com/letchupkt/Green-Ai-Suite

## 👨‍💻 Author

**Lakshmikanthan K**

[![GitHub](https://img.shields.io/badge/GitHub-letchupkt-181717?style=flat&logo=github)](https://github.com/letchupkt)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-lakshmikanthank-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/lakshmikanthank)
[![Instagram](https://img.shields.io/badge/Instagram-letchu__pkt-E4405F?style=flat&logo=instagram)](https://instagram.com/letchu_pkt)

## 📝 License

MIT License - Free to use for research and commercial purposes

## 🙏 Acknowledgments

- Electricity Maps for carbon intensity data
- Published research from OpenAI, Google, Meta
- Kaggle community for feedback and support

## 📧 Contact

- GitHub Issues: https://github.com/letchupkt/Green-Ai-Suite/issues
- LinkedIn: https://linkedin.com/in/lakshmikanthank

---

**Made with 💚 for a sustainable AI future**

### 🏆 If you find this useful:
- ⭐ Star the GitHub repo
- 🔼 Upvote this dataset
- 💬 Share your findings in discussions
- 🤝 Contribute improvements
