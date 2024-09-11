import pandas as pd
import json
from groq import Groq
import os


def ask_doctor_about_std(query):
    # Initialize the Groq client with your API key
    client = Groq(
        api_key= os.environ.get('GOOGLE_API_KEY')
    )

    
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": query,
        }
    ],
    model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content # Extract the relevant response
    return response.replace('*','')



def df_to_text(df):
    rows = []
    for index, row in df.iterrows():

        row_str = f"Sr. No: {len(rows) + 1}\n"
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
        

