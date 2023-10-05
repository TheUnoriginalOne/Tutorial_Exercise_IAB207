# Import necessary modules from the 'travel' package
from travel import db, create_app

# Create a Flask application using the 'create_app' function
app = create_app()

# Create an application context to work within the Flask application
ctx = app.app_context()

# Push the application context to make it the active context
ctx.push()

# Create database tables based on SQLAlchemy model definitions
db.create_all()

# Exit the script
quit()
