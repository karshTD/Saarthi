"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  ClassInfo,
  NGO_CLASSES,
  NGO_RESOURCES,
  NGO_SESSIONS,
  NGO_STUDENTS,
  ResourceItem,
  SessionRecord,
  StudentRecord,
} from "../../lib/ngoData";
import styles from "./dashboard.module.css";

const DEMO_SESSION_ID = 1;

const levelKey: Record<string, string> = {
  struggling: "Struggling",
  on_track: "On Track",
  advanced: "Advanced",
  unassessed: "Unassessed",
};

const dotClass: Record<string, string> = {
  struggling: styles.dotStruggling,
  on_track: styles.dotOnTrack,
  advanced: styles.dotAdvanced,
};

const tagClass: Record<string, string> = {
  struggling: styles.tagStruggling,
  on_track: styles.tagOnTrack,
  advanced: styles.tagAdvanced,
};

const pillClass: Record<string, string> = {
  struggling: styles.levelStruggling,
  on_track: styles.levelOnTrack,
  advanced: styles.levelAdvanced,
};

export type NavTab = "dashboard" | "classes" | "planner" | "students" | "resources";

interface Activity {
  level: string;
  title: string;
  prompt: string;
  generated_by?: string;
}

interface SessionInfo {
  topic: string;
  subject: string;
  duration_minutes: number;
}

