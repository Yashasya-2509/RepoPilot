
import { useState } from "react";
import {
  Activity,
  Bot,
  Braces,
  FileCode2,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

type Result = Record<string, any>;

async function request(
  path: string,
  body?: Result,
  token = ""
): Promise<Result> {
  const response = await fetch(`/api${path}`, {
    method: body ? "POST" : "GET",
    headers: {
      ...(body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return data;
}

export default function App() {
  const [repository, setRepository] = useState("demo-repo");
  const [token, setToken] = useState("");
  const [query, setQuery] = useState("");
  const [bugReport, setBugReport] = useState("");

  const [inventory, setInventory] = useState<Result | null>(null);
  const [searchResults, setSearchResults] = useState<Result | null>(null);
  const [investigation, setInvestigation] = useState<Result | null>(null);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function runAction(action: () => Promise<void>) {
    setBusy(true);
    setError("");

    try {
      await action();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setBusy(false);
    }
  }

  const repo = { repository_name: repository };

  function inspectRepository() {
    return runAction(async () => {
      const data = await request(
        "/repositories/inspect",
        repo,
        token
      );
      setInventory(data);
    });
  }

  function searchCode() {
    return runAction(async () => {
      const data = await request(
        "/repositories/search",
        { ...repo, query, limit: 10 },
        token
      );
      setSearchResults(data);
    });
  }

  function investigateBug() {
    return runAction(async () => {
      const data = await request(
        "/investigations",
        { ...repo, bug_report: bugReport },
        token
      );
      setInvestigation(data);
    });
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Bot size={24} /></div>
          <div>
            <h2>RepoPilot</h2>
            <small>ENGINEERING AGENT</small>
          </div>
        </div>

        <p className="side-label">WORKSPACE</p>
        <div className="nav active"><Braces size={17} /> Repository lab</div>
        <div className="nav"><Activity size={17} /> Investigations</div>
        <div className="nav"><FileCode2 size={17} /> Patch review</div>

        <div className="security-note">
          <ShieldCheck size={20} />
          <div>
            <strong>Human in control</strong>
            <p>Review generated changes before applying them.</p>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <span className="eyebrow">SOFTWARE INTELLIGENCE</span>
            <h1>Repository lab</h1>
          </div>
          <span className="connection">● Local workspace</span>
        </header>

        <section className="hero">
          <span className="tag"><Sparkles size={14} /> EVIDENCE-DRIVEN DEBUGGING</span>
          <h2>Understand the bug.<br /><em>Prove the change.</em></h2>
          <p>
            Explore source code, find relevant lines, investigate reported
            problems, and prepare reviewable software changes.
          </p>
        </section>

        {error && <div className="error">{error}</div>}

        <section className="panel repository-panel">
          <div>
            <span className="eyebrow">01 / REPOSITORY</span>
            <h3>Connect a local workspace</h3>
          </div>

          <label>
            Repository folder name
            <input
              value={repository}
              onChange={(e) => setRepository(e.target.value)}
              placeholder="demo-repo"
            />
          </label>

          <label>
            API token (only if configured)
            <input
              type="password"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Optional bearer token"
            />
          </label>

          <button disabled={busy || !repository.trim()} onClick={inspectRepository}>
            {busy ? "Working..." : "Inspect repository"}
          </button>
        </section>

        <div className="section-title">
          <div>
            <span className="eyebrow">02 / DISCOVERY</span>
            <h3>Explore your codebase</h3>
          </div>
        </div>

        <section className="cards">
          <article className="panel">
            <div className="card-title">
              <FileCode2 />
              <div><h3>Repository inventory</h3><p>Files and languages</p></div>
            </div>

            {inventory ? (
              <>
                <div className="stat">
                  <strong>{inventory.file_count ?? inventory.files?.length ?? 0}</strong>
                  <span>Eligible files</span>
                </div>
                {Object.entries(inventory.languages ?? {}).map(([name, count]) => (
                  <div className="list-row" key={name}>
                    <span>{name}</span><b>{String(count)}</b>
                  </div>
                ))}
              </>
            ) : (
              <p className="muted">
                Inspect a repository to view its inventory.
              </p>
            )}
          </article>

          <article className="panel">
            <div className="card-title">
              <Search />
              <div><h3>Code search</h3><p>Find relevant source lines</p></div>
            </div>

            <form onSubmit={(e) => { e.preventDefault(); void searchCode(); }}>
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. calculate_total"
                required
              />
              <button disabled={busy}>Search code</button>
            </form>

            {searchResults?.results?.map((hit: Result, index: number) => (
              <div className="result" key={`${hit.path}-${hit.line_number}-${index}`}>
                <b>{hit.path}:{hit.line_number}</b>
                <code>{hit.line}</code>
              </div>
            ))}

            {searchResults && !searchResults.results?.length && (
              <p className="muted">No matching lines found.</p>
            )}
          </article>
        </section>

        <div className="section-title">
          <div>
            <span className="eyebrow">03 / INVESTIGATION</span>
            <h3>Investigate a bug</h3>
          </div>
        </div>

        <section className="panel">
          <label>
            Bug report
            <textarea
              rows={4}
              value={bugReport}
              onChange={(e) => setBugReport(e.target.value)}
              placeholder="Describe the observed problem, expected behavior, and steps to reproduce..."
            />
          </label>

          <button
            disabled={busy || bugReport.trim().length < 8}
            onClick={investigateBug}
          >
            <Bot size={16} /> Investigate with evidence
          </button>

          {investigation && (
            <div className="investigation">
              <span className="eyebrow">
                INVESTIGATION · {investigation.provider ?? "provider"}
              </span>
              <h3>{investigation.summary}</h3>

              <h4>Possible explanations</h4>
              <ul>
                {(investigation.hypotheses ?? []).map((item: string, i: number) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>

              <h4>Retrieved evidence</h4>
              {(investigation.evidence ?? []).map((item: Result, i: number) => (
                <div className="result" key={i}>
                  <b>{item.path}:{item.line_number}</b>
                  <code>{item.excerpt}</code>
                </div>
              ))}

              <p className="muted">
                {(investigation.limitations ?? []).join(" · ")}
              </p>
            </div>
          )}
        </section>

        <div className="section-title">
          <div>
            <span className="eyebrow">04 / PATCH REVIEW</span>
            <h3>Controlled changes</h3>
          </div>
        </div>

        <section className="panel">
          <div className="card-title">
            <ShieldCheck />
            <div>
              <h3>Patch review workflow</h3>
              <p>Human approval before changes are applied or tested.</p>
            </div>
          </div>
          <p className="muted">
            This starter dashboard does not generate or apply patches through
            this panel yet. Add the patch-generation, review-copy, and isolated
            test-runner endpoints to the backend before connecting those actions.
          </p>
        </section>

        <footer>RepoPilot · Local-first developer tooling</footer>
      </main>
    </div>
  );
}
