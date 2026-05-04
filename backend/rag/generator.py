import ollama

def generate_answer(retrieved_docs, user_question):

    context = "\n\n".join(retrieved_docs)

    prompt = f"""
You are an AI assistant.

Use the context below to answer.

Context:
{context}

Question:
{user_question}

Answer clearly.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]