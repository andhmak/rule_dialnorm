# Script performing rule-based normalization (RBN) on the idioms, by dialectal grouping,
# and saving the outputs to .csv files, per dialectal group

import pandas as pd
import re

# Function reversing Northern vowelism in the masculine singular nominative
def north_masc_nom_sing(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    # Define a pattern to match "ου" and its immediate next word if it exists and ends with "ους".
    pattern = r"\b([Οο]υ)\b(?:\s+(\w*ους)\b)?"

    def replacer(match):
        # Replace "ου" with "ο"
        result = match.group(1)[:-1]
        if match.group(2):  # If there is a next word ending with "ους" immediately after
            # Replace the next word ending in "ου" with "ο"
            result += f" {match.group(2)[:-2]}ς"
        return result

    # Apply the regex replacement
    return re.sub(pattern, replacer, sentence)

# Function reversing Northern vowelism in the 3rd person singular copula
def north_be_3rd(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    pattern = r"\b([Εε]ίνι)\b"

    def replacer(match):
        result = f" {match.group(1)[:-1]}αι"
        return result

    # Apply the regex replacement
    return re.sub(pattern, replacer, sentence)

# Function reversing the Southern lexical form of the word "what"
def south_what(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    pattern = r"\b([Ίί]ντα)\b"

    def replacer(match):
        if match.group(1)[0] == "Ί":
            return "Τι"
        else:
            return "τι"

    # Apply the regex replacement
    temp = re.sub(pattern, replacer, sentence)

    pattern = r"\b([Εε]ίντα)\b"

    def replacer(match):
        if match.group(1)[0] == "Ε":
            return "Τι"
        else:
            return "τι"

    # Apply the regex replacement
    return re.sub(pattern, replacer, temp)

# Function reversing Southern palatalization on the coordinating particle
def south_coord(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    
    pattern = r"\b(τ[σζ]ι?αι)\b"

    def replacer1(match):
        return "και"

    # Apply the regex replacement
    temp = re.sub(pattern, replacer1, sentence)
    
    pattern = r"τζι?'"

    def replacer2(match):
        return "κι"
    
    # Apply the regex replacement
    temp2 = re.sub(pattern, replacer2, temp)
    
    pattern = r"\b(κια[ιί])\b"

    def replacer2(match):
        return "και"
    
    # Apply the regex replacement
    return re.sub(pattern, replacer2, temp2)

# Function reversing the Pontic lexical form of the word "what"
def pontus_what(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    pattern = r"\b([Νν]το)\b"

    def replacer(match):
        if match.group(1)[0] == "Ν":
            return "Τι"
        else:
            return "τι"

    # Apply the regex replacement
    return re.sub(pattern, replacer, sentence)

# Function reversing the Pontic lexical form of the 3rd person singular copula
def pontus_be(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    pattern = r"\b([Εε]ν)\b"

    def replacer(match):
        if match.group(1)[0] == "Ε":
            return "Είναι"
        else:
            return "εὶναι"

    # Apply the regex replacement
    temp = re.sub(pattern, replacer, sentence)

    pattern = r"εὶναι'"

    def replacer(match):
        return match.group(0)[:-1]

    # Apply the regex replacement
    return re.sub(pattern, replacer, temp)

# Function applying all the rules for Pontus
def normalize_pontus(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    return pontus_be(pontus_what(sentence))

# Function applying the rules applicable for all dialectal groups
def normalize_dialects(sentence):
    """
    Args:
        sentence (str): The input sentence.

    Returns:
        str: The modified sentence.
    """
    return south_coord(north_masc_nom_sing(south_what(north_be_3rd(sentence))))

# Read the input
input_file = 'data/balanced_corpus.csv'
df = pd.read_csv(input_file)

# Apply the most general rules to the text column
df['normtext'] = df['text'].apply(normalize_dialects)

# Separate Northern dialects
condition = df["place"].str.split(r'[ ,]').str[0].isin(["Μακεδονία", "Θράκη", "Σκύρος", "Ήπειρος", "Μικρά", "Αιτωλία", "Ανατολική", "Εύβοια", "Λέσβος", "Ιωάννινα"])
north = df[condition]
nonorth = df[-condition]

# Separate Pontus
condition = nonorth["place"].str.split(r'[ ,]').str[0].isin(["Πόντος"])
pontus = nonorth[condition]
south = nonorth[-condition]

# Apply the Pontus-specific rules to Pontus
pontus['normtext'] = pontus['normtext'].apply(normalize_pontus)

# Write the outputs
north.to_csv("data/north.csv", index=False)
south.to_csv("data/south.csv", index=False)
pontus.to_csv("data/pontus.csv", index=False)

print(f"RBN outputs saved to data/north.csv, data/south.csv, data/pontus.csv")