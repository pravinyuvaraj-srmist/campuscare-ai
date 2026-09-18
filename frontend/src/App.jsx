import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const starterQuestions = [
  "I lost my student ID. What should I do?",
  "How can I get medical assistance?",
  "Who can help with a hostel issue?",
];

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion(event) {
    event?.preventDefault();
    const value = question.trim();
    if (!value) return;

    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: value }),
      });

      if (!response.ok) {
        throw new Error("The backend returned an error.");
      }

      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setAnswer("");
      setSources([]);
      setError(
        "Could not reach the CampusCare backend. Start the FastAPI server and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">OPEN INNOVATION • CODE CORTEX</p>
          <h1>CampusCare AI</h1>
          <p className="subtitle">
            A student-friendly assistant for campus services, support, and
            emergency guidance.
          </p>
        </div>
      </section>

      <section className="card">
        <form onSubmit={askQuestion}>
          <label htmlFor="question">Ask CampusCare</label>
          <textarea
            id="question"
            rows="4"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Type a campus question..."
          />
          <button type="submit" disabled={loading}>
            {loading ? "Checking..." : "Ask AI"}
          </button>
        </form>

        <div className="suggestions">
          {starterQuestions.map((item) => (
            <button
              className="suggestion"
              key={item}
              type="button"
              onClick={() => setQuestion(item)}
            >
              {item}
            </button>
          ))}
        </div>
      </section>

      {error && <section className="card error">{error}</section>}

      {answer && (
        <section className="card">
          <h2>Guidance</h2>
          <p className="answer">{answer}</p>

          <h3>Sources</h3>
          {sources.length ? (
            <div className="sources">
              {sources.map((source) => (
                <div className="source" key={source.title}>
                  <strong>{source.title}</strong>
                  <span>{source.source}</span>
                </div>
              ))}
            </div>
          ) : (
            <p>No matching sources were returned.</p>
          )}
        </section>
      )}
    </main>
  );
}
