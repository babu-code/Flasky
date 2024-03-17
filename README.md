Flasky
Flasky is a microblogging application built using Flask, a lightweight and versatile web framework for Python. It allows users to create accounts, share posts, follow other users, and engage in discussions through comments.

Features
User Authentication: Secure user authentication system with registration, login, and logout functionality.
Post Creation and Sharing: Users can create, edit, and delete their posts. Posts can include text, images, or links.
User Profiles: Each user has a profile page displaying their information and list of posts.
Following System: Users can follow other users to see their posts in their timeline.
Comments: Users can comment on posts and engage in discussions.
Pagination: Pagination for posts, followers, and followed users to optimize performance.
Email Notifications: Email notifications for account activation and password reset requests.
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/flasky.git
Navigate to the project directory:
bash
Copy code
cd flasky
Create and activate a virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Configure environment variables:
Create a .env file in the root directory.
Define the following variables:
plaintext
Copy code
FLASK_APP=flasky.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=your_database_uri
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
Initialize the database:
bash
Copy code
flask db upgrade
Run the application:
bash
Copy code
flask run
The application will be accessible at http://localhost:5000 by default.

Contributing
Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please open an issue on the GitHub repository.

License
This project is licensed under the MIT License. See the LICENSE file for details.
