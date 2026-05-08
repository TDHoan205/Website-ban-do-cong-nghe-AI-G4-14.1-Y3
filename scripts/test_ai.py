"""
Test AI Service - Kiểm tra các provider
Chạy: python test_ai.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.chat.services.ai_service import ai_service, OLLAMA_BASE_URL


def test_provider(name, is_available_fn, generate_fn):
    """Test một provider."""
    print(f"\n{'='*50}")
    print(f"  Test: {name}")
    print('='*50)

    # Check availability
    available = is_available_fn()
    print(f"  Available: {'✓' if available else '✗'}")

    if not available:
        print(f"  → Skip (khong kha dung)")
        return False

    # Test generate
    print(f"\n  Sending test message...")
    test_prompt = "Xin chao, ban la ai?"

    result = generate_fn(test_prompt, "Ban la tro ly AI cua TechStore - cua hang ban do cong nghe.")

    if result:
        print(f"  → Success!")
        print(f"\n  Response preview:")
        print(f"  {result[:200]}...")
        return True
    else:
        print(f"  → Failed!")
        return False


def main():
    print("\n" + "="*60)
    print("    TEST AI SERVICE - TechStore Chatbot")
    print("="*60)

    # Show status
    print("\n[Provider Status]")
    status = ai_service.get_status()
    for name, info in status.items():
        icon = "✓" if info['available'] else "✗"
        print(f"  [{icon}] {info['name']}")

    # Count available
    available_count = sum(1 for s in status.values() if s['available'])
    print(f"\n  Total available: {available_count}/4")

    if available_count == 0:
        print("\n[WARN] Khong co provider nao kha dung!")
        print("\nDe su dung AI:")
        print("  1. Cai Ollama: https://ollama.com/download")
        print("  2. Hoac lay API key tu OpenRouter/Groq/Gemini")
        print("  3. Them vao file .env")
        return

    # Test each provider
    print("\n" + "="*60)
    print("    Testing Providers")
    print("="*60)

    # Test Ollama
    test_provider(
        "Ollama (Local)",
        lambda: ai_service.providers['ollama'].is_available(),
        lambda p, c: ai_service.providers['ollama'].generate(p, c)
    )

    # Test OpenRouter
    test_provider(
        "OpenRouter (Cloud)",
        lambda: ai_service.providers['openrouter'].is_available(),
        lambda p, c: ai_service.providers['openrouter'].generate(p, c)
    )

    # Test Groq
    test_provider(
        "Groq (Cloud)",
        lambda: ai_service.providers['groq'].is_available(),
        lambda p, c: ai_service.providers['groq'].generate(p, c)
    )

    # Test Gemini
    test_provider(
        "Gemini (Cloud)",
        lambda: ai_service.providers['gemini'].is_available(),
        lambda p, c: ai_service.providers['gemini'].generate(p, c)
    )

    # Test full flow
    print("\n" + "="*60)
    print("    Test Full AI Flow")
    print("="*60)

    test_messages = [
        "Xin chao",
        "Gia iPhone 15 la bao nhieu?",
        "Co khuyen mai gi khong?",
        "Giao hang trong bao lau?",
    ]

    for msg in test_messages:
        print(f"\n  User: {msg}")
        response, intent, products, escalate = ai_service.generate_response(msg)
        print(f"  Bot:  {response[:100]}...")
        print(f"  Intent: {intent} | Products: {len(products)}")

    print("\n" + "="*60)
    print("    Hoan tat test!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
