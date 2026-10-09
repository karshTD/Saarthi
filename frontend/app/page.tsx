import Link from "next/link";
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main>
      <nav className={`${styles.wrap} ${styles.nav}`}>
        <div className={styles.wordmark}>
          saa<span>rthi</span>
        </div>
        <Link href="/dashboard" className={styles.navCta}>
          See the dashboard
        </Link>
      </nav>

      <section className={`${styles.wrap} ${styles.hero}`}>
        <div className={styles.heroText}>
          <h1>Every child learns differently. Now every lesson can too.</h1>
          <p>
            Saarthi helps NGO volunteers turn limited prep time into personalized
            lessons — pitched at every child&apos;s level, with a clear plan for
            the next session.
          </p>
          <div className={styles.heroCtas}>
            <Link href="/dashboard" className={styles.btnPrimary}>
              See the dashboard
            </Link>
            <a href="#how-it-works" className={styles.btnSecondary}>
              How it works
            </a>
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.mockupFrame}>
            <div className={styles.mockupTopbar}>
              <span style={{ background: "#F2A93B" }} />
              <span style={{ background: "#6C7FD8" }} />
              <span style={{ background: "#4FBFA8" }} />
            </div>
            <Image
              src="/dashboard-preview.png"
              alt="Preview of the Saarthi volunteer dashboard"
              width={1400}
              height={740}
              style={{ width: "100%", height: "auto" }}
              priority
            />
          </div>
        </div>
      </section>

      <section className={`${styles.wrap} ${styles.problem}`}>
        <h2>Most volunteer sessions start from zero.</h2>
        <p>
          One hour, a dozen children, three or four different starting points
          — and rarely enough time left to plan for all of them at once.
          Saarthi doesn&apos;t replace the volunteer. It gives that hour a
          running start.
        </p>
      </section>

      <section id="how-it-works" className={`${styles.wrap} ${styles.features}`}>
        <div className={styles.featureRow}>
          <div className={styles.featureText}>
            <div className={styles.featureNum}>Before the session</div>
            <h3>Understand the class</h3>
            <p>
              Saarthi looks at how each child has been doing and groups them
              by what they&apos;re ready for — so planning starts from where
              the class actually is, not a guess.
            </p>
          </div>
          <div className={styles.featureVisual} style={{ background: "#EEF0FC" }}>
            <div className={styles.miniRow}>
              <div className={styles.miniPill} style={{ background: "#FDECE3" }}>
                <span className={styles.n} style={{ color: "#E0703C" }}>3</span>
                <span className={styles.l} style={{ color: "#E0703C" }}>STRUGGLING</span>
              </div>
              <div className={styles.miniPill} style={{ background: "#E9EDFC" }}>
                <span className={styles.n} style={{ color: "#6C7FD8" }}>4</span>
                <span className={styles.l} style={{ color: "#6C7FD8" }}>ON TRACK</span>
              </div>
              <div className={styles.miniPill} style={{ background: "#E4F6F1" }}>
                <span className={styles.n} style={{ color: "#4FBFA8" }}>3</span>
                <span className={styles.l} style={{ color: "#4FBFA8" }}>ADVANCED</span>
              </div>
            </div>
          </div>
        </div>

        <div className={`${styles.featureRow} ${styles.reverse}`}>
          <div className={styles.featureText}>
            <div className={styles.featureNum}>Planning the lesson</div>
            <h3>Teach at every level</h3>
            <p>
              One topic, three sets of activities — so a child who&apos;s
              struggling and a child who&apos;s ready to move ahead are both
              working on something that fits.
            </p>
          </div>
          <div className={styles.featureVisual} style={{ background: "#FDF0DC" }}>
            <div className={styles.miniRow}>
              <div className={styles.miniCard}>
                <div className={styles.t}>Visual model</div>
                <div className={styles.s}>Struggling</div>
              </div>
              <div className={styles.miniCard}>
                <div className={styles.t}>Numeric drill</div>
                <div className={styles.s}>On Track</div>
              </div>
              <div className={styles.miniCard}>
                <div className={styles.t}>Simplify &amp; extend</div>
                <div className={styles.s}>Advanced</div>
              </div>
            </div>
          </div>
        </div>

        <div className={styles.featureRow}>
          <div className={styles.featureText}>
            <div className={styles.featureNum}>During the session</div>
            <h3>Run it without losing the thread</h3>
            <p>
              Log responses as the session happens, so nothing has to be
              reconstructed from memory afterward.
            </p>
          </div>
          <div className={styles.featureVisual} style={{ background: "#E9F8F3" }}>
            <div className={styles.miniTable}>
              <div className={styles.miniTableRow}>
                <span>Diya</span>
                <span style={{ color: "#6C7FD8", fontWeight: 700 }}>On Track · 85%</span>
              </div>
              <div className={styles.miniTableRow}>
                <span>Vivaan</span>
                <span style={{ color: "#4FBFA8", fontWeight: 700 }}>Advanced · 95%</span>
              </div>
              <div className={styles.miniTableRow}>
                <span>Aarav</span>
                <span style={{ color: "#E0703C", fontWeight: 700 }}>Struggling · 60%</span>
              </div>
            </div>
          </div>
        </div>

        <div className={`${styles.featureRow} ${styles.reverse}`}>
          <div className={styles.featureText}>
            <div className={styles.featureNum}>After the session</div>
            <h3>Know what&apos;s next</h3>
            <p>
              A plain-language summary of what each child needs next time —
              so progress carries forward, even between different volunteers.
            </p>
          </div>
          <div className={styles.featureVisual} style={{ background: "#EEF0FC" }}>
            <div className={styles.miniReco}>
              <div className={styles.h}>NEXT SESSION RECOMMENDATION</div>
              <div className={styles.b}>
                3 children are ready for unlike fractions. 3 need another
                visual pass on the core concept first.
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={`${styles.wrap} ${styles.workflow}`}>
        <h2>How a session moves through Saarthi</h2>
        <div className={styles.flowRow}>
          {[
            { t: "Pick a class", d: "Choose who you're teaching today." },
            { t: "Plan the lesson", d: "Generated from the topic and each child's level." },
            { t: "Teach & assess", d: "Run the activities, log how it went." },
            { t: "Update progress", d: "Each child's record reflects today." },
            { t: "See what's next", d: "A recommendation for the next session." },
          ].map((step, i) => (
            <div className={styles.flowStep} key={step.t}>
              {i < 4 && <div className={styles.flowLine} />}
              <div className={styles.n}>{i + 1}</div>
              <div className={styles.t}>{step.t}</div>
              <div className={styles.d}>{step.d}</div>
            </div>
          ))}
        </div>
      </section>

      <footer className={`${styles.wrap} ${styles.footer}`}>
        <div className={styles.statusPill}>
          <span className={styles.statusDot} />
          Prototype · in active development
        </div>
        <div className={styles.credit}>
          Built by Utkarsh, an individual volunteer at
          <br />A Ray of Hope Charitable Trust
        </div>
      </footer>
    </main>
  );
}
