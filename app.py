
from flask import Flask, request, jsonify
import utility

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

if __name__ == '__main__':
    app.run(port=5000, debug=False)
