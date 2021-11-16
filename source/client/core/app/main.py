from flask import Flask, jsonify, request, render_template
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)

@app.route("/login", methods=['GET'])
def login():
  return render_template('./modal/login.html')

@app.route(endpoint_constants.CLIENT, methods=['GET'])
def in_post_link() -> str:
  return render_template("./section/home.html", logged_in=False)

if __name__ == '__main__':
  app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)