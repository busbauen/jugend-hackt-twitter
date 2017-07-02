#!/usr/bin/env python
from flask import Flask
import twitter_fun
app = Flask(__name__)


@app.route("/")
def index():
    (tweet, choices, sol) = twitter_fun.generate_question()
    return "<strong>Tweet</strong>: {}<br><strong>Choices</strong>: {}<br><strong>Solution</strong>: {}".format(tweet, " ".join(choices),  sol)

if __name__ == '__main__':
    app.run(debug=True)
