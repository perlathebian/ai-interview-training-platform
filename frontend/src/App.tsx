import { BrowserRouter, Routes, Route } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import ResumePage from "./pages/ResumePage";
import NewTrainingTargetPage from "./pages/NewTrainingTargetPage";
import TrainingTargetsPage from "./pages/TrainingTargetsPage";
import NewInterviewPage from "./pages/NewInterviewPage";
import InterviewPage from "./pages/InterviewPage";
import InterviewHistoryPage from "./pages/InterviewHistoryPage";
import InterviewReportPage from "./pages/InterviewReportPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/resume"
          element={
            <ProtectedRoute>
              <ResumePage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/training-targets"
          element={
            <ProtectedRoute>
              <TrainingTargetsPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/training-targets/new"
          element={
            <ProtectedRoute>
              <NewTrainingTargetPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/interviews/new"
          element={
            <ProtectedRoute>
              <NewInterviewPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/interviews/:id"
          element={
            <ProtectedRoute>
              <InterviewPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/interviews/history"
          element={
            <ProtectedRoute>
              <InterviewHistoryPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/interviews/:id/report"
          element={
            <ProtectedRoute>
              <InterviewReportPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
