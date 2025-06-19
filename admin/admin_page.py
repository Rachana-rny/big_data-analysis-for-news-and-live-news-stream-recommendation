from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is working! Visit <a href='/admin'>/admin</a> to view the dashboard."

@app.route('/admin')
def admin_dashboard():
    try:
        # Load the CSV file
        df = pd.read_csv("../data/user_interaction.csv")

        # Group by 'action' and count
        summary = df.groupby('action').size().to_dict()
    except Exception as e:
        return f"<h2>Error loading CSV:</h2><pre>{e}</pre>"

    # Inline HTML Template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }
            h1 { color: #333; }
            ul { padding: 0; list-style: none; }
            li { background: #fff; margin: 10px 0; padding: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>User Interaction Summary</h1>
        <ul>
            {% for action, count in summary.items() %}
                <li><strong>{{ action }}:</strong> {{ count }}</li>
            {% endfor %}
        </ul>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    """

    return render_template_string(html_template, summary=summary)

if __name__ == '__main__':
    app.run(port=5001)
