import json
from flask import Flask, render_template, request


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/', methods=['GET'])
def index():
    with open('databases/state_codes.json') as state_codes:
        state_dict = json.load(state_codes)
    name = request.args.get('name', 'World')
    return render_template('index.html', name=name, state_codes=state_dict)


if __name__ == "__main__":
    app.run(debug=True)