export function DashboardView({ initialTab = "dashboard" }: { initialTab?: NavTab }) {
  const [activeTab, setActiveTab] = useState<NavTab>(initialTab);
  const [connected, setConnected] = useState(false);

  // Dashboard Overview state
  const [session, setSession] = useState<SessionInfo | null>(null);
  const [recommendation, setRecommendation] = useState(
    "3 students are ready to move from like to unlike fraction addition. 3 students need another visual-first pass on the core concept before advancing."
  );
  const [recoGeneratedBy, setRecoGeneratedBy] = useState<string | null>(null);
  const [loadingReco, setLoadingReco] = useState(false);

  const [activities, setActivities] = useState<Activity[]>([]);
  const [lessonGeneratedBy, setLessonGeneratedBy] = useState<string | null>(null);
  const [loadingLesson, setLoadingLesson] = useState(false);

  // Planner state
  const [selectedSessionCode, setSelectedSessionCode] = useState<string>("G5A-003");
  const selectedSession: SessionRecord =
    NGO_SESSIONS.find((s) => s.code === selectedSessionCode) || NGO_SESSIONS[2];

  // Students Progress state
  const [searchQuery, setSearchQuery] = useState("");
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const [selectedStudent, setSelectedStudent] = useState<StudentRecord | null>(null);

  // Resources state
  const [resourceCategory, setResourceCategory] = useState<string>("all");

  // Read URL query param on mount and sync tab
  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const tabParam = params.get("tab") as NavTab | null;
      if (tabParam && ["dashboard", "classes", "planner", "students", "resources"].includes(tabParam)) {
        setActiveTab(tabParam);
      }
    }
  }, []);

  const handleTabChange = (tab: NavTab) => {
    setActiveTab(tab);
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("tab", tab);
      window.history.pushState({}, "", url.toString());
    }
  };

  useEffect(() => {
    apiFetch("/api/classes/1/analysis")
      .then((res) => {
        if (!res.ok) throw new Error("not ok");
        return res.json();
      })
      .then(() => {
        setConnected(true);
      })
      .catch(() => setConnected(false));

    apiFetch(`/api/sessions/${DEMO_SESSION_ID}`)
      .then((res) => {
        if (!res.ok) throw new Error("not ok");
        return res.json();
      })
      .then((data) =>
        setSession({ topic: data.topic, subject: data.subject, duration_minutes: data.duration_minutes })
      )
      .catch(() => {});
  }, []);

  async function handleGenerateRecommendation() {
    setLoadingReco(true);
    try {
      const res = await apiFetch(`/api/sessions/${DEMO_SESSION_ID}/recommendation`, { method: "POST" });
      if (!res.ok) throw new Error("not ok");
      const data = await res.json();
      setRecommendation(data.recommendation);
      setRecoGeneratedBy(data.generated_by);
      setConnected(true);
    } catch {
      setRecoGeneratedBy("unavailable");
    } finally {
      setLoadingReco(false);
    }
  }

  async function handleGenerateLesson() {
    setLoadingLesson(true);
    try {
      const res = await apiFetch(`/api/sessions/${DEMO_SESSION_ID}/generate-lesson`, { method: "POST" });
      if (!res.ok) throw new Error("not ok");
      const data = await res.json();
      setActivities(data.activities.map((a: any) => a.content ?? a));
      setLessonGeneratedBy(data.generated_by);
      setConnected(true);
    } catch {
      setLessonGeneratedBy("unavailable");
    } finally {
      setLoadingLesson(false);
    }
  }

  // Filter students based on search and level
  const filteredStudents = NGO_STUDENTS.filter((st) => {
    const matchesLevel = levelFilter === "all" || st.level === levelFilter;
    const matchesQuery =
      st.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      st.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      st.teacher_notes.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesLevel && matchesQuery;
  });

  // Filter resources based on category
  const filteredResources = NGO_RESOURCES.filter((res) => {
    return resourceCategory === "all" || res.category === resourceCategory;
  });

  return (
    <div className={styles.page}>
      <aside className={styles.sidebar}>
        <Link href="/" style={{ textDecoration: "none", color: "inherit" }}>
          <div className={styles.logo}>
            saa<span>rthi</span>
          </div>
        </Link>
        <div className={styles.tagline}>AI Volunteer Copilot</div>

        <button
          className={`${styles.navItem} ${activeTab === "dashboard" ? styles.navItemActive : ""}`}
          onClick={() => handleTabChange("dashboard")}
        >
          <span>📊</span> Dashboard
        </button>
        <button
          className={`${styles.navItem} ${activeTab === "classes" ? styles.navItemActive : ""}`}
          onClick={() => handleTabChange("classes")}
        >
          <span>🏫</span> My Classes
        </button>
        <button
          className={`${styles.navItem} ${activeTab === "planner" ? styles.navItemActive : ""}`}
          onClick={() => handleTabChange("planner")}
        >
          <span>🗓️</span> Session Planner
        </button>
        <button
          className={`${styles.navItem} ${activeTab === "students" ? styles.navItemActive : ""}`}
          onClick={() => handleTabChange("students")}
        >
          <span>👥</span> Student Progress
        </button>
        <button
          className={`${styles.navItem} ${activeTab === "resources" ? styles.navItemActive : ""}`}
          onClick={() => handleTabChange("resources")}
        >
          <span>📚</span> Resources
        </button>
      </aside>

      <main className={styles.main}>
        {/* Mobile horizontal tab bar */}
        <div className={styles.mobileNav}>
          <button
            className={`${styles.mobileNavBtn} ${activeTab === "dashboard" ? styles.mobileNavBtnActive : ""}`}
            onClick={() => handleTabChange("dashboard")}
          >
            Dashboard
          </button>
          <button
            className={`${styles.mobileNavBtn} ${activeTab === "classes" ? styles.mobileNavBtnActive : ""}`}
            onClick={() => handleTabChange("classes")}
          >
            My Classes
          </button>
          <button
            className={`${styles.mobileNavBtn} ${activeTab === "planner" ? styles.mobileNavBtnActive : ""}`}
            onClick={() => handleTabChange("planner")}
          >
            Session Planner
          </button>
          <button
            className={`${styles.mobileNavBtn} ${activeTab === "students" ? styles.mobileNavBtnActive : ""}`}
            onClick={() => handleTabChange("students")}
          >
            Student Progress
          </button>
          <button
            className={`${styles.mobileNavBtn} ${activeTab === "resources" ? styles.mobileNavBtnActive : ""}`}
            onClick={() => handleTabChange("resources")}
          >
            Resources
          </button>
        </div>

        {/* Global Topbar */}
        <div className={styles.topbar}>
          <div>
            <h1 className={styles.greetingH1}>Grade 5 — Section A</h1>
            <p className={styles.greetingP}>
              Mathematics · Fractions · 10 students
              {connected && <span style={{ color: "#4FBFA8", fontWeight: 700 }}> · live backend</span>}
            </p>
          </div>
          <div className={styles.avatar} title="Demo Volunteer (demo@saarthi.dev)">
            U
          </div>
        </div>

        {/* ========================================================================= */}
        {/* TAB 1: DASHBOARD OVERVIEW */}
        {/* ========================================================================= */}
        {activeTab === "dashboard" && (
          <div>
            <div className={styles.gridTop}>
              <div className={styles.card}>
                <div className={styles.cardLabel}>Today&apos;s Session</div>
                <div className={styles.sessionTopic}>{session?.topic ?? "Adding Like Fractions"}</div>
                <div className={styles.sessionMeta}>
                  {session?.duration_minutes ?? 45} min · Differentiated across 3 levels
                </div>
                <span className={styles.badgeProgress}>
                  {activities.length > 0 ? "Lesson generated" : "Lesson plan ready"}
                </span>
                <div className={styles.progressBar}>
                  <div className={styles.progressBarFill} />
                </div>
                <button
                  className={styles.secondaryBtn}
                  onClick={handleGenerateLesson}
                  disabled={loadingLesson}
                >
                  {loadingLesson ? "Generating…" : "Generate lesson"}
                </button>
                {lessonGeneratedBy && lessonGeneratedBy !== "unavailable" && (
                  <span className={styles.genBadge}>generated by: {lessonGeneratedBy}</span>
                )}
                {lessonGeneratedBy === "unavailable" && (
                  <span className={styles.genBadge}>backend unreachable</span>
                )}
              </div>

              <div className={styles.card}>
                <div className={styles.cardLabel}>Avg. Score</div>
                <div className={`${styles.statNum} ${styles.statMarigold}`}>78%</div>
                <div className={styles.statLabel}>Across 5 completed sessions</div>
              </div>

              <div className={styles.card}>
                <div className={styles.cardLabel}>Sessions Logged</div>
                <div className={`${styles.statNum} ${styles.statMint}`}>5 / 8</div>
                <div className={styles.statLabel}>62% of term completed</div>
              </div>
            </div>

            {activities.length > 0 && (
              <>
                <div className={styles.sectionTitle}>Differentiated Activities</div>
                <div className={styles.activitiesGrid} style={{ marginBottom: 18 }}>
                  {activities.map((a) => (
                    <div key={a.level} className={styles.activityCard}>
                      <span className={`${styles.tag} ${tagClass[a.level] || ""}`}>
                        {levelKey[a.level] || a.level}
                      </span>
                      <div className={styles.sessionTopic} style={{ fontSize: 14, marginTop: 8 }}>
                        {a.title}
                      </div>
                      <div className={styles.activityPrompt}>{a.prompt}</div>
                    </div>
                  ))}
                </div>
              </>
            )}

            <div className={styles.card} style={{ marginBottom: 18 }}>
              <div className={styles.cardLabel}>Class Level Breakdown</div>
              <div className={styles.levelsRow}>
                <div className={`${styles.levelPill} ${pillClass["struggling"]}`}>
                  <span className={styles.n}>3</span>
                  Struggling
                </div>
                <div className={`${styles.levelPill} ${pillClass["on_track"]}`}>
                  <span className={styles.n}>4</span>
                  On Track
                </div>
                <div className={`${styles.levelPill} ${pillClass["advanced"]}`}>
                  <span className={styles.n}>3</span>
                  Advanced
                </div>
              </div>
            </div>

            <div className={styles.gridBottom}>
              <div className={styles.card}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                  <div className={styles.cardLabel} style={{ margin: 0 }}>
                    Student Progress
                  </div>
                  <button
                    className={styles.actionBtnOutline}
                    onClick={() => handleTabChange("students")}
                  >
                    View All 10 Students →
                  </button>
                </div>
                <div className={styles.tableScroll}>
                  <table className={styles.table}>
                    <thead>
                      <tr>
                        <th>Student</th>
                        <th>Level</th>
                        <th>Avg Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {NGO_STUDENTS.slice(0, 6).map((s) => (
                        <tr key={s.student_id}>
                          <td>
                            <div className={styles.studentName}>
                              <span className={`${styles.dot} ${dotClass[s.level] || ""}`} />
                              {s.name} ({s.code})
                            </div>
                          </td>
                          <td>
                            <span className={`${styles.tag} ${tagClass[s.level] || ""}`}>
                              {levelKey[s.level] || s.level}
                            </span>
                          </td>
                          <td>{Math.round(s.avg_score * 100)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className={styles.reco}>
                <h3>Next Session Recommendation</h3>
                <p>{recommendation}</p>
                <button
                  className={styles.chip}
                  onClick={handleGenerateRecommendation}
                  disabled={loadingReco}
                >
                  {loadingReco ? "Generating…" : "Generate recommendation"}
                </button>
                {recoGeneratedBy && recoGeneratedBy !== "unavailable" && (
                  <span style={{ fontSize: 10, opacity: 0.8, marginLeft: 8 }}>
                    generated by: {recoGeneratedBy}
                  </span>
                )}
                {recoGeneratedBy === "unavailable" && (
                  <span style={{ fontSize: 10, opacity: 0.8, marginLeft: 8 }}>
                    backend unreachable — showing cached text
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: MY CLASSES */}
        {/* ========================================================================= */}
        {activeTab === "classes" && (
          <div>
            <div className={styles.viewHeader}>
              <h2 className={styles.viewTitle}>My Classes</h2>
              <div className={styles.viewSubtitle}>
                Assigned NGO Learning Centres &amp; Student Cohorts · A Ray of Hope Charitable Trust
              </div>
            </div>

            <div className={styles.classGrid}>
              {NGO_CLASSES.map((cls) => {
                const isActive = cls.code === "G5A";
                return (
                  <div
                    key={cls.id}
                    className={`${styles.classCard} ${isActive ? styles.classCardActive : ""}`}
                  >
                    <div className={styles.classHeader}>
                      <div>
                        <h3 className={styles.classTitle}>{cls.name}</h3>
                        <span className={styles.classCodeBadge}>{cls.code}</span>
                      </div>
                      <span
                        className={styles.tag}
                        style={{
                          background: isActive ? "#E4F6F1" : "#F0EDF9",
                          color: isActive ? "#4FBFA8" : "#6B6685",
                        }}
                      >
                        {cls.status}
                      </span>
                    </div>

                    <div className={styles.classMetaRow}>
                      <span>📍 {cls.location}</span>
                      <span>👤 {cls.volunteer_name}</span>
                      <span>⏰ {cls.schedule}</span>
                    </div>

                    <div className={styles.classStatsGrid}>
                      <div className={styles.classStatItem}>
                        <div className={styles.classStatVal}>{cls.student_count}</div>
                        <div className={styles.classStatLbl}>Enrolled</div>
                      </div>
                      <div className={styles.classStatItem}>
                        <div className={styles.classStatVal} style={{ color: "#4FBFA8" }}>
                          {cls.attendance_rate}%
                        </div>
                        <div className={styles.classStatLbl}>Attendance</div>
                      </div>
                      <div className={styles.classStatItem}>
                        <div className={styles.classStatVal} style={{ color: "#6C7FD8" }}>
                          {cls.grade}
                        </div>
                        <div className={styles.classStatLbl}>Level</div>
                      </div>
                    </div>

                    <div style={{ fontSize: 12.5, color: "#6B6685", marginBottom: 14 }}>
                      <strong>Active Topic:</strong> {cls.active_topic}
                    </div>

                    <div style={{ fontSize: 12, color: "#6B6685", marginBottom: 16 }}>
                      <strong>Curriculum:</strong> {cls.curriculum}
                    </div>

                    <div style={{ display: "flex", gap: 10 }}>
                      <button
                        className={styles.secondaryBtn}
                        style={{ margin: 0 }}
                        onClick={() => handleTabChange("planner")}
                      >
                        Session Planner →
                      </button>
                      <button
                        className={styles.actionBtnOutline}
                        onClick={() => handleTabChange("students")}
                      >
                        Class Roster
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className={styles.card}>
              <div className={styles.cardLabel}>Class Demographics &amp; Context</div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16, marginTop: 10 }}>
                <div style={{ background: "var(--paper)", padding: 14, borderRadius: 12 }}>
                  <div style={{ fontSize: 12, color: "var(--ink-soft)", fontWeight: 600 }}>Home Languages</div>
                  <div style={{ fontSize: 14, fontWeight: 700, marginTop: 4 }}>
                    Hindi (40%) · Marathi (30%) · English (30%)
                  </div>
                  <div style={{ fontSize: 11.5, color: "var(--ink-soft)", marginTop: 4 }}>
                    Bilingual instruction recommended for fractions vocabulary.
                  </div>
                </div>

                <div style={{ background: "var(--paper)", padding: 14, borderRadius: 12 }}>
                  <div style={{ fontSize: 12, color: "var(--ink-soft)", fontWeight: 600 }}>Age Distribution</div>
                  <div style={{ fontSize: 14, fontWeight: 700, marginTop: 4 }}>
                    9 to 11 Years Old
                  </div>
                  <div style={{ fontSize: 11.5, color: "var(--ink-soft)", marginTop: 4 }}>
                    Diverse prior schooling backgrounds across NGO community.
                  </div>
                </div>

                <div style={{ background: "var(--paper)", padding: 14, borderRadius: 12 }}>
                  <div style={{ fontSize: 12, color: "var(--ink-soft)", fontWeight: 600 }}>Instruction Delivered</div>
                  <div style={{ fontSize: 14, fontWeight: 700, marginTop: 4 }}>
                    225 Minutes (5 Sessions)
                  </div>
                  <div style={{ fontSize: 11.5, color: "var(--ink-soft)", marginTop: 4 }}>
                    Logged systematically in NGO database.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: SESSION PLANNER */}
        {/* ========================================================================= */}
        {activeTab === "planner" && (
          <div>
            <div className={styles.viewHeader}>
              <h2 className={styles.viewTitle}>Session Planner</h2>
              <div className={styles.viewSubtitle}>
                Structured 45-minute lesson plans, tiered activities &amp; real volunteer reflections
              </div>
            </div>

            <div className={styles.plannerLayout}>
              {/* Left Column: Session Selector */}
              <div>
                <div className={styles.cardLabel} style={{ marginBottom: 10 }}>
                  Sessions History &amp; Upcoming
                </div>
                <div className={styles.sessionList}>
                  {NGO_SESSIONS.map((sess) => {
                    const isSelected = sess.code === selectedSessionCode;
                    return (
                      <button
                        key={sess.code}
                        className={`${styles.sessionItemBtn} ${
                          isSelected ? styles.sessionItemBtnActive : ""
                        }`}
                        onClick={() => setSelectedSessionCode(sess.code)}
                      >
                        <div className={styles.sessionItemCode}>
                          <span>{sess.code}</span>
                          <span style={{ textTransform: "capitalize", color: sess.status === "completed" ? "#4FBFA8" : "#F2A93B" }}>
                            {sess.status}
                          </span>
                        </div>
                        <div className={styles.sessionItemTopic}>{sess.topic}</div>
                        <div className={styles.sessionItemDate}>
                          {sess.date} · {sess.duration_minutes} min {sess.rating && `· ⭐ ${sess.rating}/5`}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Right Column: Selected Session Detail */}
              <div>
                <div className={styles.card}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 10 }}>
                    <div>
                      <span className={styles.classCodeBadge} style={{ marginRight: 8 }}>
                        {selectedSession.code}
                      </span>
                      <span className={styles.tag} style={{ background: selectedSession.status === "completed" ? "#E4F6F1" : "#FDF0DC", color: selectedSession.status === "completed" ? "#4FBFA8" : "#E0703C" }}>
                        {selectedSession.status.toUpperCase()}
                      </span>
                      <h3 className={styles.classTitle} style={{ marginTop: 8 }}>
                        {selectedSession.topic}
                      </h3>
                      <div className={styles.sessionMeta}>
                        {selectedSession.subject} · {selectedSession.date} · {selectedSession.duration_minutes} Minutes · Language: {selectedSession.language.toUpperCase()} · Planned By: {selectedSession.planned_by}
                      </div>
                    </div>

                    <button
                      className={styles.secondaryBtn}
                      style={{ margin: 0 }}
                      onClick={handleGenerateLesson}
                      disabled={loadingLesson}
                    >
                      {loadingLesson ? "Generating…" : "Generate AI Lesson Plan"}
                    </button>
                  </div>

                  {/* 45-min Structured Lesson Breakdown */}
                  <div className={styles.sectionTitle} style={{ marginTop: 18 }}>
                    45-Minute Lesson Pacing Structure
                  </div>
                  <div className={styles.lessonTimeline}>
                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>00 – 05 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Warm-up &amp; Diagnostic Recap</h4>
                        <p>Quick recall of like denominators. Ask 2 quick oral questions to activate prior session memory.</p>
                      </div>
                    </div>

                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>05 – 16 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Introduce the Concept (Visual / Concrete)</h4>
                        <p>Draw fraction bar models on whiteboard. Demonstrate shaded slices before writing numeric formulas.</p>
                      </div>
                    </div>

                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>16 – 27 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Guided Practice with Volunteer</h4>
                        <p>Volunteer works through 2 examples together with the class, prompting students to explain each step.</p>
                      </div>
                    </div>

                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>27 – 38 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Differentiated Activities (3 Tiers)</h4>
                        <p>Students work on worksheets calibrated to their current level (Struggling, On Track, Advanced).</p>
                      </div>
                    </div>

                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>38 – 43 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Check Understanding &amp; Assessment</h4>
                        <p>3 quick check questions logged into diagnostic assessment sheet.</p>
                      </div>
                    </div>

                    <div className={styles.timelineStep}>
                      <div className={styles.timelineTime}>43 – 45 min</div>
                      <div className={styles.timelineContent}>
                        <h4>Wrap-up &amp; Celebration</h4>
                        <p>Review key takeaway and preview next session&apos;s challenges.</p>
                      </div>
                    </div>
                  </div>

                  {/* Tiered Activities for Selected Session */}
                  {selectedSession.activities && (
                    <>
                      <div className={styles.sectionTitle}>Tiered Activity Worksheets</div>
                      <div className={styles.activitiesGrid} style={{ marginBottom: 18 }}>
                        {selectedSession.activities.map((act) => (
                          <div key={act.level} className={styles.activityCard}>
                            <span className={`${styles.tag} ${tagClass[act.level] || ""}`}>
                              {levelKey[act.level] || act.level}
                            </span>
                            <div className={styles.sessionTopic} style={{ fontSize: 14, marginTop: 8 }}>
                              {act.title}
                            </div>
                            <div className={styles.activityPrompt}>{act.prompt}</div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  {/* Volunteer Feedback Log */}
                  {selectedSession.rating && (
                    <div className={styles.feedbackBox}>
                      <h4>
                        <span>📝</span> Onsite Volunteer Feedback ({selectedSession.rating}/5 Stars)
                      </h4>
                      <div className={styles.feedbackGrid}>
                        <div className={styles.feedbackPoint}>
                          <strong>What Worked:</strong>
                          <span>{selectedSession.what_worked}</span>
                        </div>
                        <div className={styles.feedbackPoint}>
                          <strong>What Needs Improvement:</strong>
                          <span>{selectedSession.what_didnt}</span>
                        </div>
                      </div>
                      <div style={{ marginTop: 10, fontSize: 11.5, color: "#9C6508" }}>
                        Pacing Note: {selectedSession.time_overran ? "Overran planned 45-min duration — allocate less time to warm-up" : "Finished within the 45-minute target"}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: STUDENT PROGRESS */}
        {/* ========================================================================= */}
        {activeTab === "students" && (
          <div>
            <div className={styles.viewHeader}>
              <h2 className={styles.viewTitle}>Student Progress &amp; Diagnostics</h2>
              <div className={styles.viewSubtitle}>
                10 students across 3 readiness levels from NGO assessment dataset · G5A Cohort
              </div>
            </div>

            {/* Metrics Row */}
            <div className={styles.gridTop} style={{ marginBottom: 20 }}>
              <div className={styles.card}>
                <div className={styles.cardLabel}>Class Size</div>
                <div className={`${styles.statNum} ${styles.statPeriwinkle}`}>10</div>
                <div className={styles.statLabel}>Active students enrolled</div>
              </div>
              <div className={styles.card}>
                <div className={styles.cardLabel}>Class Average</div>
                <div className={`${styles.statNum} ${styles.statMarigold}`}>78%</div>
                <div className={styles.statLabel}>Assessment accuracy</div>
              </div>
              <div className={styles.card}>
                <div className={styles.cardLabel}>Attendance Rate</div>
                <div className={`${styles.statNum} ${styles.statMint}`}>96%</div>
                <div className={styles.statLabel}>48 / 50 session attendances</div>
              </div>
            </div>

            {/* Filter and Search Bar */}
            <div className={styles.filtersRow}>
              <input
                type="text"
                placeholder="Search by student name, code, or teacher notes..."
                className={styles.searchInput}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />

              <button
                className={`${styles.filterChip} ${levelFilter === "all" ? styles.filterChipActive : ""}`}
                onClick={() => setLevelFilter("all")}
              >
                All Levels (10)
              </button>
              <button
                className={`${styles.filterChip} ${levelFilter === "struggling" ? styles.filterChipActive : ""}`}
                onClick={() => setLevelFilter("struggling")}
              >
                Struggling (3)
              </button>
              <button
                className={`${styles.filterChip} ${levelFilter === "on_track" ? styles.filterChipActive : ""}`}
                onClick={() => setLevelFilter("on_track")}
              >
                On Track (4)
              </button>
              <button
                className={`${styles.filterChip} ${levelFilter === "advanced" ? styles.filterChipActive : ""}`}
                onClick={() => setLevelFilter("advanced")}
              >
                Advanced (3)
              </button>
            </div>

            {/* Students Table */}
            <div className={styles.card}>
              <div className={styles.tableScroll} style={{ maxHeight: 520 }}>
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th>Code &amp; Name</th>
                      <th>Age / Language</th>
                      <th>Level</th>
                      <th>Score</th>
                      <th>Attendance</th>
                      <th>Observed Misconceptions</th>
                      <th>Volunteer Notes</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStudents.map((st) => (
                      <tr key={st.student_id}>
                        <td>
                          <div className={styles.studentName}>
                            <span className={`${styles.dot} ${dotClass[st.level] || ""}`} />
                            <div>
                              <div>{st.name}</div>
                              <span style={{ fontSize: 10.5, color: "#6B6685" }}>{st.code}</span>
                            </div>
                          </div>
                        </td>
                        <td>
                          {st.age} yrs · {st.home_language.toUpperCase()}
                        </td>
                        <td>
                          <span className={`${styles.tag} ${tagClass[st.level] || ""}`}>
                            {levelKey[st.level]}
                          </span>
                        </td>
                        <td style={{ fontWeight: 700 }}>{Math.round(st.avg_score * 100)}%</td>
                        <td>
                          {st.attendance_present}/{st.attendance_total} ({st.attendance_rate}%)
                        </td>
                        <td>
                          {st.misconceptions.map((m) => (
                            <span key={m} className={styles.misconceptionTag}>
                              {m}
                            </span>
                          ))}
                        </td>
                        <td style={{ fontSize: 12, color: "#6B6685", maxWidth: 200 }}>
                          {st.teacher_notes}
                        </td>
                        <td>
                          <button
                            className={styles.actionBtnOutline}
                            style={{ padding: "4px 8px", fontSize: 11 }}
                            onClick={() => setSelectedStudent(st)}
                          >
                            Details
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Selected Student Detail Drawer / Modal */}
            {selectedStudent && (
              <div className={styles.studentDetailModal}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <div>
                    <h3 style={{ margin: "0 0 4px", fontFamily: "var(--font-display)", fontSize: 18 }}>
                      {selectedStudent.name} ({selectedStudent.code}) — Diagnostic Profile
                    </h3>
                    <div style={{ fontSize: 12.5, color: "var(--ink-soft)" }}>
                      Age: {selectedStudent.age} · Primary Language: {selectedStudent.home_language.toUpperCase()} · Level: {levelKey[selectedStudent.level]}
                    </div>
                  </div>
                  <button
                    className={styles.actionBtnOutline}
                    onClick={() => setSelectedStudent(null)}
                  >
                    Close ✕
                  </button>
                </div>

                <div style={{ margin: "14px 0", fontSize: 12.5, background: "white", padding: 12, borderRadius: 10, border: "1px solid var(--border)" }}>
                  <strong>Volunteer Observation:</strong> {selectedStudent.teacher_notes}
                </div>

                <div className={styles.cardLabel} style={{ marginBottom: 8 }}>
                  Recent Assessment Items &amp; Hints Used
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 10 }}>
                  {selectedStudent.recent_questions.map((q, idx) => (
                    <div
                      key={idx}
                      style={{
                        background: "white",
                        border: "1px solid var(--border)",
                        borderRadius: 10,
                        padding: 10,
                        fontSize: 12,
                      }}
                    >
                      <div style={{ fontWeight: 700, marginBottom: 4 }}>{q.question}</div>
                      <div style={{ display: "flex", justifyContent: "space-between", color: "var(--ink-soft)" }}>
                        <span>Diff: {q.difficulty}</span>
                        <span style={{ color: q.correct ? "#4FBFA8" : "#E0703C", fontWeight: 700 }}>
                          {q.correct ? "✓ Correct" : "✗ Incorrect"}
                        </span>
                      </div>
                      <div style={{ fontSize: 10.5, color: "#6B6685", marginTop: 4 }}>
                        Time: {q.time_seconds}s {q.hint_used && "· Hint Used"}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 5: RESOURCES */}
        {/* ========================================================================= */}
        {activeTab === "resources" && (
          <div>
            <div className={styles.viewHeader}>
              <h2 className={styles.viewTitle}>Teaching Resources &amp; Fractions Corpus</h2>
              <div className={styles.viewSubtitle}>
                Calibrated classroom aids, diagnostic question banks &amp; volunteer reflection archives
              </div>
            </div>

            {/* Category Filter Chips */}
            <div className={styles.filtersRow}>
              <button
                className={`${styles.filterChip} ${resourceCategory === "all" ? styles.filterChipActive : ""}`}
                onClick={() => setResourceCategory("all")}
              >
                All Resources
              </button>
              <button
                className={`${styles.filterChip} ${resourceCategory === "aids" ? styles.filterChipActive : ""}`}
                onClick={() => setResourceCategory("aids")}
              >
                Hands-on Aids
              </button>
              <button
                className={`${styles.filterChip} ${resourceCategory === "question_bank" ? styles.filterChipActive : ""}`}
                onClick={() => setResourceCategory("question_bank")}
              >
                Diagnostic Question Bank
              </button>
              <button
                className={`${styles.filterChip} ${resourceCategory === "misconceptions" ? styles.filterChipActive : ""}`}
                onClick={() => setResourceCategory("misconceptions")}
              >
                Misconception Guide
              </button>
              <button
                className={`${styles.filterChip} ${resourceCategory === "reflections" ? styles.filterChipActive : ""}`}
                onClick={() => setResourceCategory("reflections")}
              >
                Volunteer Reflections
              </button>
            </div>

            {/* Resources Grid */}
            <div className={styles.resourceGrid}>
              {filteredResources.map((res: ResourceItem) => (
                <div key={res.id} className={styles.resourceCard}>
                  <div className={styles.resourceCardTop}>
                    <span className={styles.resourceBadge}>{res.badge}</span>
                    <h3 className={styles.resourceTitle}>{res.title}</h3>
                    <div className={styles.resourceDesc}>{res.description}</div>
                    <ul className={styles.resourceDetailsList}>
                      {res.details.map((item, idx) => (
                        <li key={idx} style={{ marginBottom: 6 }}>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
                    <button className={styles.actionBtnOutline}>
                      Download Worksheet / Guide
                    </button>
                    <button
                      className={styles.actionBtnOutline}
                      onClick={() => handleTabChange("planner")}
                    >
                      Use in Lesson Plan
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Fractions Diagnostic Grounding Card */}
            <div className={styles.card} style={{ marginTop: 20 }}>
              <div className={styles.cardLabel}>Corpus Grounding Note</div>
              <p style={{ fontSize: 13, color: "var(--ink-soft)", margin: "6px 0 0", lineHeight: 1.55 }}>
                Saarthi&apos;s lesson generation engine prioritizes these approved fractions corpus definitions.
                When generating tiered activities, prompts adhere strictly to visual bar representations for struggling students,
                numerical common denominator methods for on-track students, and simplification/extension for advanced learners.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

