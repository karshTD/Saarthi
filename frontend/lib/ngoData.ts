export interface ClassInfo {
  id: number;
  code: string;
  name: string;
  grade: string;
  location: string;
  volunteer_name: string;
  volunteer_email: string;
  student_count: number;
  subject: string;
  attendance_rate: number;
  active_topic: string;
  status: string;
  schedule: string;
  curriculum: string;
}

export interface SessionRecord {
  id: number;
  code: string;
  class_code: string;
  date: string;
  subject: string;
  topic: string;
  duration_minutes: number;
  language: string;
  planned_by: "saarthi" | "manual";
  status: "completed" | "planned";
  volunteer_notes: string;
  rating?: number;
  what_worked?: string;
  what_didnt?: string;
  time_overran?: boolean;
  activities?: {
    level: "struggling" | "on_track" | "advanced";
    title: string;
    prompt: string;
  }[];
}

export interface StudentRecord {
  student_id: number;
  code: string;
  name: string;
  age: number;
  home_language: "hi" | "mr" | "en";
  level: "struggling" | "on_track" | "advanced";
  avg_score: number;
  attendance_present: number;
  attendance_total: number;
  attendance_rate: number;
  teacher_notes: string;
  misconceptions: string[];
  recent_questions: {
    question: string;
    difficulty: "easy" | "medium" | "hard";
    correct: boolean;
    time_seconds: number;
    hint_used: boolean;
  }[];
}

export interface ResourceItem {
  id: string;
  category: "aids" | "question_bank" | "misconceptions" | "reflections";
  title: string;
  subtitle: string;
  description: string;
  badge: string;
  details: string[];
}

// ---------------------------------------------------------------------------
// 1. Classes Data (from classes.csv & volunteers.csv)
// ---------------------------------------------------------------------------
export const NGO_CLASSES: ClassInfo[] = [
  {
    id: 1,
    code: "G5A",
    name: "Grade 5 — Section A",
    grade: "Grade 5",
    location: "Demo Centre, Ray of Hope",
    volunteer_name: "Demo Volunteer",
    volunteer_email: "demo@saarthi.dev",
    student_count: 10,
    subject: "Mathematics · Fractions",
    attendance_rate: 96,
    active_topic: "Adding Like Fractions & Visual Models",
    status: "In Progress (Week 5 of 8)",
    schedule: "Every Monday · 4:00 PM – 4:45 PM",
    curriculum: "Foundational Fractions (Halves, Thirds, Fourths, Eighths)",
  },
  {
    id: 2,
    code: "G6A",
    name: "Grade 6 — Section A",
    grade: "Grade 6",
    location: "Demo Centre, Ray of Hope",
    volunteer_name: "Demo Volunteer",
    volunteer_email: "demo@saarthi.dev",
    student_count: 1,
    subject: "Mathematics · Number Sense",
    attendance_rate: 100,
    active_topic: "Diagnostic Pre-assessment",
    status: "Upcoming Term",
    schedule: "Every Wednesday · 4:00 PM – 4:45 PM",
    curriculum: "Upper Primary Math Foundations",
  },
];

