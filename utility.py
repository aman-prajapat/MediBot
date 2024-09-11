import pandas as pd
import json
from groq import Groq

def ask_doctor_about_std(query):
    # Initialize the Groq client with your API key
    client = Groq(api_key='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')
    
    # Create a chat completion request with the user's query
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": query  # User's query related to STD/STI
            }
        ],
        temperature=.89,
        max_tokens=2000,
        top_p=1,
        stream=False,
        stop=None,
          
    )
    
    # Collect the response from the LLM
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    
    return response.replace('*',"")



def df_to_text(df):
    rows = []
    for index, row in df.iterrows():

        row_str = f"Sr. No: {len(row) + 1}\n"
        row_str += f"Name of Medical Officer: {row['Medical_Officer_Name']}\n"
        row_str += f"Medical Officer Contact: {row['Medical_Officer_Contact']}\n"
        row_str += f"Name of Counselor: {row['Counselor_Name']}\n"
        row_str += f"Counselor Contact: {row['Counselor_Contact']}\n"
        row_str += f"Health Facility: {row['Health_Facility_Name']}\n"
        row_str += f"Address: {row['Address']}\n"
        row_str += f"City: {row['City']}, State: {row['State']}\n"
        row_str += "-" * 40  # Separator line
        rows.append(row_str)
    
    return "\n\n".join(rows)


# Load the Excel file
file_path = 'new_data.csv'
df = pd.read_csv(file_path) 
df.fillna('Not Available',inplace=True)

# Function to find nearest service provider based on city and state
def find_service_provider(city = 'NA', state = 'NA'):
    # Filter rows based on city and state
    filtered_df = df[(df['City'].str.lower() == city.lower()) & (df['State'].str.lower() == state.lower())]
    
    if not filtered_df.empty:
        return df_to_text(filtered_df)
    else:
        print("No service providers found for the given city")
        return df_to_text(df[(df['State'].str.lower() == state.lower())])
        

