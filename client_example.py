import httpx

user_question = input("Ask your question: ")
response = httpx.post(
    "https://entropic-api.onrender.com/predictlife", json={"question": user_question}
)
print(response.json())
