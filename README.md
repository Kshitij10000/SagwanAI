# Nirmaan_Finance

Nirmaan_Finance is a Django-based web application that provides users with real-time financial data, investment options, watchlists, and user profile management. The project integrates various technologies to offer a seamless experience for financial enthusiasts and professionals.

## Features

- **User Authentication and Registration**
  - Secure user login and registration system.
  - Profile management with the ability to upload profile pictures.

- **Live Stock Data**
  - Real-time display of stock prices using Yahoo Finance data.
  - Interactive charts for stock performance visualization.

- **Investment Options**
  - Detailed financial data for NSE-listed companies.
  - Dynamic tables with customizable columns for in-depth analysis.

- **Watchlist Functionality**
  - Personalized watchlists for tracking selected stocks.
  - Category-based stock filtering and search functionality.

- **Email Notifications**
  - Contact form for user inquiries.
  - Email sending capabilities using SMTP.

- **Background Task Processing**
  - Asynchronous tasks for data fetching and processing using Celery.
  - Scheduled tasks with Celery Beat for periodic updates.

## Tech Stack

### Backend

- **[Python 3.x](https://www.python.org/doc/)**
  - The core programming language used for the project.

- **[Django 5.1](https://docs.djangoproject.com/en/5.1/)**
  - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.

- **[PostgreSQL](https://www.postgresql.org/docs/)**
  - An advanced open-source relational database used as the primary database for the application.

- **[Redis](https://redis.io/documentation)**
  - An in-memory data structure store used as a message broker for Celery tasks.

- **[Celery 5.x](https://docs.celeryproject.org/en/stable/)**
  - An asynchronous task queue/job queue used for handling background tasks.

- **[Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)**
  - A scheduler that enables scheduling periodic tasks within Celery.

- **[django-celery-beat](https://github.com/celery/django-celery-beat)**
  - An extension that stores Celery Beat schedules in the Django database, allowing dynamic scheduling.

- **[django-celery-results](https://github.com/celery/django-celery-results)**
  - Enables storing Celery task results in the Django database.

- **[yfinance](https://pypi.org/project/yfinance/)**
  - A library to download market data from Yahoo Finance, used for fetching live stock data.

- **[pandas](https://pandas.pydata.org/docs/)**
  - A data analysis and manipulation tool used for handling data frames and data manipulation in tasks.

- **[Import-Export](https://django-import-export.readthedocs.io/en/latest/)**
  - A Django application and library for importing and exporting data with included admin integration.

### Frontend

- **[Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)**
  - A CSS framework directed at responsive, mobile-first front-end web development.

- **[Chart.js](https://www.chartjs.org/docs/latest/)**
  - An open-source JavaScript library for data visualization, used for displaying interactive stock charts.

- **[jQuery](https://api.jquery.com/)**
  - A fast, small, and feature-rich JavaScript library used for simplified AJAX calls and DOM manipulation.

- **HTML5 & CSS3**
  - Markup and styling for structuring and designing the web pages.

- **JavaScript**
  - Client-side scripting for interactive features.

### Other Libraries and Tools

- **[django-import-export](https://django-import-export.readthedocs.io/en/latest/)**
  - Facilitates data import and export in the admin interface.

- **[django.contrib.admin](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/)**
  - Django's built-in admin interface for managing models.

- **[django.contrib.auth](https://docs.djangoproject.com/en/5.1/topics/auth/)**
  - Django's authentication framework for user authentication and authorization.

- **[django.contrib.messages](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)**
  - A framework for storing and retrieving temporary messages.

- **[django.contrib.staticfiles](https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/)**
  - Manages static files like CSS, JavaScript, and images.

- **Logging**
  - Python's built-in logging module used for tracking events during execution.

## Installation

### Prerequisites

- **Python 3.x** installed on your system.
- **PostgreSQL** database setup.
- **Redis** server running.
- **Node.js and npm** (for frontend dependencies, if necessary).

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Nirmaan_finance.git
   cd Nirmaan_finance

2. **Create a Virtual Environment**
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Backend Dependencies**
    pip install -r requirements.txt

4. **Configure Environment Variables**
    Rename .env.example to .env and update the settings accordingly.

5.  **Apply Migrations**
    
    python manage.py migrate

6.  **Collect Static Files**
    python manage.py collectstatic

7.  **Run the Development Server**
    python manage.py runserver

8.  **Start Redis Server**
    Ensure Redis is running on your system. For most systems, you can start it using:
    redis-server

9.  **Start Celery Worker**
    celery -A Nirmaan_finance worker -l info

10. **Start Celery Beat**
    celery -A Nirmaan_finance beat -l info

### Usage
Visit http://localhost:8000/ in your web browser.

Register a new user or log in with existing credentials.

Navigate through the application using the navigation bar.

Access the admin interface at http://localhost:8000/admin/ (requires superuser credentials).

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
Thanks to the developers of Django and the open-source libraries used in this project.
Yahoo Finance for providing financial data.
Contact
For any inquiries or feedback, please contact kshitijsarve2001@gmail.com.
