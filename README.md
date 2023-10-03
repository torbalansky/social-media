# Social Media Clone App

This is a Django-based social media clone application that allows users to post "Yeets" (similar to tweets) and follow other users.

## Features

- User registration and authentication
- Posting and viewing Yeets
- Following and unfollowing other users
- User profiles with profile pictures and bio
- Yeet liking and sharing
- User search functionality

## Installation

### Clone the repository to your local machine:

   git clone <https://github.com/torbalansky/social-media-clone.git>
   cd social-media-clone

### Create a virtual environment

    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate

### Install the dependencies

    pip install -r requirements.txt

### Apply database migrations

    python manage.py migrate

### Create super user

    python manage.py createsuperuser

### Start the dev server

    python manage.py runserver

