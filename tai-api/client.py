import requests
import sys


prompt = " ".join(sys.argv[1:])

print("submitting:", prompt)

payload = {"prompt": prompt}
r = requests.post("http://localhost:9000/engines/hf-gpt-2/completions", json=payload)
print(r.json()['response'][0]['generated_text'])
