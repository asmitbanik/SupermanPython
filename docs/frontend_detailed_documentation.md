# SupermanPython Frontend Documentation

This document provides detailed documentation for each main JavaScript/TypeScript file in the `frontend` directory of the SupermanPython project. It covers the purpose, main components/functions, and usage of each file.

---

## 1. next.config.js

**Purpose:**
- Next.js configuration file.
- Enables React strict mode and experimental app directory support.

**Key Elements:**
- `reactStrictMode: true`: Activates additional React checks.
- `experimental: { appDir: true }`: Enables the `/app` directory for routing and layouts.

---

## 2. pages/index.js

**Purpose:**
- Main landing page for the app (traditional Next.js pages directory).
- Provides a UI for asking questions and displaying answers/context.

**Key Elements:**
- Uses React state for `question` and `answer`.
- `askQuestion`: Sends a POST request to `/api/ask` with the user's question.
- Renders `AnswerBox` and `ContextBox` components.

---

## 3. components/AnswerBox.js

**Purpose:**
- Displays the answer returned from the backend.

**Key Elements:**
- Receives `answer` as a prop and renders it inside a styled box.

---

## 4. components/ContextBox.js

**Purpose:**
- Placeholder for displaying relevant context to the user.

**Key Elements:**
- Static content indicating where context will appear.

---

## 5. pages/api/ask.js

**Purpose:**
- Next.js API route for handling question requests from the frontend.
- Proxies requests to the backend Flask API.

**Key Elements:**
- Handles POST requests by forwarding them to `http://localhost:5000/api/ask`.
- Returns the backend's response to the frontend.
- Returns 405 for unsupported methods.

---

## 6. app/page.tsx

**Purpose:**
- Main page for the app using the Next.js `/app` directory (modern approach).
- Provides a UI for indexing a GitHub repo and asking questions with citations.

**Key Elements:**
- Uses React state for `repo`, `question`, `answer`, `cites`, and status messages.
- `doIndex`: Sends a POST request to the backend to index a GitHub repo.
- `ask`: Sends a POST request to the backend to ask a question about the repo.
- Displays answer and citations with styled UI.
- Uses environment variable for backend URL (supports deployment flexibility).

---

## 7. app/api/ask/route.ts

**Purpose:**
- Optional proxy route for Next.js API if deploying frontend and backend together.
- Can be used to forward requests to the backend from the Next.js app directory.

**Key Elements:**
- Example POST handler (commented out) for forwarding requests to the backend.
- Returns a placeholder response if not implemented.

---

# End of Documentation
