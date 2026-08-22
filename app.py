from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "book-nook-secret-key"


# Open a connection to the SQLite database.
# sqlite3.Row lets us access database columns by their names,
# which makes the returned data easier to use in Jinja templates.
def get_db_connection():
    connection = sqlite3.connect("instance/blog.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create the posts table if the database does not already contain it.
# This function runs when the application starts, so the required
# table is available before any post-related route is used.
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


# The home page loads all saved posts from the database.
# Posts are ordered by creation time so the newest entries appear first.
@app.route("/")
def home():
    connection = get_db_connection()

    posts = connection.execute(
        "SELECT * FROM posts ORDER BY created_at DESC"
    ).fetchall()

    connection.close()

    return render_template("home.html", posts=posts)


# The add page handles both displaying the writing form and saving
# a new post. GET displays the form, while POST processes its data.
@app.route("/add", methods=["GET", "POST"])
def add_post():

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # strip() removes surrounding whitespace before checking
        # whether the user has actually entered any content.
        if not title.strip() or not content.strip():
            flash("Please fill in both the title and content.")
            return redirect(url_for("add_post"))

        connection = get_db_connection()

        # Parameterized SQL values are used here instead of building
        # the query directly from user input.
        connection.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title, content)
        )

        connection.commit()
        connection.close()

        flash("Your story has been added to the shelf.")

        # After saving the post, return to the home page so the new
        # entry can immediately appear on the shelf.
        return redirect(url_for("home"))

    # A GET request simply displays the empty writing form.
    return render_template("add.html")


# Display a single post using its database ID.
@app.route("/post/<int:post_id>")
def view_post(post_id):

    connection = get_db_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    connection.close()

    # If the requested ID does not exist, show the custom 404 page.
    if post is None:
        return render_template("404.html"), 404

    return render_template("post.html", post=post)


# The edit route first retrieves the existing post.
# GET displays the current values in the form, while POST updates them.
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    connection = get_db_connection()

    post = connection.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    # Editing a post that does not exist should result in the same
    # custom error page used by the individual post route.
    if post is None:
        connection.close()
        return render_template("404.html"), 404

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # Do not allow the existing post to be replaced with an
        # empty title or empty content.
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

        # Once the update is complete, show the edited post.
        return redirect(url_for("view_post", post_id=post_id))

    connection.close()

    # For a GET request, send the existing post to the edit template
    # so its title and content can be displayed in the form.
    return render_template("edit.html", post=post)


# Delete a post using its database ID.
# This route accepts POST requests because deleting data changes
# the contents of the database.
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

    # Return to the home page after the post has been deleted.
    return redirect(url_for("home"))


# Search through saved posts using the text provided in the URL.
# The search checks both the title and the content of each post.
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

    # The original search text is also sent to the template so it
    # can remain visible in the search field.
    return render_template(
        "search.html",
        posts=posts,
        search_text=search_text
    )


# Make sure the database and its required table exist before
# the Flask development server starts handling requests.
create_database()


# This block runs the development server only when app.py is
# executed directly, rather than when the file is imported.
if __name__ == "__main__":
    app.run(debug=True)
