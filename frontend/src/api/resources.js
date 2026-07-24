import { api } from "./client";

// --- Auth ---
export const login = (email, password) => api.post("/auth/login", { email, password });
export const getMe = () => api.get("/auth/me");

// --- Site content ---
export const getSiteContent = () => api.get("/site-content");
export const updateSiteContent = (data) => api.put("/site-content", data);

// --- Experiences ---
export const listExperiences = (includeHidden = false) =>
  api.get(`/experiences?include_hidden=${includeHidden}`);
export const createExperience = (data) => api.post("/experiences", data);
export const updateExperience = (id, data) => api.put(`/experiences/${id}`, data);
export const deleteExperience = (id) => api.delete(`/experiences/${id}`);

// --- Projects ---
export const listProjects = (includeHidden = false) =>
  api.get(`/projects?include_hidden=${includeHidden}`);
export const createProject = (data) => api.post("/projects", data);
export const updateProject = (id, data) => api.put(`/projects/${id}`, data);
export const deleteProject = (id) => api.delete(`/projects/${id}`);

// --- Education ---
export const listEducation = (includeHidden = false) =>
  api.get(`/education?include_hidden=${includeHidden}`);
export const createEducation = (data) => api.post("/education", data);
export const updateEducation = (id, data) => api.put(`/education/${id}`, data);
export const deleteEducation = (id) => api.delete(`/education/${id}`);

// --- Achievements ---
export const listAchievements = (includeHidden = false) =>
  api.get(`/achievements?include_hidden=${includeHidden}`);
export const createAchievement = (data) => api.post("/achievements", data);
export const updateAchievement = (id, data) => api.put(`/achievements/${id}`, data);
export const deleteAchievement = (id) => api.delete(`/achievements/${id}`);

// --- Resume ---
export const getActiveResume = () => api.get("/resume/active");
export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/resume/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

// --- Chatbot ---
export const sendChatMessage = (sessionId, message) =>
  api.post("/chatbot/message", { session_id: sessionId, message });

// --- FAQs (admin) ---
export const listFaqs = () => api.get("/faqs");
export const createFaq = (data) => api.post("/faqs", data);
export const updateFaq = (id, data) => api.put(`/faqs/${id}`, data);
export const deleteFaq = (id) => api.delete(`/faqs/${id}`);
export const triggerReindex = () => api.post("/admin/reindex");