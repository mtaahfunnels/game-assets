// =======================================================
// 🧠 SECTION 1: Globals & Utilities
// =======================================================

let currentLessonId = null;

// 🎧 Speech Function with Word-by-Word Highlighting
function speak(text, element = null) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";

  if (element) {
    const words = text.trim().split(/\s+/);
    element.innerHTML = words.map(word => `<span class="word">${word}</span>`).join(" ");
    const spans = element.querySelectorAll("span.word");

    let wordIndex = 0;
    utterance.onboundary = (event) => {
      if (event.name === "word" && wordIndex < spans.length) {
        spans.forEach(span => span.style.background = "");
        spans[wordIndex].style.background = "yellow";
        wordIndex++;
      }
    };

    utterance.onend = () => {
      spans.forEach(span => span.style.background = "");
    };
  }

  speechSynthesis.speak(utterance);
}

// =======================================================
// 📚 SECTION 2: Load & Display Lesson
// =======================================================

function loadLesson(path) {
  fetch(path)
    .then((res) => res.json())
    .then((lesson) => {
      currentLessonId = lesson.id;
      showStory(lesson.story_text, lesson.story_images || []);
      showQuestions(lesson.questions);
    });
}

// =======================================================
// 📖 SECTION 3: Story Display & Interaction
// =======================================================

function showStory(storyLines, storyImages = []) {
  const storyDiv = document.getElementById("story");
  storyDiv.innerHTML = "<h2>Story</h2>";

  const narratorBtn = document.createElement("button");
  narratorBtn.textContent = "🔊 Play Full Story";
  narratorBtn.onclick = () => speak(storyLines.join(" "));
  narratorBtn.classList.add("narrator-button");
  storyDiv.appendChild(narratorBtn);

  storyLines.forEach((line, i) => {
    const container = document.createElement("div");
    container.className = "story-block";

    // ✅ Show image first
    if (storyImages[i]) {
      const img = document.createElement("img");
      img.src = storyImages[i];
      img.alt = "Story illustration";
      img.className = "story-img";
      img.style.display = "block";
      img.style.maxWidth = "100%";
      img.style.borderRadius = "10px";
      img.style.marginBottom = "10px";
      container.appendChild(img);
    }

    const p = document.createElement("p");
    p.textContent = line;
    p.onclick = () => speak(line, p);
    container.appendChild(p);

    storyDiv.appendChild(container);
  });
}

// =======================================================
// ❓ SECTION 4: Question & Answer Logic
// =======================================================

function showQuestions(questions) {
  const qDiv = document.getElementById("questions");
  qDiv.innerHTML = "<h2>Questions</h2>";

  let correctCount = 0;

  questions.forEach((q) => {
    const qEl = document.createElement("div");
    qEl.classList.add("question-block");
    qEl.innerHTML = `<p>${q.question}</p>`;

    q.choices.forEach((choice) => {
      const btn = document.createElement("button");
      btn.textContent = choice;

      btn.onclick = () => {
        if (choice === q.answer) {
          btn.style.background = "#4caf50";
          btn.disabled = true;
          correctCount++;

          if (correctCount === questions.length) {
            alert("🎉 You finished the lesson!");
            trackProgress(currentLessonId);
            showRewardBadge();
          }
        } else {
          btn.style.background = "#f44336";
        }
      };

      qEl.appendChild(btn);
    });

    qDiv.appendChild(qEl);
  });
}

// =======================================================
// 🏅 SECTION 5: Reward Badge Display
// =======================================================

function showRewardBadge() {
  const badge = document.createElement("div");
  badge.innerHTML = "🏅 Great job!";
  badge.style.position = "fixed";
  badge.style.top = "40%";
  badge.style.left = "40%";
  badge.style.fontSize = "40px";
  badge.style.padding = "20px";
  badge.style.background = "#fff";
  badge.style.border = "2px solid #333";
  badge.style.borderRadius = "12px";
  badge.style.zIndex = "9999";
  badge.style.boxShadow = "0 0 20px gold";

  document.body.appendChild(badge);
  setTimeout(() => document.body.removeChild(badge), 3000);
}

// =======================================================
// 📊 SECTION 6: Progress Tracking
// =======================================================

function trackProgress(lessonId) {
  const key = `completed_${lessonId}`;
  localStorage.setItem(key, "1");
}

function isCompleted(lessonId) {
  return localStorage.getItem(`completed_${lessonId}`) === "1";
}

// =======================================================
// 🔗 SECTION 7: Auto-Load Lesson via URL
// =======================================================

function getLessonFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("lesson");
}

// =======================================================
// 🚀 SECTION 8: Initialize Page on Load
// =======================================================

document.addEventListener("DOMContentLoaded", () => {
  const lessonFile = getLessonFromURL();
  if (lessonFile) {
    loadLesson("lessons/" + lessonFile);
  }
});
