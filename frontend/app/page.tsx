"use client";
import { useState } from "react";
import axios from "axios";

type Cite = { path: string; rank: number; score: number; line_start?: number; line_end?: number };

export default function Page() {
  const [repo, setRepo] = useState("facebook/react");
  const [indexing, setIndexing] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [cites, setCites] = useState<Cite[]>([]);
  const [msg, setMsg] = useState("");
  // Optional: default branch used for deep links
  const [branch, setBranch] = useState("main");

  // Use environment variable injected at build time for client components
  // Avoid process.env in browser: use public env or fallback
  const backend = typeof window !== "undefined" && (window as any).NEXT_PUBLIC_BACKEND_URL
    ? (window as any).NEXT_PUBLIC_BACKEND_URL as string
    : "http://localhost:5000";

  async function doIndex() {
    setMsg(""); setIndexing(true);
    try {
      const res = await axios.post(`${backend}/index`, { repo });
      setMsg(`Indexed: ${res.data.indexed} chunks, Updated: ${res.data.updated ?? 0}`);
    } catch (e: any) {
      setMsg("Index error: " + (e?.response?.data?.detail || e.message));
    } finally {
      setIndexing(false);
    }
  }

  async function ask() {
    setMsg(""); setAnswer(""); setCites([]);
    try {
      const res = await axios.post(`${backend}/ask`, { repo, question });
      setAnswer(res.data.answer);
      setCites(res.data.citations || []);
    } catch (e: any) {
      setMsg("Ask error: " + (e?.response?.data?.detail || e.message));
    }
  }

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: 16, fontFamily: "Inter, system-ui, Arial" }}>
      <h1>Developer Onboarding Helper</h1>
      <p style={{ opacity: 0.8 }}>Index a GitHub repo (incremental), then ask grounded questions with citations.</p>

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={repo}
          onChange={e => setRepo(e.target.value)}
          placeholder="owner/repo e.g. facebook/react"
          style={{ flex: 1, padding: 10, border: "1px solid #ccc", borderRadius: 6 }}
        />
        <input
          value={branch}
          onChange={e => setBranch(e.target.value)}
          placeholder="branch (e.g. main)"
          style={{ width: 140, padding: 10, border: "1px solid #ccc", borderRadius: 6 }}
          title="Branch for GitHub deep links"
        />
        <button onClick={doIndex} disabled={indexing} style={{ padding: "10px 16px" }}>
          {indexing ? "Indexing..." : "Index Repo"}
        </button>
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Ask about the repo..."
          style={{ flex: 1, padding: 10, border: "1px solid #ccc", borderRadius: 6 }}
        />
        <button onClick={ask} style={{ padding: "10px 16px" }}>Ask</button>
      </div>

      {msg && <div style={{ marginTop: 12, color: "#444" }}>{msg}</div>}

      {answer && (
        <>
          <h3 style={{ marginTop: 24 }}>Answer</h3>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f6f8fa", padding: 16, borderRadius: 6 }}>
            {answer}
          </pre>
        </>
      )}

      {cites.length > 0 && (
        <>
          <h4 style={{ marginTop: 16 }}>Citations</h4>
          <ul>
            {cites.map((c, i) => {
              const hasLines = typeof c.line_start === "number" && typeof c.line_end === "number";
              const lineAnchor = hasLines
                ? (c.line_start === c.line_end
                    ? `#L${c.line_start}`
                    : `#L${c.line_start}-L${c.line_end}`)
                : "";
              const href = `https://github.com/${repo}/blob/${branch}/${c.path}${lineAnchor}`;
              const copyText = hasLines
                ? `${repo}/${c.path}:${c.line_start}-${c.line_end}`
                : `${repo}/${c.path}`;
              return (
                <li key={i} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <a href={href} target="_blank" rel="noreferrer" title="Open on GitHub">
                    <code>{c.path}</code>
                  </a>
                  <span>• rank {c.rank} • score {c.score.toFixed(3)}</span>
                  {hasLines && <span>• lines {c.line_start}–{c.line_end}</span>}
                  <button
                    onClick={() => navigator.clipboard?.writeText(copyText)}
                    style={{ marginLeft: 6, padding: "2px 6px", border: "1px solid #ccc", borderRadius: 4, background: "#f8f8f8" }}
                    title="Copy path to clipboard"
                  >
                    Copy
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </main>
  );
}
