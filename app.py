from flask import Flask, render_template, request, session
import math
import re

app = Flask(__name__)
app.secret_key = "sketchbook_secret"

profile_data = {
    "name": "Prince Martin",
    "title": "Data Structure and Algorithm | BSCPE 2-3",
    "location": "Navotas, Philippines",
    "email": "princegabmartin@gmail.com",
    "phone": "+639159442573",
    "github": "github.com/princegabmartin",
    "about": "I am an artist and creative developer who enjoys blending imagination, color, and technology. I draw ideas into life through visual storytelling, design, and thoughtful digital experiences.",
    "education": "Bachelor of Science in Computer Engineering",
    "skills": ["Swimming", "Sketching", "Python", "Flask", "Portrait Drawing"],
    "interests": ["Art", "Drawing", "Food", "Games"]
}

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
}


def infix_to_postfix(expression):
    if expression is None:
        raise ValueError("Please enter an infix expression.")

    expr = expression.strip()
    if not expr:
        raise ValueError("Please enter an infix expression.")

    tokens = re.findall(r'\d+(?:\.\d+)?|[A-Za-z_]\w*|[()+\-*/%^]', expr)

    if not tokens:
        raise ValueError("Please enter a valid infix expression.")

    postfix = []
    stack = []

    for token in tokens:
        if re.fullmatch(r'\d+(?:\.\d+)?|[A-Za-z_]\w*', token):
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses.")
            stack.pop()
        elif token in PRECEDENCE:
            while (
                stack and stack[-1] != '(' and
                PRECEDENCE.get(stack[-1], 0) >= PRECEDENCE[token]
            ):
                postfix.append(stack.pop())
            stack.append(token)
        else:
            raise ValueError(f"Unsupported token: {token}")

    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses.")
        postfix.append(stack.pop())

    return " ".join(postfix)


@app.route("/")
def index():
    return render_template("index.html", profile=profile_data)


@app.route("/profile")
def profile():
    return render_template("profile.html", profile=profile_data)


@app.route("/works", methods=["GET", "POST"])
def works():
    result = None
    postfix_result = None
    infix_expression = ""

    if request.method == "POST":
        if "inputString" in request.form:
            text = request.form.get("inputString", "").strip()
            result = text.upper()

        elif "infixExpression" in request.form:
            infix_expression = request.form.get("infixExpression", "").strip()
            try:
                postfix_result = infix_to_postfix(infix_expression)
            except ValueError as exc:
                postfix_result = str(exc)

    return render_template(
        "works.html",
        result=result,
        postfix_result=postfix_result,
        infix_expression=infix_expression,
    )


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
                message = "Please enter a name."

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