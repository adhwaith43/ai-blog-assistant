from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database helper
def get_db():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db()
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("create.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("edit.html", post=post)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    conn.close()
    app.run(debug=True)
