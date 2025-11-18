from transformers import pipeline

# Load IBM Granite model
pipe = pipeline(
    "text-generation",
    model="ibm-granite/granite-3.3-2b-instruct"
)

def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": "You are StudyMate, an AI assistant that answers from the provided PDF context only."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}\nAnswer using only the context."}
    ]

    output = pipe(messages, max_new_tokens=300)
    return output[0]["generated_text"]
