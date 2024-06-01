

from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import io
from new_app import new_app  # Import the blueprint
import uuid
import numpy as np 
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management
UPLOAD_FOLDER = 'uploads'
DATAFRAME_FOLDER = 'dataframes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATAFRAME_FOLDER'] = DATAFRAME_FOLDER
# Register the blueprint
app.register_blueprint(new_app, url_prefix='/')
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DATAFRAME_FOLDER):
    os.makedirs(DATAFRAME_FOLDER)
# Function to load CSV file and return DataFrame
def load_csv(filepath):
    return pd.read_csv(filepath)
# Function to perform operations on DataFrame
def perform_operation(df, operation, column=None):
    if operation == "mean":
        return df[column].mean() if column else df.mean().to_frame().to_html()
    elif operation == "median":
        return df[column].median() if column else df.median().to_frame().to_html()
    elif operation == "mode":
        return df[column].mode().iloc[0] if column else df.mode().iloc[0].to_frame().to_html()
    elif operation == "null_values":
        return df.isnull().sum().to_frame().to_html()
    elif operation == "total_null_values":
        return str(df.isnull().sum().sum())
    elif operation == "shape":
        return str(df.shape)
    elif operation == "description":
        return df.describe().to_html()
    elif operation == "info":
        buf = io.StringIO()
        df.info(buf=buf)
        return "<pre>" + buf.getvalue() + "</pre>"
    elif operation == "head":
        return df.head().to_html()
    else:
        return "Invalid operation"
# Function to save DataFrame to a file and return the file path
def save_dataframe(df):
    filepath = os.path.join(app.config['DATAFRAME_FOLDER'], f"{uuid.uuid4()}.pkl")
    df.to_pickle(filepath)
    return filepath
# Home route
@app.route("/")
def home():
    filepath = session.get('dataframe_path')
    if filepath and os.path.exists(filepath):
        df = pd.read_pickle(filepath)
        columns = df.columns.tolist()
        return render_template("index.html", columns=columns)
    return render_template("index.html")
# Route to handle CSV upload and display column selection
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            session['filename'] = file.filename  # Save the filename in session
            df = load_csv(filepath)
            dataframe_path = save_dataframe(df)  # Save DataFrame to a file
            session['dataframe_path'] = dataframe_path  # Save the file path in session
            columns = df.columns.tolist()
            return render_template("index.html", columns=columns, file=file.filename)
    return redirect(url_for("home"))
# Route to handle operation selection and display result
@app.route("/perform_operation", methods=["POST"])
def perform_operation_route():
    if request.method == "POST":
        operation = request.form["operation"]
        filepath = session.get('dataframe_path')
        if filepath and os.path.exists(filepath):
            df = pd.read_pickle(filepath)
            column = request.form.get("column")
            result = perform_operation(df, operation, column)
            return render_template("index.html", result=result, file=session['filename'], columns=df.columns.tolist())
    return redirect(url_for("home"))
# New route to redirect to the blueprint
@app.route("/navigate")
def navigate():
    return redirect(url_for("new_app.hello_world"))
if __name__ == "__main__":
    app.run(debug=True)

