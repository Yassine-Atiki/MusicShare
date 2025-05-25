# Django Music Platform

A web-based music platform built with Django that allows users to upload, manage, and share their music. Users can create playlists, manage their music library, and interact with other users' public playlists.

## Features

- User authentication and profile management
- Music upload and management
- Playlist creation and management
- Public/private playlist visibility
- Music player integration
- User listening history
- Profile customization

## Technologies Used

- Python 3.x
- Django 5.2.1
- MySQL
- HTML/CSS/JavaScript
- Pillow (Python Imaging Library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/django-music-platform.git
cd django-music-platform
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root and add your environment variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

```
musique_project/
├── media/                  # User uploaded files
├── static/                 # Static files (CSS, JS, images)
├── users/                  # Main application
│   ├── migrations/        # Database migrations
│   ├── templates/        # HTML templates
│   ├── forms.py          # Form definitions
│   ├── models.py         # Database models
│   ├── urls.py           # URL configurations
│   └── views.py          # View logic
├── MusiqueProject/        # Project configuration
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── manage.py             # Django management script
└── requirements.txt      # Project dependencies
```

## Usage

1. Register a new account or login with existing credentials
2. Upload your music files through the upload interface
3. Create and manage your playlists
4. Browse other users' public playlists
5. Track your listening history
6. Customize your profile

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django documentation and community
- Contributors and testers
- Open source packages used in this project

## Contact

YASSINE ATIKI - yassineatiki28@gmail.com
