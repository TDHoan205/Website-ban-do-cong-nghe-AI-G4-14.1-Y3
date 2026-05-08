# Hướng Dẫn Cài Đặt AI Chatbot - HOÀN TOÀN FREE!

## Tổng Quan

Hệ thống AI Chatbot của TechStore hỗ trợ **4 Provider** theo thứ tự ưu tiên:

| Priority | Provider | Chi phí | Giới hạn |
|----------|----------|---------|-----------|
| 1 | **Ollama** (Local) | FREE | Không giới hạn |
| 2 | **OpenRouter** | Free Tier | $5 credit |
| 3 | **Groq** | Free Tier | 14,400 req/phút |
| 4 | **Gemini** | Có phí | Giới hạn |

---

## Bước 1: Cài Ollama (QUAN TRỌNG NHẤT)

### Tải và cài đặt:

1. **Windows**: Tải từ https://ollama.com/download
2. **Mac**: `brew install ollama`
3. **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

### Sau khi cài xong:

```bash
# Pull model (chỉ cần làm 1 lần)
ollama pull llama3.2

# Kiểm tra hoạt động
ollama list

# Test nhanh
ollama run llama3.2 "Xin chào"
```

### Model khuyến nghị (RAM 8GB+):

| Model | Kích thước | RAM cần |
|-------|------------|---------|
| `llama3.2` | 2GB | 4GB |
| `qwen2.5:3b` | 2GB | 4GB |
| `deepseek-r1:1.5b` | 1.5GB | 3GB |

---

## Bước 2: Lấy API Keys (Tùy chọn)

### OpenRouter ($5 Free Credit):

1. Vào https://openrouter.ai/credits
2. Đăng nhập (Google/GitHub)
3. Copy API Key

**Models miễn phí:**
- `google/gemini-2.0-flash` (Khuyến nghị!)
- `anthropic/claude-3.5-haiku`
- `meta-llama/llama-3.2-3b-instruct`

### Groq (Rất nhiều Free!):

1. Vào https://console.groq.com/keys
2. Tạo API Key

**Models miễn phí:**
- `llama-3.2-3b-vision` (Khuyến nghị!)
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

---

## Bước 3: Cấu hình .env

Mở file `.env` trong thư mục gốc và thêm:

```env
# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OpenRouter (Tùy chọn)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# Groq (Tùy chọn)
GROQ_API_KEY=gsk_xxxxx

# Priority
AI_PROVIDER_PRIORITY=ollama,openrouter,groq
```

---

## Bước 4: Khởi động Ollama

**LUÔN chạy Ollama trước khi dùng chatbot:**

```bash
# Windows: Chạy app Ollama từ Start Menu
# Hoặc mở terminal:
ollama serve
```

---

## Cách hoạt động

```
User nhắn tin → Hệ thống check theo thứ tự:
    ↓ Ollama (http://localhost:11434) → Nếu Ollama đang chạy → Dùng AI local
    ↓ OpenRouter → Nếu có API key → Dùng cloud free
    ↓ Groq → Nếu có API key → Dùng cloud free
    ↓ Gemini → Nếu có API key → Dùng cloud
    ↓ Fallback → Rule-based response
```

---

## Xem trạng thái AI

Trong Django shell:

```bash
python manage.py shell
```

```python
from apps.chat.services.ai_service import ai_service
print(ai_service.get_status())
```

Output:
```
{'ollama': {'available': True, 'name': 'Ollama (llama3.2)'},
 'openrouter': {'available': False, 'name': 'OpenRouter (google/gemini-2.0-flash)'},
 'groq': {'available': False, 'name': 'Groq (llama-3.2-3b-vision)'},
 'gemini': {'available': False, 'name': 'Gemini'}}
```

---

## Troubleshooting

### Ollama không chạy?

```bash
# Kiểm tra trạng thái
ollama list

# Khởi động lại
ollama serve

# Kiểm tra port
netstat -an | grep 11434
```

### Lỗi "Connection refused"?

Đảm bảo Ollama đang chạy:
```bash
ollama serve
```

### Model không tìm thấy?

```bash
ollama pull llama3.2
```

---

## Tiết kiệm chi phí TỐI ĐA

| Tình huống | Nên dùng | Chi phí |
|------------|----------|---------|
| Hỏi nhanh, ngắn | Ollama | $0 |
| Cần model mạnh | Groq (14,400 req/p) | $0 |
| Ollama + Groq fail | OpenRouter | $0 (credit) |
| Hết credits | Vẫn Ollama | $0 |

**Kết luận:** Với Ollama + Groq, bạn gần như **KHÔNG TỐN GÌ**!

---

## Liên hệ hỗ trợ

Nếu cần giúp đỡ, tạo issue trên GitHub hoặc liên hệ team phát triển.
