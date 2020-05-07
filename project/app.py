from flask import Flask, render_template, request, render_template
from sparql import spa


app = Flask(__name__, template_folder='templates')

x = spa()

x = "heihei"

@app.route("/", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        author = request.form["author"]
        print(author)

        #return render_template("response.html", content=response)
    else:
        response = ""
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)




