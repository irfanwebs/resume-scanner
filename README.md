# ResumeAI - AI-Powered Resume Screener & Feedback Tool

An intelligent resume analysis tool that provides real-time feedback on your resume against specific job descriptions. Built with **SvelteKit + TypeScript** on the frontend and **FastAPI + Python** on the backend, powered by Claude AI.

## What It Does

Upload your PDF resume and paste a job description. ResumeAI will:

- **Keyword Match Scoring** - Identifies missing and matched keywords between your resume and the target JD
- **Weak Phrase Detection** - Highlights vague or passive language with stronger alternatives
- **Actionable Suggestions** - Provides structured, prioritised feedback to improve your resume
- **Real-time Analysis** - Streams AI feedback as it's generated for a responsive UX

## Tech Stack

### Frontend
- **SvelteKit** with TypeScript
- **TailwindCSS** for styling
- Drag-and-drop PDF upload with progress states
- Server-Sent Events (SSE) for streaming AI responses

### Backend
- **FastAPI** (Python)
- **PyMuPDF** for PDF text extraction
- **Anthropic Claude API** for AI-powered analysis
- Streaming responses via SSE

### Infrastructure
- Frontend deployed on **Vercel**
- Backend deployed on **Railway** / **Fly.io**
- CI/CD via **GitHub Actions**

## Project Structure

```
resume-screener/
├── frontend/               # SvelteKit app
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/ # Svelte components
│   │   │   ├── stores/     # Svelte stores for state management
│   │   │   ├── types/      # TypeScript interfaces
│   │   │   └── utils/      # Helper functions
│   │   └── routes/         # SvelteKit routes
│   ├── static/
│   ├── svelte.config.js
│   ├── tailwind.config.js
│   └── package.json
├── backend/                # FastAPI app
│   ├── app/
│   │   ├── main.py         # FastAPI entry point
│   │   ├── services/
│   │   │   ├── pdf_parser.py
│   │   │   └── ai_analyser.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- Anthropic API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env file
echo "PUBLIC_API_URL=http://localhost:8000" > .env

# Run dev server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to see the app.

## Design Decisions

- **Streaming over polling**: SSE gives users instant feedback as the AI analyses their resume, rather than waiting for a full response.
- **No auth, no database**: Intentionally kept simple. Resumes are processed in-memory and never stored. Privacy by design.
- **Component-driven UI**: Each feedback section (keywords, weak phrases, suggestions) is an isolated Svelte component with its own state.
- **Accessible by default**: Keyboard navigation, ARIA labels, and screen reader support throughout.

## License

MIT
