from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import spacy

# Load the CSV data
data = pd.read_csv('C:\\Users\\dell\\Documents\\demo\\housing.csv')
print(data.columns)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize Flask app
app = Flask(__name__)

# Helper function to check property availability
def check_availability(property_query):
    for _, row in data.iterrows():
        if property_query.lower() in row['Address'].lower():
            # Check if the property has a price listed as an indicator of availability
            return f"The property '{row['Address']}' is available at a price of ${row['Price']}." if not pd.isna(row['Price']) else f"The property '{row['Address']}' is not available."
    return "Property not found."

# Route to handle incoming WhatsApp messages
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    doc = nlp(incoming_msg)
    
    # Extract property name or location (simple example)
    property_name = ""
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE", "FAC", "LOC"]:
            property_name = ent.text
            break
    
    # Generate response based on extracted property name
    response_text = "I'm sorry, I didn't understand your request." if not property_name else check_availability(property_name)
    
    # Twilio Messaging Response
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
