# Project Setup Guide

## Introduction

Welcome to our project This guide will walk you through setting up your development environment, installing dependencies, and running the Django development server.

## Setting Up Your Virtual Environment

Before you start, you'll need to set up a virtual environment to keep your project's dependencies isolated from other Python projects on your system.

### Step 1: Install Virtualenv

If you don't already have `virtualenv` installed, you can install it using pip:
bash pip install virtualenv


### Step 2: Create a Virtual Environment

Navigate to your project directory and create a new virtual environment. Replace `venv` with whatever you'd like to name your virtual environment:

bash cd path/to/your/project virtualenv venv

### Step 3: Activate the Virtual Environment

Activate the virtual environment. On Windows, run:
bash .\venv\Scripts\activate

On macOS and Linux, run:
bash source venv/bin/activate

Your terminal prompt should change to indicate that the virtual environment is active.


## Installing Dependencies

With your virtual environment activated, you can now install the project's dependencies. These are listed in the `requirements.txt` file.

### Step 1: Install Dependencies

Run the following command to install all dependencies listed in `requirements.txt`:

bash pip install -r requirements.txt


This command reads the `requirements.txt` file and installs all the packages listed there.

## Running the Django Development Server

Once your dependencies are installed, you can start the Django development server to begin working on your project.

### Step 1: Start the Django Development Server

Run the following command to start the Django development server:
python manage.py runserver

By default, the server will start on port 8000. You can access your project by opening a web browser and navigating to `http://127.0.0.1:8000`.

## Next Steps

- Explore the project's codebase.
- Familiarize yourself with Django's documentation and the Django admin interface.
- Begin developing your project!

Remember, if you encounter any issues, refer to the project's documentation or seek help from the community.