// ---------------------------------------------------------------------------
// 2. Sessions Data (from sessions.csv & lesson_feedback.csv)
// ---------------------------------------------------------------------------
export const NGO_SESSIONS: SessionRecord[] = [
  {
    id: 1,
    code: "G5A-001",
    class_code: "G5A",
    date: "2026-08-31",
    subject: "Mathematics",
    topic: "Fractions baseline diagnostic",
    duration_minutes: 45,
    language: "en",
    planned_by: "manual",
    status: "completed",
    volunteer_notes: "Initial diagnostic across 10 children to establish baseline reading and numeracy levels.",
    rating: 4,
    what_worked: "Students engaged enthusiastically with paper fraction strips.",
    what_didnt: "Ran out of time for quiet individual practice.",
    time_overran: true,
    activities: [
      {
        level: "struggling",
        title: "Visual Parts Identification",
        prompt: "Color 1 of 2 equal parts of a circle, then 2 of 4 parts of a square. Name the fraction.",
      },
      {
        level: "on_track",
        title: "Like Fractions Diagnostic",
        prompt: "Solve 1/4 + 2/4 using a bar model, then verify with numeric addition.",
      },
      {
        level: "advanced",
        title: "Parts and Wholes Extension",
        prompt: "Which is larger: 3/4 or 5/8? Draw both and justify your reasoning.",
      },
    ],
  },
  {
    id: 2,
    code: "G5A-002",
    class_code: "G5A",
    date: "2026-09-07",
    subject: "Mathematics",
    topic: "Like fractions & numerator meaning",
    duration_minutes: 45,
    language: "en",
    planned_by: "saarthi",
    status: "completed",
    volunteer_notes: "Reinforced that denominator is the size of each piece and numerator counts how many pieces.",
    rating: 3,
    what_worked: "Visual chocolate bar aids helped students grasp why the bottom number doesn't change.",
    what_didnt: "A few students got confused when introduced to unlike denominators too quickly.",
    time_overran: false,
    activities: [
      {
        level: "struggling",
        title: "Concrete Bar Division",
        prompt: "Fold a paper strip into 4 equal pieces. Shade 1 piece, then shade 2 more. Count the total shaded.",
      },
      {
        level: "on_track",
        title: "Adding Equal Slices",
        prompt: "Calculate 2/7 + 3/7. Write a sentence explaining why the 7 stays the same.",
      },
      {
        level: "advanced",
        title: "Missing Numerator Challenge",
        prompt: "Find the missing number: ?/9 + 4/9 = 8/9. Explain your strategy.",
      },
    ],
  },
  {
    id: 3,
    code: "G5A-003",
    class_code: "G5A",
    date: "2026-09-14",
    subject: "Mathematics",
    topic: "Adding like fractions",
    duration_minutes: 45,
    language: "en",
    planned_by: "saarthi",
    status: "completed",
    volunteer_notes: "Deep dive into addition of like fractions with peer pairing.",
    rating: 5,
    what_worked: "Peer work was highly effective; advanced students enjoyed tutoring buddies.",
    what_didnt: "Struggling students required more 1-on-1 step-by-step scaffolding.",
    time_overran: true,
    activities: [
      {
        level: "struggling",
        title: "Adding Fractions with Pictures",
        prompt: "Draw 1/4 and 2/4 as shaded bars: count the shaded parts: 1/4 + 2/4 = ?",
      },
      {
        level: "on_track",
        title: "Adding Like Fractions Drill",
        prompt: "Solve 3/8 + 2/8 and explain your method to your peer partner.",
      },
      {
        level: "advanced",
        title: "Adding and Simplifying Fractions",
        prompt: "Solve 4/6 + 3/6 and convert the improper fraction into a mixed number.",
      },
    ],
  },
  {
    id: 4,
    code: "G5A-004",
    class_code: "G5A",
    date: "2026-09-21",
    subject: "Mathematics",
    topic: "Unlike fractions & common denominators",
    duration_minutes: 45,
    language: "en",
    planned_by: "saarthi",
    status: "completed",
    volunteer_notes: "Transitioned from like to unlike fractions (halves and quarters).",
    rating: 2,
    what_worked: "Real-life examples with sharing rotis and samosas clicked immediately.",
    what_didnt: "Attempted too many complex questions in one session; pacing felt rushed.",
    time_overran: false,
    activities: [
      {
        level: "struggling",
        title: "Halves to Quarters Comparison",
        prompt: "Show that 1/2 is the exact same size as 2/4 using paper overlay.",
      },
      {
        level: "on_track",
        title: "Converting to Common Denominators",
        prompt: "Rewrite 1/2 as a fraction with denominator 4, then compute 1/2 + 1/4.",
      },
      {
        level: "advanced",
        title: "Unlike Addition with Thirds and Sixths",
        prompt: "Solve 1/3 + 2/6. Explain how you created matching pieces.",
      },
    ],
  },
  {
    id: 5,
    code: "G5A-005",
    class_code: "G5A",
    date: "2026-09-28",
    subject: "Mathematics",
    topic: "Equivalent fractions & simplification",
    duration_minutes: 45,
    language: "en",
    planned_by: "saarthi",
    status: "completed",
    volunteer_notes: "Exploring equivalent fractions on number lines and simplifying answers.",
    rating: 4,
    what_worked: "Overall class showed strong improvement in identifying equal proportions.",
    what_didnt: "Advanced students finished quickly and needed harder stretch tasks.",
    time_overran: true,
    activities: [
      {
        level: "struggling",
        title: "Equivalent Fractions Visual Match",
        prompt: "Find three fractions equal to 1/2 using the fraction wall (2/4, 3/6, 4/8).",
      },
      {
        level: "on_track",
        title: "Simplifying by Common Factor",
        prompt: "Simplify 4/12 and 6/8 to their simplest form by dividing numerator and denominator.",
      },
      {
        level: "advanced",
        title: "Multi-step Word Problem",
        prompt: "Rani ate 2/8 of a cake and Kabir ate 1/4. Who ate more? Justify with mathematics.",
      },
    ],
  },
  {
    id: 6,
    code: "G5A-006",
    class_code: "G5A",
    date: "2026-10-26",
    subject: "Mathematics",
    topic: "Comparing & Ordering Fractions",
    duration_minutes: 45,
    language: "en",
    planned_by: "saarthi",
    status: "planned",
    volunteer_notes: "Next session: 3 students ready for unlike fractions; 3 need another visual pass on equivalent denominators.",
    activities: [
      {
        level: "struggling",
        title: "Visual Benchmark Comparison",
        prompt: "Compare 3/8 and 5/8 using shaded circles. Next compare 1/2 and 3/8 with a number line benchmark.",
      },
      {
        level: "on_track",
        title: "Ordering Fractions with Common Denominators",
        prompt: "Order from smallest to largest: 5/12, 1/12, 9/12, 7/12. State the rule for ordering.",
      },
      {
        level: "advanced",
        title: "Cross-Multiplication & Common Denominator Reasoning",
        prompt: "Compare 2/3 and 3/4 without converting to decimals. Write two different mathematical justifications.",
      },
    ],
  },
];

