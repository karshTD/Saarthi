"use client";

import { useEffect, useState } from "react";
import styles from "./dashboard.module.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Shown immediately and used as a fallback if the backend isn't reachable,
// so the UI never shows a blank/broken screen during a live demo.
const FALLBACK_STUDENTS = [
  { student_id: 1, name: "Diya", level: "on_track", avg_score: 0.85 },
  { student_id: 2, name: "Vivaan", level: "advanced", avg_score: 0.95 },
  { student_id: 3, name: "Aarav", level: "struggling", avg_score: 0.6 },
  { student_id: 4, name: "Ishaan", level: "on_track", avg_score: 0.7 },
];
const FALLBACK_COUNTS = { struggling: 3, on_track: 4, advanced: 3 };

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

type StudentRow = { student_id: number; name: string; level: string; avg_score: number | null };
type Counts = Record<string, number>;

export default function DashboardPage() {
  const [students, setStudents] = useState<StudentRow[]>(FALLBACK_STUDENTS);
  const [counts, setCounts] = useState<Counts>(FALLBACK_COUNTS);
  const [connected, setConnected] = useState(false);

  const [recommendation, setRecommendation] = useState(
    "3 students are ready to move from like to unlike fraction addition. 3 students need another visual-first pass on the core concept before advancing."
  );
  const [generatedBy, setGeneratedBy] = useState<string | null>(null);
  const [loadingReco, setLoadingReco] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/api/classes/1/analysis`)
      .then((res) => {
        if (!res.ok) throw new Error("not ok");
        return res.json();
      })
      .then((data) => {
        setStudents(data.students.slice(0, 4));
        setCounts(data.level_counts);
        setConnected(true);
      })
      .catch(() => setConnected(false));
  }, []);

  async function handleGenerateRecommendation() {
    setLoadingReco(true);
    try {
      const res = await fetch(`${API_URL}/api/sessions/1/recommendation`, { method: "POST" });
      if (!res.ok) throw new Error("not ok");
      const data = await res.json();
      setRecommendation(data.recommendation);
      setGeneratedBy(data.generated_by);
      setConnected(true);
    } catch {
      setGeneratedBy("unavailable");
    } finally {
      setLoadingReco(false);
    }
  }

  return (
    <div className={styles.page}>
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          saa<span>rthi</span>
        </div>
        <div className={styles.tagline}>AI Volunteer Copilot</div>
        <div className={`${styles.navItem} ${styles.navItemActive}`}>Dashboard</div>
        <div className={styles.navItem}>My Classes</div>
        <div className={styles.navItem}>Session Planner</div>
        <div className={styles.navItem}>Student Progress</div>
        <div className={styles.navItem}>Resources</div>
      </aside>

      <main className={styles.main}>
        <div className={styles.topbar}>
          <div>
            <h1 className={styles.greetingH1}>Grade 5 — Section A</h1>
            <p className={styles.greetingP}>
              Mathematics · Fractions · 10 students
              {connected && <span style={{ color: "#4FBFA8", fontWeight: 700 }}> · live</span>}
            </p>
          </div>
          <div className={styles.avatar}>U</div>
        </div>

        <div className={styles.gridTop}>
          <div className={styles.card}>
            <div className={styles.cardLabel}>Today&apos;s Session</div>
            <div className={styles.sessionTopic}>Adding Like Fractions</div>
            <div className={styles.sessionMeta}>45 min · Differentiated across 3 levels</div>
            <span className={styles.badgeProgress}>Lesson plan ready</span>
            <div className={styles.progressBar}>
              <div className={styles.progressBarFill} />
            </div>
          </div>
          <div className={styles.card}>
            <div className={styles.cardLabel}>Avg. Score</div>
            <div className={`${styles.statNum} ${styles.statMarigold}`}>78%</div>
            <div className={styles.statLabel}>Last session, class average</div>
          </div>
          <div className={styles.card}>
            <div className={styles.cardLabel}>Sessions Logged</div>
            <div className={`${styles.statNum} ${styles.statMint}`}>12</div>
            <div className={styles.statLabel}>Since this term began</div>
          </div>
        </div>

        <div className={styles.card} style={{ marginBottom: 18 }}>
          <div className={styles.cardLabel}>Class Level Breakdown</div>
          <div className={styles.levelsRow}>
            {["struggling", "on_track", "advanced"].map((lvl) => (
              <div key={lvl} className={`${styles.levelPill} ${pillClass[lvl]}`}>
                <span className={styles.n}>{counts[lvl] ?? 0}</span>
                {levelKey[lvl]}
              </div>
            ))}
          </div>
        </div>

        <div className={styles.gridBottom}>
          <div className={styles.card}>
            <div className={styles.cardLabel}>Student Progress</div>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Level</th>
                  <th>Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {students.map((s) => (
                  <tr key={s.student_id}>
                    <td>
                      <div className={styles.studentName}>
                        <span className={`${styles.dot} ${dotClass[s.level] || ""}`} />
                        {s.name}
                      </div>
                    </td>
                    <td>
                      <span className={`${styles.tag} ${tagClass[s.level] || ""}`}>
                        {levelKey[s.level] || s.level}
                      </span>
                    </td>
                    <td>{s.avg_score != null ? `${Math.round(s.avg_score * 100)}%` : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className={styles.reco}>
            <h3>Next Session Recommendation</h3>
            <p>{recommendation}</p>
            <button className={styles.chip} onClick={handleGenerateRecommendation} disabled={loadingReco}>
              {loadingReco ? "Generating…" : "Generate recommendation"}
            </button>
            {generatedBy && generatedBy !== "unavailable" && (
              <span style={{ fontSize: 10, opacity: 0.8, marginLeft: 8 }}>
                generated by: {generatedBy}
              </span>
            )}
            {generatedBy === "unavailable" && (
              <span style={{ fontSize: 10, opacity: 0.8, marginLeft: 8 }}>
                backend unreachable — showing cached text
              </span>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
