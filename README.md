## SagwanAI 🚀📊
SagwanAI is a Django-based web application designed to empower users with AI-driven financial insights and automated trading capabilities. This project leverages cutting-edge technologies to enhance investment strategies and streamline financial workflows for both enthusiasts and professionals.

## 🌟 Features
👤 User Authentication and Registration

Secure user login and registration system
Profile management with capabilities to upload profile pictures

## 🔐 API Security and Credential Protection

Robust encryption for storing and handling broker API credentials
Secure integration with multiple brokerage platforms
Regular security audits and compliance with financial data protection standards

## 🤖 AI-Powered Stock Predictions

Real-time AI-based predictions for stock movements
Automated trading decisions including entry, exit, stop loss, and target setting

## 📈 Live Stock Data

Real-time display of stock prices using Yahoo Finance data
Interactive charts for trend visualization and performance analysis

## 💹 Automated Order Placement

AI-driven execution of buy and sell orders based on predefined criteria and real-time market data
Support for multiple brokerage APIs with secure credential management

## 📊 Position Tracking and Management

Real-time monitoring and adjustment of stock positions
Detailed reports and analysis on current holdings and historical performance

## 🧠 Market Analysis and Decision Making

Comprehensive market analysis utilizing AI to determine investment viability
Quick decision-making tools for agile trading

## 👀 Watchlist Functionality

Personalized watchlists for tracking selected stocks
Advanced filtering and search capabilities based on categories

## 📧 Email Notifications

Automated email alerts for significant market movements and trade confirmations
Contact form for user inquiries and support

## ⚙️ Background Task Processing

Asynchronous tasks for data fetching, market analysis, and order execution using Celery
Scheduled tasks with Celery Beat for periodic data updates and system checks

## 🧪 Paper Trading

Simulate trades in a risk-free environment to test AI strategies
Realistic market conditions using real-time data without financial risk
Performance tracking and analysis of paper trading results

## 🛠️ Tech Stack
# Backend

Python 3.x: The core programming language used for backend logic
Django 5.1: A high-level Python Web framework that encourages rapid development
PostgreSQL: Advanced open-source relational database
Redis: In-memory data structure store used as a message broker
Celery 5.x: Asynchronous task queue/job queue
Celery Beat: Scheduler that enables scheduling periodic tasks
django-celery-beat: Stores Celery Beat schedules in the Django database
django-celery-results: Enables storing Celery task results in the Django database
yfinance: Library to fetch real-time market data from Yahoo Finance
pandas: Data analysis and manipulation library

# Frontend

Bootstrap 5.3: Responsive, mobile-first front-end framework
Chart.js: JavaScript library for interactive charts
jQuery: Simplifies HTML document traversing, event handling, and Ajax interactions
HTML5 & CSS3: Standard web technologies for structuring and designing web pages

## 🚀 Installation
Prerequisites

Python 3.x, PostgreSQL, Redis, and Node.js with npm (for managing frontend dependencies)

# Steps

Clone the Repository:
git clone https://github.com/yourusername/SagwanAI.git

Set Up Virtual Environment and Install Dependencies:
Using Python's venv and pip
Configure Environment Variables:
Rename .env.example to .env and adjust settings, including API keys and security configurations
Database Setup:
python manage.py migrate

Static Files:
python manage.py collectstatic

Run the Development Server:
python manage.py runserver

Start Redis and Celery Services:
Ensure background services for task handling are running

## 🖥️ Usage

Visit http://localhost:8000/ to register or log in.
Navigate to the profile section to securely add your broker API credentials.
Use the navigation bar to explore AI features, manage investments, and access the paper trading platform.
Test strategies using the paper trading feature before engaging in live trading.
Access the admin interface for additional management capabilities.

## 🔒 API Security
SagwanAI prioritizes the security of user credentials and financial data:

All broker API credentials are encrypted at rest using industry-standard encryption algorithms.
Secure communication protocols (HTTPS) are enforced for all data transmissions.
Regular security audits are conducted to ensure the integrity of the system.
Users have full control over their API integrations and can revoke access at any time.

## 📝 Paper Trading
The paper trading feature allows users to:

Test AI-generated trading strategies without financial risk.
Simulate market conditions using real-time data.
Track and analyze performance of simulated trades.
Gain confidence in the AI system before transitioning to live trading.

##🤝 Contributing
Contributions to SagwanAI are welcome! Fork the repository and create a pull request with your changes.

##📄 License
Licensed under the MIT License.

##🙏 Acknowledgments
Special thanks to the developers of Django, Yahoo Finance, and the many open-source libraries that support this project.
For any inquiries or feedback, please contact kshitijsarve2001@gmail.com.