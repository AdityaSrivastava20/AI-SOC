import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [scans, setScans] = useState([]);
  const [stats, setStats] = useState({
    total_scans: 0,
    safe_urls: 0,
    suspicious_urls: 0,
    high_risk: 0,
  });

  const fetchData = async () => {
    try {
      const scansResponse = await fetch(`${API_URL}/scan/scans`);

      const statsResponse = await fetch(`${API_URL}/scan/stats`);

      const scansData = await scansResponse.json();
      const statsData = await statsResponse.json();

      setScans(scansData);
      setStats(statsData);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const scanUrl = async () => {
    if (!url.trim()) {
      alert("Please enter a URL");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/scan/url?url=${encodeURIComponent(url)}`,
        {
          method: "POST",
        },
      );

      const data = await response.json();

      setResult(data);
      setUrl("");

      fetchData();
    } catch (error) {
      console.error("Scan error:", error);
      alert("Unable to connect to AI-SOC backend");
    }
  };

  const getSeverityClass = (severity) => {
    if (severity === "HIGH") {
      return "severity-high";
    }

    if (severity === "MEDIUM") {
      return "severity-medium";
    }

    return "severity-low";
  };

  const getPredictionClass = (prediction) => {
    return prediction === 0 ? "prediction-safe" : "prediction-suspicious";
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div>
          <h1>AI-SOC</h1>
          <p>AI-Powered URL Threat Detection System</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>

      <main className="container">
        {/* Scan Section */}
        <section className="scan-section">
          <h2>🔍 Scan a URL</h2>

          <p className="section-description">
            Enter a URL to analyze its security risk using the AI threat
            detection model.
          </p>

          <div className="scan-box">
            <input
              type="text"
              placeholder="Enter URL, e.g. https://google.com"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  scanUrl();
                }
              }}
            />

            <button onClick={scanUrl}>Scan URL</button>
          </div>
        </section>

        {/* Scan Result */}
        {result && (
          <section className="result-section">
            <h2>🛡️ Scan Result</h2>

            <div className="result-card">
              <div className="result-url">
                <span>URL</span>
                <strong>{result.url}</strong>
              </div>

              <div className="result-grid">
                <div className="result-item risk-result">
                  <div className="risk-title">
                    <span>Risk Score</span>

                    <strong
                      className={
                        result.risk_score >= 80
                          ? "severity-high"
                          : result.risk_score >= 50
                            ? "severity-medium"
                            : "severity-low"
                      }
                    >
                      {result.risk_score}/100
                    </strong>
                  </div>

                  <div className="risk-bar">
                    <div
                      className={
                        result.risk_score >= 80
                          ? "risk-fill risk-fill-high"
                          : result.risk_score >= 50
                            ? "risk-fill risk-fill-medium"
                            : "risk-fill risk-fill-low"
                      }
                      style={{
                        width: `${result.risk_score}%`,
                      }}
                    ></div>
                  </div>
                </div>

                <div className="result-item">
                  <span>Severity</span>

                  <strong className={getSeverityClass(result.severity)}>
                    {result.severity}
                  </strong>
                </div>

                <div className="result-item">
                  <span>Confidence</span>

                  <strong>{result.confidence}%</strong>
                </div>

                <div className="result-item">
                  <span>Risk Score</span>

                  <strong
                    className={
                      result.risk_score >= 80
                        ? "severity-high"
                        : result.risk_score >= 50
                          ? "severity-medium"
                          : "severity-low"
                    }
                  >
                    {result.risk_score}/100
                  </strong>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Statistics */}
        <section className="stats-section">
          <div className="stat-card">
            <div className="stat-icon">📊</div>

            <h3>Total Scans</h3>

            <p>{stats.total_scans}</p>
          </div>

          <div className="stat-card safe-card">
            <div className="stat-icon">✓</div>

            <h3>Safe URLs</h3>

            <p>{stats.safe_urls}</p>
          </div>

          <div className="stat-card suspicious-card">
            <div className="stat-icon">⚠</div>

            <h3>Suspicious URLs</h3>

            <p>{stats.suspicious_urls}</p>
          </div>

          <div className="stat-card high-card">
            <div className="stat-icon">🚨</div>

            <h3>High Risk</h3>

            <p>{stats.high_risk}</p>
          </div>
        </section>

        {/* Scan History */}
        <section className="history-section">
          <div className="history-header">
            <div>
              <h2>📋 Scan History</h2>

              <p className="section-description">Previously analyzed URLs</p>
            </div>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>URL</th>
                  <th>Prediction</th>
                  <th>Severity</th>
                  <th>Risk Score</th>
                </tr>
              </thead>

              <tbody>
                {scans.map((scan) => (
                  <tr key={scan.id}>
                    <td>#{scan.id}</td>

                    <td className="url-cell">{scan.url}</td>

                    <td>
                      <span
                        className={
                          scan.prediction === 0
                            ? "badge safe-badge"
                            : "badge suspicious-badge"
                        }
                      >
                        {scan.prediction === 0 ? "✓ Safe" : "⚠ Suspicious"}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`badge ${getSeverityClass(scan.severity)}`}
                      >
                        {scan.severity}
                      </span>
                    </td>

                    <td>
                      <span
                        className={
                          scan.risk_score >= 80
                            ? "risk-high"
                            : scan.risk_score >= 50
                              ? "risk-medium"
                              : "risk-low"
                        }
                      >
                        {scan.risk_score}/100
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      <footer>AI-SOC • AI-Powered Security Operations Center</footer>
    </div>
  );
}

export default App;
