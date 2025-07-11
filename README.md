# ⛺️ Get The Camp Site(s)

**Get The Camp Site(s)**
Is a project that was recommended to me
by a family member who struggled to be able to book competitive camping sites.
This inspired me to go on a self-hackathon over a weekend to see if I could create
an application that could not only allow him to book sites way ahead of time via a queue
system, but also compete with actual humans to get a spot at popular campgrounds. 
---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Next.js (TypeScript) + React.js
- **Message Queue:** Celery
- **Message Broker:** Redis
- **Email:** SMTP for notifications of adding sites to cart

---

## ✨ Features

- Frontend to send requests
- Backend route to trigger worker
- Task function featuring the ability to sign in, go to specified campground, and reserve sites
- Captcha solver

---

## 🔨 Improvable Areas
- Better captcha solver: Main bottle neck of workflow as current captcha solver only solves about 40% of time.
- Increased server memory and CPU power, currently runs on t420 with dual core processor and ~4gb ram.
---

## 🧑‍💻 Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis server
- SMTP credentials (for email features)

### Backend (Python)

```bash
- py -m venv venv_name
- source venv_name/bin/activate
- py -m pip install requirements.txt
- uvicorn submit_api:app --reload
```

## Frontend (Next.js)
```bash
npm install
npm run dev
```

## Misc.
- startup of redis server is expected
- application assumes a worked with concurrency 5 has also been started.
