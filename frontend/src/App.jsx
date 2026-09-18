import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const starterQuestions = [
  "I lost my student ID. What should I do?",
  "How can I get medical assistance?",
  "Who can help with a hostel issue?",
];

const featureCards = [
  { icon: "01", title: "Ask", text: "Describe your campus problem in plain language." },
  { icon: "02", title: "Retrieve", text: "CampusCare finds the most relevant trusted guidance." },
  { icon: "03", title: "Respond", text: "You get a clear answer together with its sources." },
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
        throw new Error(
          data.detail || "The CampusCare backend returned an error."
        );
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
    setAnswer("");
    setSources([]);
  }

  function clearConversation() {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <main className="page-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <section className="app-card">
        <header className="topbar">
          <div className="brand">
            <div className="brand-mark" aria-hidden="true">C</div>
            <div>
              <strong>CampusCare AI</strong>
              <span>Student support assistant</span>
            </div>
          </div>

          <div className="status-pill">
            <span className="status-dot" />
            Open Innovation
          </div>
        </header>

        <section className="hero">
          <div className="eyebrow">CODE CORTEX 3.0 • AI-POWERED SUPPORT</div>
          <h1>Get the right campus guidance, <em>faster.</em></h1>
          <p className="hero-copy">
            CampusCare helps students find support information through a simple
            question-and-answer experience grounded in a trusted knowledge base.
          </p>
        </section>

        <section className="feature-grid" aria-label="How CampusCare works">
          {featureCards.map((item) => (
            <article className="feature-card" key={item.icon}>
              <span className="feature-number">{item.icon}</span>
              <div>
                <strong>{item.title}</strong>
                <p>{item.text}</p>
              </div>
            </article>
          ))}
        </section>

        <section className="question-card">
          <div className="section-heading">
            <div>
              <div className="section-kicker">ASK CAMPUSCARE</div>
              <h2>What do you need help with?</h2>
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
              <span className="hint">Enter to ask • Shift + Enter for a new line</span>
              <button
                className="primary-button"
                type="submit"
                disabled={loading || !question.trim()}
              >
                {loading ? "Finding guidance..." : "Ask CampusCare"}
              </button>
            </div>
          </form>

          <div className="suggestions">
            <span className="suggestions-label">Quick questions</span>
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
            <strong>We could not reach the backend</strong>
            <p>{error}</p>
          </section>
        )}

        <section className="answer-card" aria-live="polite">
          <div className="section-heading">
            <div>
              <div className="section-kicker">RESPONSE</div>
              <h2>CampusCare guidance</h2>
            </div>
            <span className={loading ? "status-dot loading" : "status-dot"} />
          </div>

          {loading ? (
            <div className="loading-state">
              <span className="spinner" />
              <strong>Checking the knowledge base…</strong>
              <p>Finding the most relevant campus information.</p>
            </div>
          ) : answer ? (
            <>
              <div className="answer-panel">
                <div className="answer-label">AI GUIDANCE</div>
                <p className="answer-text">{answer}</p>
              </div>

              <div className="sources-section">
                <div className="sources-heading">
                  <div>
                    <div className="section-kicker">TRACEABILITY</div>
                    <h3>Sources used</h3>
                  </div>
                  <span className="source-count">
                    {sources.length} {sources.length === 1 ? "source" : "sources"}
                  </span>
                </div>

                {sources.length > 0 ? (
                  <div className="source-grid">
                    {sources.map((source, index) => (
                      <article className="source" key={source.title || index}>
                        <span className="source-icon">↗</span>
                        <div>
                          <strong>{source.title || "Campus source"}</strong>
                          <span>{source.source || "Knowledge base"}</span>
                        </div>
                      </article>
                    ))}
                  </div>
                ) : (
                  <p className="muted">No source metadata was returned for this answer.</p>
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">?</div>
              <strong>Your answer will appear here</strong>
              <p>Start with a question about campus services or student support.</p>
            </div>
          )}
        </section>

        <footer className="footer-note">
          <span>CampusCare AI • MVP</span>
          <span>Connected to <code>/api/chat</code></span>
        </footer>
      </section>
    </main>
  );
}
