import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json

def solve_questions():
    try:
        df = pd.read_csv('uploads/b643ca28-393f-4763-9068-d57046d0d470/highest_grossing_films.csv')

        # Clean data
        df['Worldwide gross'] = df['Worldwide gross'].astype(str).replace({r'\$': '', ',': ''}, regex=True)
        df['Worldwide gross'] = df['Worldwide gross'].str.extract(r'(\d+\.?\d*)', expand=False).astype(float)
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df.dropna(subset=['Worldwide gross', 'Year', 'Rank', 'Peak'], inplace=True)
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        df['Peak'] = pd.to_numeric(df['Peak'], errors='coerce')

        # 1. How many $2 bn movies were released before 2000?
        movies_2bn_before_2000 = df[(df['Worldwide gross'] >= 2_000_000_000) & (df['Year'] < 2000)]
        answer1 = len(movies_2bn_before_2000)

        # 2. Which is the earliest film that grossed over $1.5 bn?
        movies_1_5bn = df[df['Worldwide gross'] >= 1_500_000_000]
        earliest_film = movies_1_5bn.sort_values('Year').iloc[0]
        answer2 = earliest_film['Title']

        # 3. What's the correlation between the Rank and Peak?
        correlation = df['Rank'].corr(df['Peak'])
        answer3 = correlation

        # 4. Draw a scatterplot of Rank and Peak
        plt.figure(figsize=(8, 6))
        sns.regplot(x='Rank', y='Peak', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red', 'linestyle':'--'})
        plt.title('Rank vs. Peak of Highest-Grossing Films')
        plt.xlabel('Rank')
        plt.ylabel('Peak')
        plt.grid(True)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        answer4 = f"data:image/png;base64,{image_base64}"
        buf.close()
        plt.close()

        final_answers = [answer1, answer2, answer3, answer4]
        with open('uploads/b643ca28-393f-4763-9068-d57046d0d470/result.json', 'w') as f:
            json.dump(final_answers, f)

    except Exception as e:
        # Write error to result file to indicate failure
        with open('uploads/b643ca28-393f-4763-9068-d57046d0d470/result.json', 'w') as f:
            json.dump({'error': str(e)}, f)

solve_questions()