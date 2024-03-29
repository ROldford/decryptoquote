from flask import Flask, render_template, request, abort
from decryptoquote.decryptoquote import decrypt_quote, decrypt_quote_fully

app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_index():
    return render_template('index.html'), 200


# form data:
# required: full_solve, coded_quote
# optional: coded_author
@app.route("/solution", methods=['GET'])
def get_solution():
    coded_quote = request.args.get('codedQuote')
    coded_author = request.args.get('codedAuthor')
    full_solve = request.args.get('fullSolve')
    show_cypher = request.args.get('showCypher') is not None
    if not coded_quote:
        if coded_quote == "":
            return render_index(form_data_invalid=True), 400
        abort(400)
    if full_solve:
        solutions = decrypt_quote_fully(
            coded_quote, coded_author=coded_author, show_cypher=show_cypher)
    else:
        solutions = decrypt_quote(
            coded_quote, coded_author=coded_author, show_cypher=show_cypher)
        # TODO template needs loading indicator
    return render_index(solutions=solutions), 200


@app.errorhandler(400)
def bad_request(error):
    return render_index(bad_request=True), 400


@app.errorhandler(500)
def server_error(error):
    return render_index(server_error=True), 500


def render_index(**kwargs):
    return render_template('index.html', **kwargs)


# @app.route('/hello/', methods=['GET', 'POST'])
# def welcome():
#     return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
