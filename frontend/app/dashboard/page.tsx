// frontend/app/dashboard/page.tsx
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './dashboard.module.css';

export default function DashboardPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'reports' | 'settings'>('overview');

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className={styles.moduleCard}>
            <h2>Dashboard Overview</h2>
            <p>Welcome back! Here is a summary of your recent activities.</p>
            <div className={styles.metricsGrid}>
              <div className={styles.metricBox}>
                <h3>Total Active Tasks</h3>
                <p className={styles.metricValue}>12</p>
              </div>
              <div className={styles.metricBox}>
                <h3>System Status</h3>
                <p className={styles.metricValue} style={{ color: '#22c55e' }}>Operational</p>
              </div>
            </div>
          </div>
        );
      case 'analytics':
      case 'reports':
      case 'settings':
        return (
          <div className={styles.moduleCard}>
            <h2>Work in Progress</h2>
            <p>The <strong>{activeTab.toUpperCase()}</strong> module is currently under active development.</p>
            <div className={styles.wipBox}>
              <span className={styles.badge}>Coming Soon</span>
              <p>Expected features include real-time data filtering, export tools, and custom configurations.</p>
              <button 
                className={styles.actionButton}
                onClick={() => alert('You will be notified when this feature launches!')}
              >
                Request Early Access
              </button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.dashboardContainer}>
      {/* Sidebar Navigation */}
      <aside className={styles.sidebar}>
        <h2 className={styles.logo} onClick={() => router.push('/')}>Workspace</h2>
        <nav className={styles.nav}>
          <button 
            className={activeTab === 'overview' ? styles.activeNavBtn : styles.navBtn}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button 
            className={activeTab === 'analytics' ? styles.activeNavBtn : styles.navBtn}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics
          </button>
          <button 
            className={activeTab === 'reports' ? styles.activeNavBtn : styles.navBtn}
            onClick={() => setActiveTab('reports')}
          >
            Reports
          </button>
          <button 
            className={activeTab === 'settings' ? styles.activeNavBtn : styles.navBtn}
            onClick={() => setActiveTab('settings')}
          >
            Settings
          </button>
        </nav>
        <div className={styles.sidebarFooter}>
          <button className={styles.logoutBtn} onClick={() => router.push('/')}>
            Back to Home
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className={styles.mainContent}>
        <header className={styles.header}>
          <h1>Dashboard</h1>
          <div className={styles.userProfile}>
            <span>Utkarsh Singh</span>
          </div>
        </header>
        <section className={styles.contentBody}>
          {renderContent()}
        </section>
      </main>
    </div>
  );
}
