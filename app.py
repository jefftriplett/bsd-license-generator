import os
import textwrap

from datetime import datetime
from flask import Flask, request, render_template
from flaskext.markdown import Markdown


app = Flask(__name__)
Markdown(app)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/colophon')
def colophon():
    content = open('README.md', 'r').read()
    return render_template('colophon.html', content=content)


@app.route('/license', methods=['GET'])
def license():
    columns = request.args.get('columns', 79, type=int) - 1
    organization = request.args.get('organization', None)
    owner = request.args.get('owner', None)
    license = request.args.get('license', None)
    data = {
        'organization': organization or '*ORGANIZATION*',
        'owner': owner or '*OWNER*',
        'year': datetime.now().strftime('%Y')
    }
    licenses = {
        'bsd3': 'bsd-3-clause.txt',
        'bsd4': 'bsd-4-clause.txt',
        'mit3': 'mit-3-clause.txt',
        'mit4': 'mit-4-clause.txt',
    }

    template_name = os.path.join('licenses', licenses[license or 'bsd3'])
    license = render_template(template_name, **data)
    license = '\n'.join([textwrap.fill(line, columns, subsequent_indent='   ' if line.startswith(' * ') else '') for line in license.split('\n')])

    return render_template('license.html', license=license)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
