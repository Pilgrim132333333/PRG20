# Local Setup Guide (Quick Version)

## 1. Database (SQL)

1. **Start MySQL** (ensure the local MySQL service is running).
2. **Create the database** (name must match `DB_NAME` in the project root `.env`; default is `pga_platform`):
   ```sql
   CREATE DATABASE IF NOT EXISTS pga_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   USE pga_platform;
   ```
3. **Run the schema script** (adjust the path to match your machine):
   ```bash
   mysql -u your_user -p pga_platform < backend/init_schema.sql
   ```
4. **(Optional) Import sample data**: after configuring `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in the project root `.env`, run:
   ```bash
   python backend/seed_data.py
   ```

---

## 2. Start the Back End (FastAPI)

1. Enter the back-end directory and install dependencies (first time only):
   ```bash
   cd fastapi-backend
   pip install -r requirements.txt
   ```
2. Verify the database connection:
   ```bash
   python check_db.py
   ```
   Confirm you see **OK** before continuing.
3. Start the server (default port `8000`):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open `http://127.0.0.1:8000/` in a browser. If it returns JSON, the back end is up.

---

## 3. Access the Front End

- **Option A**: Open the static page directly in your browser (adjust path to your machine):  
  `vue-frontend/index.html` (home) → Login / Sign up → `student.html`
- **Option B**: Serve `vue-frontend/` with a local static server (avoids `file://` restrictions in some browsers):
  ```bash
  cd vue-frontend
  python -m http.server 8080
  ```
  Then open `http://127.0.0.1:8080/index.html` in your browser.

The front-end API base URL is `http://127.0.0.1:8000/api` — keep it consistent with the back-end port.
