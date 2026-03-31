# 5 Software Design

This chapter presents the architectural and implementation design decisions of the **AI Programming Question Bank** application. It outlines the programming languages, frameworks, and data organisation used on the server and client, summarises the rationale for a RESTful service layer, describes the student-facing user interface, and explains the testing approaches employed during development.

---

## 5.1 Architectural Design Decisions

Architectural design explains how the system is partitioned and how its parts cooperate. Somerville argues that **compactness**, **performance**, **availability** (in the sense of evolvability and ease of adding features), **security**, and **maintainability** are central concerns when choosing an architecture [26]. **Compactness** here means that components fit together with minimal duplication and each layer has a clear responsibility. **Performance** covers response times for typical API calls and page interactions. **Availability** is interpreted as the team’s ability to extend the system (e.g., new routes or UI sections) without redesigning the whole stack. **Maintainability** depends on modular code, predictable naming, and documentation (e.g., OpenAPI). **Security** covers credential storage, transport assumptions, and separation of public static assets from authenticated API usage. The following subsections justify the main choices for this project.

### 5.1.1 Three-tier layout: browser, application server, database

The system follows a **classic three-tier pattern**: (1) a **presentation tier** implemented as static HTML pages with client-side JavaScript; (2) an **application tier** implemented in **Python** using **FastAPI**; and (3) a **data tier** using **MySQL** as a relational database. This separation aligns with Somerville’s maintainability criterion: the front end can be adjusted independently of SQL or PDF generation logic, and database schema evolution is localised to migrations and SQL scripts. Compared with an all-in-one monolith in a single scripting file, the split keeps responsibilities **compact** and errors easier to localise.

### 5.1.2 FastAPI and Python for the application tier

**FastAPI** is an asynchronous-capable web framework for Python that exposes HTTP endpoints and automatically generates **OpenAPI** documentation [33]. For this project, database access is implemented primarily with **synchronous** SQLAlchemy sessions (using `pymysql`), which is sufficient for coursework scale and keeps the mental model simple. Python was chosen for rapid development, readable syntax, and rich ecosystem libraries (ORM, password hashing, HTTP client for AI providers, PDF generation). The framework’s **router** mechanism maps URI prefixes (`/api/questions`, `/api/auth`, etc.) to cohesive modules, which supports **maintainability** and matches the REST style described in §5.1.4.

### 5.1.3 Static multi-page front end (HTML, Tailwind CDN, Vanilla JavaScript)

Unlike a single-page application (SPA) built with Angular or React, the **student portal** is delivered as **multiple HTML documents** (`login.html`, `signup.html`, `student.html`, etc.) augmented with **Tailwind CSS** via CDN and plain `fetch()` calls to the API. This choice trades the unified component model of an SPA for **simplicity** and **fast onboarding**: there is no build step, and each page loads only the scripts it needs. **Performance** for interactive features (filters, charts, AI chat) depends on efficient DOM updates in JavaScript rather than a virtual DOM framework; for the intended user base and page complexity, this remains acceptable. **Cross-origin** access is handled by enabling CORS on the API and by serving pages over `http://localhost` rather than `file://`, which avoids browser restrictions on API calls.

### 5.1.4 MySQL as the relational data store

**MySQL** is used as the primary relational DBMS. Entities such as **Questions**, **Materials**, **Users**, and associative tables (**Question_Material_Link**, **User_Question_State**) are modelled with **primary and foreign keys**, preserving referential integrity and supporting transactional updates. Relational modelling fits the domain naturally: questions link to many materials, and each user has many per-question flags (favourite, completed). MySQL’s maturity, tooling, and compatibility with standard SQL scripts (`init_schema.sql`, optional `clear_all_data.sql`, CSV seeding) support **maintainability** and team collaboration.

Deployment for local development uses a **MySQL instance** on the developer machine; production could follow a **Linux** host with MySQL and a process manager for **Uvicorn** (ASGI server). The sample chapter’s **LAMP** stack emphasised PHP; here **Python** replaces PHP while retaining **MySQL** and a conventional web server arrangement (static files + reverse proxy to the API if desired).

### 5.1.5 RESTful API design

The backend exposes a **REST-oriented** HTTP API under the `/api` prefix. **REST** encourages **stateless** request handling: each HTTP request carries enough information (e.g., `user_id` as a query parameter where implemented) for the server to complete the operation without server-side session storage for every route [46]. Stateless handlers simplify horizontal scaling and debugging, because failures can be reproduced from a single request. Resources are grouped by noun-like paths (`/questions`, `/materials`, `/auth`, `/ai`), and HTTP methods express intent (`GET` for reads, `POST` for creation or chat, `PUT` / `DELETE` for updates). FastAPI’s automatic **OpenAPI** schema at `/docs` lowers the cost of **manual testing** and integration.

---

## 5.2 Implementation Design Decisions

### 5.2.1 Project structure and naming conventions

The repository separates concerns into **`fastapi-backend/`** (application code), **`backend/`** (SQL scripts, CSV templates, static material files), and **`vue-frontend/`** (static HTML/CSS/JS pages—despite the folder name, the implementation is not the Vue.js framework). Python modules follow conventional **package layout**: `app/main.py` registers routers; `app/api/routes/` holds one file per domain (`questions.py`, `auth.py`, `ai.py`, …); `app/models/`, `app/crud/`, and `app/services/` isolate persistence and cross-cutting logic (e.g., PDF building, AI context assembly). This structure limits **merge conflicts** and helps new contributors find code by feature area.

### 5.2.2 User authentication, validation, and password protection

