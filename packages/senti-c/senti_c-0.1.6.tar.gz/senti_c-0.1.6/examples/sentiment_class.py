from senti_c import SentenceSentimentClassification

sentence_classifier = SentenceSentimentClassification()

test_data = ["我很喜歡這家店！超級無敵棒！","這個服務生很不親切..."]  
result = sentence_classifier.predict(test_data, run_split=True, aggregate_strategy=False)
print("\n *** \nBelow is the results:")
print(result)
