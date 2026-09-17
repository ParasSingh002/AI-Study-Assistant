// Grabbing all the elements we need to read from / write to.
const askBtn = document.getElementById("askBtn");
const notesInput = document.getElementById("notes");
const questionInput = document.getElementById("question");
const loading = document.getElementById("loading");
const answerBox = document.getElementById("answerBox");
const answerText = document.getElementById("answerText");
const errorBox = document.getElementById("errorBox");
const errorText = document.getElementById("errorText");

askBtn.addEventListener("click", async () => {
  const notes = notesInput.value;
  const question = questionInput.value;

  // Basic validation before we even talk to the backend.
  if (!question.trim()) {
    showError("Please type a question first.");
    return;
  }

  // Reset UI state: hide old answers/errors, show loading, disable button
  // so the user can't spam-click while we wait for a response.
  answerBox.classList.add("hidden");
  errorBox.classList.add("hidden");
  loading.classList.remove("hidden");
  askBtn.disabled = true;

  try {
    // This is the actual network call to our own Flask backend,
    // which then talks to Gemini on the server side (keeps the API
    // key hidden from the browser — never call Gemini directly from JS
    // with your key exposed).
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notes, question }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    answerText.textContent = data.answer;
    answerBox.classList.remove("hidden");

  } catch (err) {
    showError("Could not reach the server. Is app.py running?");
  } finally {
    loading.classList.add("hidden");
    askBtn.disabled = false;
  }
});

function showError(message) {
  errorText.textContent = message;
  errorBox.classList.remove("hidden");
}
