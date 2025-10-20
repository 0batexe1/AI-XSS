import http.client
import json

def generate_payload(prompt):
    conn = http.client.HTTPConnection("localhost", 11434)
    headers = {"Content-Type": "application/json"}
    body = json.dumps({
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    conn.request("POST", "/api/generate", body, headers)
    response = conn.getresponse()
    data = response.read().decode()

    try:
        return json.loads(data)["response"].strip()
    except Exception as e:
        print(f"[!] GPT Hatası: {e}")
        return "alert(1)"  # fallback
