import knime.scripting.io as knio
from textblob import TextBlob

df = knio.input_tables[0].to_pandas()

def get_sentiment_score(text):
    text = str(text)
    if not text.strip():
        return 0.0
    return TextBlob(text).sentiment.polarity

df["sentiment_score"] = df["reviews.text"].fillna("").apply(get_sentiment_score)

df["sentiment_label"] = df["sentiment_score"].apply(
    lambda x: "positive" if x > 0 else ("negative" if x < 0 else "neutral")
)

knio.output_tables[0] = knio.Table.from_pandas(df)
