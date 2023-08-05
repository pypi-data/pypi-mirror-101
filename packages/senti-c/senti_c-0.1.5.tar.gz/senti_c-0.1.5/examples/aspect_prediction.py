
from senti_c import AspectSentimentAnalysis

aspect_classifier = AspectSentimentAnalysis()

test_data = ["我很喜歡這家店！超級無敵棒！","這個服務生很不親切..."]   
result = aspect_classifier.predict(test_data, output_result="all")

print("\n *** \n")
print("Aspect and Sentiment", result['AspectTermAndSentimentExtraction'])

nseg = len(result['InputWords'])
# result['AspectTermTags']
for seg in range(nseg):
    print(f"   Sentence {seg}")
    a1 = result['InputWords'][seg]
    a2 = result['AspectTermAndSentimentTags'][seg]
    for x1, x2 in zip(a1, a2):
        print(x1, x2)