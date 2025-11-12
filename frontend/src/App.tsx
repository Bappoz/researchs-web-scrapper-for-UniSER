import React, { useState, useEffect } from "react";
import Dashboard from "./pages/Dashboard";
import ResearchersHistory from "./pages/ResearchersHistory";
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
      default:
        return <Dashboard />;
    }
  };

  return <div className='App'>{renderPage()}</div>;
}

export default App;
