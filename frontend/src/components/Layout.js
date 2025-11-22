import { Link, NavLink, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Layout.css";

const Layout = ({ children }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="layout">
      {/* Ocean Animated Background */}
      <div className="ocean-background"></div>
      {/* Content Overlay for Readability */}
      <div className="content-overlay"></div>

      <nav className="navbar">
        <div className="nav-content">
          <Link to="/" className="nav-brand">
            <div className="nav-brand-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" />
                <path
                  d="M2 17L12 22L22 17"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                />
                <path
                  d="M2 12L12 17L22 12"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                />
              </svg>
            </div>
            <span className="nav-brand-text">
              <span className="nav-brand-text-main">OCEAN</span>
              <span className="nav-brand-text-accent">AI</span>
            </span>
          </Link>
          {isAuthenticated && (
            <div className="nav-links">
              <NavLink
                to="/dashboard"
                end
                className={({ isActive }) => {
                  const isDashboardActive =
                    isActive || location.pathname === "/";
                  return isDashboardActive ? "nav-link active" : "nav-link";
                }}
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/projects/new"
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                New Project
              </NavLink>
              <button onClick={handleLogout} className="nav-logout">
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>
      <main className="main-content">{children}</main>
    </div>
  );
};

export default Layout;
