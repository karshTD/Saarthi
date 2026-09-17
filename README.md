# Saarthi — AI Volunteer Copilot

> **Plan better. Teach smarter. Make every session count.**

Saarthi is an AI-powered teaching assistant designed for NGO volunteers working with children with diverse learning levels.

It helps volunteers move from **class planning → personalized lesson generation → interactive assessment → session analysis → next-session recommendations** through a single workflow.

The project is being developed as a deployable prototype, with the current implementation focused on demonstrating the product experience and core AI-assisted workflow.

---

## Problem

NGO volunteers often work with limited preparation time and classrooms where students have different levels of understanding.

Preparing a lesson, creating activities for different ability levels, conducting an assessment, and deciding what to teach next can become repetitive and time-consuming.

Saarthi aims to reduce this workload while keeping the volunteer in control of the teaching process.

---

## What Saarthi Does

### AI-Assisted Lesson Planning

Volunteers provide the subject, topic, class profile, duration, language, and available resources. Saarthi generates a structured lesson plan around those constraints.

### Class Analysis

The system analyzes existing student performance to identify learning gaps and classify students by their current level of understanding.

### Differentiated Activities

Activities can be generated at different difficulty levels so that students who need additional support and students who are ready for more challenging problems can work on the same underlying concept.

### Interactive Sessions

Volunteers can conduct activities and assessments directly through the platform while recording student responses.

### Session Intelligence

After a session, Saarthi summarizes class performance, identifies areas requiring reinforcement, and recommends what should be addressed in the next session.

### Resource-Grounded Generation

The AI layer can retrieve relevant information from approved educational resources before generating lesson content, reducing reliance on generic LLM responses.

---

## Core Workflow

```text
Volunteer
    │
    ▼
Class Selection
    │
    ▼
Session Configuration
    │
    ▼
Class Analysis
    │
    ▼
Resource Retrieval
    │
    ▼
AI Lesson Generation
    │
    ▼
Differentiated Activities
    │
    ▼
Interactive Session
    │
    ▼
Assessment
    │
    ▼
Progress Update
    │
    ▼
Next Session Recommendation
```

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   React / Next.js   │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                            REST API
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │     Python API      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        PostgreSQL         AI Services         FAISS
              │                │                │
              │          ┌─────┴─────┐          │
              │          ▼           ▼          │
              │       Planner     Analyzer      │
              │          │           │          │
              │          └─────┬─────┘          │
              │                ▼                │
              │               LLM ◄─────────────┘
              │
              ▼
        Student Progress
```

The backend follows a modular-monolith architecture rather than splitting the prototype into unnecessary microservices.

---

## Technology Stack

### Frontend

* React / Next.js
* TypeScript
* Responsive UI
* REST API integration

### Backend

* Python
* FastAPI
* Pydantic
* REST APIs

### Data

* PostgreSQL
* SQLAlchemy
* Database migrations

### AI / ML

* LLM-based structured generation
* Retrieval-Augmented Generation (RAG)
* SentenceTransformers
* FAISS

### Infrastructure

* Docker
* Git / GitHub
* Cloud deployment

---

## Project Structure

```text
saarthi/
│
├── frontend/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ai/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── db/
│   │   └── core/
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── resources/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## Running Locally

### Prerequisites

* Node.js
* Python 3.11+
* PostgreSQL
* Git
* Docker (recommended)

### Clone

```bash
git clone <repository-url>
cd saarthi
```

### Backend

```bash
cd backend

python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables using `.env.example`.

Start the API:

```bash
uvicorn app.main:app --reload
```

The API documentation will be available through FastAPI's generated documentation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=
LLM_API_KEY=
SECRET_KEY=
CORS_ORIGINS=
```

Never commit API keys, passwords, tokens, or production credentials to Git.

---

## Prototype Scope

The current prototype prioritizes:

* A polished volunteer-facing interface
* A complete end-to-end demonstration workflow
* Real FastAPI APIs
* Persistent application data
* AI-assisted lesson generation
* Resource retrieval
* Interactive assessment
* Student progress tracking
* Deployment readiness

The initial demonstration focuses on **Mathematics and Fractions**. The underlying workflow is designed to support additional subjects and educational resources in future iterations.

---

## Responsible AI

Saarthi is designed as a **copilot for human volunteers**, not as a replacement for educators.

AI-generated lesson plans and educational material should be reviewed by the volunteer before being used with students.

The prototype uses synthetic learner data for development and demonstration. Personal or sensitive information should not be collected unless it is necessary for the application's educational purpose and appropriately protected.

---

## Future Development

Potential future iterations include:

* Additional subjects
* Multilingual lesson generation
* Voice-assisted interaction
* Expanded educational resource libraries
* Improved learner analytics
* Volunteer feedback loops
* More sophisticated personalization
* Production-scale monitoring and evaluation

---

## Status

**Prototype / Active Development**

Saarthi is being developed as a service-learning project in collaboration with an NGO focused on supporting and educating children in need.

---

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
