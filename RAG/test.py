from qwen import qwen_generate

msg = [{"role": "user", "content": "Привет! Расскажи в одном предложении, кто ты."}]
print(qwen_generate(msg, max_tokens=128, temperature=0.2))