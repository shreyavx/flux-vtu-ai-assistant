import ollama


def ask_llm(prompt):

    response = ollama.chat(

        model="phi3",

        options={
            "num_predict": 150
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def is_rag_question(question):

    prompt = f"""
    Determine whether this question requires
    retrieving information from uploaded academic PDFs.

    Reply ONLY with:
    YES
    or
    NO

    Question:
    {question}
    """

    response = ask_llm(prompt)

    return "YES" in response.upper()