# Django Zoho Lead Sync System

A Django-based backend system that synchronizes Lead data between a local database and Zoho CRM with reliable two-way syncing, background processing, and clean service-layer architecture.

This project was developed as part of a technical assessment for a Senior/Mid-Level Django Engineer role.

---

## 📌 Tech Stack

- Python 3.10+
- Django 4.2+
- PostgreSQL (via psycopg2)
- Celery + Redis
- Zoho CRM APIs (OAuth2)
- Docker & Docker Compose

---

## 📁 Project Structure

```

elevate_now_task/
├── config/
│   ├── settings.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
│
├── leads/
│   ├── models.py
│   ├── admin.py
│   ├── tasks.py
│   ├── services/
│   │   └── zoho_client.py
│   ├── views.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── README.md

````

---

## 🧠 Architecture Overview

The application follows a **Service Layer pattern**:

- **Admin / Views**
  - Trigger sync actions
  - No business logic

- **Service Layer (`services/zoho_client.py`)**
  - Handles all Zoho API interactions
  - OAuth token management
  - API request/response handling

- **Background Layer**
  - Celery workers execute sync jobs
  - Redis used as broker
  - Celery Beat handles scheduled sync

This ensures clean separation of concerns, testability, and scalability.

---

## 🗄️ Lead Model

```python
class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=50, blank=True, null=True)
    zoho_id = models.CharField(max_length=50, null=True, blank=True)
    zoho_modified_time = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
````

---

## 🔁 Sync Strategy

### 1️⃣ Local → Zoho (Push Sync)

Triggered via:

* Django Admin action
* Celery background task

**Logic**

* If `zoho_id` is empty → Create Lead in Zoho
* If `zoho_id` exists → Update Zoho Lead
* Save returned `zoho_id` locally

Handled in:

* `leads.tasks.sync_lead_to_zoho`
* `services.zoho_client.create_lead / update_lead`

---

### 2️⃣ Zoho → Local (Pull Sync)

Triggered via:

* Celery Beat (scheduled)

**Logic**

* Fetch leads modified after last sync using `Modified_Time`
* Upsert into local DB using `update_or_create`
* Update local fields like `status`

Handled in:

* `leads.tasks.sync_zoho_to_local`

---

## ⚔️ Conflict Handling Strategy

**Source of Truth Rule**

* Zoho CRM is treated as the **source of truth** for externally modified fields.

**Conflict Resolution**

* If Zoho `Modified_Time` > local `zoho_modified_time` → Zoho wins
* Local changes always overwrite Zoho only when explicitly pushed

**Why this works**

* Prevents infinite update loops
* Ensures deterministic sync behavior
* Matches real-world CRM workflows

---

## 🔐 Zoho OAuth Token Handling

* Uses **OAuth2 Refresh Token Flow**
* Access tokens cached in memory for ~55 minutes
* New token generated only when expired
* Prevents unnecessary token regeneration and rate-limit issues

---

## ⚙️ Background Processing

| Component   | Purpose                        |
| ----------- | ------------------------------ |
| Celery      | Executes async sync jobs       |
| Redis       | Message broker                 |
| Celery Beat | Scheduled Zoho → Local polling |

---

## 🐳 Docker Setup

### Services

* Django Web
* Celery Worker
* Celery Beat
* Redis
* Postgres

---

## 🚀 Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/nisaaaaar/django-zoho-lead-sync.git
cd django-zoho-lead-sync
```

---

### 2️⃣ Create `.env` file

```env
DEBUG=1
DJANGO_SECRET_KEY=your-secret-key

DB_HOST=db
DB_NAME=zoho_sync
DB_USER=root
DB_PASSWORD=root

REDIS_URL=redis://redis:6379/0

ZOHO_BASE_URL=https://www.zohoapis.in
ZOHO_ACCOUNTS_URL=https://accounts.zoho.in
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
```

---

### 3️⃣ Start Containers

```bash
docker compose up --build
```

---

### 4️⃣ Run Migrations

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

### 5️⃣ Access Admin

```
http://localhost:8000/admin
```

---

## 🎥 Demo Video

A demo video showcasing:

* Lead creation
* Local → Zoho sync
* Zoho → Local sync
* Background task execution

📎 **Video Link:** *(https://drive.google.com/file/d/1_g4henDxbyQOoIRZiRSEZNODc0t3I41V/view?usp=drive_link)*

---

## 🧪 Admin Features

* Add / edit leads
* Manual Zoho sync action
* View sync status
* Schedule periodic sync using Celery Beat

---

## 🛠 Future Enhancements

* Replace polling with Zoho Webhooks
* Add sync audit logs
* Retry policies with dead-letter queues
* Fine-grained conflict resolution rules

---

## 👨‍💻 Author

**Nisar Ahmad**
---

