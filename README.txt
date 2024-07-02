Excel to JSON Layouts Converter

This Streamlit application allows you to upload an Excel file and convert its content to a JSON structure. The progress of the conversion is displayed with a progress spinner.

Prerequisites

Make sure you have Python installed on your system. You can download Python from https://www.python.org/.

Setup and Running the Application

Follow these steps to set up the virtual environment, install dependencies, and run the Streamlit application using the provided bash script:

1. Make the Bash Script Executable

   Give execute permission to the `setup_and_run.sh` script:

   chmod +x setup_and_run.sh

2. Run the Bash Script

   Execute the bash script to set up the virtual environment, install dependencies, and run the Streamlit app:

   ./setup_and_run.sh

   This script will:
   - Create a virtual environment if it doesn't already exist.
   - Activate the virtual environment.
   - Install the required packages listed in `requirements.txt`.
   - Run the Streamlit app.
   - Deactivate the virtual environment after exiting Streamlit.

3. Access the Application

   Once the script runs, you can access the Streamlit application in your web browser at http://localhost:8501.

Usage

1. Open the application in your web browser.
2. Upload an Excel file using the file uploader.
3. Wait for the progress spinner to complete.
4. View the resulting JSON structure in the app.
5. Optionally, download the JSON output using the provided download button.

File Overview

- `streamlit_app.py`: The main script containing the Streamlit application and the functions for processing the Excel file.
- `setup_and_run.sh`: Bash script to set up the virtual environment, install dependencies, and run the Streamlit app.
- `requirements.txt`: List of required Python packages for the project.

Additional Notes

- Ensure your Excel file has the following sheets: `Panel settings`, `panel name`, `Market settings`, `Market name`, `Selections settings`.
- The JSON structure generated is based on the data from these sheets.

License

This project is licensed under the MIT License.

Acknowledgments

Thanks to the contributors and the open-source community for their valuable resources and support.
