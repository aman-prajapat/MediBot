import threading
import time
from flask import Flask, request, jsonify
import utility
import requests
# from dotenv import load_dotenv, dotenv_values
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
        # Get the JSON data from the request
        data = request.get_json()
        query = data['queryResult']['queryText']
        intent = data['queryResult']['intent']['displayName']

        response_message = 'done done'
        
        if intent == 'Find the nearest service provider':
            state = data['queryResult']['parameters']['State']
            city = data['queryResult']['parameters']['city']
            response_message = utility.find_service_provider(city,state)


        elif intent == 'Get information on STI/STD treatment':
            prompt = f'I want to get information on {query} treatment, please make it concise'
            response_message = utility.ask_doctor_about_std(prompt)

        elif intent == 'Learn about STI/STD symptoms':
            prompt = f'I would like to learn about the symptoms of {query}.show the common symptoms associated with this infection, including any early signs, advanced symptoms, and potential complications?'
            response_message = utility.ask_doctor_about_std(prompt)
            
        
        elif intent == 'Other inquiries':
            
            response_message = utility.ask_doctor_about_std(query)
            
        else:
            response_message = utility.ask_doctor_about_std(query)

            
            

    # Return the message as JSON
        return jsonify({
        "fulfillmentText": response_message
        })
        # return jsonify(response), 200


@app.route('/')
def home():
    return "Hello, Flask app running on Render!"

@app.route('/health')
def health():
    return "Healthy", 200

# Function to ping the app periodically
def ping_app():
    while True:
        try:
            response = requests.get("https://medibot-een5.onrender.com/health")
            print(f"Ping response: {response.status_code}")
        except Exception as e:
            print(f"Error pinging app: {e}")
        time.sleep(240)  # Ping every 10 minutes

if __name__ == '__main__':
    print("Starting the app....")
    ping_thread = threading.Thread(target=ping_app)
    ping_thread.daemon = True
    ping_thread.start()
    port = int(os.environ.get("PORT", 5000))  # Use the dynamic PORT variable
    app.run(host='0.0.0.0', port=port)  # Bind to 0.0.0.0 for external access





