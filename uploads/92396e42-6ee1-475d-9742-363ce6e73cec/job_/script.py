import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
import re

# Step 1: Use pandas to directly read the HTML table for better reliability
url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'
try:
    # The main table is the first one with the 'wikitable' class
    tables = pd.read_html(url, attrs={'class': 'wikitable'})
    df = tables[0]
except (ValueError, IndexError):
    # Fallback if the specific table isn't found, just get all tables
    tables = pd.read_html(url)
    df = tables[0] # Assume the first table is the correct one

# Step 2: Clean the DataFrame
# The table can have multi-level headers, so we flatten them by taking the last level
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(-1)

# Keep only the necessary columns
df = df[['Rank', 'Peak', 'Title', 'Worldwide gross', 'Year']]

# Clean 'Worldwide gross' column: remove '$', ',', and references like '[#]'
def clean_gross(gross_text):
    # Split string at reference notes (e.g., '[1]') and take the numeric part
    gross_str = re.split(r'\s*\[', str(gross_text))[0]
    # Remove non-numeric characters
    return int(re.sub(r'[\$,]', '', gross_str))

df['Worldwide_gross'] = df['Worldwide gross'].apply(clean_gross)

# Clean 'Year' column: remove references
df['Year'] = df['Year'].apply(lambda x: int(re.split(r'\s*\[', str(x))[0]))

# Ensure Rank and Peak are clean integers
df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
df['Peak'] = pd.to_numeric(df['Peak'], errors='coerce')
df.dropna(subset=['Rank', 'Peak'], inplace=True)
df['Rank'] = df['Rank'].astype(int)
df['Peak'] = df['Peak'].astype(int)

# --- Question 1: How many $2 bn movies were released before 2000? ---
movies_over_2bn_before_2000 = df[(df['Worldwide_gross'] >= 2_000_000_000) & (df['Year'] < 2000)]
answer1 = len(movies_over_2bn_before_2000)

# --- Question 2: Which is the earliest film that grossed over $1.5 bn? ---
movies_over_1_5bn = df[df['Worldwide_gross'] >= 1_500_000_000]
earliest_film = movies_over_1_5bn.sort_values(by='Year').iloc[0]
answer2 = earliest_film['Title']

# --- Question 3: What's the correlation between the Rank and Peak? ---
correlation = df['Rank'].corr(df['Peak'])
answer3 = correlation

# --- Question 4: Draw a scatterplot of Rank and Peak with a regression line ---
plt.figure(figsize=(10, 6))
sns.regplot(x='Rank', y='Peak', data=df, 
            scatter_kws={'alpha': 0.6}, 
            line_kws={'color': 'red', 'linestyle': '--'})
plt.title('Rank vs. Peak of Highest-Grossing Films')
plt.xlabel('Rank')
plt.ylabel('Peak')
plt.grid(True)

# Save plot to a bytes buffer
buf = io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)

# Encode image to base64, with a check for size
image_base64 = base64.b64encode(buf.read()).decode('utf-8')
if len(image_base64.encode('utf-8')) > 100000:
    answer4 = "[IMAGE_BASE64_STRIPPED]"
else:
    answer4 = f'data:image/png;base64,{image_base64}'

buf.close()
plt.close()


# --- Combine answers and save to result.json ---
final_answers = [answer1, answer2, answer3, answer4]

with open('uploads/92396e42-6ee1-475d-9742-363ce6e73cec/result.json', 'w') as f:
    json.dump(final_answers, f)

print("Corrected analysis complete. Results saved to result.json.")
