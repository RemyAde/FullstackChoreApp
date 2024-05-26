# Chorey - Full-Stack API Application with FastAPI

## Overview

Chorey is a full-stack API application built with FastAPI, allowing users to create and edit chores, providing user authentication and authorization, and using Jinja2 for rendering data from the backend to the frontend.

## Features

- **Create Chores:** Users can create new chores with details such as title, description, due date, and assigned user.
- **Edit Chores:** Existing chores can be edited to update their details.
- **Authentication and Authorization:** Secure user authentication and authorization mechanisms are implemented to control access to API endpoints.
- **Jinja2 Templating:** Jinja2 is used to render data from the backend to the frontend, providing dynamic and interactive user interfaces.

## Technologies Used

- FastAPI
- Python
- SQLite (or your preferred database)
- Jinja2
- JWT for authentication

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RemyAde/FullstackChoreApp.git
   ```

2. Install dependencies:

   ```bash
   pip install -r BackEnd/requirements.txt
   ```

3. Set up environment variables for database connection and JWT secret key.

4. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. Register and authenticate as a user to obtain a JWT token.
2. Use the token to access protected endpoints for managing chores.
3. Use the frontend interface powered by Jinja2 to interact with the application.

## Documentation

Detailed API documentation is automatically generated and can be accessed at `/docs` endpoint when the server is running. It provides information about all available endpoints, request parameters, and response formats.

## Credits

This project was inspired by the "FastAPI - The complete course" by codingwithroby.
