from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up the database
database_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

# Catalog model for the basic catalog table
class CatalogItem(db.Model):
    __tablename__ = 'catalog_items'
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.Text, nullable=True)
    long_description = db.Column(db.Text, nullable=True)
    specifications = db.Column(db.JSON, nullable=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/catalog')
def catalog():
    catalog_items_count = CatalogItem.query.count()
    
    num_rows = 3  # Change this variable to generate more or fewer rows
    
    page_html = f'''
    <h1>This is the catalog page.</h1>

    <h3>Currently there are {catalog_items_count} items in the catalog.</h3>

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