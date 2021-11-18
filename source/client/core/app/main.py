from flask import Flask, jsonify, request, render_template
import endpoint_constants
import constants
import app_constants
import random

app = Flask(__name__)

@app.context_processor
def inject_endpoint_constants():
    return dict(
      home_endpoint = in_post_link.__name__,
      crawled_content_endpoint = handle_crawled_content.__name__
    )

@app.route("/error", methods=['GET'])
def handle_error():
  error_dict = {'error_status': 404, 'error_message': 'Page not found'}
  return render_template('./error/error.html', error=error_dict)

@app.route(endpoint_constants.CLIENT, methods=['GET'])
def in_post_link() -> str:
  return render_template("./section/home.html", logged_in=True)

@app.route(endpoint_constants.CRAWLED_CONTENT, methods=['GET'])
def handle_crawled_content() -> str:
  random_dict = dict()
  for i in range(0, 15):
    n = random.randint(1, 30)
    m = random.randint(1, 100)
    random_dict[n]=m

  return render_template("./section/crawled_content.html", logged_in=False, table_vals=random_dict)

if __name__ == '__main__':
  app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)