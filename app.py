from flask import Flask, render_template
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
    # Query all items from the CatalogItem table
    items = CatalogItem.query.all()
    
    # Render the catalog.html template and pass the items to it
    return render_template('catalog.html', items=items)