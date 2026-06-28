# 🚜 Tracktor

A lightweight, professional issue tracking system built with Python and Flask.
Tracktor helps teams manage, prioritise and resolve service requests efficiently
with a clean goldenrod themed interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- 🎫 **Ticket management** — Create, view, edit and close service requests
- 🔴 **Priority levels** — Critical, high, medium and low with colour coded badges
- 📁 **Categories** — Organise tickets by type (hardware, software, network and more)
- 👷 **Technician profiles** — Assign tickets to technicians with Gravatar avatars
- 🔍 **Search and filter** — Find any ticket instantly by keyword, priority, status or category
- 📊 **Live dashboard** — See critical tickets and stats at a glance
- 🎨 **Professional UI** — Clean goldenrod theme throughout

---

## 🖥️ Requirements

Before you begin make sure you have the following installed:

| Requirement | Version | Download |
|---|---|---|
| Python | 3.8 or higher | https://www.python.org/downloads |
| Git | Any recent version | https://git-scm.com/downloads |
| SQLite | Any recent version | https://www.sqlite.org/download.html |

---

## 🚀 Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/srinathsherma/Tracktor.git
cd Tracktor
```

### Step 2 — Create a virtual environment

**On Windows:**
```bash
python -m venv ticketor
ticketor\Scripts\activate
```

**On Linux or Mac:**
```bash
python -m venv ticketor
source ticketor/bin/activate
```

You should see `(ticketor)` at the start of your command prompt.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Seed the database with sample data

```bash
python seed.py
```

You should see:

👷 Adding technicians...

✅ Added 4 technicians!

📁 Adding categories...

✅ Added 6 categories!

🎫 Adding tickets...

✅ Added 8 tickets!

🚜 Tracktor database seeded successfully!

### Step 5 — Run Tracktor

```bash
python app.py
```

### Step 6 — Open your browser

Visit: http://127.0.0.1:5001

You should see Tracktor running with sample data! 🚜

---

## 📁 Project structure
Tracktor/

├── templates/                  ← HTML templates

│   ├── base.html               ← Base template with navigation

│   ├── dashboard.html          ← Live stats dashboard

│   ├── index.html              ← Ticket list with search and filter

│   ├── new_ticket.html         ← Create new ticket

│   ├── view_ticket.html        ← View ticket details

│   ├── edit_ticket.html        ← Edit existing ticket

│   ├── technicians.html        ← Technician directory

│   ├── new_technician.html     ← Add new technician

│   ├── view_technician.html    ← Technician profile

│   ├── edit_technician.html    ← Edit technician profile

│   ├── categories.html         ← Category list

│   └── new_category.html       ← Add new category

├── app.py                      ← Flask app setup and configuration

├── models.py                   ← Database models

├── routes.py                   ← Ticket routes

├── technician_routes.py        ← Technician routes

├── category_routes.py          ← Category routes

├── seed.py                     ← Sample data seeder

├── requirements.txt            ← Python dependencies

└── .gitignore                  ← Git ignore rules

---

## 🎫 Using Tracktor

### Creating a ticket
1. Click **+ New Ticket** on the home page
2. Fill in the title and description
3. Set the priority level
4. Optionally assign a category and technician
5. Click **Save Ticket**

### Managing tickets
- Click any ticket title to view full details
- Click **Edit ticket** to update any field
- Click **Mark as closed** to close a resolved ticket

### Using the dashboard
- Click **Dashboard** in the navigation bar
- See live counts of open, critical and in progress tickets
- View breakdowns by priority, category and technician
- Click **View tickets →** on any card to jump to filtered results

### Managing technicians
- Click **Technicians** in the navigation bar
- Click **+ Add technician** to add a new team member
- Click **View profile** to see a technician's full profile and ticket history
- Click **Edit profile** to update their details

### Setting up a profile photo
Tracktor uses [Gravatar](https://gravatar.com) for profile photos. To set a
photo for a technician:
1. Visit https://gravatar.com
2. Sign up using the technician's email address
3. Upload a photo
4. The photo will appear automatically in Tracktor

### Searching and filtering tickets
Use the filter bar on the home page to filter by:
- **Keyword** — searches title and description
- **Priority** — critical, high, medium or low
- **Status** — open, in progress or closed
- **Category** — any category in the system
- **Technician** — any technician in the system

Click **Clear** to reset all filters.

---

## 🗄️ Database

Tracktor uses SQLite which requires zero configuration. The database file
`issuetracker.db` is created automatically when you first run the app.

### Reseed the database
To clear all data and reload the sample data:

```bash
python seed.py
```

The script will warn you before clearing any existing data.

### Database schema
tickets

├── id

├── title

├── description

├── status (open, in_progress, closed)

├── priority (critical, high, medium, low)

├── technician_id → technicians.id

├── category_id → categories.id

├── notes

├── date_requested

├── date_completed

├── created_at

└── updated_at
technicians

├── id

├── name

├── email

├── phone

├── job_title

├── department

├── bio

└── date_joined
categories

├── id

├── name

└── description

---

## 🔧 Configuration

Open `app.py` to change these settings:

| Setting | Default | Description |
|---|---|---|
| `SECRET_KEY` | `change-this-before-going-to-production` | Change this before deploying! |
| `port` | `5001` | Port Tracktor runs on |
| `debug` | `True` | Set to False in production |

---

## 🤝 Contributing

Contributions are welcome! Here is how to get started:

1. Fork the repository on GitHub
2. Create a new branch for your feature
3. Make your changes
4. Push to your branch
5. Open a pull request

---

## 📜 License

This project is licensed under the MIT License — feel free to use it, modify
it and share it!

---

## 👨‍💻 Author

Built with ❤️ by Srinath Sherma

🌐 [ssherma.com](https://ssherma.com)
🐙 [github.com/srinathsherma](https://github.com/srinathsherma)

---

*🚜 Tracktor — built to work as hard as a tractor!*
