# AI-XSS

# XSS Payload Generator with Ollama GPT (Yerel GPT Destekli)

Bu proje, **yerel GPT modeli (Ollama Mistral)** kullanarak otomatik XSS payloadları üretip, hedef URL’de parametre yansımalarını test eden Python tabanlı bir araçtır.

---

## Özellikler

- Ollama GPT modeli ile dinamik ve bağlama özel XSS payload üretimi
- GET ve POST metodları desteklenir
- Hedef URL ve parametre ismi kullanıcı tarafından belirlenir
- Harici kütüphane gerektirmez (saf Python)
- Tamamen offline ve ücretsiz (Ollama yüklü olması yeterli)

---

## Gereksinimler

- Python 3
- Ollama (https://ollama.com/) ve Mistral modeli yüklü ve çalışır durumda
- İnternet bağlantısı gerekmez (yerel GPT ile çalışır)

---

## Kurulum

1. Ollama'yı kur (5.5-7 GB RAM 4-5 GB Harddisk) : curl -fsSL https://ollama.com/install.sh | sh

   
   
----

   KULLANIM:
   
   1-ollama run mistral

   Örnek GET isteği ile test
   python3 xssgen.py --url "http://hedef.com/search?q=test" --param q --method GET

   Örnek POST isteği ile test
   python3 xssgen.py --url "http://hedef.com/search" --param q --method POST --data "q=test"

