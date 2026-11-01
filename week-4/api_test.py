import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"))

models = ["meta-llama/llama-3.3-70b-instruct", "openai/gpt-4o-mini"]
prompt = "In two sentences, what is model interpretability?"

for m in models:
    r = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}])
    print(f"=== {m} ===\n{r.choices[0].message.content}\n")