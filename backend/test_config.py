#!/usr/bin/env python3
"""
Script de teste para verificar se o config.py está carregando corretamente.
"""
import os
import sys

# Testa diferentes formatos de CORS_ORIGINS
test_cases = [
    ('["https://frontend.com"]', ['https://frontend.com']),
    ('https://frontend.com', ['https://frontend.com']),
    ('https://frontend1.com,https://frontend2.com', ['https://frontend1.com', 'https://frontend2.com']),
]

print("🧪 Testando parse de CORS_ORIGINS...\n")

for test_input, expected_output in test_cases:
    print(f"Input: {test_input}")

    # Define a variável de ambiente
    os.environ['CORS_ORIGINS'] = test_input

    try:
        # Importa o settings novamente
        if 'app.config' in sys.modules:
            del sys.modules['app.config']

        from app.config import settings

        print(f"Output: {settings.CORS_ORIGINS}")
        print(f"Expected: {expected_output}")

        if settings.CORS_ORIGINS == expected_output:
            print("✅ PASSOU!\n")
        else:
            print("❌ FALHOU!\n")
    except Exception as e:
        print(f"❌ ERRO: {e}\n")
        import traceback
        traceback.print_exc()

# Limpa a variável de ambiente
if 'CORS_ORIGINS' in os.environ:
    del os.environ['CORS_ORIGINS']

print("\n" + "="*50)
print("Testando configuração padrão (sem variável de ambiente):")
print("="*50 + "\n")

try:
    if 'app.config' in sys.modules:
        del sys.modules['app.config']

    from app.config import settings

    print(f"APP_NAME: {settings.APP_NAME}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"CORS_ORIGINS: {settings.CORS_ORIGINS}")
    print("\n✅ Config carregada com sucesso!")
except Exception as e:
    print(f"❌ ERRO ao carregar config: {e}")
    import traceback
    traceback.print_exc()
