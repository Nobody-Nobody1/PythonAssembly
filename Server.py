from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
        <h1>Hello from Python!</h1>
        <p>This is now running in a browser.</p>
    """)

if __name__ == "__main__":
    app.run(debug=True)
