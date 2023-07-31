### CS6460 Project: Developing a Multimodal Conversation Interface for Personalized Foreign Language Learning using Large Language Models

Created by [Owen Sizemore](mailto:psizemore3@gatech.edu)

The following instructions will serve as a guide for accessing and running the project on a local computer.
1. Ensure that Python is installed on your local computer.
2. Clone the repository to your computer with the command `git clone https://github.com/owensizemore/cs6460project.git`, or by following the cloning steps on the GitHub website.
3. In your local file system or terminal, navigate to the project repository with the command `cd cs6460project`.
4. Create a new virtual environment with the command `python -m venv venv`. Note that you may have to run this command with python3 depending on the Python version installed on your computer.
5. Activate the virtual environment with the command `. venv/bin/activate`.
6. Install the required Python libraries for the project with the command `pip install -r requirements.txt`.
7. Create a copy of the example environment variables file with the command `cp .env.example .env`.
8. In your preferred IDE (such as VSCode), open the project repository and navigate to the newly-created `.env` file. Add your own API Keys for `OPENAI_API_KEY` and `ASTICA_API_KEY`.
9. Save the `.env` file and use the command `flask run` to begin the Flask application. Note that if the error message “Error: While importing 'app', an ImportError was raised.” appears in your console, check the `app.py` file for any libraries that were not properly installed and install them with the command `pip install [LIBRARY_NAME]`.
10. Navigate to `127.0.0.1:5000/` or `localhost:5000/` in your browser to open the Flask application.

If you experience error messages involving the openai library while interacting with the Flask application, complete the following steps:
1. Uninstall the openai package with the command `pip uninstall openai`.
2. Upgrade your pip installation with the command `pip install --upgrade pip`.
3. Reinstall the openai package with the command `pip install openai`.
