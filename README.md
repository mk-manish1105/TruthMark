# TruthMark – AI Content Detection System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **An AI-generated text detection system achieving 93.2% accuracy using RoBERTa embeddings and custom neural networks**

Deployed production-ready FastAPI service that distinguishes between human-written and AI-generated text using state-of-the-art transformer models.

---

## 🎯 Project Highlights

- ✅ **93.2% Validation Accuracy** on 353K samples
- ✅ **98.25% ROC-AUC Score** - exceptional discriminative ability
- ✅ **RoBERTa-base** transformer with frozen embeddings
- ✅ **Custom Neural Network** classifier for efficient inference
- ✅ **Dockerized FastAPI** deployed on Render & Hugging Face
- ✅ **Real-time Analysis** with multi-factor scoring

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Validation Accuracy** | 93.2% |
| **ROC-AUC Score** | 98.25% |
| **Training Samples** | 300,000+ |
| **Validation Samples** | ~53,000 |
| **Model Type** | RoBERTa + Custom NN |
| **Inference Time** | <500ms |

---

## 🏗️ Architecture Overview

```
Input Text (50-350 words)
         ↓
RoBERTa Tokenizer (Max 128 tokens)
         ↓
RoBERTa-base Embeddings (FROZEN)
         ↓
Custom Neural Network Classifier
         ↓
Binary Classification Output
(AI-Generated vs Human-Written)
```

---

## 🛠️ Technology Stack

### Machine Learning & NLP
- **RoBERTa** (`roberta-base`) - Pre-trained transformer embeddings
- **TensorFlow 2.15** - Deep learning framework
- **Hugging Face Transformers** - Model and tokenizer utilities
- **NumPy & Scikit-learn** - Data processing and metrics

### Backend & API
- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Deployment
- **Docker** - Containerization
- **Render** - Cloud hosting
- **Hugging Face Spaces** - Model hosting

### Frontend
- **HTML5/CSS3/JavaScript** - Responsive web interface

---

## 📁 Project Structure

```
TruthMark/
│
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── model_loader.py            # Model initialization
│   ├── predictor.py               # Inference logic
│   ├── requirements.txt           # Dependencies
│   ├── Dockerfile                 # Container config
│   └── truthmark_artifacts/       # Model files
│       ├── meta.json
│       ├── tokenizer/             # RoBERTa tokenizer
│       └── truthmark_full_model/  # TensorFlow SavedModel
│
└── frontend/
    ├── index.html                 # Web interface
    ├── scripts.js                 # Frontend logic
    └── styles.css                 # Styling
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/truthmark.git
cd truthmark

# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access
- **API Docs**: http://localhost:8000/docs
- **Frontend**: Open `frontend/index.html`

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t truthmark-api ./backend

# Run container
docker run -d -p 8000:8000 truthmark-api
```

---

## 📡 API Usage

### Endpoint: `/analyze-text`

**Request:**
```json
POST /analyze-text
Content-Type: application/json

{
  "text": "Your text here (50-350 words)..."
}
```

**Response:**
```json
{
  "overall_ai_score": 75.32,
  "overall_human_score": 24.68,
  "verdict": "Likely AI-Generated",
  "confidence": "High",
  "badge_color": "red",
  "breakdown": {
    "Perplexity_proxy_Repetition": 68.45,
    "Vocabulary_Richness_proxy": 72.10,
    "Syntactic_Variation_proxy": 80.55
  },
  "model_note": "Probabilistic AI-vs-human classifier",
  "limitations": [...]
}
```

---

## 🎯 Verdict Categories

| AI Score | Verdict | Confidence | Badge |
|----------|---------|------------|-------|
| 70-100% | Likely AI-Generated | High | 🔴 Red |
| 40-69% | Mixed/Uncertain | Medium | 🟡 Yellow |
| 0-39% | Likely Human-Created | Low | 🟢 Green |

---

## 📊 Model Training Details

### Dataset
- **Total Samples**: 353,000
- **Training Set**: ~300,000 (85%)
- **Validation Set**: ~53,000 (15%)
- **Split Strategy**: Stratified sampling
- **Preprocessing**: Text cleaning, class balancing

### Model Architecture
```
RoBERTa-base (Frozen Embeddings)
    ↓
[CLS] Token (768-dim)
    ↓
Dense Layer (256 units, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense Layer (128 units, ReLU)
    ↓
Dropout (0.2)
    ↓
Dense Layer (1 unit, Sigmoid)
```

### Training Configuration
- **Optimizer**: Adam (lr=2e-5)
- **Loss**: Binary Cross-Entropy
- **Batch Size**: 32
- **Early Stopping**: Patience=3
- **Max Sequence Length**: 128 tokens

### Results
- **Validation Accuracy**: 93.2%
- **ROC-AUC**: 98.25%
- **F1-Score**: 92.8%
- **Precision**: 94.1%
- **Recall**: 91.6%

---

## 📈 Breakdown Metrics

1. **Perplexity Proxy (Repetition)**
   - Measures trigram repetition patterns
   - Higher scores indicate more repetitive text

2. **Vocabulary Richness Proxy**
   - Inverse Type-Token Ratio (TTR)
   - Higher scores indicate less diverse vocabulary

3. **Syntactic Variation Proxy**
   - Analyzes sentence length consistency
   - Higher scores indicate less varied structure

---

## ⚠️ Known Limitations

- **Accuracy**: Not 100% accurate; use as supplementary tool
- **Style Sensitivity**: Formal human writing may flag as AI
- **Edited Content**: AI text heavily edited by humans may evade detection
- **Tool Identification**: Detects AI likelihood, not specific tools
- **Text Length**: Optimal for 50-350 words
- **Language**: Currently optimized for English only

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Batch processing API
- [ ] Model explainability (SHAP/LIME)
- [ ] Real-time streaming
- [ ] Performance monitoring dashboard
- [ ] Mobile application

---

## 🧪 Testing

### Using cURL
```bash
curl -X POST "http://localhost:8000/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your sample text here..."}'
```

### Using Python
```bash
pip install requests
python -c "import requests; print(requests.post('http://localhost:8000/analyze-text', json={'text': 'Your text'}).json())"
```

---

## 🚀 Deployment

### Render
1. Connect GitHub repository
2. Set build command: `cd backend && pip install -r requirements.txt`
3. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy

### Hugging Face Spaces
1. Create Docker Space
2. Upload code and Dockerfile
3. Build and deploy

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **Hugging Face** - RoBERTa models
- **TensorFlow** - Deep learning framework
- **FastAPI** - Web framework
- **Open Source Community**

---

## 📞 Contact

**Your Name**
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- Portfolio: [yourportfolio.com](https://yourportfolio.com)

---

## 🌟 Support

If you find this project useful, please ⭐ star the repository!

[Report Bug](https://github.com/yourusername/truthmark/issues) · [Request Feature](https://github.com/yourusername/truthmark/issues)

---

<div align="center">

**Built with ❤️ using RoBERTa, TensorFlow, and FastAPI**

**Status**: Production Ready ✅

</div>
