# Script calling GPT, providing it with the original idioms and a prompt tailored to each dialectal group,
# and saving the outputs to .csv files, per dialectal group

from openai import OpenAI
import pandas as pd
from openai._exceptions import OpenAIError
import time

client = OpenAI(api_key="<key>")    # add your API key here

# Function to retry when API call fails
def get_response(prompt):
    while True:  # Keep retrying forever
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-2024-11-20",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            
            response = ''
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response += chunk.choices[0].delta.content
            return response  # Return response if successful
        
        except Exception as e:  # Catch all exceptions
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying

# Load the CSV files
input_files = ["data/south.csv", "data/north.csv", "data/pontus.csv"]
dfs = [pd.read_csv(input_file) for input_file in input_files]
# Add column where the normalized output will be stored
for df in dfs:
    df['GPTnorm'] = None
# Name dataframes
dfsouth = dfs[0]
dfnorth = dfs[1]
dfpontus = dfs[2]

# Get responses for Pontus
responses = []
for proverb in dfpontus.itertuples(index=True):
    # Save all GPT responses
    text = proverb.text
    place = proverb.place
    prompt = f"""
            Given a Greek sentence from Πόντος. Translate it to standard Greek. Keep the same style, do not make it more official. Use words with the same etymology if and only if they exist in standard Greek, otherwise use different words. Show just the translation and nothing else.

            For example:

            Πόντος:
            Ποιος βάλλ' το χέρ΄ν ατ' 'ς σο μέλ' και 'κι λείχ' τα δάχτυλα 'τ'

            Standard Greek:
            Ποιος βάζει το χέρι του στο μέλι και δεν γλείφει τα δάχτυλά του

            Πόντος:
            Κι'αν παθάνης κι μαθάνεις

            Standard Greek:
            Αν δεν παθαίνεις δεν μαθαίνεις

            Πόντος:
            Ο νέον θολόν ποτάμιν είναι!

            Standard Greek:
            Ο νέος θολό ποτάμι είναι!

            Πόντος:
            {text}

            Standard Greek:"""
    # Save the response
    response = get_response(prompt)
    responses.append((proverb.Index, response))

for idx, response in responses:
    dfpontus.at[idx, "GPTnorm"] = response

dfpontus.to_csv("data/pontus_GPTο_fromplain.csv", index=False)

# Get responses for Southern dialects
responses = []
for proverb in dfsouth.itertuples(index=True):
    # Save all GPT responses
    text = proverb.text
    place = proverb.place
    prompt = f"""
            Given a Greek sentence from {place}. Translate it to standard Greek. Keep the same style, do not make it more official. Use words with the same etymology if and only if they exist in standard Greek, otherwise use different words. Show just the translation and nothing else.

            For example:

            {place}:
            Καλλιά 'ν' το διακονίκι, παρά το βασιλίκι

            Standard Greek:
            Καλύτερα είναι το διακονίκι, παρά το βασιλίκι

            {place}:
            Τάχει η γραι στο λοϊσμό τζη τα θωρεί και στο όνειρό τζη

            Standard Greek:
            Τά 'χει η γρια στον λογισμό της τα βλέπει και στο όνειρό της

            {place}:
            Των βρενίμων τα παιδκιά πριν πεινασουν μαειρεύκουν

            Standard Greek:
            Των φρονίμων τα παιδιά πριν πεινάσουν μαγειρεύουν

            {place}:
            {text}

            Standard Greek:"""
    # Save the response
    response = get_response(prompt)
    responses.append((proverb.Index, response))

for idx, response in responses:
    dfsouth.at[idx, "GPTnorm"] = response

dfsouth.to_csv("data/south_GPTο_fromplain.csv", index=False)

# Get responses for Northern dialects
responses = []
for proverb in dfnorth.itertuples(index=True):
    # Save all GPT responses
    text = proverb.text
    place = proverb.place
    prompt = f"""
            Given a Greek sentence from {place}. Translate it to standard Greek. Keep the same style, do not make it more official. Use words with the same etymology if and only if they exist in standard Greek, otherwise use different words. Show just the translation and nothing else.

            For example:

            {place}:
            Γίδα ψουριάρα, νουρά κουρδουμέν'

            Standard Greek:
            Γίδα ψωριάρα, ουρά κορδωμένη

            {place}:
            Μι πήρι, σι πήρι, τουν πήρι του πουτάμ'

            Standard Greek:
            Με πήρε, σε πήρε, τον πήρε το ποτάμι

            {place}:
            Τ' γάμσι του κέρατου

            Standard Greek:
            Του γάμησε το κέρατο

            {place}:
            {text}

            Standard Greek:"""
    # Save the response
    response = get_response(prompt)
    responses.append((proverb.Index, response))

for idx, response in responses:
    dfnorth.at[idx, "GPTnorm"] = response

dfnorth.to_csv("data/north_GPTο_fromplain.csv", index=False)