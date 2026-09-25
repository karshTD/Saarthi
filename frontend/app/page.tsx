// frontend/app/page.tsx
'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import styles from './page.module.css';

export default function LandingPage() {
  const router = useRouter();

  return (
    <main className={styles.main}>
      <div className={styles.hero}>
        <h1 className={styles.title}>Welcome to Your Workspace</h1>
        <p className={styles.subtitle}>
          Your central hub for tracking, analytics, and management.
        </p>
        <div className={styles.ctaGroup}>
          <button 
            className={styles.primaryButton} 
            onClick={() => router.push('/dashboard')}
          >
            Go to Dashboard
          </button>
          <button 
            className={styles.secondaryButton} 
            onClick={() => router.push('/dashboard?tab=settings')}
          >
            View Settings
          </button>
        </div>
      </div>
    </main>
  );
}
