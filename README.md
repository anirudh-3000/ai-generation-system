# AI Generation System

## Overview
Welcome to my AI Video and Image Generation System Assignment! This project is designed to demonstrate the integration of advanced AI tools to create motivational videos and images based on user-provided prompts. Below, you’ll find detailed information about the project’s functionality, setup, and usage.

## Project Description
The AI Video and Image Generation System allows users to generate motivational videos and images from text prompts. The system leverages AI tools for content creation and provides an intuitive web interface for users to access their content. Users are notified when their content is ready.

## Features

### 1. Text-to-Video and Text-to-Image Generation:
* Accepts a user-provided text prompt.
* Generates 5 videos and 5 images per prompt.
* Saves videos as .mp4 and images as .jpg or .png files.

### 2. Content Management:
* Stores generated content in generated_content/<user_id>/ directory.
* Tracks content and user activity in a database.

### 3. User Notifications:
* Notifies users when content at user specified time.(Prints an in-terminal text)
* Allows users to specify preferred notification time.
* User can leave the notification field blank if he/she wants to receive notification immediately after content generation


### 4. Web Page for User Access:
* Simple, user-friendly web page built with Flask.
* Users can log in using their unique identifier (user_id).
* Displays generated videos and images or status updates.

### 5. Activity Logging:
* Logs user login attempts and content views in the database.

## Technologies Used
* Programming Language: Python
* Web Framework: Flask 
* AI Tools:
- Diffusers Library (for video generation)
- Stable Diffusion (for image generation)
* Database: SQLite

## System overview
### 1. Text-to-Video and Text-to-Image Generation
* Running the main file carries out the main functionalities for content's generation.
* After running the main file, user will have fill two input fields, one for prompt and another for notification time.
* After entering a desired prompt, a unique user id is generated.
* After generation of unique id, user will have to enter a specific notification time in HH:MM format.
  - The notification is in form a simple print statement that will be printed on your terminal.
  - The notification will be printed only after the generation of whole of the content (5 videos and 5 images) is completed.
  - If the content is generated before user specified time: Notification will be printed at user specified time.
  - If the content is not generated before user specified time: Notification will be printed immediately after content is generated.
  - If user leaves notification time field empty: Notification will be printed immediately after content is generated.
* After filling both fields, content generation starts.
* After generation is completed, generated content is saved as:
  - Videos as .mp4 files.
  - Images as .png files.
* Content is then stored in a directory named generated_content/<user_id>/.

### 2. Storing and Managing Content:
An SQLite Database with the following tables is maintained: user_content and user_activity
1. user_content has following fields:
 - user_id: unique identifier for the user
 - prompt: text provided by the user
 - video_paths: string of file paths (paths separated by commas) to the generated videos
 - image_paths: list of file paths (paths separated by commas) to the generated images
 - status: "Processing" or "Completed"
 - generated_at: timestamp of content generation
* When user fills the both input fields, a unique user id is generated and generation starts following fields are updated: user_
* Once the generation is complete:
Mark the status as "Completed" in the database.
Notify the user that their content is ready (via email or console output) at specified time.
## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/anirudh-3000/ai-generation-system
```
```bash
cd ai-generation-system
```

###2. Install Dependencies
Install the required Python libraries using the requirements.txt file:
```bash
pip install -r requirements.txt
```

###3. Set Up the Database
Run the schema.sql file to create the necessary database tables:
```bash
sqlite3 content_generation.db < schema.sql
```

###4. Start the System
Run the two main components:

a. Generate Content
This generates the motivational videos and images:
```bash
python main.py
```
After running the main file, and entering your prompt, copy the unique user id that has been created.

b. Start the Web Server
This hosts the Flask app to let users log in and view their generated content:
```bash
python app.py
```
And finally, login via your unique user id to view your content.
