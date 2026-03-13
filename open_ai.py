import knime.scripting.io as knio
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key="open_api_key")

df = knio.input_tables[0].to_pandas()
df = df.head(20).copy()

def analyze_sentiment(text):

    if pd.isna(text):
        return "neutral", 0, ""

    prompt = f"""
Analyze the sentiment of this product review.

Return:
label: positive/negative/neutral
score: number from -100 to 100
summary: one sentence summary

Review:
{text}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    result = response.output_text

    label = "neutral"
    score = 0
    summary = ""

    for line in result.split("\n"):
        if "label:" in line.lower():
            label = line.split(":")[1].strip()
        elif "score:" in line.lower():
            try:
                score = int(line.split(":")[1].strip())
            except:
                score = 0
        elif "summary:" in line.lower():
            summary = line.split(":")[1].strip()

    return label, score, summary


df["sentiment_label"], df["sentiment_score"], df["summary"] = zip(
    *df["reviews.text"].apply(analyze_sentiment)
)

knio.output_tables[0] = knio.Table.from_pandas(df)
