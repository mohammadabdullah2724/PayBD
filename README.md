# 🤖 PayBD — AI Coding Instruction

> **How to use:** Paste this file as a system prompt at the start of any AI coding session, OR upload it directly to Claude/ChatGPT as a reference file. All rules apply for the entire session unless you explicitly override them in chat.

**Stack:** FastAPI · Next.js 14 · PostgreSQL · Redis · Celery  
**Compliance:** Bangladesh Labour Act 2006  
**Dev Env:** GitHub Codespaces  
**Version:** 1.0 — Pavel Digital Solutions

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Directory Structure](#3-project-directory-structure)
4. [Coding Rules & Conventions](#4-coding-rules--conventions)
5. [PayBD Domain Logic (BLA 2006)](#5-paybd-domain-logic-bla-2006)
6. [API Design Rules](#6-api-design-rules)
7. [How AI Must Respond](#7-how-ai-must-respond)
8. [Current Development Status](#8-current-development-status)
9. [Environment Variables Reference](#9-environment-variables-reference)
10. [Common Dev Commands](#10-common-dev-commands)
11. [Quick Cheat Sheet](#11-quick-cheat-sheet)

---

## 1. Project Overview

| Property | Value |
|---|---|
| **Project Name** | PayBD — Bangladesh Payroll Management SaaS |
| **Developer** | Mohammad (Junior Payroll Officer, Accenture Footwear & Leather Products Ltd.) |
| **Purpose** | Automate payroll for Bangladeshi businesses, compliant with Bangladesh Labour Act 2006 |
| **Stage** | Active development — backend running, frontend auth in progress |
| **Dev Environment** | GitHub Codespaces (low-RAM — always write RAM-efficient code) |
| **Deployment Target** | Cloud SaaS — paybd.com.bd |
| **Side Brand** | Pavel Digital Solutions |

---

## 2. Technology Stack

### 2.1 Backend

| Technology | Version / Rule |
|---|---|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI — all endpoints must be `async def` |
| **ORM** | SQLAlchemy 2.0 — use `Mapped[]` / `mapped_column()` syntax, async sessions |
| **Database** | PostgreSQL 15 — UUID primary keys always, never auto-increment int |
| **Cache** | Redis — for session cache and rate limiting |
| **Task Queue** | Celery — for payroll processing, payslip email dispatch |
| **Auth** | JWT via `python-jose` — access token 15 min, refresh token 7 days |
| **Migrations** | Alembic — always autogenerate, never alter DB manually |
| **Validation** | Pydantic v2 — use `model_config`, `field_validator`, NOT old `@validator` |
| **Config** | `python-dotenv` + Pydantic `BaseSettings` — no hardcoded secrets ever |
| **Testing** | Pytest + `pytest-asyncio` — write tests for all new endpoints |
| **DB Driver** | `psycopg3` (async) — not psycopg2 |
| **Email** | `FastAPI-Mail` via SMTP — dispatch through Celery task asynchronously |

### 2.2 Frontend

| Technology | Version / Rule |
|---|---|
| **Framework** | Next.js 14 — App Router only, never Pages Router patterns |
| **Language** | TypeScript — strict mode, no `any` type unless absolutely necessary |
| **Styling** | Tailwind CSS — no inline styles, no separate CSS files unless unavoidable |
| **UI Components** | shadcn/ui — use existing components before building custom ones |
| **Global State** | Zustand |
| **Server State** | TanStack React Query |
| **Forms** | React Hook Form + Zod |
| **HTTP Client** | Axios — with interceptors for auth token injection and silent refresh |
| **Icons** | Lucide React only — no other icon libraries |
| **Charts** | Recharts — for all data visualizations |
| **Auth** | NextAuth.js with custom credentials provider calling FastAPI JWT |

### 2.3 Infrastructure

- **Package manager (Python):** `pip` + `requirements.txt` — no Poetry unless asked
- **Package manager (Node):** `npm` — not yarn or pnpm
- **File storage:** Local filesystem in dev; S3-compatible in production
- **API versioning:** Always `/api/v1/` prefix

---

## 3. Project Directory Structure

Always follow this exact structure. Never create files outside it without asking first.

```
paybd/
├── backend/
│   ├── app/
│   │   ├── api/          ← route handlers (v1/employees, v1/payroll, etc.)
│   │   ├── core/         ← config.py, security.py, dependencies.py
│   │   ├── models/       ← SQLAlchemy ORM models (one file per domain)
│   │   ├── schemas/      ← Pydantic request/response schemas
│   │   ├── services/     ← business logic (payroll_service.py, etc.)
│   │   ├── tasks/        ← Celery background tasks
│   │   ├── utils/        ← helpers, formatters, BLA calculators
│   │   └── main.py       ← FastAPI app entry point
│   ├── alembic/          ← database migrations
│   ├── tests/            ← pytest test files
│   └── requirements.txt
├── frontend/
│   ├── app/              ← Next.js App Router pages
│   │   ├── (auth)/       ← login, register routes (route group)
│   │   ├── dashboard/
│   │   ├── employees/
│   │   ├── payroll/
│   │   ├── attendance/
│   │   ├── reports/
│   │   └── settings/
│   ├── components/
│   │   ├── ui/           ← shadcn/ui base components
│   │   └── paybd/        ← PayBD-specific components
│   ├── lib/              ← api.ts, auth.ts, utils.ts
│   ├── stores/           ← Zustand stores
│   ├── types/            ← TypeScript interfaces
│   └── package.json
└── .env.example          ← always update when adding new env vars
```

---

## 4. Coding Rules & Conventions

### 4.1 General Rules (All Code)

- Write **production-quality** code — not tutorial or demo quality
- Every function must have a **single clear responsibility**
- Add **docstrings** to all Python functions and classes — minimum one-line summary
- **No commented-out dead code** in final output
- **No `print()` for debugging** — use Python `logging` module with correct log levels
- **No hardcoded secrets, URLs, or credentials** — always use environment variables
- **Always handle errors explicitly** — never use bare `except:`, catch specific exceptions
- Write **RAM-efficient code** — this runs in GitHub Codespaces with limited memory

### 4.2 Python / FastAPI Rules

- All endpoints must be `async def` — **never** `def` in route handlers
- Use `Depends()` for all dependency injection (DB session, current user, permissions)
- Router files: always use `APIRouter(prefix='/api/v1/resource', tags=['Resource'])`
- Always return **typed Pydantic schemas** — never return raw dict or SQLAlchemy objects
- Use `HTTPException` with correct status codes:
  - `400` bad input, `401` unauthorized, `403` forbidden, `404` not found, `422` validation error
- Use **SQLAlchemy 2.0 style**: `select()`, `where()` — not legacy `.query()` ORM style
- Always close DB sessions via `async with` or `Depends` — never leave sessions open
- **Payroll calculations belong in `services/payroll_service.py`** — never in route handlers

**Correct SQLAlchemy 2.0 model pattern:**

```python
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, func
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # soft delete
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
```

**Database rules:**
- All tables must have: `id` (UUID), `created_at`, `updated_at`
- Use `snake_case` for all column names
- Add indexes on all foreign keys and frequently queried fields
- **Soft delete only** — add `is_active: bool` — never hard delete employee records

### 4.3 TypeScript / Next.js Rules

- Use `'use client'` only when required (event handlers, hooks) — default to Server Components
- All API calls go through `lib/api.ts` — **never** `fetch()` directly in components
- Define all API response types in `types/` folder and import from there
- **No `any` type** — use `unknown` + type guard if necessary
- Use `next/image` for all images — never raw `<img>` tags
- Use `next/link` for all internal navigation — never `<a href>`
- **Loading states:** always use `Suspense` or `loading.tsx` — never leave UI blank while fetching
- **Error states:** every data-fetching component must handle and display error state

---

## 5. PayBD Domain Logic (BLA 2006)

> ⚠️ The AI must apply these rules in all payroll-related code automatically — without being asked each time.

### 5.1 Bangladesh Labour Act 2006 Compliance

| Provision | Rule | Implementation |
|---|---|---|
| **Section 108 — Overtime** | 2× basic hourly rate for hours beyond 8/day or 48/week | Always configurable per company; default = 2× |
| **Festival Bonus** | 2 per year, each = 1 month's basic salary | Auto-schedule before Eid-ul-Fitr and Eid-ul-Adha |
| **Section 52 — Gratuity** | 30 days' last basic salary per completed year | Calculate on separation only; never during employment |
| **Section 117 — Provident Fund** | Worker + employer contributions tracked separately | Default worker rate: 5–10% of basic |
| **Leave Encashment** | Unused annual leave paid on separation | Rate = basic ÷ 26 working days |
| **Maternity Benefit** | 16 weeks paid (8 pre + 8 post) | Process as payroll item; cannot be deducted |
| **Working Hours** | Max 8 hours/day, 48 hours/week | OT cap: 2 hours/day unless DOLE exemption |

### 5.2 Salary Calculation Formula

```python
# PayBD standard salary calculation

gross_salary = basic + house_rent + medical + transport + other_allowances

# Allowance defaults (all configurable per company/grade):
# house_rent  = 40–60% of basic
# medical     = Fixed Tk 1,500/month OR per policy
# transport   = Fixed OR per grade

# Overtime (BLA Compliance Mode)
overtime_hourly_rate = (basic / 26 / 8) * 2
overtime_pay = overtime_hours * overtime_hourly_rate

total_earnings = gross_salary + overtime_pay

# Deductions
pf_employee    = basic * pf_rate          # 0.05 to 0.10
absence_deduct = (gross_salary / 26) * absent_days
loan_deduct    = monthly_loan_installment  # if applicable
income_tax     = calculate_tax(annual_income)  # NBR slabs

net_salary = total_earnings - pf_employee - absence_deduct - loan_deduct - income_tax
```

### 5.3 Payroll Module Responsibilities

| Module | Responsibility |
|---|---|
| **Employee Master** | Source of truth for salary structure per employee |
| **Attendance Module** | Feeds present days, absent days, OT hours into payroll engine |
| **Leave Module** | Deducts unpaid leave; maintains paid leave balance |
| **Payroll Engine** | Core calculation — lives in `services/payroll_service.py` |
| **Payslip Generator** | PDF output via ReportLab or WeasyPrint |
| **Approval Workflow** | HR calculates → Finance approves → Finalize & lock |

---

## 6. API Design Rules

### 6.1 Endpoint Naming Convention

```
GET    /api/v1/employees              # list (paginated)
POST   /api/v1/employees              # create
GET    /api/v1/employees/{id}         # get single
PATCH  /api/v1/employees/{id}         # partial update
DELETE /api/v1/employees/{id}         # soft delete (is_active=False)

POST   /api/v1/payroll/calculate      # trigger calculation
POST   /api/v1/payroll/approve        # finance approval
GET    /api/v1/payroll/{month}/{year} # fetch payroll run
GET    /api/v1/reports/payroll        # payroll register report
```

### 6.2 Standard Response Envelope

Always wrap responses in this structure — no exceptions:

```json
{
  "success": true,
  "message": "Employees retrieved successfully",
  "data": { },
  "meta": {
    "total": 145,
    "page": 1,
    "per_page": 20,
    "pages": 8
  }
}
```

```json
{
  "success": false,
  "message": "Employee not found",
  "error_code": "EMPLOYEE_NOT_FOUND",
  "detail": null
}
```

### 6.3 Auth Rules

- All protected endpoints require `Authorization: Bearer <access_token>` header
- Use `get_current_user: Annotated[User, Depends(get_current_active_user)]` dependency
- Refresh endpoint: `POST /api/v1/auth/refresh` — return new access token only
- Role check: use `Depends(get_current_user_with_role('hr_manager'))` pattern

---

## 7. How AI Must Respond

### ✅ Always Do

- Provide **complete, runnable code** — never truncate with `# ... rest of code ...`
- Show the **full file** when creating a new file
- When editing, show **only the changed block** with a clear `FIND / REPLACE WITH` format
- Include **all import statements** at the top of every snippet
- Add the **exact file path** as a comment on the first line: `# backend/app/services/payroll_service.py`
- **Lead with code** — explain after, not before
- If a BLA 2006 rule applies, **explicitly state which section** was used
- **Flag any assumption** made about business logic that needs verification

### ❌ Never Do

- Write placeholder code like `return {"todo": "implement this"}`
- Skip error handling and say "add error handling later"
- Use deprecated patterns: old SQLAlchemy `.query()`, old Pydantic `@validator`
- Suggest packages outside the approved stack without a clear reason
- Generate Alembic migrations manually — always use `alembic revision --autogenerate`
- Use `print()` for debugging in any generated code

### 📝 Explanation Style

- Keep explanations **concise** — one short paragraph per major code section
- When there is a choice between approaches, **briefly state which you chose and why**
- If a business rule is ambiguous, **ask before assuming** — especially for BLA 2006 calculations

### 🔧 Edit Instruction Format

When asked for targeted edits, use this format:

```
FILE: backend/app/services/payroll_service.py
ACTION: Replace the calculate_overtime() function

FIND:
def calculate_overtime(hours, rate):
    return hours * rate

REPLACE WITH:
def calculate_overtime(hours: float, basic_salary: Decimal) -> Decimal:
    """Calculate OT at 2x basic hourly rate — BLA 2006 Section 108."""
    hourly_rate = basic_salary / 26 / 8
    return Decimal(str(hours)) * hourly_rate * 2
```

---

## 8. Current Development Status

> Update this section after each completed module.

| Module | Status | Notes |
|---|---|---|
| Backend — Auth (JWT) | ✅ Complete | Login, register, refresh token working |
| Backend — Employee CRUD | ✅ Complete | All endpoints working |
| Backend — Payroll Engine | ✅ Complete | Compliance & actual-hours modes |
| Backend — Attendance | ⚠️ Partial | Manual entry done; file import pending |
| Backend — Leave Module | ⚠️ Partial | Leave types done; approval workflow pending |
| Backend — Reports | ❌ Not started | — |
| Frontend — Auth UI | ⚠️ Bug active | Login page built; env variable mismatch (see below) |
| Frontend — Dashboard | ❌ Not started | — |
| Frontend — Employee UI | ❌ Not started | — |
| Frontend — Payroll UI | ❌ Not started | — |
| Payslip PDF Generator | ❌ Not started | — |
| Email Notifications | ❌ Not started | — |

> 🐛 **Active Bug:** Frontend login cannot connect to FastAPI backend.  
> **Root cause:** `NEXT_PUBLIC_API_URL` in `frontend/.env.local` does not match the Codespaces port-forwarded URL for the backend.  
> **Fix:** Set `NEXT_PUBLIC_API_URL` to the exact Codespaces forwarded URL (e.g. `https://xxxx-8000.app.github.dev`).

---

## 9. Environment Variables Reference

```env
# backend/.env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/paybd
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<strong-random-secret-min-32-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=<gmail-app-password>
MAIL_FROM=noreply@paybd.com.bd
ENVIRONMENT=development
```

```env
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
# In Codespaces: use the forwarded URL → https://xxxx-8000.app.github.dev

NEXTAUTH_SECRET=<strong-random-secret>
NEXTAUTH_URL=http://localhost:3000
```

---

## 10. Common Dev Commands

### Backend

```bash
cd backend

# Install
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload --port 8000

# New migration
alembic revision --autogenerate -m "add leave_requests table"

# Apply migrations
alembic upgrade head

# Run tests
pytest tests/ -v

# Start Celery worker
celery -A app.tasks worker --loglevel=info
```

### Frontend

```bash
cd frontend

# Install
npm install

# Dev server
npm run dev

# Production build
npm run build

# Add shadcn/ui component
npx shadcn@latest add button

# Type check
npx tsc --noEmit
```

---

## 11. Quick Cheat Sheet

Copy this block alone for short sessions when you don't need the full document:

```
PayBD — AI Coding Quick Reference

Stack:
  Backend:   FastAPI (async) | PostgreSQL | SQLAlchemy 2.0 | Redis | Celery
  Frontend:  Next.js 14 App Router | TypeScript strict | shadcn/ui | Tailwind
  Auth:      JWT (15min access / 7d refresh) | NextAuth on frontend
  Forms:     React Hook Form + Zod
  State:     Zustand (global) | React Query (server)
  Icons:     Lucide React only
  Charts:    Recharts only

Always:
  - async def for all FastAPI routes
  - UUID primary keys
  - Typed Pydantic schemas in responses
  - Explicit error handling
  - Env vars for all secrets
  - Soft delete (is_active) — never hard delete

Never:
  - Sync route handlers
  - print() for debug
  - any TypeScript type
  - Hardcoded secrets or URLs
  - Bare except:
  - Raw dict returns from endpoints

BLA 2006 Rules:
  - Overtime = 2× basic hourly rate (Section 108)
  - Festival Bonus = 2× per year, each = 1 month basic
  - Gratuity = 30 days last basic per completed year
  - PF = 5–10% of basic (employee + employer tracked separately)

Active Bug:
  - Frontend NEXT_PUBLIC_API_URL mismatch with Codespaces port
```

---

*PayBD AI Coding Instruction — v1.0 | Pavel Digital Solutions | paybd.com.bd*  
*Update this file as the project evolves. Commit changes to the repo.*
