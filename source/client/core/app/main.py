from flask import Flask, jsonify, request, render_template
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)


@app.route(endpoint_constants.CLIENT, methods=['GET'])
def in_post_link() -> str:
  # text = request.json.get(constants.START_LINK_KEY, None)

  data = [
    ("01-01-2021", 1000),
    ("02-01-2021", 1200),
    ("03-01-2021", 100),
    ("04-01-2021", 2000),
    ("05-01-2021", 1000),
    ("06-01-2021", 1040),
    ("07-01-2021", 1200),
    ("08-01-2021", 1050),
    ("09-01-2021", 1500),
    ("10-01-2021", 5000)
  ]

  labels = [row[0] for row in data]
  values = [row[1] for row in data]

  return render_template("./dashboard_template/index.html")
  # return render_template("graph.html", labels=labels, values=values)
  # return render_template("./ample-admin-lite-master/dashboard.html")#, labels=labels, values=values)

if __name__ == '__main__':
  app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)