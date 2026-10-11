from flask import Flask, render_template, request, session
import math

app = Flask(__name__)
app.secret_key = "sketchbook_secret"

profile_data = {
    "name": "Prince Martin",
    "title": "Data Structure Algorithms | BSCPE 2-3",
    "location": "Manila, Philippines",
    "email": "princegabmartin@gmail.com",
    "phone": "+63 915 944 2573",
    "github": "github.com/princegabmartin",
    "about": "I am an artist and creative developer who enjoys blending imagination, color, and technology. I draw ideas into life through visual storytelling, design, and thoughtful digital experiences.",
    "education": "Bachelor of Science in Computer Engineering",
    "skills": ["Illustration", "Sketching", "Swimming", "Python", "Flask"],
    "interests": ["Art", "Drawing", "Design", "Creative Coding"]
}

def convert_infix_to_postfix(infix):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    for char in infix:
        if char.isalnum():
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack:
                stack.pop()
        elif char in precedence:
            while (
                stack
                and stack[-1] != '('
                and stack[-1] in precedence
                and precedence[stack[-1]] >= precedence[char]
            ):
                postfix.append(stack.pop())
            stack.append(char)

    while stack:
        postfix.append(stack.pop())

    return ''.join(postfix)

@app.route("/")
def index():
    return render_template("index.html", profile=profile_data)

@app.route("/profile")
def profile():
    return render_template("profile.html", profile=profile_data)

@app.route("/works", methods=["GET", "POST"])
def works():
    result = None
    if request.method == "POST":
        text = request.form.get("inputString", "").strip()
        result = text.upper()
    return render_template("works.html", result=result)

@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result = None
    radius = ""
    if request.method == "POST":
        radius = request.form.get("radius", "").strip()
        try:
            r = float(radius)
            if r < 0:
                result = "Radius must be positive."
            else:
                result = round(math.pi * r * r, 2)
        except ValueError:
            result = "Please enter a valid number."
    return render_template("circle.html", result=result, radius=radius)

@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result = None
    base = ""
    height = ""
    if request.method == "POST":
        base = request.form.get("base", "").strip()
        height = request.form.get("height", "").strip()
        try:
            b = float(base)
            h = float(height)
            if b < 0 or h < 0:
                result = "Base and height must be positive."
            else:
                result = round(0.5 * b * h, 2)
        except ValueError:
            result = "Please enter valid numbers."
    return render_template("triangle.html", result=result, base=base, height=height)

@app.route("/works/infix-postfix", methods=["GET", "POST"])
def infix_postfix():
    result = None
    infix = ""
    if request.method == "POST":
        infix = request.form.get("infix", "").strip()
        try:
            result = convert_infix_to_postfix(infix)
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("infix_postfix.html", result=result, infix=infix)

@app.route("/works/linked-list", methods=["GET", "POST"])
def linked_list():
    if "linked_list" not in session:
        session["linked_list"] = ["Bloom", "Ink", "Canvas", "Sketch"]

    items = session["linked_list"]
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "add":
            if value:
                if value not in items:
                    items.append(value)
                    message = f"Added '{value}' to the sketchpad."
                else:
                    message = f"'{value}' is already on the page."
            else:
                message = "Please enter a value."

        elif action == "delete":
            if value and value in items:
                items.remove(value)
                message = f"Removed '{value}' from the sketchpad."
            else:
                message = "Item not found."

        elif action == "clear":
            items.clear()
            message = "Sketchpad cleared."

        session["linked_list"] = items

    return render_template("linked_list.html", linked_list=items, message=message)

@app.route("/contact")
def contact():
    return render_template("contact.html", profile=profile_data)

if __name__ == "__main__":
    app.run(debug=True)