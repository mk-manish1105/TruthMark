const analyzeBtn = document.getElementById("analyzeBtn");
const textInput = document.getElementById("textInput");
const wordCounter = document.getElementById("wordCounter");
const loadingDiv = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const badge = document.getElementById("badge");
const confidenceText = document.getElementById("confidenceText");
const verdictText = document.getElementById("verdictText");
const progressFill = document.getElementById("progressFill");
const b1 = document.getElementById("b1");
const b2 = document.getElementById("b2");
const b3 = document.getElementById("b3");

const API_URL = "https://mkmanish-truthmark-api.hf.space/analyze-text";

/* Utility */
function getWordCount(text) {
  const words = text.trim().split(/\s+/).filter(w => w.length > 0);
  return words.length;
}

/* Word Counter Logic */
function updateWordCounter() {
  const text = textInput.value.trim();
  const count = getWordCount(text);

  wordCounter.textContent = `${count} words (50-350 required)`;

  if (count === 0) {
    wordCounter.classList.remove("valid", "error");
    analyzeBtn.disabled = true;
  } 
  else if (count < 50) {
    wordCounter.classList.remove("valid");
    wordCounter.classList.add("error");
    wordCounter.textContent = `${count} words (need ${50 - count} more)`;
    analyzeBtn.disabled = true;
  } 
  else if (count > 350) {
    wordCounter.classList.remove("valid");
    wordCounter.classList.add("error");
    wordCounter.textContent = `${count} words (${count - 350} over limit)`;
    analyzeBtn.disabled = true;
  } 
  else {
    wordCounter.classList.remove("error");
    wordCounter.classList.add("valid");
    wordCounter.textContent = `${count} words ✓`;
    analyzeBtn.disabled = false;
  }
}

textInput.addEventListener("input", updateWordCounter);

/* Analyze Button */
analyzeBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  const wordCount = getWordCount(text);

  if (wordCount < 50) {
    alert("⚠️ Please enter at least 50 words for reliable detection.");
    return;
  }

  if (wordCount > 350) {
    alert("⚠️ Please limit your text to a maximum of 350 words.");
    return;
  }

  loadingDiv.classList.remove("hidden");
  resultDiv.classList.add("hidden");
  analyzeBtn.disabled = true;

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Server error");
    }

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    alert(
      "❌ Unable to connect to the backend server.\n\nError: " +
      err.message
    );
    console.error("API ERROR:", err);
  } finally {
    loadingDiv.classList.add("hidden");
    analyzeBtn.disabled = false;
  }
});

/* Render Result */
function renderResult(data) {
  const score = Math.round(data.overall_ai_score);

  badge.textContent = `🤖 AI: ${score}%`;
  confidenceText.textContent = `Confidence: ${data.confidence}`;
  verdictText.textContent = data.verdict;

  setTimeout(() => {
    progressFill.style.width = `${score}%`;
  }, 100);

  if (data.breakdown) {
    b1.textContent = data.breakdown.Perplexity_proxy_Repetition + "%";
    b2.textContent = data.breakdown.Vocabulary_Richness_proxy + "%";
    b3.textContent = data.breakdown.Syntactic_Variation_proxy + "%";
  }

  /* Badge Color */
  if (score >= 70) {
    badge.style.background = "rgba(239,68,68,0.15)";
    badge.style.color = "#ef4444";
    badge.style.borderColor = "rgba(239,68,68,0.3)";
  } 
  else if (score >= 40) {
    badge.style.background = "rgba(245,158,11,0.15)";
    badge.style.color = "#f59e0b";
    badge.style.borderColor = "rgba(245,158,11,0.3)";
  } 
  else {
    badge.style.background = "rgba(16,185,129,0.15)";
    badge.style.color = "#10b981";
    badge.style.borderColor = "rgba(16,185,129,0.3)";
  }

  /* NEW: Render Model Note */
  const modelNoteElem = document.getElementById("modelNote");
  if (data.model_note && modelNoteElem) {
    modelNoteElem.textContent = data.model_note;
  }

  /* NEW: Render Limitations */
  const limitsElem = document.getElementById("limitations");
  if (data.limitations && limitsElem) {
    limitsElem.innerHTML = "";
    data.limitations.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      limitsElem.appendChild(li);
    });
  }

  resultDiv.classList.remove("hidden");
}


/* Keyboard Shortcut */
textInput.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter" && !analyzeBtn.disabled) {
    analyzeBtn.click();
  }
});
