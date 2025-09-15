# 🔄 SkillSwap

A **Flask-based web application** that enables users to exchange skills, featuring an **Admin Dashboard** for managing users and skills. The project is fully **Dockerized** for consistent setup and easy sharing.



## ✨ Features

- 👤 User registration, login, and profile management  
- 🔍 Skill browsing and swap requests  
- 🛠️ Admin panel for user and skill management  
- 🗄️ SQLite database backend (persisted with Docker volumes)  
- 🐳 Fully Dockerized for easy deployment  



## 📦 Prerequisites

- [Docker](https://www.docker.com/) (recommended)  
- [Python 3.12+](https://www.python.org/) (if running without Docker)  
- [Git](https://git-scm.com/)  



## 🚀 Installation & Usage

### 1️⃣ Clone the repository


git clone https://github.com/KaliyaVrajesh/SkillSwap.git
cd SkillSwap


2️⃣ Using Docker (Recommended)
Build the Docker image:


Copy code
docker build -t skillswap-app:latest .
Create a Docker volume for persistent data:


Copy code
docker volume create skillswap_data
Run the container exposing port 5000:


Copy code
docker run -d -p 5000:5000 \
-v skillswap_data:/app/instance \
--name skillswap_container \
skillswap-app:latest
👉 Access the app at: http://localhost:5000

3️⃣ Running Without Docker
Set up a Python virtual environment:


Copy code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:


Copy code
pip install -r requirements.txt
Set up the database and run the app:


Copy code
flask db upgrade
python run.py
⚙️ Configuration
The app uses environment variables (via .env) for key settings:

SECRET_KEY → Flask app secret

SQLALCHEMY_DATABASE_URI → Defaults to SQLite at instance/skillswap.db

Email server settings (optional)

📌 Important Notes
Mount a volume to /app/instance inside Docker to persist the database

App listens on port 5000 by default

🛠️ Troubleshooting
View container logs:


Copy code
docker logs skillswap_container
Ensure Docker volume is mounted correctly for database persistence

Verify environment variables if using features like email notifications

🤝 Contributing
Contributions are welcome!
Please fork the repository and submit a pull request 🚀

📬 Contact
For questions or support, contact:
📧 [www.bittukumar.07@.com]