// ---------------------------------------------------------------------------
// 3. Students Data (from students.csv, attendance.csv & assessment_items.csv)
// ---------------------------------------------------------------------------
export const NGO_STUDENTS: StudentRecord[] = [
  {
    student_id: 1,
    code: "S01",
    name: "Aarav",
    age: 9,
    home_language: "hi",
    level: "struggling",
    avg_score: 0.60,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Shy but tries; thrives with physical fraction strips and patient encouragement.",
    misconceptions: ["ignored common denominator", "compared numerators only"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: false, time_seconds: 120, hint_used: true },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 111, hint_used: true },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 115, hint_used: false },
      { question: "7/10 - 3/10 = ?", difficulty: "hard", correct: true, time_seconds: 108, hint_used: false },
    ],
  },
  {
    student_id: 2,
    code: "S02",
    name: "Vivaan",
    age: 10,
    home_language: "mr",
    level: "struggling",
    avg_score: 0.50,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Needs encouragement; tends to add denominators when working under time pressure.",
    misconceptions: ["added denominators", "ignored common denominator"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: false, time_seconds: 63, hint_used: false },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 76, hint_used: true },
      { question: "5/6 - 2/6 = ?", difficulty: "hard", correct: true, time_seconds: 132, hint_used: true },
      { question: "7/10 - 3/10 = ?", difficulty: "hard", correct: false, time_seconds: 107, hint_used: true },
    ],
  },
  {
    student_id: 3,
    code: "S03",
    name: "Aditya",
    age: 11,
    home_language: "en",
    level: "struggling",
    avg_score: 0.55,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Confident with whole numbers; needs conceptual bridging to fractional pieces.",
    misconceptions: ["forgot to simplify", "added denominators"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 44, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 37, hint_used: false },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 104, hint_used: false },
      { question: "5/6 - 2/6 = ?", difficulty: "hard", correct: false, time_seconds: 130, hint_used: false },
    ],
  },
  {
    student_id: 4,
    code: "S04",
    name: "Vihaan",
    age: 9,
    home_language: "hi",
    level: "on_track",
    avg_score: 0.70,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Sometimes distracted; refocuses well when solving problems in small peer pairs.",
    misconceptions: ["added denominators", "forgot to simplify"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 20, hint_used: false },
      { question: "2/5 + 1/5 = ?", difficulty: "easy", correct: true, time_seconds: 25, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 106, hint_used: false },
      { question: "7/10 - 3/10 = ?", difficulty: "hard", correct: true, time_seconds: 115, hint_used: false },
    ],
  },
  {
    student_id: 5,
    code: "S05",
    name: "Arjun",
    age: 10,
    home_language: "mr",
    level: "on_track",
    avg_score: 0.75,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Asks thoughtful questions; demonstrates great curiosity and perseveres through errors.",
    misconceptions: ["forgot to simplify", "ignored common denominator"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 50, hint_used: false },
      { question: "2/5 + 1/5 = ?", difficulty: "easy", correct: true, time_seconds: 18, hint_used: false },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 93, hint_used: false },
      { question: "5/6 - 2/6 = ?", difficulty: "hard", correct: false, time_seconds: 126, hint_used: true },
    ],
  },
  {
    student_id: 6,
    code: "S06",
    name: "Sai",
    age: 11,
    home_language: "en",
    level: "on_track",
    avg_score: 0.80,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Quiet, methodical worker; reliable understanding of like fraction addition.",
    misconceptions: ["forgot to simplify"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 51, hint_used: false },
      { question: "2/5 + 1/5 = ?", difficulty: "easy", correct: true, time_seconds: 20, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 70, hint_used: false },
      { question: "5/6 - 2/6 = ?", difficulty: "hard", correct: true, time_seconds: 178, hint_used: true },
    ],
  },
  {
    student_id: 7,
    code: "S07",
    name: "Reyansh",
    age: 9,
    home_language: "hi",
    level: "on_track",
    avg_score: 0.75,
    attendance_present: 4,
    attendance_total: 5,
    attendance_rate: 80,
    teacher_notes: "Helps peers patiently; missed session 2 but caught up rapidly during recap.",
    misconceptions: ["compared numerators only", "added denominators"],
    recent_questions: [
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 58, hint_used: false },
      { question: "7/10 - 3/10 = ?", difficulty: "hard", correct: true, time_seconds: 175, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 140, hint_used: false },
    ],
  },
  {
    student_id: 8,
    code: "S08",
    name: "Ayaan",
    age: 10,
    home_language: "mr",
    level: "advanced",
    avg_score: 0.90,
    attendance_present: 4,
    attendance_total: 5,
    attendance_rate: 80,
    teacher_notes: "Very capable mathematician; takes extra time to write clean explanations.",
    misconceptions: ["forgot to simplify"],
    recent_questions: [
      { question: "1/4 + 2/4 = ?", difficulty: "easy", correct: true, time_seconds: 24, hint_used: false },
      { question: "3/7 + 2/7 = ?", difficulty: "easy", correct: true, time_seconds: 28, hint_used: false },
      { question: "4/11 + 5/11 = ?", difficulty: "medium", correct: true, time_seconds: 35, hint_used: false },
      { question: "7/12 - 3/12 = ?", difficulty: "hard", correct: true, time_seconds: 45, hint_used: false },
    ],
  },
  {
    student_id: 9,
    code: "S09",
    name: "Krishna",
    age: 11,
    home_language: "en",
    level: "advanced",
    avg_score: 0.95,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Improving steadily; grasps unlike fractions quickly and assists peers.",
    misconceptions: ["ignored common denominator (rarely)"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 26, hint_used: false },
      { question: "2/5 + 1/5 = ?", difficulty: "easy", correct: true, time_seconds: 19, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 42, hint_used: false },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 31, hint_used: false },
    ],
  },
  {
    student_id: 10,
    code: "S10",
    name: "Ishaan",
    age: 9,
    home_language: "hi",
    level: "advanced",
    avg_score: 0.92,
    attendance_present: 5,
    attendance_total: 5,
    attendance_rate: 100,
    teacher_notes: "Eager to learn; challenges himself with improper fraction conversion.",
    misconceptions: ["forgot to simplify (subtraction)"],
    recent_questions: [
      { question: "1/2 + 1/2 = ?", difficulty: "easy", correct: true, time_seconds: 30, hint_used: false },
      { question: "2/5 + 1/5 = ?", difficulty: "easy", correct: true, time_seconds: 23, hint_used: false },
      { question: "3/8 + 2/8 = ?", difficulty: "medium", correct: true, time_seconds: 82, hint_used: true },
      { question: "1/3 + 1/3 = ?", difficulty: "medium", correct: true, time_seconds: 75, hint_used: false },
    ],
  },
];

