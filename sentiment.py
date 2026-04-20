from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch 

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


tweet_example = "The market is crashing, total disaster, very bad!"

def get_sentiment(tweet):
    inputs = tokenizer(tweet, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs)
    scores = torch.nn.functional.softmax(output.logits, dim=-1)
    print(scores)
    return scores[0][0].item() - scores[0][1].item()

print(get_sentiment(tweet_example))
