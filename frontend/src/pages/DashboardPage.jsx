import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  FileSearch,
  Loader2,
  LogOut,
  ShieldCheck,
  Upload,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import apiClient from "../api/client";

function StatCard({ icon: Icon, label, value, tone }) {
  return (
    <article className={`stat-card ${tone}`}>
      <div className="stat-icon">
        <Icon size={22} />
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
      </div>
    </article>
  );
}

function getAlertTone(alertLevel) {
  if (alertLevel === "Red") return "red";
  if (alertLevel === "Yellow") return "yellow";
  return "green";
}

function getTopHighlights(analysis) {
  if (!analysis?.document_heatmap?.highlights) {
    return [];
  }

  return analysis.document_heatmap.highlights.slice(0, 6);
}

function getDocumentAlertLevel(document) {
  return document.alert_level || document.risk_analysis?.alert_level || "Green";
}

function getDocumentRiskScore(document) {
  return document.risk_score ?? document.risk_analysis?.risk_score ?? 0;
}

function DashboardPage({ user, onLogout }) {
  const [activeView, setActiveView] = useState("dashboard");
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [adminDocuments, setAdminDocuments] = useState([]);
  const [adminError, setAdminError] = useState("");

  async function loadHistory() {
    try {
      const response = await apiClient.get("/documents/history?limit=10");
      setHistory(response.data.documents || []);
    } catch (err) {
      console.error("Failed to load document history", err);
    }
  }

  async function loadAdminDocuments() {
    setAdminError("");

    try {
      const response = await apiClient.get("/admin/documents?limit=50");
      setAdminDocuments(response.data.documents || []);
    } catch (err) {
      setAdminDocuments([]);
      setAdminError("Admin access denied or admin documents could not be loaded.");
      console.error("Failed to load admin documents", err);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function handleUpload(event) {
    event.preventDefault();

    if (!selectedFile) {
      setError("Please select a document first.");
      return;
    }

    setError("");
    setUploading(true);
    setAnalysis(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await apiClient.post("/documents/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setAnalysis(response.data);
      loadHistory();
    } catch (err) {
      setError("Upload failed. Please login again or check backend server.");
    } finally {
      setUploading(false);
    }
  }

  const alertLevel = analysis?.risk_analysis?.alert_level || "Green";
  const riskScore = analysis?.risk_analysis?.risk_score ?? 0;
  const trustScore = analysis?.risk_analysis?.trust_score ?? 100;
  const alertTone = getAlertTone(alertLevel);

  const evidenceChartData =
    analysis?.risk_report?.evidence?.map((item) => ({
      name: item.category,
      count: item.count,
    })) || [];

  const alertPieData = [
    { name: "Risk Score", value: riskScore, color: "#dc2626" },
    { name: "Trust Score", value: trustScore, color: "#16a34a" },
  ];

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <ShieldCheck size={30} />
          <div>
            <strong>Red Alert AI</strong>
            <span>Document Risk Intelligence</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button
            className={activeView === "dashboard" ? "active" : ""}
            onClick={() => setActiveView("dashboard")}
          >
            <Activity size={18} />
            Dashboard
          </button>

          <button
            className={activeView === "dashboard" ? "active" : ""}
            onClick={() => setActiveView("dashboard")}
          >
            <Upload size={18} />
            Upload
          </button>

          <button
            className={activeView === "history" ? "active" : ""}
            onClick={() => {
              setActiveView("history");
              loadHistory();
            }}
          >
            <FileSearch size={18} />
            History
          </button>

          <button
            className={activeView === "admin" ? "active" : ""}
            onClick={() => {
              setActiveView("admin");
              loadAdminDocuments();
            }}
          >
            <ShieldCheck size={18} />
            Admin
          </button>
        </nav>
      </aside>

      <section className="main-area">
        <header className="topbar">
          <div>
            <p className="eyebrow-dark">Security Console</p>
            <h1>Document Risk Dashboard</h1>
          </div>

          <div className="user-box">
            <span>{user.email}</span>
            <button onClick={onLogout}>
              <LogOut size={17} />
              Logout
            </button>
          </div>
        </header>

        <section className="stats-grid">
          <StatCard
            icon={FileSearch}
            label="Current Risk Score"
            value={riskScore}
            tone={alertTone}
          />

          <StatCard
            icon={ShieldCheck}
            label="Trust Score"
            value={trustScore}
            tone="green"
          />

          <StatCard
            icon={AlertTriangle}
            label="Alert Level"
            value={alertLevel}
            tone={alertTone}
          />

          <StatCard
            icon={Activity}
            label="Highlights"
            value={analysis?.document_heatmap?.total_highlights || 0}
            tone="blue"
          />
        </section>

        {activeView === "dashboard" && (
          <section className="content-grid">
            <article className="upload-panel">
              <div>
                <p className="eyebrow-dark">AI Scanner</p>
                <h2>Upload Document For Risk Analysis</h2>
                <p>
                  Upload PDF, DOCX, TXT, PNG, JPG, or JPEG files. The system
                  will extract text, detect threats, and generate a red alert
                  report.
                </p>
              </div>

              <form className="upload-form" onSubmit={handleUpload}>
                <label className="drop-zone">
                  <Upload size={34} />
                  <strong>
                    {selectedFile ? selectedFile.name : "Choose a document"}
                  </strong>
                  <span>Click here to select a file from your computer.</span>

                  <input
                    type="file"
                    accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
                    onChange={(event) => setSelectedFile(event.target.files[0])}
                  />
                </label>

                {error && <p className="error-message">{error}</p>}

                <button
                  className="primary-action"
                  type="submit"
                  disabled={uploading}
                >
                  {uploading ? (
                    <>
                      <Loader2 className="spin" size={18} />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Upload size={18} />
                      Analyze Document
                    </>
                  )}
                </button>
              </form>
            </article>

            <article className={`result-panel ${alertTone}`}>
              <div className="result-header">
                <div>
                  <p className="eyebrow-dark">AI Result</p>
                  <h2>
                    {analysis
                      ? analysis.risk_report.title
                      : "No Document Scanned"}
                  </h2>
                  <p>
                    {analysis
                      ? analysis.risk_report.overview
                      : "Upload a document to see the risk score, alert level, and findings."}
                  </p>
                </div>

                {analysis && (
                  <span className={`alert-badge ${alertTone}`}>
                    {analysis.risk_analysis.alert_level}
                  </span>
                )}
              </div>

              {analysis && (
                <div className="result-stack">
                  <div className="risk-meter">
                    <span>Risk Score</span>
                    <strong>{analysis.risk_analysis.risk_score}/100</strong>
                  </div>

                  <div className="summary-box">
                    <strong>AI Summary</strong>
                    <p>{analysis.summary.summary_text}</p>
                  </div>

                  <div className="recommendation-box">
                    <strong>Recommendation</strong>
                    <p>{analysis.risk_report.recommendation}</p>
                  </div>

                  <div className="mini-section">
                    <h3>Risk Evidence</h3>
                    <div className="finding-list">
                      {analysis.risk_report.evidence.map((item) => (
                        <div key={item.category} className="finding-item">
                          <span>{item.category}</span>
                          <strong>{item.count}</strong>
                          <small>{item.explanation}</small>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mini-section">
                    <h3>Highlighted Suspicious Sections</h3>
                    <div className="highlight-list">
                      {getTopHighlights(analysis).map((item, index) => (
                        <div
                          key={`${item.category}-${index}`}
                          className={`highlight-item ${item.color}`}
                        >
                          <span>{item.category}</span>
                          <strong>{item.label}</strong>
                          <small>
                            Severity: {item.severity} | Risk points:{" "}
                            {item.risk_points}
                          </small>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mini-section">
                    <h3>Risk Factors</h3>
                    <div className="factor-list">
                      {analysis.risk_analysis.risk_factors.map((factor) => (
                        <span key={factor}>{factor}</span>
                      ))}
                    </div>
                  </div>

                  {analysis.tampering_analysis?.tampering_suspicions_found >
                    0 && (
                    <div className="mini-section">
                      <h3>Tampering Suspicion</h3>
                      <div className="highlight-list">
                        {analysis.tampering_analysis.findings.map((item) => (
                          <div key={item.type} className="highlight-item red">
                            <span>{item.type}</span>
                            <strong>{item.description}</strong>
                            <small>Risk points: {item.risk_points}</small>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </article>

            <article className="analytics-panel">
              <div>
                <p className="eyebrow-dark">Analytics</p>
                <h2>Risk Breakdown</h2>
              </div>

              {analysis ? (
                <div className="chart-grid">
                  <div className="chart-card">
                    <h3>Evidence Count</h3>
                    <ResponsiveContainer width="100%" height={260}>
                      <BarChart data={evidenceChartData}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Bar
                          dataKey="count"
                          radius={[6, 6, 0, 0]}
                          fill="#dc2626"
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="chart-card">
                    <h3>Risk vs Trust</h3>
                    <ResponsiveContainer width="100%" height={260}>
                      <PieChart>
                        <Pie
                          data={alertPieData}
                          dataKey="value"
                          nameKey="name"
                          innerRadius={58}
                          outerRadius={92}
                          paddingAngle={4}
                        >
                          {alertPieData.map((entry) => (
                            <Cell key={entry.name} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              ) : (
                <p className="empty-text">
                  Upload a document to generate analytics.
                </p>
              )}
            </article>

            <HistoryPanel history={history} />
          </section>
        )}

        {activeView === "history" && (
          <section className="content-grid">
            <HistoryPanel history={history} />
          </section>
        )}

        {activeView === "admin" && (
          <section className="content-grid">
            <article className="admin-panel">
              <div>
                <p className="eyebrow-dark">Admin</p>
                <h2>All Uploaded Documents</h2>
              </div>

              {adminError && <p className="error-message">{adminError}</p>}

              <div className="admin-table">
                <div className="admin-row admin-head">
                  <span>Filename</span>
                  <span>User</span>
                  <span>Alert</span>
                  <span>Risk</span>
                </div>

                {adminDocuments.length === 0 ? (
                  <p className="empty-text">No admin documents loaded.</p>
                ) : (
                  adminDocuments.map((document) => {
                    const documentAlertLevel = getDocumentAlertLevel(document);
                    const documentRiskScore = getDocumentRiskScore(document);

                    return (
                      <div key={document.document_id} className="admin-row">
                        <span>{document.filename}</span>
                        <span>{document.uploaded_by_email || "Unknown"}</span>
                        <span
                          className={`history-badge ${documentAlertLevel.toLowerCase()}`}
                        >
                          {documentAlertLevel}
                        </span>
                        <span>{documentRiskScore}</span>
                      </div>
                    );
                  })
                )}
              </div>
            </article>
          </section>
        )}
      </section>
    </main>
  );
}

function HistoryPanel({ history }) {
  return (
    <article className="history-panel">
      <div>
        <p className="eyebrow-dark">History</p>
        <h2>Recent Documents</h2>
      </div>

      <div className="history-list">
        {history.length === 0 ? (
          <p className="empty-text">No uploaded documents found.</p>
        ) : (
          history.map((document) => {
            const documentAlertLevel = getDocumentAlertLevel(document);

            return (
              <div key={document.document_id} className="history-item">
                <div>
                  <strong>{document.filename}</strong>
                  <span>{document.uploaded_by_email || "Current user"}</span>
                </div>

                <span
                  className={`history-badge ${documentAlertLevel.toLowerCase()}`}
                >
                  {documentAlertLevel}
                </span>
              </div>
            );
          })
        )}
      </div>
    </article>
  );
}

export default DashboardPage;