import urllib.parse
import urllib.request
import html.parser
import re
import json
import sys
import argparse
from ollama_gpt import generate_payload

# Basit HTML parser
class ParamContextExtractor(html.parser.HTMLParser):
    def __init__(self, param_value):
        super().__init__()
        self.param_value = param_value
        self.found_context = ""

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if self.param_value in attr[1]:
                self.found_context = f"<{tag} {attr[0]}=\"{attr[1]}\">"

    def handle_data(self, data):
        if self.param_value in data:
            self.found_context = data.strip()

def extract_context(html, param_value):
    parser = ParamContextExtractor(param_value)
    parser.feed(html)
    return parser.found_context or "text"

def make_request(url, method="GET", data=None):
    try:
        if method == "GET":
            with urllib.request.urlopen(url) as response:
                return response.read().decode()
        else:
            data_encoded = data.encode()
            req = urllib.request.Request(url, data=data_encoded, method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            with urllib.request.urlopen(req) as response:
                return response.read().decode()
    except Exception as e:
        print(f"[!] Hata: {e}")
        return ""

def check_reflected(response, payload):
    return payload in response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Hedef URL")
    parser.add_argument("--param", required=True, help="Test edilecek parametre adı")
    parser.add_argument("--method", default="GET", help="GET veya POST")
    parser.add_argument("--data", help="POST verisi (param1=val1&param2=val2)")
    args = parser.parse_args()

    test_value = "xsstest123"
    target_url = args.url
    param_name = args.param

    if args.method.upper() == "GET":
        parsed = urllib.parse.urlparse(target_url)
        query = urllib.parse.parse_qs(parsed.query)
        query[param_name] = [test_value]
        new_query = urllib.parse.urlencode(query, doseq=True)
        new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
        response = make_request(new_url)
    else:
        post_data = args.data.replace(param_name + "=test", param_name + "=" + test_value)
        response = make_request(target_url, method="POST", data=post_data)

    print("[*] Bağlam analizi yapılıyor...")
    context = extract_context(response, test_value)
    print(f"[+] Bağlam: {context[:100]}...")

    print("[*] GPT'den payload isteniyor...")
    prompt = f"Aşağıdaki bağlam için etkili bir XSS payload üret: {context}"
    payload = generate_payload(prompt)
    print(f"[+] GPT Payload: {payload}")

    final_value = urllib.parse.quote(payload)
    if args.method.upper() == "GET":
        query[param_name] = [final_value]
        final_query = urllib.parse.urlencode(query, doseq=True)
        test_url = urllib.parse.urlunparse(parsed._replace(query=final_query))
        final_response = make_request(test_url)
    else:
        final_data = args.data.replace(param_name + "=test", param_name + "=" + final_value)
        final_response = make_request(target_url, method="POST", data=final_data)

    if check_reflected(final_response, payload):
        print("[✅] Payload yansıdı! Potansiyel XSS var.")
    else:
        print("[❌] Payload yansımadı.")

if __name__ == "__main__":
    main()