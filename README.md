# 🛣️ RoadFix-LK

## Smart Road Damage Reporting & Management System

<div align="center">

**A web-based civic technology platform for reporting, managing, tracking, and resolving road-related issues in Sri Lanka.**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![OpenCV](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)
![Leaflet](https://img.shields.io/badge/Maps-Leaflet.js-green)
![OpenStreetMap](https://img.shields.io/badge/Map-OpenStreetMap-orange)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-purple)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📖 Table of Contents

* [Project Overview](#-project-overview)
* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [How the System Works](#-how-the-system-works)
* [Main Users](#-main-users)
* [Core Features](#-core-features)
* [System Workflow](#-system-workflow)
* [System Architecture](#-system-architecture)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Database Design](#-database-design)
* [Main Modules](#-main-modules)
* [API Endpoints](#-api-endpoints)
* [Security](#-security)
* [Screenshots](#-screenshots)
* [Installation](#-installation)
* [Configuration](#-configuration)
* [Running the Application](#-running-the-application)
* [Testing](#-testing)
* [Future Improvements](#-future-improvements)
* [Project Roadmap](#-project-roadmap)
* [Future Real-Time Architecture](#-future-real-time-architecture)
* [Contribution](#-contribution)
* [Author](#-author)
* [License](#-license)

---

# 📌 Project Overview

**RoadFix-LK** is a Smart Road Damage Reporting and Management System designed for Sri Lanka.

The system allows citizens to report road-related problems such as:

* 🕳️ Potholes
* 🛣️ Damaged roads
* 🧱 Road cracks
* 🌊 Flooded roads
* 🪨 Landslides
* 💡 Damaged street infrastructure
* ⚠️ Other road hazards

Citizens can submit a report with a description, image, and geographical location.

Administrators can then review reports, verify the reported problem, update its status, and manage the repair process.

The system provides a central platform that connects **citizens and responsible authorities**.

---

# 🚨 Problem Statement

Road damage is a common problem in Sri Lanka.

Citizens often report road problems through:

* Phone calls
* Social media
* Messages
* Informal communication
* Personal complaints

These methods can make it difficult for authorities to:

* Track complaints
* Identify exact locations
* Prioritize serious problems
* Avoid duplicate complaints
* Monitor repair progress
* Maintain historical records

RoadFix-LK provides a centralized digital solution for managing these problems.

---

# 🎯 Objectives

The main objectives of RoadFix-LK are:

1. Allow citizens to report road damage easily.
2. Capture the exact location of the reported issue.
3. Allow users to upload images as evidence.
4. Store reports in a centralized database.
5. Allow administrators to review submitted reports.
6. Categorize road damage.
7. Prioritize serious road problems.
8. Track report status.
9. Display reported locations on an interactive map.
10. Improve communication between citizens and authorities.
11. Provide a foundation for future AI-based road damage detection.
12. Support real-time road monitoring in future versions.

---

# 👥 Main Users

## 👤 Citizen

Citizens can:

* Register an account
* Login
* Submit road damage reports
* Upload images
* Add descriptions
* Share location
* View submitted reports
* Track report status
* View road problems on a map

---

## 👨‍💼 Administrator

Administrators can:

* Login to the administration dashboard
* View submitted reports
* Review reports
* Verify reports
* Reject invalid reports
* Change report status
* Manage reported road issues
* View locations on a map
* Monitor unresolved issues
* Manage users

---

# ⚡ Core Features

## 1. 👤 User Registration & Login

Users can create accounts and securely access the system.

Features:

* Registration
* Login
* Logout
* Session management
* User profile

---

## 2. 📝 Road Damage Reporting

Citizens can create a report by entering:

* Road damage type
* Description
* Location
* Image
* Date/time
* Additional information

Example:

```text
Type: Pothole
Location: Colombo
Description: Large pothole near the main junction.
Severity: High
Image: pothole.jpg
```

---

## 3. 📍 GPS Location

The system can capture the geographical location of a road issue.

The location can be represented using:

```text
Latitude
Longitude
```

Example:

```text
Latitude: 6.9271
Longitude: 79.8612
```

---

## 4. 🗺️ Interactive Map

Road reports can be displayed using:

* Leaflet.js
* OpenStreetMap

Users can visually identify where road problems have been reported.

Example:

```text
             MAP
 ┌─────────────────────────────┐
 │                             │
 │       🔴 Pothole            │
 │                             │
 │              🟠 Crack       │
 │                             │
 │   🔴 Flood                  │
 │                             │
 └─────────────────────────────┘
```

---

## 5. 📷 Image Upload

Citizens can upload images of damaged roads.

Images provide evidence that helps administrators verify reports.

Supported formats can include:

```text
JPG
JPEG
PNG
WEBP
```

---

## 6. 📊 Report Status Tracking

Each report can have a status.

Example lifecycle:

```text
SUBMITTED
    ↓
UNDER REVIEW
    ↓
VERIFIED
    ↓
ASSIGNED
    ↓
IN PROGRESS
    ↓
RESOLVED
```

Invalid reports can be:

```text
REJECTED
```

---

# 🔄 System Workflow

The complete system workflow is:

```text
                 ┌───────────────┐
                 │    Citizen    │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Register/Login│
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Create Report   │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Upload Image          Capture Location
              │                     │
              └──────────┬──────────┘
                         ▼
                  ┌──────────────┐
                  │ Submit Report│
                  └───────┬──────┘
                          │
                          ▼
                  ┌──────────────┐
                  │   Database   │
                  └───────┬──────┘
                          │
                          ▼
                  ┌──────────────┐
                  │ Admin Review │
                  └───────┬──────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          Rejected                 Verified
                                      │
                                      ▼
                                Assigned for Repair
                                      │
                                      ▼
                                Work in Progress
                                      │
                                      ▼
                                   Resolved
```

---

# 🏗️ System Architecture

RoadFix-LK follows a simple layered web architecture.

```text
┌──────────────────────────────────────────────┐
│              USER INTERFACE                  │
│                                              │
│ HTML5 + CSS3 + Bootstrap + JavaScript        │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              FLASK APPLICATION               │
│                                              │
│ Routes + Authentication + Business Logic     │
└──────────────────────┬───────────────────────┘
                       │
          ┌────────────┴─────────────┐
          ▼                          ▼
┌───────────────────┐       ┌──────────────────┐
│ SQLite Database   │       │ File/Image Store │
│                   │       │                  │
│ Users             │       │ Road Images      │
│ Reports           │       │ Uploaded Files   │
│ Status            │       │                  │
└───────────────────┘       └──────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│             Mapping Services                 │
│                                              │
│ Leaflet.js + OpenStreetMap                   │
└──────────────────────────────────────────────┘
```

---

# 🛠️ Technology Stack

| Layer             | Technology               |
| ----------------- | ------------------------ |
| Backend           | Python                   |
| Web Framework     | Flask                    |
| Frontend          | HTML5                    |
| Styling           | CSS3                     |
| UI Framework      | Bootstrap                |
| Client-side Logic | JavaScript               |
| Database          | SQLite                   |
| Image Processing  | OpenCV                   |
| Maps              | Leaflet.js               |
| Map Data          | OpenStreetMap            |
| Version Control   | Git & GitHub             |
| Deployment        | Flask-compatible hosting |

---

# 📁 Project Structure

A recommended project structure is:

```text
RoadFix-LK/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── database/
│   └── roadfix.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   ├── images/
│   │
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── report.html
│   ├── reports.html
│   ├── dashboard.html
│   ├── admin.html
│   └── map.html
│
└── utils/
    └── image_processing.py
```

> The structure above represents the recommended organization. Adjust filenames according to the actual repository structure.

---

# 🗄️ Database Design

The main database can contain tables such as:

## Users

```text
Users
│
├── id
├── name
├── email
├── password
├── role
└── created_at
```

---

## Reports

```text
Reports
│
├── id
├── user_id
├── damage_type
├── description
├── image
├── latitude
├── longitude
├── severity
├── status
└── created_at
```

---

## Status History

For a future expanded version:

```text
StatusHistory
│
├── id
├── report_id
├── old_status
├── new_status
├── updated_by
└── updated_at
```

---

# 🔗 Database Relationship

```text
                 USERS
                   │
                   │ 1
                   │
                   │
                   │ N
                REPORTS
                   │
                   │
                   ▼
             STATUS HISTORY
```

One user can create multiple reports.

One report can have multiple status history records.

---

# 🧩 Main Modules

## Module 01 — Authentication

Responsible for:

* Registration
* Login
* Logout
* Session management
* Role checking

---

## Module 02 — Report Management

Responsible for:

* Create report
* Read report
* Update report
* Delete report
* Report validation

---

## Module 03 — Location Management

Responsible for:

* Latitude
* Longitude
* Map markers
* Location visualization

---

## Module 04 — Image Management

Responsible for:

* Image upload
* File validation
* Image storage
* Image processing

---

## Module 05 — Admin Dashboard

Responsible for:

* Viewing reports
* Filtering reports
* Updating status
* Managing users
* Monitoring unresolved issues

---

## Module 06 — Map Module

Responsible for:

* Interactive map
* Report markers
* Location information
* Damage visualization

---

## Module 07 — OpenCV Module

OpenCV can be used for future computer vision functionality.

Possible features:

```text
Road Image
     ↓
Image Preprocessing
     ↓
Feature Detection
     ↓
Damage Detection
     ↓
Damage Classification
     ↓
Severity Estimation
```

---

# 📡 API Endpoints

The API structure can be expanded as the project becomes more REST-oriented.

## Authentication

| Method | Endpoint        | Description      |
| ------ | --------------- | ---------------- |
| POST   | `/api/register` | Register user    |
| POST   | `/api/login`    | Login user       |
| POST   | `/api/logout`   | Logout user      |
| GET    | `/api/profile`  | Get user profile |

---

## Reports

| Method | Endpoint            | Description   |
| ------ | ------------------- | ------------- |
| GET    | `/api/reports`      | Get reports   |
| POST   | `/api/reports`      | Create report |
| GET    | `/api/reports/<id>` | Get report    |
| PUT    | `/api/reports/<id>` | Update report |
| DELETE | `/api/reports/<id>` | Delete report |

---

## Admin

| Method | Endpoint                     | Description          |
| ------ | ---------------------------- | -------------------- |
| GET    | `/admin/dashboard`           | Admin dashboard      |
| GET    | `/admin/reports`             | Manage reports       |
| PUT    | `/admin/reports/<id>/status` | Update report status |
| GET    | `/admin/users`               | Manage users         |

> These endpoints should only be documented as active once they exist in the implementation.

---

# 🔐 Security

RoadFix-LK should follow basic web application security practices.

## Password Security

Passwords should never be stored as plain text.

Use password hashing such as:

```text
Werkzeug Password Hashing
```

---

## Authentication

Authenticated sessions should be protected.

Unauthorized users should not be allowed to access administrator functions.

---

## Role-Based Access Control

Example:

```text
Citizen
   │
   ├── Create Report
   ├── View Own Reports
   └── Track Status

Admin
   │
   ├── View Reports
   ├── Verify Reports
   ├── Update Status
   └── Manage Users
```

---

## Input Validation

Validate:

* User input
* Email addresses
* Report descriptions
* Image files
* Latitude/longitude
* File sizes

---

## File Upload Security

Uploaded files should be validated before storing them.

Recommended restrictions:

```text
Allowed:
JPG
JPEG
PNG
WEBP
```

Avoid allowing executable file types.

---

# 🖥️ Screenshots

Add actual screenshots from the application here.

## 🏠 Home Page

```text
docs/screenshots/home.png
```

![Home Page](docs/screenshots/home.png)

---

## 🔐 Login Page

```text
docs/screenshots/login.png
```

![Login Page](docs/screenshots/login.png)

---

## 📝 Report Submission

```text
docs/screenshots/report.png
```

![Report Submission](docs/screenshots/report.png)

---

## 🗺️ Road Damage Map

```text
docs/screenshots/map.png
```

![Road Damage Map](docs/screenshots/map.png)

---

## 👨‍💼 Admin Dashboard

```text
docs/screenshots/admin-dashboard.png
```

![Admin Dashboard](docs/screenshots/admin-dashboard.png)

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/DulanMadhukaWeerathunga2000/RoadFix-LK.git
```

```bash
cd RoadFix-LK
```

---

# 🐍 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

# 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet:

```bash
pip install flask
```

Install other dependencies according to the implemented modules.

---

# ⚙️ Configuration

Create a `.env` file if environment variables are used.

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_PATH=roadfix.db
UPLOAD_FOLDER=static/uploads
```

Do not commit sensitive credentials to GitHub.

Add `.env` to:

```text
.gitignore
```

---

# ▶️ Running the Application

Run:

```bash
python app.py
```

The Flask development server will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

---

# 🧪 Testing

Basic testing should cover:

### Authentication

* Registration
* Login
* Logout
* Invalid credentials

### Reporting

* Create report
* Upload image
* Validate location
* Validate required fields

### Administration

* Admin login
* View reports
* Change report status
* Reject invalid reports

### Map

* Display markers
* Display correct coordinates
* Open report information

---

# 📊 Example Report Lifecycle

```text
                    ┌───────────┐
                    │ SUBMITTED │
                    └─────┬─────┘
                          │
                          ▼
                  ┌──────────────┐
                  │ UNDER REVIEW │
                  └──────┬───────┘
                         │
                 ┌───────┴───────┐
                 ▼               ▼
             REJECTED         VERIFIED
                                 │
                                 ▼
                              ASSIGNED
                                 │
                                 ▼
                            IN PROGRESS
                                 │
                                 ▼
                              RESOLVED
```

---

# 🔮 Future Improvements

RoadFix-LK can be expanded into a real-world smart road monitoring platform.

## 🤖 1. AI Road Damage Detection

Use computer vision to detect:

* Potholes
* Cracks
* Road surface damage
* Damage severity

Possible pipeline:

```text
Image
  ↓
OpenCV Preprocessing
  ↓
AI/ML Model
  ↓
Damage Detection
  ↓
Classification
  ↓
Severity Score
```

---

## 📱 2. Mobile Application

Future versions can provide:

* Android application
* iOS application
* GPS-based reporting
* Camera integration
* Push notifications
* Offline reporting

---

## 🔔 3. Notifications

Users could receive:

```text
Report Submitted
        ↓
Report Verified
        ↓
Repair Started
        ↓
Repair Completed
```

Notifications can later be implemented using email, SMS, or push notifications.

---

## 🔄 4. Real-Time Updates

Future versions can use:

```text
WebSocket / Socket.IO
```

for real-time:

* Report status updates
* Admin notifications
* New road damage alerts
* Dashboard updates

---

## 📊 5. Analytics Dashboard

The system can provide:

* Total reports
* Resolved reports
* Pending reports
* Reports by district
* Reports by damage type
* Monthly statistics
* Average resolution time

Example:

```text
Total Reports       : 1,250
Resolved            : 850
Pending             : 250
Under Investigation : 100
Rejected            : 50
```

---

## 📍 6. Heatmap

Road damage reports can be converted into a heatmap.

```text
Low Risk     🟢
Medium Risk  🟡
High Risk    🟠
Critical     🔴
```

This can help authorities identify areas requiring urgent attention.

---

# 🗺️ Project Roadmap

## Phase 1 — Foundation

* [x] Project setup
* [x] Flask backend
* [x] Basic frontend
* [x] SQLite database
* [x] User authentication

---

## Phase 2 — Road Reporting

* [x] Road damage report form
* [x] Image upload
* [x] Description
* [x] Location information
* [x] Database storage

---

## Phase 3 — Map Integration

* [x] Leaflet.js integration
* [x] OpenStreetMap
* [x] Report markers
* [ ] Advanced filtering
* [ ] Damage heatmap

---

## Phase 4 — Admin Management

* [x] Admin dashboard
* [x] Report management
* [x] Status management
* [ ] Assignment management
* [ ] Repair verification

---

## Phase 5 — Smart Features

* [ ] Duplicate report detection
* [ ] Automatic severity classification
* [ ] OpenCV image analysis
* [ ] AI pothole detection
* [ ] AI damage classification

---

## Phase 6 — Real-Time Platform

* [ ] WebSocket integration
* [ ] Real-time notifications
* [ ] Live dashboard updates
* [ ] SMS notifications
* [ ] Email notifications

---

## Phase 7 — Mobile Application

* [ ] Android application
* [ ] iOS application
* [ ] GPS integration
* [ ] Offline reporting
* [ ] Push notifications

---

## Phase 8 — Production Deployment

* [ ] Production database
* [ ] HTTPS
* [ ] Cloud deployment
* [ ] Monitoring
* [ ] Automated backups
* [ ] CI/CD pipeline

---

# 🌐 Future Real-Time Architecture

The long-term architecture can evolve into:

```text
                 CITIZEN MOBILE APP
                         │
                         ▼
                 ┌───────────────┐
                 │  API Gateway  │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Report Service  User Service   AI Service
          │              │              │
          │              │              ▼
          │              │        Damage Detection
          │              │
          └───────┬──────┘
                  ▼
             PostgreSQL
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
     Redis              File Storage
        │
        ▼
   Real-Time Events
        │
        ▼
   Admin Dashboard
        │
        ▼
 Authorities / Repair Teams
```

---

# 🎯 Real-World Version

The final real-world version of RoadFix-LK can follow this workflow:

```text
Citizen
   ↓
Capture Road Damage
   ↓
GPS Location
   ↓
Upload Image
   ↓
AI Damage Detection
   ↓
Duplicate Detection
   ↓
Severity Calculation
   ↓
Database
   ↓
Authority Dashboard
   ↓
Assign Repair Team
   ↓
Repair Work
   ↓
Upload Completion Evidence
   ↓
Admin Verification
   ↓
RESOLVED
   ↓
Citizen Notification
```

This transforms RoadFix-LK from a simple complaint management system into a **Smart Road Infrastructure Monitoring Platform**.

---

# 📈 Expected Benefits

RoadFix-LK can help:

### Citizens

* Report road problems easily
* Track complaints
* See reported road issues
* Provide evidence through images

### Authorities

* Centralize complaints
* Identify high-priority locations
* Monitor unresolved problems
* Track repair progress
* Analyze road damage data

### Community

* Improve road safety
* Reduce duplicate complaints
* Improve transparency
* Support data-driven road maintenance

---

# 🤝 Contribution

Contributions are welcome.

### Step 1

Fork the repository.

### Step 2

Create a feature branch:

```bash
git checkout -b feature/new-feature
```

### Step 3

Make your changes.

### Step 4

Commit:

```bash
git commit -m "Add new road reporting feature"
```

### Step 5

Push:

```bash
git push origin feature/new-feature
```

### Step 6

Create a Pull Request.

---

# 👨‍💻 Author

## Dulan Madhuka Weerathunga

GitHub:

https://github.com/DulanMadhukaWeerathunga2000

Project:

https://github.com/DulanMadhukaWeerathunga2000/RoadFix-LK

---

# 🙏 Acknowledgments

RoadFix-LK uses and is inspired by open-source technologies and mapping resources including:

* Python
* Flask
* SQLite
* Bootstrap
* JavaScript
* OpenCV
* Leaflet.js
* OpenStreetMap

Special thanks to the open-source community and developers contributing to civic technology and road safety solutions.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# ⭐ RoadFix-LK

**Report. Track. Repair. Improve.**

> Building a smarter and safer road infrastructure management system for Sri Lanka 🇱🇰

---
