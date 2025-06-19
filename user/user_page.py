from flask import Flask, render_template_string
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    # Load CSV
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/recommended_news.csv'))
    df = pd.read_csv(csv_path)

    # Format date and handle optional category
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df['publishedAt'] = df['publishedAt'].dt.strftime('%B %d, %Y, %I:%M %p')
    if 'category' not in df.columns:
        df['category'] = 'General'

    news_list = df.to_dict(orient='records')

    # Embedded HTML Template
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Recommended News</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                font-family: Arial, sans-serif;
            }
            th, td {
                border: 1px solid #aaa;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #444;
                color: white;
            }
            td a {
                color: #1a0dab;
            }
            button {
                margin-top: 5px;
                padding: 5px 10px;
                background-color: #008CBA;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #005f73;
            }
        </style>
    </head>
    <body>
        <h1>Recommended News</h1>
        <table>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Category</th>
                <th>Published At</th>
                <th>Actions</th>
            </tr>
            {% for article in news %}
            <tr>
                <td>{{ article.title }}</td>
                <td>{{ article.description }}</td>
                <td>{{ article.category }}</td>
                <td>{{ article.publishedAt }}</td>
                <td>
                    <a href="{{ article.url }}" target="_blank">Read More</a><br>
                    <button onclick="alert('Liked: {{ article.title }}')">Like</button>
                    <button onclick="alert('Saved: {{ article.title }}')">Save</button>
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''

    return render_template_string(html, news=news_list)

if __name__ == '__main__':
    app.run(port=5000)
