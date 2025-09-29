# Health Pay: A Comprehensive Hospital Management System

**Health Pay** is an advanced, full-stack hospital management system built with Django. It provides a seamless and interactive platform for managing hospital operations, including patient care, doctor-patient communication, and administrative tasks. The application is designed with a modular architecture and leverages real-time technologies to deliver a modern and efficient user experience.

🔗 **Live Demo**: [healthpay.up.railway.app](https://healthpay.up.railway.app) 
🔗 **GitHub Repository**: [Health Pay on GitHub](https://github.com/Aadii170/Health_pay.git)

---

## 🚀 Core Features

- **Role-Based Dashboards**: Separate, feature-rich dashboards for Admins, Doctors, Patients, and Pathologists.
- **Appointment Management**: Patients can book, view, and track appointments with doctors. Admins can approve or reject appointment requests.
- **Patient & Doctor Management**: Admins have full CRUD functionality over doctor and patient records, including account approval.
- **Electronic Health Records (EHR)**: Doctors can view patient details, prescribe medication, and access medical history.
- **Medical Reports**: Pathologists can upload and manage patient reports, which are then accessible to both doctors and patients.
- **Real-Time Chat**: Secure, real-time chat functionality between doctors and their assigned patients, powered by Django Channels.
- **Real-Time Notifications**: Instant notifications for key events, such as account approval, using WebSockets.
- **Billing & Discharge**: Admins can generate and manage patient bills, and download them as PDFs.

---

## 🛠️ Tech Stack

| Category      | Technology                               |
|---------------|------------------------------------------|
| **Backend**   | Django, Django Channels, Daphne          |
| **Frontend**  | HTML, CSS, Bootstrap, JavaScript         |
| **Database**  | PostgreSQL (production), SQLite (dev)    |
| **Real-Time** | WebSockets, Redis                        |
| **Deployment**| Railway, Heroku (via Procfile)           |
| **Email**     | Gmail SMTP                               |

---

## 🏗️ System Architecture

### Backend

The backend is built using Django and is organized into several modular applications:

- **`hospital`**: The core app that manages administrative tasks, user authentication, and overall site navigation.
- **`doctor`**: Contains the models, views, and URLs for all doctor-related functionalities.
- **`patient`**: Manages patient data, appointments, and interactions with the system.
- **`pathologist`**: Handles the logic for pathologists, including report uploads.
- **`chat`**: Implements the real-time chat feature using Django Channels.

### Frontend

The frontend is built with standard web technologies and follows Django's templating conventions:

- **Templates**: The `templates` directory is organized by application, with each app having its own set of HTML files. Base templates are used to ensure a consistent UI across the application.
- **Static Files**: The `static` directory contains the project's CSS, JavaScript, and image assets. The application uses a single, centralized `style.css` file for custom styling.

### Database

The database schema is designed to support the application's core functionalities. Key relationships include:

- **User Model**: The built-in `User` model is extended using a `OneToOneField` to create `Doctor`, `Patient`, and `Pathologist` profiles.
- **Doctor-Patient Relationship**: A `Patient` is assigned a `Doctor` via an `assignedDoctorId` field. *Note: This is currently implemented as a `PositiveIntegerField` rather than a `ForeignKey`, which is a design choice to consider for future improvements.*
- **One-to-Many Relationships**: `Patient` records are linked to `PrescriptionDetail` and `Report` models via `ForeignKey` relationships, allowing a single patient to have multiple prescriptions and reports.

### Real-Time Communication

The application uses **Django Channels** and **WebSockets** to provide real-time functionality:

- **Chat**: The `chat` app uses a `ChatConsumer` to manage WebSocket connections for real-time messaging between doctors and patients.
- **Notifications**: The `hospital` app uses a `NotificationConsumer` to send instant notifications to users, for example, when their account is approved by an administrator.

---

## 🔬 Core Computer Science Concepts

- **Object-Oriented Programming (OOP)**: Django's model-view-template (MVT) architecture is fundamentally object-oriented. Models are classes that represent database tables, and views are functions or classes that encapsulate the logic for processing requests and returning responses.
- **Client-Server Architecture**: The application follows a classic client-server model, where the user's browser (the client) sends requests to the Django backend (the server), which then processes the request and returns an HTML page or data.
- **Database Management (DBMS)**: The project uses a relational database to store and manage data. The use of Django's ORM abstracts away the direct SQL queries and helps maintain data integrity through models and their defined relationships.
- **Computer Networks (CN)**: The application leverages several networking protocols, including HTTP for web requests, SMTP for sending emails, and WebSockets for real-time, bidirectional communication.

---

## ⚙️ Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Aadii170/Health_pay.git
    cd Health_pay
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` File**
    Create a `.env` file in the root directory and add the following environment variables:
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

5.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start the Development Server**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

---

## 📂 Project Structure

```
Health_pay/
├── doctor/
├── patient/
├── hospital/
├── pathologist/
├── chat/
├── templates/
├── static/
├── hospitalmanagement/  # Main settings & routing
├── .env
└── manage.py
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 📬 Contact

- **Author**: Aditya Kumar  
- **Email**: kumaradity1702@gmail.com  
- **GitHub**: [Aadii170](https://github.com/Aadii170)

---

> Built with ❤️ in India 🇮🇳
