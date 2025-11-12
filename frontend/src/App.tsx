import React, { useState, useEffect } from "react";
import Dashboard from "./pages/Dashboard";
import ResearchersHistory from "./pages/ResearchersHistory";
import HelpPage from "./pages/HelpPage";
import { ThemeProvider } from "./context/ThemeContext";
import "./index.css";

function App() {
  // State to track the current route
  const [currentRoute, setCurrentRoute] = useState(
    window.location.hash.replace("#", "") || "/"
  );

  // Listen to hash changes
  useEffect(() => {
    const handleHashChange = () => {
      const newRoute = window.location.hash.replace("#", "") || "/";
      console.log("🔄 Route changed to:", newRoute);
      setCurrentRoute(newRoute);
    };

    // Add event listener
    window.addEventListener("hashchange", handleHashChange);

    // Cleanup
    return () => {
      window.removeEventListener("hashchange", handleHashChange);
    };
  }, []);

  const renderPage = () => {
    switch (currentRoute) {
      case "/history":
        return <ResearchersHistory />;
      case "/help":
        return <HelpPage />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <ThemeProvider>
      <div className='App'>{renderPage()}</div>
    </ThemeProvider>
  );
}

export default App;
