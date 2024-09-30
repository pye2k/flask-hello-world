from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/catalog')
def catalog():
    num_rows = 3  # Change this variable to generate more or fewer rows
    page_html = '''
    <h1>This is the catalog page.</h1>

    <table border="1">
        <tr>
            <th>Row Number</th>
            <th>Square of Row Number</th>
        </tr>
    '''
    for i in range(1, num_rows + 1):
        page_html += f'''
        <tr>
            <td>{i}</td>
            <td>{i**2}</td>
        </tr>
        '''
    page_html += '</table>'
    
    return page_html