# Social Media Clone App

This is a Django-based social media clone application that allows users to post "Yeets" (similar to tweets) and follow other users.

## Features

- User registration and authentication
- Posting and viewing Yeets
- Following and unfollowing other users
- User profiles with profile pictures and bio
- Yeet liking and sharing
- User search functionality

## Technologies Used

- Python
- Django
- HTML/CSS
- Bootstrap
- SQLite (by default, but can be changed to another database)

## Dependencies

This project relies on several Python packages. You can install them using the following steps:

### Installation

```shell
# Clone the repository to your local machine:
git clone https://github.com/torbalansky/social-media-clone.git
cd social-media-clone

# Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# Install the required dependencies:
pip install -r requirements.txt

# Apply database migrations:
python manage.py migrate

# Create a superuser for admin access (optional):
python manage.py createsuperuser

# Start the development server:
python manage.py runserver
```
These instructions will set up your local development environment for the Social Media Clone App.

