Project Structure Scanner - README
Overview
The Project Structure Scanner is a Python-based GUI application that allows you to scan a folder's contents and create a structured overview of its files and directories. The application scans for specific file types, displays the project structure, and exports this information in Markdown, JSON, or plain text format.

Features
GUI interface to select folders and scan project structures.
Filters for specific file types (.js, .ts, .py, .md, etc.).
Exports results in multiple formats: Markdown, JSON, and Text.
Progress bar and status updates during the scanning process.
Requirements
Python 3.7 or later
Required Packages: tkinter, os, pathlib, json, datetime, threading
Installation
Clone or download the script file onto your machine.

Open a terminal and ensure Python 3.7+ is installed:

bash
Copy code
python --version
No additional libraries are required, as tkinter and other packages are included in the standard Python library.

Usage Instructions
Run the Script: Open a terminal in the script's directory and run:

bash
Copy code
python path_to_your_script.py
Using the GUI:

Select Folder: Click the "Select Folder" button to choose the project folder to scan.
Choose Export Format: Select the desired output format (Markdown, JSON, or Text) in the "Export Format" section.
View Progress: A progress bar will display the scan status.
Once complete, the exported file will be saved in the selected folder.
Supported File Types: The scanner filters files with specific extensions, such as .js, .py, .md, and other common project files like package.json and requirements.txt.

Exported Data
The exported files contain:

Project Name
Scan Date
Directory Structure: A nested structure of the project folder.
File Details: File size, last modified date, and file content (if readable).
Example Output
Here’s an example of the structure in Markdown format:

markdown
Copy code
# Project: example_project

Scanned on: 2024-11-14

## Directory Structure

- folder1
  - file1.py
  - folder2
    - file2.js

## Files

### folder1/file1.py
**Size:** 123 bytes
**Last Modified:** 2024-11-14 15:30:00

Content of file1.py

Copy code
Notes
If a file cannot be read, an error message will be included in the exported file.
If you encounter any issues, ensure you have the necessary permissions to access the folders being scanned.