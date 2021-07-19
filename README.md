# Learning Journal Built with Flask


Summary:

This app uses Flask to create a web app for creating and updating journal entries.
The app data is stored in a database created through the peewee module.
User can navigate the web app in a browser to create, read, update, and delete entries.
On the initial run of app, a journal.db file will be created with placeholder data from entry.csv file.


Setup:

1. Create a new virtual Python environment

python -m venv env

2. Activate your new virtual Python environment

Mac/Linux:

source ./env/bin/activate

Windows:

.\env\Scripts\activate

3. Install required dependencies into your Python environment

pip install -r requirements.txt

4. Run the app

python app.py

