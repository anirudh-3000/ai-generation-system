from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

@app.route('/')
def index():
    """Home page with login form."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login by user_id."""
    user_id = request.form['user_id'].strip()
    if user_id:
        # Fetch record from the database
        user_content = database.fetch_record(user_id)
        if user_content:
            # Log user login activity
            database.log_activity(user_id, "Login attempt")

            # Check if content generation is completed
            if user_content[4] == 'Completed':  # Check 'status' column
                # Log content view activity
                database.log_activity(user_id, "Content view")
                return redirect(url_for('view_content', user_id=user_id))
            else:
                return render_template('processing.html', user_id=user_id)
        else:
            return render_template('not_found.html')  # User not found
    return render_template('index.html', error="User ID is required.")

@app.route('/view_content/<user_id>')
def view_content(user_id):
    """Display the generated videos and images if available."""
    # Fetch user content
    user_content = database.fetch_record(user_id)
    
    if user_content:
        prompt = user_content[1]
        # Fetch paths from the record
        video_paths = user_content[2].split(',') if user_content[2] else []
        image_paths = user_content[3].split(',') if user_content[3] else []

        return render_template('view_content.html', prompt=prompt, user_id=user_id, video_paths=video_paths, image_paths=image_paths)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logout the user and return to the home page."""
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)