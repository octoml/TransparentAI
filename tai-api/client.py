import requests
import sys


prompt = " ".join(sys.argv[1:])

print("Submitting:", prompt)

payload = {"prompt": prompt}
r = requests.post("http://localhost:9000/engines/hf-gpt-2/completions", json=payload)

print("Generated Text:", r.json()['response'][0]['generated_text'])
print("Time for request: {:.3f} s".format(float(r.headers['x-process-time'])))
