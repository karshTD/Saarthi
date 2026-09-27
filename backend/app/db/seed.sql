-- Seed data: one volunteer, one class, 10 students across all levels,
-- one completed fractions session with differentiated activities and
-- recorded assessments, and resulting progress snapshots.

INSERT INTO volunteers (id, name, email) VALUES
  (1, 'Utkarsh Sharma', 'volunteer1@saarthi.dev');

INSERT INTO classes (id, name, volunteer_id) VALUES
  (1, 'Grade 5 - Section A', 1);

INSERT INTO students (id, name, class_id, level) VALUES
  (1, 'Aarav',   1, 'struggling'),
  (2, 'Diya',    1, 'on_track'),
  (3, 'Vivaan',  1, 'advanced'),
  (4, 'Ananya',  1, 'struggling'),
  (5, 'Ishaan',  1, 'on_track'),
  (6, 'Saanvi',  1, 'on_track'),
  (7, 'Reyansh', 1, 'advanced'),
  (8, 'Myra',    1, 'struggling'),
  (9, 'Kabir',   1, 'on_track'),
  (10, 'Anika',  1, 'advanced');

INSERT INTO sessions (id, class_id, subject, topic, language, duration_minutes, status) VALUES
  (1, 1, 'Mathematics', 'Fractions - Addition of Like Fractions', 'en', 45, 'completed');

INSERT INTO activities (id, session_id, title, difficulty_level, content, order_index) VALUES
  (1, 1, 'Adding fractions with pictures', 'struggling',
    '{"type": "visual", "question": "1/4 + 2/4 = ?", "options": ["3/4", "3/8", "1/2"], "answer": "3/4"}', 1),
  (2, 1, 'Adding like fractions', 'on_track',
    '{"type": "numeric", "question": "3/8 + 2/8 = ?", "answer": "5/8"}', 1),
  (3, 1, 'Adding and simplifying fractions', 'advanced',
    '{"type": "numeric", "question": "4/6 + 3/6 = ? (simplify)", "answer": "7/6 = 1 1/6"}', 1);

-- Assessments: each student attempted the activity matching their level
INSERT INTO assessments (activity_id, student_id, score, time_taken_seconds, attempt_count) VALUES
  (1, 1, 0.60, 210, 2),
  (1, 4, 0.40, 260, 3),
  (1, 8, 0.80, 180, 1),
  (2, 2, 0.85, 150, 1),
  (2, 5, 0.70, 190, 2),
  (2, 6, 0.90, 140, 1),
  (2, 9, 0.75, 170, 1),
  (3, 3, 0.95, 120, 1),
  (3, 7, 1.00, 100, 1),
  (3, 10, 0.90, 130, 1);

-- Progress snapshots derived from the above (what session-intelligence would compute)
INSERT INTO progress (student_id, topic, mastery_level, avg_score, notes) VALUES
  (1, 'Fractions', 'struggling', 0.60, 'Needs continued visual/picture-based practice on like fractions.'),
  (2, 'Fractions', 'on_track', 0.85, 'Ready to move to unlike fraction addition next session.'),
  (3, 'Fractions', 'advanced', 0.95, 'Ready for mixed-number and subtraction problems.'),
  (4, 'Fractions', 'struggling', 0.40, 'Struggling with core concept; recommend 1:1 support next session.'),
  (5, 'Fractions', 'on_track', 0.70, 'Solid grasp, minor errors on carrying/simplifying.'),
  (6, 'Fractions', 'on_track', 0.90, 'Close to advanced level; consider promoting next session.'),
  (7, 'Fractions', 'advanced', 1.00, 'Fully mastered like-fraction addition; introduce unlike fractions.'),
  (8, 'Fractions', 'struggling', 0.80, 'Improved significantly; consider promoting to on_track.'),
  (9, 'Fractions', 'on_track', 0.75, 'Steady progress, continue at current level.'),
  (10, 'Fractions', 'advanced', 0.90, 'Strong performance, ready for more complex fraction operations.');
