from flask import Flask, render_template, request, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import enricher
from enricher_openai import OpenAIEnricher
from enricher_anthropic import AnthropicEnricher
import base64
import re

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
    image_url = db.Column(db.Text, nullable=True)
    model = db.Column(db.Text, nullable=True)

@app.route('/')
def hello_world():
    return redirect(url_for('catalog'))

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
        # Clean up the resultant JSON
        enriched_resp = enriched_resp.replace('\n', '')
        # Remove leading and trailing spaces in keys using regex
        enriched_resp = re.sub(r'"\s*([^"]*?)\s*"\s*:', r'"\1":', enriched_resp)
        enriched_data = json.loads(enriched_resp)

        # Extract the fields from the returned JSON object
        title = enriched_data.get('title')
        short_description = enriched_data.get('short_description')
        detailed_description = enriched_data.get('detailed_description')
        specifications = enriched_data.get('specifications')

        print(f'''Persisting the following fields:
              Title         : {title}
              Short Desc    : {short_description}
              Detailed Desc : {detailed_description}
              Specifications: {specifications}

              For the input : {input_text}
              ''')

        # Create a new CatalogItem object with the extracted data
        new_item = CatalogItem(
            input=input_text,
            title=title,
            short_description=short_description,
            long_description=detailed_description,
            specifications=specifications,
            model="gpt-4o-mini"
        )
        
        # Persist the new item to the database
        db.session.add(new_item)
        db.session.commit()
    
        # Redirect to some confirmation or the catalog list after adding
        return redirect(url_for('catalog'))
    
    # Render the form when the method is GET
    return render_template('catalog_add.html')

@app.route('/catalog/realtime')
def catalog_realtime():
    # Get the 'id' query parameter from the URL
    item_id = request.args.get('id')
    if item_id is None:
        return "Error: No 'id' parameter provided. Please specify an 'id' in the URL."
    try:
        # Convert id to integer
        item_id = int(item_id)
    except ValueError:
        return "Error: Invalid 'id' parameter. Please provide a valid integer."

    # Query the CatalogItem with the given id
    item = CatalogItem.query.get(item_id)
    if item is None:
        return f"Error: No item found with id {item_id}."

    # Get the 'search_query' parameter if it exists
    search_query = request.args.get('search_query', '').strip()

    # Initialize personalized_description
    personalized_description = ''
    highlighted_result = ''

    # If search_query exists, process it
    if search_query:
        try:
            # Call the enricher.interweave function
            personalized_description = enricher.interweave(item.short_description, search_query)

            # Split the search_query into individual keywords
            search_keywords = search_query.split()

            # Highlight the keywords in the personalized_description
            highlighted_result = enricher.highlight_keywords(personalized_description, search_keywords)
        except Exception as e:
            personalized_description = f"An error occurred while processing your search: {str(e)}"

    # Render the template, passing the item, search_query, and personalized_description
    return render_template(
        'catalog_realtime.html',
        item=item,
        search_query=search_query,
        personalized_description=highlighted_result
    )

@app.route('/catalog/from_image', methods=['GET', 'POST'])
def catalog_from_image():
    descriptions = {}
    if request.method == 'POST':
        image_url = request.form.get('image_url', '').strip()
        additional_context = request.form.get('context', '').strip()

        try:
            enrichers = [OpenAIEnricher(), AnthropicEnricher()]
            for enricher in enrichers:
                print(f"Running enricher for: {enricher.model}")
                descriptions = enricher.enrich_from_image(image_url, additional_context)

                # Create a new CatalogItem object with the extracted data
                new_item = CatalogItem(
                    input=additional_context,
                    image_url=image_url,
                    title=descriptions['product_title'],
                    short_description=descriptions['short_description'],
                    long_description=descriptions['detailed_description'],
                    specifications=descriptions['specifications'],
                    model=enricher.model
                )

                # Persist the new item to the database
                db.session.add(new_item)
                db.session.commit()
        except Exception as e:
            return render_template('catalog_from_image.html', error=f"An error occurred: {str(e)}")

    return render_template('catalog_from_image.html', descriptions=descriptions)

@app.route('/catalog/pdp')
def catalog_pdp():
    # Get the 'id' query parameter from the URL
    item_id = request.args.get('id')
    if item_id is None:
        return "Error: No 'id' parameter provided. Please specify an 'id' in the URL."
    try:
        # Convert id to integer
        item_id = int(item_id)
    except ValueError:
        return "Error: Invalid 'id' parameter. Please provide a valid integer."

    # Query the CatalogItem with the given id
    item = CatalogItem.query.get(item_id)
    if item is None:
        return f"Error: No item found with id {item_id}."

    return render_template('catalog_pdp.html', item=item)