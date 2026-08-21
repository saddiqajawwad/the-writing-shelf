from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "book-nook-secret-key"


# Connect to the database
def get_db_connection():
    connection = sqlite3.connect("instance/blog.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create the database table if it does not exist
def create_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# Home page
@app.route("/")
def home():
    connection = get_db_connection()

    posts = connection.execute(
        "SELECT * FROM posts ORDER BY created_at DESC"
    ).fetchall()

    connection.close()

    return render_template("home.html", posts=posts)


# Add a new post
@app.route("/add", methods=["GET", "POST"])
def add_post():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        if not title.strip() or not content.strip():
            flash("Please fill in both the title and content.")
            return redirect(url_for("add_post"))

        connection = get_db_connection()

        connection.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title, content)
        )

        connection.commit()
        connection.close()

        flash("Your story has been added to the shelf.")

        return redirect(url_for("home"))

    return render_template("add.html")


# View one post
@app.route("/post/<int:post_id>")
def view_post(post_id):

    connection = get_db_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    connection.close()

    if post is None:
        return render_template("404.html"), 404

    return render_template("post.html", post=post)


# Edit a post
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    connection = get_db_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    if post is None:
        connection.close()
        return render_template("404.html"), 404

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        if not title.strip() or not content.strip():
            flash("Please fill in both the title and content.")
            connection.close()
            return redirect(url_for("edit_post", post_id=post_id))

        connection.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id)
        )

        connection.commit()
        connection.close()

        flash("Your story has been updated.")

        return redirect(url_for("view_post", post_id=post_id))

    connection.close()

    return render_template("edit.html", post=post)


# Delete a post
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM posts WHERE id = ?",
        (post_id,)
    )

    connection.commit()
    connection.close()

    flash("The page has been removed from your shelf.")

    return redirect(url_for("home"))


# Search posts
@app.route("/search")
def search():

    search_text = request.args.get("q", "").strip()

    connection = get_db_connection()

    posts = connection.execute(
        """
        SELECT * FROM posts
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
        """,
        (f"%{search_text}%", f"%{search_text}%")
    ).fetchall()

    connection.close()

    return render_template(
        "search.html",
        posts=posts,
        search_text=search_text
    )


# Create database when the application starts
create_database()


if __name__ == "__main__":
    app.run(debug=True)