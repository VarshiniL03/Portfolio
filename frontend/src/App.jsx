import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AdminLogin from "./pages/admin/Login";
import AdminDashboard from "./pages/admin/Dashboard";
import AdminExperiences from "./pages/admin/Experiences";
import AdminProjects from "./pages/admin/Projects";
import AdminEducation from "./pages/admin/Education";
import AdminAchievements from "./pages/admin/Achievements";
import AdminSiteContent from "./pages/admin/SiteContentEditor";
import AdminResume from "./pages/admin/ResumeManager";
import AdminFaqs from "./pages/admin/Faqs";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/admin/login" element={<AdminLogin />} />
      <Route
        path="/admin"
        element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/experiences"
        element={
          <ProtectedRoute>
            <AdminExperiences />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/projects"
        element={
          <ProtectedRoute>
            <AdminProjects />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/education"
        element={
          <ProtectedRoute>
            <AdminEducation />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/achievements"
        element={
          <ProtectedRoute>
            <AdminAchievements />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/site-content"
        element={
          <ProtectedRoute>
            <AdminSiteContent />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/resume"
        element={
          <ProtectedRoute>
            <AdminResume />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/faqs"
        element={
          <ProtectedRoute>
            <AdminFaqs />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<div className="p-10 text-center">Page not found</div>} />
    </Routes>
  );
}
