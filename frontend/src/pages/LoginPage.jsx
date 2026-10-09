import { useState } from "react";
import {
  AlertTriangle,
  Lock,
  Mail,
  ShieldCheck,
  User,
} from "lucide-react";
import apiClient from "../api/client";

function LoginPage({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (mode === "register") {
        await apiClient.post("/auth/register", {
          full_name: fullName,
          email,
          password,
        });

        setSuccess("Account created successfully. Please login now.");
        setMode("login");
        setPassword("");
        return;
      }

      const response = await apiClient.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      onLogin(response.data.user);
    } catch (err) {
      const backendMessage =
        err.response?.data?.detail || "Something went wrong. Please try again.";

      if (mode === "register") {
        setError(
          typeof backendMessage === "string"
            ? backendMessage
            : "Registration failed. Please check your details."
        );
      } else {
        setError("Login failed. Please check your email and password.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-visual">
        <div className="brand-mark">
          <ShieldCheck size={34} />
        </div>

        <div>
          <p className="eyebrow">AI Security Intelligence</p>
          <h1>AI Document Red Alert Detection System</h1>
          <p className="hero-copy">
            Scan uploaded documents, detect suspicious patterns, identify
            sensitive information, and generate risk intelligence instantly.
          </p>
        </div>

        <div className="risk-strip">
          <div>
            <span className="dot green"></span>
            Green
          </div>
          <div>
            <span className="dot yellow"></span>
            Yellow
          </div>
          <div>
            <span className="dot red"></span>
            Red Alert
          </div>
        </div>
      </section>

      <section className="login-panel">
        <div className="panel-header">
          <div className="panel-icon">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h2>{mode === "login" ? "Secure Login" : "Create Account"}</h2>
            <p>
              {mode === "login"
                ? "Enter your account credentials to continue."
                : "Register a new account to start scanning documents."}
            </p>
          </div>
        </div>

        <div className="auth-switch">
          <button
            type="button"
            className={mode === "login" ? "active" : ""}
            onClick={() => {
              setMode("login");
              setError("");
              setSuccess("");
            }}
          >
            Login
          </button>

          <button
            type="button"
            className={mode === "register" ? "active" : ""}
            onClick={() => {
              setMode("register");
              setError("");
              setSuccess("");
            }}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {mode === "register" && (
            <label>
              Full Name
              <div className="input-box">
                <User size={18} />
                <input
                  type="text"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  placeholder="Enter full name"
                  required
                />
              </div>
            </label>
          )}

          <label>
            Email Address
            <div className="input-box">
              <Mail size={18} />
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="user@example.com"
                required
              />
            </div>
          </label>

          <label>
            Password
            <div className="input-box">
              <Lock size={18} />
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter password"
                required
              />
            </div>
          </label>

          {error && <p className="error-message">{error}</p>}
          {success && <p className="success-message">{success}</p>}

          <button type="submit" disabled={loading}>
            {loading
              ? mode === "login"
                ? "Checking..."
                : "Creating..."
              : mode === "login"
                ? "Login"
                : "Register"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;