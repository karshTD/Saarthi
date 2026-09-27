'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import styles from './page.module.css';

export default function LandingPage() {
  const router = useRouter();

  return (
    <main>
      <div className={styles.wrap}>
        <nav className={styles.nav}>
          <div className={styles.wordmark}>
            Saarthi<span>.</span>
          </div>
          <button className={styles.navCta} onClick={() => router.push('/dashboard')}>
            Open Dashboard
          </button>
        </nav>

        <section className={styles.hero}>
          <div className={styles.heroText}>
            <h1>Turn limited volunteer time into better learning for every child.</h1>
            <p>
              Saarthi is an AI volunteer copilot that helps NGO volunteers understand
              each child&apos;s level, prepare the right activity, and track what happens next.
            </p>
            <div className={styles.heroCtas}>
              <button className={styles.btnPrimary} onClick={() => router.push('/dashboard')}>
                Try Saarthi
              </button>
              <button
                className={styles.btnSecondary}
                onClick={() => document.getElementById('workflow')?.scrollIntoView({ behavior: 'smooth' })}
              >
                See how it works
              </button>
            </div>
          </div>

          <div className={styles.heroVisual} aria-label="Saarthi dashboard preview">
            <div className={styles.mockupFrame}>
              <div className={styles.mockupTopbar}>
                <span style={{ background: '#ff6b6b' }} />
                <span style={{ background: '#f2c94c' }} />
                <span style={{ background: '#4fbfa8' }} />
              </div>
              <div style={{ padding: 24 }}>
                <div style={{ fontSize: 12, color: 'var(--ink-soft)', marginBottom: 8 }}>
                  TODAY&apos;S LEARNING PLAN
                </div>
                <h3 style={{ margin: 0, fontSize: 20 }}>Aarav · Mathematics</h3>
                <p style={{ color: 'var(--ink-soft)', fontSize: 13, lineHeight: 1.5 }}>
                  Practice fractions using a 15-minute activity matched to his current level.
                </p>
                <div className={styles.miniRow}>
                  <div className={styles.miniCard}>
                    <span className={styles.t}>Level</span>
                    <span className={styles.s}>Grade 5</span>
                  </div>
                  <div className={styles.miniCard}>
                    <span className={styles.t}>Focus</span>
                    <span className={styles.s}>Fractions</span>
                  </div>
                  <div className={styles.miniCard}>
                    <span className={styles.t}>Time</span>
                    <span className={styles.s}>15 min</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.problem}>
          <h2>Volunteers do not need more paperwork. They need the right context at the right moment.</h2>
          <p>
            Saarthi turns scattered observations and limited preparation time into practical,
            child-specific guidance that a volunteer can actually use during a session.
          </p>
        </section>

        <section className={styles.features}>
          <div className={styles.featureRow}>
            <div className={styles.featureText}>
              <div className={styles.featureNum}>01</div>
              <h3>Know the child before the session starts.</h3>
              <p>
                Keep a simple learning profile with recent observations, strengths, gaps,
                and the next skill worth practising.
              </p>
            </div>
            <div className={styles.featureVisual} style={{ background: '#f0effb' }}>
              <div className={styles.miniRow}>
                <div className={styles.miniPill} style={{ background: '#ffffff' }}>
                  <span className={styles.n}>82%</span>
                  <span className={styles.l}>READING</span>
                </div>
                <div className={styles.miniPill} style={{ background: '#ffffff' }}>
                  <span className={styles.n}>64%</span>
                  <span className={styles.l}>MATH</span>
                </div>
                <div className={styles.miniPill} style={{ background: '#ffffff' }}>
                  <span className={styles.n}>↑ 12%</span>
                  <span className={styles.l}>PROGRESS</span>
                </div>
              </div>
            </div>
          </div>

          <div className={`${styles.featureRow} ${styles.reverse}`}>
            <div className={styles.featureText}>
              <div className={styles.featureNum}>02</div>
              <h3>Generate an activity that fits the moment.</h3>
              <p>
                Give the volunteer a focused activity instead of a generic worksheet,
                with difficulty and timing grounded in the child&apos;s profile.
              </p>
            </div>
            <div className={styles.featureVisual} style={{ background: '#fff5e6' }}>
              <div className={styles.miniTable}>
                <div className={styles.miniTableRow}><span>Warm-up</span><strong>3 min</strong></div>
                <div className={styles.miniTableRow}><span>Core activity</span><strong>9 min</strong></div>
                <div className={styles.miniTableRow}><span>Quick check</span><strong>3 min</strong></div>
              </div>
            </div>
          </div>

          <div className={styles.featureRow}>
            <div className={styles.featureText}>
              <div className={styles.featureNum}>03</div>
              <h3>Leave every session with a useful next step.</h3>
              <p>
                Capture what happened, turn it into a lightweight progress signal,
                and make the next volunteer session easier to prepare.
              </p>
            </div>
            <div className={styles.featureVisual} style={{ background: '#eaf8f4' }}>
              <div className={styles.miniReco}>
                <div className={styles.h}>SAARTHI RECOMMENDS</div>
                <div className={styles.b}>
                  Revisit equivalent fractions next session, then move to comparison
                  once the child reaches 80% accuracy.
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.workflow} id="workflow">
          <h2>From check-in to next session.</h2>
          <div className={styles.flowRow}>
            {[
              ['1', 'Check in', 'Open the child profile.'],
              ['2', 'Understand', 'See current strengths and gaps.'],
              ['3', 'Prepare', 'Get a focused activity.'],
              ['4', 'Teach', 'Run the session with guidance.'],
              ['5', 'Reflect', 'Save the next useful step.'],
            ].map(([n, title, description], index) => (
              <div className={styles.flowStep} key={n}>
                <div className={styles.n}>{n}</div>
                {index < 4 && <div className={styles.flowLine} />}
                <div className={styles.t}>{title}</div>
                <div className={styles.d}>{description}</div>
              </div>
            ))}
          </div>
        </section>

        <footer className={styles.footer}>
          <div className={styles.statusPill}>
            <span className={styles.statusDot} />
            Built for volunteers, designed around children
          </div>
          <div className={styles.credit}>
            Saarthi — AI Volunteer Copilot<br />
            Making every volunteer hour count.
          </div>
        </footer>
      </div>
    </main>
  );
}
