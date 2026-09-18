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

    if (!value || loading) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: value }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.detail || "The CampusCare backend returned an error.");
      }

      setAnswer(data.answer || "No answer was returned.");
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not reach the CampusCare backend."
      );
    } finally {
      setLoading(false);
    }
  }

  function useSuggestion(value) {
    setQuestion(value);
    setError("");
  }

  function clearConversation() {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <main className="page-shell">
      <section className="app-card">
        <header className="hero">
          <div className="eyebrow">OPEN INNOVATION • CODE CORTEX</div>
          <h1>CampusCare AI</h1>
          <p>
            Ask questions about campus services, student support, and emergency
            guidance. Get a clear answer backed by the team’s knowledge base.
          </p>
        </header>

        <section className="question-card">
          <div className="section-heading">
            <div>
              <h2>Ask CampusCare</h2>
              <span>Type your question and press Enter or Ask AI.</span>
            </div>
            {question && (
              <button className="ghost-button" type="button" onClick={clearConversation}>
                Clear
              </button>
            )}
          </div>

          <form onSubmit={askQuestion}>
            <textarea
              id="question"
              rows="5"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  askQuestion();
                }
              }}
              placeholder="Example: What should I do if I lose my student ID?"
              aria-label="Campus question"
            />
            <div className="form-footer">
              <span className="hint">Shift + Enter for a new line</span>
              <button className="primary-button" type="submit" disabled={loading || !question.trim()}>
                {loading ? "Checking..." : "Ask AI"}
              </button>
            </div>
          </form>

          <div className="suggestions">
            <span className="suggestions-label">Try a sample</span>
            <div className="suggestion-list">
              {starterQuestions.map((item) => (
                <button
                  className="suggestion"
                  key={item}
                  type="button"
                  onClick={() => useSuggestion(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </section>

        {error && (
          <section className="message-card error-card" role="alert">
            <strong>Backend connection issue</strong>
            <p>{error}</p>
          </section>
        )}

        <section className="answer-card" aria-live="polite">
          <div className="section-heading">
            <div>
              <h2>AI Answer</h2>
              <span>{loading ? "Searching the CampusCare knowledge base..." : "Your response will appear here."}</span>
            </div>
            <span className={loading ? "status-dot loading" : "status-dot"} />
          </div>

          {loading ? (
            <div className="loading-state">
              <span className="spinner" />
              <p>Finding the most relevant campus guidance...</p>
            </div>
          ) : answer ? (
            <>
              <p className="answer-text">{answer}</p>

              <div className="sources-section">
                <h3>Sources</h3>
                {sources.length > 0 ? (
                  <div className="source-grid">
                    {sources.map((source, index) => (
                      <article className="source" key={source.title || index}>
                        <strong>{source.title || "Campus source"}</strong>
                        <span>{source.source || "Knowledge base"}</span>
                      </article>
                    ))}
                  </div>
                ) : (
                  <p className="muted">The backend did not return source metadata for this answer.</p>
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">?</div>
              <p>Start by asking a campus-related question.</p>
            </div>
          )}
        </section>

        <footer className="footer-note">
          CampusCare AI • Frontend MVP • Backend endpoint: <code>/api/chat</code>
        </footer>
      </section>
    </main>
  );
}
