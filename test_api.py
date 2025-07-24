import requests

url = "http://127.0.0.1:8000/ask"
sample_questions = [
    ("অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?", "শুম্ভুনাথ"),
    ("কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?", "মামাকে"),
    ("বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "১৫ বছর"),
]

for i, (question, expected) in enumerate(sample_questions, 1):
    data = {"user": f"test_user_{i}", "query": question}
    print(f"\nQ{i}: {question}")
    print(f"Expected: {expected}")
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("Answer:", result.get("answer"))
            print("Retrieved Chunks:", result.get("retrieved_chunks"))
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Request failed: {e}") 