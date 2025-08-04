# 🏥 Health Pay – Hospital Management System

**Health Pay** is a Django-based web application for managing hospital operations such as doctor-patient interaction, appointments, reports, and real-time communication using WebSockets.

🔗 **GitHub Repository**: [Health Pay on GitHub](https://github.com/Aadii170/Health_pay.git)

---

## 🚀 Features

- 👨‍⚕️ Doctor, Patient, Pathologist dashboards
- 📅 Appointment booking & tracking
- 📧 Email notifications via Gmail SMTP
- 💬 Real-time communication using Django Channels & Redis
- 📂 Admin panel for managing users and records
- 📁 Upload and manage reports, prescriptions, and more

---

## 📦 Tech Stack

- **Backend**: Django 3.0.5, Django Channels
- **Frontend**: HTML, CSS, Bootstrap (customized medical theme)
- **Database**: SQLite (easily switchable to PostgreSQL/MySQL)
- **WebSockets**: Channels + Redis
- **Email**: Gmail SMTP with App Password

---

## 🛠 Setup Instructions

### 1. 🔃 Clone the Repository

```bash
git clone https://github.com/Aadii170/Health_pay.git
cd Health_pay
```

### 2. 📦 Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 🛠 Install Requirements

```bash
pip install -r requirements.txt
```

### 4. 📁 Create `.env` file

Create a `.env` file in the root and add:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_RECEIVING_USER=admin@gmail.com

REDIS_HOST=localhost
REDIS_PORT=6379
```

> 🔐 Keep `.env` secret. Add it to `.gitignore`.

---

### 5. 🔌 Run Migrations

```bash
python manage.py migrate
```

### 6. 👤 Create Admin User

```bash
python manage.py createsuperuser
```

### 7. 🚀 Start Development Server

```bash
python manage.py runserver
```

Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔧 Redis Setup for Channels

Ensure Redis is installed and running on port `6379`.

**Ubuntu/Linux:**

```bash
sudo apt update
sudo apt install redis
redis-server
```

---

## 📁 Project Structure

```
Health_pay/
├── doctor/
├── patient/
├── hospital/
├── pathologist/
├── templates/
├── static/
├── media/
├── hospitalmanagement/  # Main settings & routing
├── db.sqlite3
├── .env
└── manage.py
```

---

## 📬 Contact

- **Author**: Aditya Kumar  
- **Email**: kumaradity1702@gmail.com  
- **GitHub**: [Aadii170](https://github.com/Aadii170)

---

## 📜 License

Licensed under the **MIT License** – use freely for personal or educational projects.

---

> Built with ❤️ in India 🇮🇳
