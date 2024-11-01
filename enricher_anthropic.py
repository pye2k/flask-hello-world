import anthropic
import xmltodict
from catalog_enricher import CatalogEnricher

class AnthropicEnricher(CatalogEnricher):

    def enrich_from_image(self, image_url, additional_context):
        # ensure that API key is set for os.environ.get("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system="You are a catalog enrichment expert tasked with generating e-commerce marketplace content based on an image and optional additional context. Your goal is to create engaging, SEO-optimized content that accurately describes the product and appeals to potential customers.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "<examples>\n<example>\n<IMAGE_URL>\nhttps://m.media-amazon.com/images/I/714WLj2xEnL.jpg\n</IMAGE_URL>\n<ADDITIONAL_CONTEXT>\ndiwali decorative candle holder\n</ADDITIONAL_CONTEXT>\n<ideal_output>\n<answer>\n<product_title>Elegant Diwali Ceramic Tealight Holder - Decorative Floral Design<product_title>\n\n<short_description>Transform your Diwali celebrations with this exquisitely crafted ceramic tealight holder featuring an intricate floral design. This traditional Indian candle stand combines elegant aesthetics with spiritual significance, creating a warm and festive ambiance. Perfect for adorning your home during festivals or adding a touch of ethnic charm to your everyday decor.</short_description>\n\n<detailed_description>\nElevate your Diwali celebrations and home decor with this masterfully crafted brass tealight holder that embodies traditional Indian artistry. The holder features an ornate floral pattern with intricate cutwork that creates mesmerizing light patterns when illuminated. The durable brass construction ensures longevity while developing a beautiful patina over time. The elevated design includes a broad, stable base for safety and multiple holders for tealights, allowing you to create the perfect festive atmosphere. Whether placed on your prayer altar, dining table, or as a centerpiece, this versatile piece adds a touch of traditional elegance to any space. The holder's design incorporates traditional motifs that symbolize prosperity and good fortune, making it an ideal choice for Diwali celebrations and other auspicious occasions. The thoughtful construction allows for easy cleaning and maintenance, while the timeless design ensures it remains a cherished decorative piece throughout the year. This tealight holder not only serves as a beautiful decorative element but also carries forward the ancient tradition of lighting diyas during festivals.</detailed_description>\n\n<specifications>\n     <name>Material</name>\n     <value>Brass</value>\n</specifications>\n<specifications>\n     <name>Style</name>\n     <value>Traditional Indian</value>\n</specifications>\n<specifications>\n     <name>Design Pattern</name>\n     <value>Floral Cutwork</value>\n</specifications>\n<specifications>\n     <name>Number of Tealight Holders</name>\n     <value>4</value>\n</specifications>\n<specifications>\n     <name>Finish</name>\n     <value>Ceramic</value>\n</specifications>\n<specifications>\n     <name>Suitable For</name>\n     <value>Diwali, Home Decor, Festivals, Prayer Altar</value>\n</specifications>\n<specifications>\n     <name>Care Instructions</name>\n     <value>Clean with soft dry cloth, Avoid harsh chemicals</value>\n</specifications>\n<specifications>\n     <name>Assembly Required</name>\n     <value>No</value>\n</specifications>\n</answer>\n</ideal_output>\n</example>\n<example>\n<IMAGE_URL>\nhttps://paattiskitchen.com/wp-content/uploads/2022/11/kmc_20221124_205159-2048x1152.jpg\n</IMAGE_URL>\n<ADDITIONAL_CONTEXT>\ncrispy dosa, fluffy idly\n</ADDITIONAL_CONTEXT>\n<ideal_output>\n<answer>\n<product_title>Crispy Dosa and Fluffy Idli with Traditional Chutneys<product_title>\n\n<short_description>Experience the perfect harmony of South Indian breakfast classics with our handcrafted dosa and idli combo. Featuring perfectly crispy, golden-brown dosas and cloud-soft idlis, served with authentic coconut chutney and aromatic sambar. Each dish is made with premium ingredients following traditional recipes for an unforgettable dining experience.</short_description>\n\n<detailed_description>Indulge in the ultimate South Indian breakfast experience with our meticulously prepared dosa and idli combination platter. The dosa, a crispy fermented rice and lentil crepe, is expertly spread and cooked to golden perfection, achieving the ideal balance of crispiness and tenderness. Our idlis are steamed to fluffy perfection, offering a light, airy texture that melts in your mouth. Each serving comes with house-made accompaniments including freshly ground coconut chutney, spicy red chutney, and piping hot sambar enriched with vegetables and lentils. The platter showcases the versatility of South Indian cuisine, perfect for both newcomers and connoisseurs alike. Whether you're starting your day or enjoying a satisfying meal any time, this combination offers a wholesome, protein-rich option that's both delicious and nutritious. Our commitment to authentic preparation methods and premium ingredients ensures you experience the true essence of South Indian culinary tradition.</detailed_description>\n\n<specifications>\n     <name>Serving Size</name>\n     <value>1 person</value>\n</specifications>\n<specifications>\n     <name>Dosa Quantity</name>\n     <value>1 piece</value>\n</specifications>\n<specifications>\n     <name>Idli Quantity</name>\n     <value>2 pieces</value>\n</specifications>\n<specifications>\n     <name>Accompaniments</name>\n     <value>Coconut Chutney, Sambar</value>\n</specifications>\n<specifications>\n     <name>Dietary Type</name>\n     <value>Vegetarian</value>\n</specifications>\n<specifications>\n     <name>Preparation Style</name>\n     <value>Traditional South Indian</value>\n</specifications>\n<specifications>\n     <name>Best Consumed</name>\n     <value>Within 2 hours of preparation</value>\n</specifications>\n</answer>\n</ideal_output>\n</example>\n</examples>\n\n"
                        },
                        {
                            "type": "text",
                            "text": f"You will be provided with the following:\n\n<image_url>\n{image_url}\n</image_url>\n\n<additional_context>\n{additional_context}\n</additional_context>\n\nBegin by carefully analyzing the image and any provided additional context. Pay attention to the product's features, design, materials, and potential use cases.\n\nBased on your analysis, generate the following outputs:\n\n1. Title:\n   - Create a title up to 15 words in length\n   - Optimize for readability and SEO\n   - Include key product features and benefits\n\n2. Short Description:\n   - Write 3-5 sentences\n   - Capture the user's attention\n   - Highlight the most important product features\n   - Make it descriptive and engaging\n   - Optimize for SEO\n\n3. Detailed Description:\n   - Write approximately 10 sentences (about a paragraph long)\n   - Describe use-cases and help users understand the product's value\n   - Include more SEO keywords\n   - Provide in-depth information about features, materials, and benefits\n   - Address potential customer pain points or needs\n\n4. Specifications:\n   - Create a list of name-value pairs for typical product specifications\n   - Include relevant details such as dimensions, materials, weight, color options, etc.\n   - Ensure accuracy based on the information available in the image and supplemental info\n\nFormat your entire response in XML, following this structure:\n\n<answer>\n<product_title>Your generated title here<product_title>\n<short_description>Your generated short description here</short_description>\n<detailed_description>Your generated detailed description here</detailed_description>\n<specifications>\n     <name>specification1</name>\n     <value>value1</value>\n</specifications>\n<specifications>\n     <name>specification2</name>\n     <value>value2</value>\n</specifications>\n</answer>\n\nEnsure that all content is original, engaging, and accurately reflects the product shown in the image and described in the supplemental information. Optimize all text for both readability and search engine performance."
                        }
                    ]
                }
            ]
        )
        
        # Return the data
        message_content = message.content[0].text
        return self._response_to_dict(message_content)

    def _response_to_dict(self, message_content):
        print("Converting the following XML to DICT:\n")
        print(f"\t\t{message_content}\n")

        response = xmltodict.parse(message_content)
        print(f"Product Title: {response['answer']['product_title']}")
        print(f"Short Desc:    {response['answer']['short_description']}")
        print(f"Detailed Desc: {response['answer']['detailed_description']}")
        print("Specs:")
        for spec in response['answer']['specifications']:
            print(f"     {spec['name']} : {spec['value']}")

        return response['answer']

def main():
    # Sample data for testing
    image_url = "https://contents.mediadecathlon.com/p2637798/k$6d66efba33c62e0b1b272816f7589b67/adult-padel-racket-comfort-kuikma-8862141.jpg"
    additional_context = "kuikma comfort padel racket, fibreglass surface, lightweight, 350g, forgiving, optimal control"

    enricher = AnthropicEnricher()
    enricher.enrich_from_image(image_url, additional_context)

if __name__ == "__main__":
    main()