// ---------------------------------------------------------------------------
// 4. Teaching Resources & Fractions Corpus (from data_templates & data_files.py)
// ---------------------------------------------------------------------------
export const NGO_RESOURCES: ResourceItem[] = [
  {
    id: "res-strips",
    category: "aids",
    title: "Fraction Strips & Visual Bar Kits",
    subtitle: "Hands-on printable paper manipulation tool",
    description: "Enables students in the Struggling level to fold, align, and physically verify that equal partition parts can be summed without modifying the denominator.",
    badge: "Classroom Tested",
    details: [
      "Foldable into halves, quarters, eighths, thirds, sixths, and twelfths.",
      "Used in Session G5A-001 & G5A-003 with 100% student engagement.",
      "Recommended time: 10-15 minutes during the 'Introduce the Idea' block.",
    ],
  },
  {
    id: "res-diag-bank",
    category: "question_bank",
    title: "Baseline Diagnostic 6-Item Question Bank",
    subtitle: "Standardized fractions benchmark set",
    description: "A calibrated set of 6 questions evaluated across all 10 students with time thresholds and misconception detectors.",
    badge: "Diagnostic Bank",
    details: [
      "Easy: 1/2 + 1/2 = 1 and 2/5 + 1/5 = 3/5",
      "Medium: 3/8 + 2/8 = 5/8 and 1/3 + 1/3 = 2/3",
      "Hard: 5/6 - 2/6 = 3/6 (1/2) and 7/10 - 3/10 = 4/10 (2/5)",
      "Recorded in assessment_items.csv with difficulty and attempt metrics.",
    ],
  },
  {
    id: "res-misconceptions",
    category: "misconceptions",
    title: "Volunteer Misconception Reference Guide",
    subtitle: "Decoding the 4 most frequent student errors",
    description: "Clear explanations of why children make specific fraction errors and the exact visual cue to correct them without lecturing.",
    badge: "Volunteer Guide",
    details: [
      "'Added Denominators' (e.g., 1/3 + 1/3 = 2/6): Student applies whole-number addition. Fix: Point to the physical strip pieces.",
      "'Ignored Common Denominator': Adding only top numbers while guessing bottom. Fix: Bar diagram overlay.",
      "'Compared Numerators Only': Believing 1/8 > 1/4 because 8 > 4. Fix: Cut an apple into 4 vs 8 slices.",
      "'Forgot to Simplify': Student stops at 4/8 instead of 1/2. Fix: Pair matching game.",
    ],
  },
  {
    id: "res-feedback-archive",
    category: "reflections",
    title: "Onsite Volunteer Feedback & Reflection Archive",
    subtitle: "Real lessons learned from G5A-001 through G5A-005",
    description: "Insights logged directly after teaching sessions at Demo Centre, highlighting time management and peer grouping tips.",
    badge: "5 Sessions Logged",
    details: [
      "Session 1: 'Ran out of time for practice' → Keep warm-up strictly under 6 minutes.",
      "Session 2: 'Visual chocolate aids helped' → Retain concrete examples for each new topic.",
      "Session 3: 'Peer work was effective' → Pair advanced students (Ayaan, Krishna) with on-track peers.",
      "Session 4: 'Too many questions' → Limit check-understanding to max 5 well-chosen problems.",
      "Session 5: 'Advanced students were bored' → Keep extension challenge cards pre-printed.",
    ],
  },
];
