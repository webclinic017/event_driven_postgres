# Event Driven Postgres

## This project uses Docker to test out one way to track events with a PostgreSQL database.

## Components include:
1. A Postgres container with a notification trigger
2. A flask app which allows you to post data to the database
3. A separate listener using psycopg2 which polls the notification channel for new data
