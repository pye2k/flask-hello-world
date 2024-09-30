from flask import Flask, render_template, request, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import enricher

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
    items = CatalogItem.query.order_by(desc(CatalogItem.id)).all()
    
    # Render the catalog.html template and pass the items to it
    return render_template('catalog.html', items=items)

@app.route('/catalog/add', methods=['GET', 'POST'])
def add_catalog_item():
    if request.method == 'POST':
        input_text = request.form['inputText']
        
        # Call the enricher.go function to process the input text
        enriched_resp = enricher.go(input_text)
        enriched_data = json.loads(enriched_resp.replace('\n', ''))

        # Extract the fields from the returned JSON object
        title = enriched_data.get('title')
        short_description = enriched_data.get('short_description')
        detailed_description = enriched_data.get('detailed_description')
        specifications = enriched_data.get('specifications')

        print(title)
        print(short_description)
        print(detailed_description)
        print(specifications)
      
        # Create a new CatalogItem object with the extracted data
        new_item = CatalogItem(
            input=input_text,
            title=title,
            short_description=short_description,
            long_description=detailed_description,
            specifications=specifications
        )
        
        # Persist the new item to the database
        db.session.add(new_item)
        db.session.commit()
    
        # Redirect to some confirmation or the catalog list after adding
        return redirect(url_for('catalog'))
    
    # Render the form when the method is GET
    return render_template('catalog_add.html')