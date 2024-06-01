from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
import pandas as pd
import os
import uuid
import matplotlib.pyplot as plt
import io
import base64
new_app = Blueprint('new_app', __name__)
# Function to save DataFrame to a file and return the file path
def save_dataframe(df):
    filepath = os.path.join(current_app.config['DATAFRAME_FOLDER'], f"{uuid.uuid4()}.pkl")
    df.to_pickle(filepath)
    return filepath
@new_app.route("/new")
def hello_world():
    filepath = session.get('dataframe_path')
    if filepath and os.path.exists(filepath):
        df = pd.read_pickle(filepath)
        data_preview = df.head().to_html()
        return render_template('new_app.html', data_preview=data_preview, columns=df.columns)
    else:
        return "<h1>No CSV file found</h1>"
@new_app.route("/perform_encoding", methods=["POST"])
def perform_encoding():
    filepath = session.get('dataframe_path')
    if filepath and os.path.exists(filepath):
        df = pd.read_pickle(filepath)
        encoding_type = request.form["encoding_type"]
        column = request.form["column"]
        if encoding_type == "one_hot":
            df = pd.get_dummies(df, columns=[column])
        elif encoding_type == "target_guided_ordinal":
            target_column = request.form["target_column"]
            ordered_labels = df.groupby([column])[target_column].mean().sort_values().index
            ordinal_mapping = {k: i for i, k in enumerate(ordered_labels, 0)}
            df[column] = df[column].map(ordinal_mapping)
        elif encoding_type == "ordinal":
            ordinal_labels = request.form["ordinal_labels"].split(",")
            ordinal_mapping = {k: i for i, k in enumerate(ordinal_labels, 0)}
            df[column] = df[column].map(ordinal_mapping)
        elif encoding_type == "drop_column":
            df = df.drop(columns=[column])
        # Save the updated DataFrame
        dataframe_path = save_dataframe(df)
        session['dataframe_path'] = dataframe_path
        data_preview = df.head().to_html()
        return render_template('new_app.html', data_preview=data_preview, columns=df.columns)
    return redirect(url_for("new_app.hello_world"))
@new_app.route("/handle_missing_values", methods=["POST"])
def handle_missing_values():
    filepath = session.get('dataframe_path')
    if filepath and os.path.exists(filepath):
        df = pd.read_pickle(filepath)
        action = request.form["missing_value_action"]
        column = request.form["column"]
        if action == "replace_mean":
            df[column].fillna(df[column].mean(), inplace=True)
        elif action == "replace_median":
            df[column].fillna(df[column].median(), inplace=True)
        elif action == "replace_mode":
            df[column].fillna(df[column].mode()[0], inplace=True)
        elif action == "drop_row":
            df.dropna(subset=[column], inplace=True)
        # Save the updated DataFrame
        dataframe_path = save_dataframe(df)
        session['dataframe_path'] = dataframe_path
        data_preview = df.head().to_html()
        return render_template('new_app.html', data_preview=data_preview, columns=df.columns)
    return redirect(url_for("new_app.hello_world"))
@new_app.route("/plot_graph", methods=["POST"])
def plot_graph():
    filepath = session.get('dataframe_path')
    if filepath and os.path.exists(filepath):
        df = pd.read_pickle(filepath)
        plot_type = request.form["plot_type"]
        x_column = request.form["x_column"]
        y_column = request.form["y_column"] if request.form["y_column"] else None
        plt.figure()
        try:
            if plot_type == "plot":
                plt.plot(df[x_column], df[y_column])
            elif plot_type == "scatter":
                plt.scatter(df[x_column], df[y_column])
            elif plot_type == "bar":
                plt.bar(df[x_column], df[y_column])
            elif plot_type == "hist":
                plt.hist(df[x_column])
            elif plot_type == "boxplot":
                plt.boxplot(df[x_column])
            elif plot_type == "pie":
                plt.pie(df[x_column].value_counts(), labels=df[x_column].value_counts().index)
            elif plot_type == "stem":
                plt.stem(df[x_column], df[y_column])
            elif plot_type == "fill_between":
                plt.fill_between(df[x_column], df[y_column])
            elif plot_type == "stackplot":
                plt.stackplot(df[x_column], df[y_column])
            elif plot_type == "stairs":
                plt.stairs(df[x_column], df[y_column])
            elif plot_type == "errorbar":
                plt.errorbar(df[x_column], df[y_column])
            elif plot_type == "violinplot":
                plt.violinplot(df[x_column])
            elif plot_type == "eventplot":
                plt.eventplot(df[x_column])
            elif plot_type == "hist2d":
                plt.hist2d(df[x_column], df[y_column])
            elif plot_type == "hexbin":
                plt.hexbin(df[x_column], df[y_column])
            elif plot_type == "ecdf":
                plt.ecdf(df[x_column])
            elif plot_type == "imshow":
                plt.imshow(df[[x_column, y_column]].values)
            elif plot_type == "pcolormesh":
                plt.pcolormesh(df[[x_column, y_column]].values)
            elif plot_type == "contour":
                plt.contour(df[x_column], df[y_column])
            elif plot_type == "contourf":
                plt.contourf(df[x_column], df[y_column])
            elif plot_type == "barbs":
                plt.barbs(df[x_column], df[y_column])
            elif plot_type == "quiver":
                plt.quiver(df[x_column], df[y_column])
            elif plot_type == "streamplot":
                plt.streamplot(df[x_column], df[y_column])
            elif plot_type == "tricontour":
                plt.tricontour(df[x_column], df[y_column])
            elif plot_type == "tricontourf":
                plt.tricontourf(df[x_column], df[y_column])
            elif plot_type == "tripcolor":
                plt.tripcolor(df[x_column], df[y_column])
            elif plot_type == "triplot":
                plt.triplot(df[x_column], df[y_column])
            elif plot_type == "scatter3d":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(df[x_column], df[y_column], df[y_column])
            elif plot_type == "plot_surface":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(df[x_column], df[y_column], df[y_column])
            elif plot_type == "plot_trisurf":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_trisurf(df[x_column], df[y_column], df[y_column])
            elif plot_type == "voxels":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.voxels(df[x_column], df[y_column], df[y_column])
            elif plot_type == "plot_wireframe":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_wireframe(df[x_column], df[y_column], df[y_column])
            else:
                return "<h1>Invalid plot type selected</h1>"
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            data_preview = df.head().to_html()
            return render_template('new_app.html', data_preview=data_preview, columns=df.columns, plot_url=plot_url)
        except Exception as e:
            return f"<h1>Error creating plot: {e}</h1>"
    return redirect(url_for("new_app.hello_world"))
@new_app.route("/go_back")
def go_back():
    return redirect(url_for("home"))
