import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const starterQuestions = [
  "I lost my student ID. What should I do?",
  "How can I get medical assistance?",
  "Who can help with a hostel issue?",
];

const trustItems = [
  ["Grounded", "Answers use the project knowledge base"],
  ["Traceable", "Relevant source metadata is shown"],
  ["Student-first", "Designed for quick, simple campus support"],
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

      <section className="site-frame">
        <header className="topbar">
          <div className="brand">
            <div className="brand-mark" aria-hidden="true">CC</div>
            <div>
              <strong>CampusCare AI</strong>
              <span>Student support intelligence</span>
            </div>
          </div>

          <div className="header-actions">
            <span className="secure-pill"><span /> Knowledge-grounded</span>
            <span className="track-pill">Open Innovation</span>
          </div>
        </header>

        <section className="hero-grid">
          <div className="hero">
            <div className="eyebrow">CODE CORTEX 3.0 • AI-POWERED CAMPUS SUPPORT</div>
            <h1>Campus support, <em>one clear answer</em> at a time.</h1>
            <p className="hero-copy">
              A conversational student assistant that helps you navigate campus
              services, support, and emergency guidance without hunting through
              multiple documents or offices.
            </p>

            <div className="trust-row">
              {trustItems.map(([title, text]) => (
                <div className="trust-item" key={title}>
                  <span className="trust-check">✓</span>
                  <div>
                    <strong>{title}</strong>
                    <p>{text}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <aside className="hero-panel">
            <div className="panel-label">HOW IT WORKS</div>
            <div className="workflow">
              {[
                ["01", "Ask", "Describe your campus question naturally."],
                ["02", "Retrieve", "Find relevant knowledge from the project data."],
                ["03", "Respond", "Generate guidance and surface supporting sources."],
              ].map(([number, title, text], index) => (
                <div className="workflow-step" key={number}>
                  <div className="workflow-line">
                    <span>{number}</span>
                    {index < 2 && <i />}
                  </div>
                  <div>
                    <strong>{title}</strong>
                    <p>{text}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="panel-footer">
              <span className="pulse-dot" />
              Designed for fast student support
            </div>
          </aside>
        </section>

        <section className="workspace">
          <div className="question-card">
            <div className="section-heading">
              <div>
                <div className="section-kicker">ASK CAMPUSCARE</div>
                <h2>What do you need help with?</h2>
                <p>Ask in your own words. No keywords required.</p>
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
                placeholder="Example: I lost my student ID. What should I do?"
                aria-label="Campus question"
              />

              <div className="form-footer">
                <span className="hint">Enter to ask • Shift + Enter for a new line</span>
                <button
                  className="primary-button"
                  type="submit"
                  disabled={loading || !question.trim()}
                >
                  {loading ? (
                    <>
                      <span className="mini-spinner" />
                      Finding guidance
                    </>
                  ) : (
                    <>
                      Ask CampusCare <span className="button-arrow">→</span>
                    </>
                  )}
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
          </div>

          {error && (
            <section className="message-card error-card" role="alert">
              <strong>We could not reach the AI service</strong>
              <p>{error}</p>
            </section>
          )}

          <section className="answer-card" aria-live="polite">
            <div className="section-heading">
              <div>
                <div className="section-kicker">RESPONSE</div>
                <h2>CampusCare guidance</h2>
                <p>{loading ? "Searching trusted project information..." : "Your response will appear here."}</p>
              </div>
              <span className={loading ? "status-dot loading" : "status-dot"} />
            </div>

            {loading ? (
              <div className="loading-state">
                <span className="spinner" />
                <strong>Finding the most relevant guidance…</strong>
                <p>Checking the knowledge base before generating your response.</p>
              </div>
            ) : answer ? (
              <>
                <div className="answer-panel">
                  <div className="answer-topline">
                    <span className="answer-badge">AI GUIDANCE</span>
                    <span className="verified-badge">● Source-aware</span>
                  </div>
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
                <div className="empty-icon">✦</div>
                <strong>Ready when you are</strong>
                <p>Ask a question about campus services, student support, or emergency guidance.</p>
              </div>
            )}
          </section>
        </section>

        <footer className="footer-note">
          <span>CampusCare AI • Hackathon MVP</span>
          <span>Frontend connected to <code>/api/chat</code></span>
        </footer>
      </section>
    </main>
  );
}
