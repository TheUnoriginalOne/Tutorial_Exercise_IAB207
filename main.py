# Import the 'create_app' function from the 'travel' package
from travel import create_app

# Check if this script is the main entry point (not imported as a module)
if __name__ == '__main__':
    # Create a Flask application using the 'create_app' function
    app = create_app()

    # Run the Flask application in debug mode on port 5001
    app.run(debug=True, port=5001)
