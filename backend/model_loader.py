import tensorflow as tf
from transformers import RobertaTokenizer
import json
from pathlib import Path

ARTIFACT_DIR = Path("truthmark_artifacts")

# Load metadata
with open(ARTIFACT_DIR / "meta.json") as f:
    meta = json.load(f)

MAX_LENGTH = meta["max_length"]

print("Loading tokenizer...")
tokenizer = RobertaTokenizer.from_pretrained(str(ARTIFACT_DIR / "tokenizer"), use_fast=False)

print("Loading full SavedModel...")
_loaded = tf.saved_model.load(str(ARTIFACT_DIR / "truthmark_full_model"))
infer = _loaded.signatures["serve"]

print("Model loaded successfully.")
