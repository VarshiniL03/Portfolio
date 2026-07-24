import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Experience from "../components/Experience";
import Projects from "../components/Projects";
import Education from "../components/Education";
import Achievements from "../components/Achievements";
import ResumeSection from "../components/ResumeSection";
import Contact from "../components/Contact";
import Footer from "../components/Footer";
import ChatbotWidget from "../components/ChatbotWidget";
import SectionDivider from "../components/SectionDivider";
import {
  getSiteContent,
  listExperiences,
  listProjects,
  listEducation,
  listAchievements,
  getActiveResume,
} from "../api/resources";

export default function Home() {
  const [content, setContent] = useState(null);
  const [experiences, setExperiences] = useState([]);
  const [projects, setProjects] = useState([]);
  const [education, setEducation] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      getSiteContent(),
      listExperiences(),
      listProjects(),
      listEducation(),
      listAchievements(),
      getActiveResume(),
    ]).then(([site, exp, proj, edu, ach, res]) => {
      if (site.status === "fulfilled") setContent(site.value.data);
      if (exp.status === "fulfilled") setExperiences(exp.value.data);
      if (proj.status === "fulfilled") setProjects(proj.value.data);
      if (edu.status === "fulfilled") setEducation(edu.value.data);
      if (ach.status === "fulfilled") setAchievements(ach.value.data);
      if (res.status === "fulfilled") setResume(res.value.data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading…</div>;
  }

  
  return (
    <div>
        <Navbar />
        <Hero content={content} />
        <Experience items={experiences} />
        <SectionDivider />
        <Projects items={projects} />
        <SectionDivider />
        <Education items={education} />
        <SectionDivider />
        <Achievements items={achievements} />
        <SectionDivider />
        <ResumeSection resume={resume} />
        <SectionDivider />
        <Contact content={content} />
        <Footer />
        <ChatbotWidget />
      </div>
  );
}