**Authentication** verifies identity; **authorisation** determines which actions a user may perform [48]. The current implementation provides **registration** and **login** endpoints that validate usernames, emails (via Pydantic’s `EmailStr`), and passwords with length constraints. Passwords are never stored in plain text: **bcrypt** hashing via **passlib** produces a one-way **password hash** stored in `Users.password_hash`. On login, the submitted password is verified against this hash using a constant-time comparison inside the library, which mitigates trivial timing leaks compared with manual string equality.

The login response returns **user metadata** (`user_id`, `username`, `email`, `role`). The front end persists **`user_id`** (e.g., in `localStorage`) and supplies it on subsequent API calls (e.g., as `user_id` query parameters for favourites and completion). This is a **lightweight, token-free** pattern suitable for coursework; a production system would typically issue **JSON Web Tokens (JWT)** [50] or use secure HTTP-only cookies and server-side sessions to reduce the risk of **client-side identifier tampering**. Email verification and a full **role hierarchy** (admin vs student) are **out of scope** in the baseline codebase but could extend the same router structure.

### 5.2.3 AI assistant: context construction and LLM integration

The **AI assistant** is not implemented as a long-lived WebSocket chat server. Instead, each **chat request** is **stateless** at the HTTP level: the client sends a short **message history**; the server rebuilds a **structured context string** from MySQL (questions, materials metadata, user favourites) using `build_ai_session_context`, then calls an **OpenAI-compatible** HTTP API (`POST .../chat/completions`) with configurable base URL, model name, and API key. This design **decouples** the teaching platform from any single vendor: the same client code path can target DeepSeek, OpenAI, or other compatible endpoints by configuration.

From a **performance** perspective, latency is dominated by the external LLM round-trip; the server therefore uses **timeouts** and keeps DB queries focused on the current user. From a **security** perspective, API keys reside in environment variables (e.g., `AI_API_KEY`) and must not be committed to version control.

### 5.2.4 Relational modelling: questions, materials, and user progress

Rather than modelling discussion threads as trees with **Union–Find**, this system models **bibliographic** relationships: **many-to-many** links between questions and materials live in **`Question_Material_Link`**, while **`User_Question_State`** stores per-user **favourite** and **completed** flags. Queries such as “all materials for question *q*” reduce to joins or filtered lookups on the link table—**O(n)** in the number of related rows for typical page sizes, without needing graph algorithms. This matches the domain: the primary operations are **filter**, **list**, **download**, and **export**, not recursive thread traversal.

### 5.2.5 PDF export and document generation

Selected questions can be merged into a single **PDF** on the server using **ReportLab** (`build_questions_pdf`). The endpoint accepts a list of **question IDs**, loads the corresponding rows, and streams a generated binary response. This centralises layout logic on the server so that exports remain consistent regardless of browser differences—assisting **maintainability** and reproducibility for coursework hand-ins.

### 5.2.6 User interface (student portal)

The **student** interface uses a **dark-themed**, card-based layout inspired by modern AI product UIs: a **sidebar** switches between **console** (dashboard metrics), **Question** browsing, **Coursework**, **Question Bank** (including multi-select and PDF export), and an **embedded AI chat** panel with Markdown rendering and sanitisation (**marked** + **DOMPurify**) to reduce XSS risk when displaying model output. **Chart.js** supports progress visualisation on the dashboard. The UI favours **clear typographic hierarchy** (Inter font), **consistent accent colour** (green), and **iconography** (Font Awesome) for scanability. Forms and filters reuse shared CSS utility classes (`input-gpt`, cards, transitions) to keep the experience **compact** visually and in code.

---

## 5.3 Testing Methodologies

At the time of writing, the repository does **not** ship an automated **pytest** suite; quality assurance relies primarily on **manual and exploratory testing** aligned with internal runbooks (`测试文档.md`, `README.md`):

1. **Environment and connectivity tests**: verify MySQL is reachable with credentials from `.env`, run `init_schema.sql` (or migrations), optionally `seed_data.py`, then start **Uvicorn** and confirm `GET /` returns the expected JSON payload.  
2. **API contract tests**: use FastAPI’s **`/docs`** Swagger UI to exercise `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/questions`, favourite and completion endpoints, material download URLs, `POST /api/questions/export-pdf`, and `POST /api/ai/chat` (with a valid `AI_API_KEY`).  
3. **UI tests**: load the front end via a **local static server** (not `file://`), walk through login → student dashboard → question filtering → PDF export → AI panel; verify `localStorage` holds `user_id` and that API base URLs match the running backend port.  
4. **Regression checks**: after schema changes, re-run seeding or truncation scripts and confirm PDF and AI features still operate on non-empty datasets.

This methodology prioritises **critical-path** validation under coursework time constraints. A natural **future improvement** is to add automated API tests (e.g., `httpx.AsyncClient` against a test database) and front-end smoke tests, reducing repeated manual effort.

---

## References (placeholders — replace with your course bibliography)

[26] I. Somerville, *Software Engineering* (or equivalent edition), Pearson.  
[33] FastAPI documentation — OpenAPI / automatic API docs.  
[46] R. T. Fielding, “Architectural Styles and the Design of Network-based Software Architectures,” doctoral dissertation, 2000 (REST / statelessness).  
[48] Standard distinction between authentication and authorization in security textbooks.  
[50] JWT specification (RFC 7519) — cited for contrast with the project’s current tokenless client pattern.

*(Add MySQL, bcrypt, ReportLab, and Tailwind citations as required by your programme.)*

---

*Chapter drafted to mirror the structure of the exemplar “Software Design” section (architectural rationale → implementation details → testing), while describing this repository’s actual stack: FastAPI + SQLAlchemy + MySQL + static HTML/JS/Tailwind front end.*
