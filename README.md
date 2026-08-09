# 🚧 RoadFix LK

### Smart Road Damage Reporting and Management System

RoadFix LK is a web-based road damage reporting system designed to help citizens report road problems such as potholes, cracks, damaged roads, and other road-related issues.

The system allows users to submit road damage reports with location information, photos, severity levels, and descriptions. Administrators can review and manage reported issues through the system.

---

## 📌 Project Overview

Road damage is a common problem that can affect road safety, transportation, and daily travel.

RoadFix LK provides a simple digital platform where citizens can:

- 📍 Report road problems using their current location
- 🗺️ Select the exact location using an interactive map
- 📸 Upload photos of road damage
- 🚧 Select the type of road damage
- 🚨 Set the severity level
- 📝 Add additional information
- 📋 View submitted reports
- 🔔 Receive notifications about report updates

Administrators can manage and monitor reported road issues through the system.

---

## ✨ Features

### 👤 Citizen Features

- User registration and login
- Secure authentication
- Report road damage
- Automatic location detection
- Interactive map location selection
- Draggable map marker
- Photo upload
- Road damage type selection
- Severity selection
- Report description
- View submitted reports
- Track report status
- Notifications

### 🛠️ Admin Features

- Admin login
- View road damage reports
- Review submitted reports
- Verify reports
- Manage report status
- Assign reports to responsible officers
- Monitor road issues
- View reports on an interactive map

### 🗺️ Map Features

- Interactive OpenStreetMap
- Leaflet.js map
- Automatic location detection
- Draggable location marker
- Road issue markers
- Severity-based marker colors
- Report information popup
- Map-based road issue visualization

### 🤖 Smart Features

- Duplicate report detection
- Report priority calculation
- AI-assisted road damage detection
- Image-based damage analysis

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Leaflet.js

### Backend

- Python
- Flask

### Database

- SQLite

### Maps

- Leaflet.js
- OpenStreetMap

### AI / Image Processing

- OpenCV
- Python

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Citizen        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Web Interface    │
                    │ HTML / CSS / JS /    │
                    │ Bootstrap / Leaflet  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Flask API       │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
          ┌──────────┐  ┌───────────┐  ┌──────────┐
          │  SQLite  │  │   Image   │  │   Map    │
          │ Database │  │ Processing│  │ Services │
          └──────────┘  └───────────┘  └──────────┘
                 │
                 ▼
          ┌──────────────────┐
          │      Admin       │
          │    Dashboard     │
          └──────────────────┘
---


---
## 📂 Project Structure

```text
RoadFix-LK/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   └── schema.sql
│
├── models/
│   └── db.py
│
├── routes/
│   ├── auth.py
│   ├── reports.py
│   ├── admin.py
│   └── api.py
│
├── services/
│   ├── ai.py
│   ├── duplicate.py
│   └── priority.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── map.html
│   ├── report_form.html
│   ├── my_reports.html
│   └── admin/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   └── uploads/
│
└── tests/
    └── ...
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/DulanMadhukaWeerathunga2000/RoadFix-LK.git
```

Go to the project directory:

```bash
cd RoadFix-LK
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🔐 User Roles

## Citizen

Citizens can:

```text
Register
   ↓
Login
   ↓
Report Road Issue
   ↓
Detect Location
   ↓
Upload Photo
   ↓
Select Damage Type
   ↓
Select Severity
   ↓
Submit Report
   ↓
Track Report
```

## Administrator

Administrators can:

```text
Login
   ↓
View Reports
   ↓
Review Reports
   ↓
Verify Reports
   ↓
Assign Officer
   ↓
Update Status
   ↓
Monitor Progress
```

---

# 🗺️ Road Issue Reporting Flow

```text
User
 │
 ▼
Detect Current Location
 │
 ▼
Show Location on Map
 │
 ▼
User Confirms / Moves Pin
 │
 ▼
Upload Road Image
 │
 ▼
Select Damage Type
 │
 ▼
Select Severity
 │
 ▼
Submit Report
 │
 ▼
Database
 │
 ▼
Admin Review
 │
 ▼
Map Visualization
```

---

# 📍 Location Detection

RoadFix LK uses browser-based geolocation to detect the user's current location.

Users can also manually adjust the location by:

* Dragging the map marker
* Clicking a location on the map

This is useful when the automatically detected location is not accurate enough.

---

# 🚨 Severity Levels

Road issues can be categorized based on their severity:

| Severity    | Description                                         |
| ----------- | --------------------------------------------------- |
| 🔴 Critical | Dangerous road condition requiring urgent attention |
| 🟠 High     | Serious road issue that should be addressed soon    |
| 🟡 Medium   | Moderate road damage                                |
| 🟢 Low      | Minor road issue                                    |

---

# 🗺️ Map Visualization

Reported road issues are displayed on an interactive map.

Different colors are used to represent the severity/status of road issues.

```text
🔴 Critical
🟠 High
🟡 Medium / Low
🟢 Resolved
```

Users can click a marker to view information about the reported issue.

---

# 🤖 AI-Based Features

RoadFix LK includes AI/image-processing related functionality to support road damage analysis.

The system can be extended to detect:

* Potholes
* Road cracks
* Surface damage
* Other visible road defects

The AI component can assist administrators by providing an initial damage classification.

---

# 🔄 Report Status

A road report can move through different stages:

```text
New
 ↓
Verified
 ↓
Assigned
 ↓
In Progress
 ↓
Resolved
 ↓
Confirmed
```

This allows citizens and administrators to track the progress of reported road issues.

---

# 🧪 Testing

The project can be tested locally using:

* Manual functional testing
* User authentication testing
* Report submission testing
* Location testing
* Image upload testing
* Map testing
* Admin functionality testing
* API testing

---

# 🔒 Security Considerations

The project includes authentication and role-based access concepts.

For production use, additional security improvements should be implemented, including:

* Strong password hashing
* Secure session management
* CSRF protection
* File upload validation
* Input validation
* Rate limiting
* Secure secret keys
* Production database configuration

---

# 🎯 Future Improvements

Future versions of RoadFix LK can include:

* 📱 Mobile application
* 🤖 Improved AI road damage detection
* 📊 Advanced analytics dashboard
* 📧 Email notifications
* 📱 SMS notifications
* 🗺️ Advanced GIS features
* 👮 Officer mobile interface
* 📈 Road maintenance statistics
* ☁️ Cloud deployment
* 🔐 Two-factor authentication

---

# 🎓 Academic Project

RoadFix LK was developed as a software engineering project to demonstrate the practical application of:

* Web application development
* Software engineering principles
* Database management
* REST API development
* Location-based services
* Map integration
* Image processing
* User authentication
* Role-based access control

---

# 👨‍💻 Author

**Dulan Madhuka Weerathunga**

GitHub:

[https://github.com/DulanMadhukaWeerathunga2000](https://github.com/DulanMadhukaWeerathunga2000)

Project:

[https://github.com/DulanMadhukaWeerathunga2000/RoadFix-LK](https://github.com/DulanMadhukaWeerathunga2000/RoadFix-LK)

---

# 📄 License

This project is developed for educational and academic purposes.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

````

