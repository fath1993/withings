# Health Website to Track Health Status

This project is a web application that allows users to track their health status using data from Fitbit and Withings devices via a REST API and OAuth2. The platform provides insights into various health metrics, enabling users to monitor their fitness progress and overall health.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Integration**: Connect and sync data from Fitbit and Withings devices for a comprehensive health overview.
- **Health Metrics Tracking**: Monitor key health metrics such as heart rate, sleep patterns, activity levels, and weight.
- **User-Friendly Dashboard**: An intuitive dashboard displaying personalized health insights and trends.
- **Goal Setting**: Set and track health and fitness goals to stay motivated.
- **Historical Data**: View historical data trends to understand your health journey over time.
- **User Authentication**: Secure user accounts with authentication and profile management.
- **REST API**: Access and manipulate health data programmatically via a RESTful API.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/health-website-tracker.git
    ```

2. Navigate into the project directory:
    ```bash
    cd health-website-tracker
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for the admin interface (optional):
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

Once the server is running, visit `http://127.0.0.1:8000/` in your browser to access the health tracking website.

- **Connect Devices**: Link your Fitbit and Withings accounts to import your health data.
- **View Metrics**: Navigate to the dashboard to view your current health metrics and trends.
- **Set Goals**: Create health goals and track your progress over time.
- **Historical Data**: Access historical data to review your health journey.

## API Documentation

### Authentication
To access the API, authenticate your requests using your API key. Include the key in the headers:

