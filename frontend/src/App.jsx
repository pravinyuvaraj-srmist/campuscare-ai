import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const starterQuestions = [
  {
    icon: "🪪",
    title: "Lost student ID",
    text: "I lost my student ID. What should I do?",
  },
  {
    icon: "🩺",
    title: "Medical help",
    text: "How can I get medical assistance?",
  },
  {
    icon: "🏠",
    title: "Hostel support",
    text: "Who can help with a hostel issue?",
  },
  {
    icon: "🚨",
    title: "Emergency help",
    text: "What should I do in a campus emergency?",
  },
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
      setAnswer(data.answer || "No guidance was returned.");
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

  function selectStarter(text) {
    setQuestion(text);
    setError("");
  }

  function clearConversation() {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <main className="page">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">✦</div>
          <div>
            <strong>CampusCare</strong>
            <span>AI Student Assistant</span>
          </div>
        </div>

        <div className="status-pill">
          <span className="status-dot" />
          Open Innovation MVP
        </div>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">SMART CAMPUS • SIMPLE SUPPORT</p>
          <h1>
            Get the right campus help,
            <span> without the searching.</span>
          </h1>
          <p className="subtitle">
            Ask a question in plain language and get grounded guidance with
            source references from the CampusCare knowledge base.
          </p>

          <div className="hero-pills">
            <span>⚡ Fast answers</span>
            <span>📚 Grounded sources</span>
            <span>🎓 Student-first</span>
          </div>
        </div>

        <div className="hero-orbit" aria-hidden="true">
          <div className="orbit-ring ring-one" />
          <div className="orbit-ring ring-two" />
          <div className="orbit-core">✦</div>
          <span className="orbit-icon orbit-icon-one">🩺</span>
          <span className="orbit-icon orbit-icon-two">📚</span>
          <span className="orbit-icon orbit-icon-three">🏠</span>
        </div>
      </section>

      <section className="chat-card">
        <div className="section-heading">
          <div>
            <p className="section-kicker">YOUR QUESTION</p>
            <h2>Ask CampusCare AI</h2>
          </div>
          {(answer || error || question) && (
            <button className="clear-button" type="button" onClick={clearConversation}>
              Clear
            </button>
          )}
        </div>

        <form onSubmit={askQuestion}>
          <div className="input-shell">
            <textarea
              id="question"
              rows="4"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="e.g. Where can I get medical assistance on campus?"
              aria-label="Ask CampusCare a question"
            />
            <button className="ask-button" type="submit" disabled={loading || !question.trim()}>
              {loading ? (
                <>
                  <span className="spinner" />
                  Thinking…
                </>
              ) : (
                <>
                  Ask AI
                  <span aria-hidden="true">→</span>
                </>
              )}
            </button>
          </div>
        </form>

        <div className="suggestion-header">
          <span>Try a quick question</span>
          <span className="tiny-label">Tap to fill</span>
        </div>

        <div className="suggestions">
          {starterQuestions.map((item) => (
            <button
              className="suggestion"
              key={item.text}
              type="button"
              onClick={() => selectStarter(item.text)}
            >
              <span className="suggestion-icon">{item.icon}</span>
              <span>
                <strong>{item.title}</strong>
                <small>{item.text}</small>
              </span>
              <span className="suggestion-arrow" aria-hidden="true">↗</span>
            </button>
          ))}
        </div>
      </section>

      {error && (
        <section className="notice error">
          <span className="notice-icon">!</span>
          <div>
            <strong>We could not connect.</strong>
            <p>{error}</p>
          </div>
        </section>
      )}

      {answer && (
        <section className="result-card">
          <div className="result-header">
            <div className="result-title">
              <div className="result-icon">✦</div>
              <div>
                <p className="section-kicker">CAMPUSCARE RESPONSE</p>
                <h2>Here’s what you can do</h2>
              </div>
            </div>
            <span className="result-badge">Grounded guidance</span>
          </div>

          <div className="answer">
            {answer}
          </div>

          <div className="sources-block">
            <div className="sources-heading">
              <div>
                <p className="section-kicker">REFERENCE MATERIAL</p>
                <h3>Sources used</h3>
              </div>
              <span className="source-count">{sources.length}</span>
            </div>

            {sources.length ? (
              <div className="sources">
                {sources.map((source, index) => (
                  <div className="source" key={`${source.title || "source"}-${index}`}>
                    <span className="source-index">{String(index + 1).padStart(2, "0")}</span>
                    <div>
                      <strong>{source.title || "Campus resource"}</strong>
                      <span>{source.source || "Knowledge base"}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-source">No matching sources were returned.</p>
            )}
          </div>
        </section>
      )}

      <footer className="footer">
        <div>
          <strong>CampusCare AI</strong>
          <span>Built for the Code Cortex Open Innovation track.</span>
        </div>
        <span className="footer-badge">AI • RAG • Student Support</span>
      </footer>
    </main>
  );
}
