import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import tkinter as tk
from tkinter import *

def summarize():
    try:
        url = url_text.get("1.0", "end").strip()
        print(f"URL Entered: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.title.string.strip() if soup.title else "No title found"

        # Extract text from paragraph tags
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])

        if not article_text.strip():
            raise ValueError("No article content found.")

        # Display data in GUI
        title_var.config(state='normal')
        summary_var.config(state='normal')
        sentiment_var.config(state='normal')

        title_var.delete("1.0", "end")
        summary_var.delete("1.0", "end")
        sentiment_var.delete("1.0", "end")

        title_var.insert(END, title)

        # Summarize
        parser = PlaintextParser.from_string(article_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)
        summary_text = " ".join(str(sentence) for sentence in summary)

        summary_var.insert(END, summary_text if summary_text else "No summary generated.")

        # Sentiment
        analysis = TextBlob(article_text)
        polarity = analysis.sentiment.polarity
        sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        sentiment_var.insert(END, sentiment)

        title_var.config(state='disabled')
        summary_var.config(state='disabled')
        sentiment_var.config(state='disabled')

    except Exception as e:
        print("Error:", str(e))
        summary_var.config(state='normal')
        summary_var.delete("1.0", "end")
        summary_var.insert(END, f"An error occurred: {str(e)}")
        summary_var.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("Article Summarizer")
root.geometry("800x600")

Label(root, text="Enter URL:").pack()
url_text = Text(root, height=2, width=100)
url_text.pack()

Label(root, text="Title:").pack()
title_var = Text(root, height=2, width=100)
title_var.pack()
title_var.config(state='disabled')

Label(root, text="Summary:").pack()
summary_var = Text(root, height=10, width=100)
summary_var.pack()
summary_var.config(state='disabled')

Label(root, text="Sentiment:").pack()
sentiment_var = Text(root, height=2, width=100)
sentiment_var.pack()
sentiment_var.config(state='disabled')

Button(root, text="Summarize", command=summarize).pack()

root.mainloop()