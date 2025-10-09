#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fix_syntax_errors():
    """Corrige os erros de sintaxe no arquivo api.py"""
    
    file_path = r"c:\Users\landr\Eng. Software\UniProjs\web-scrapper\src\api.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📝 Arquivo lido com sucesso")
    
    # Corrigir os parênteses duplicados
    content = content.replace(
        "filename = exporter.export_research_data(result))\n                        )",
        "filename = exporter.export_research_data(result)"
    )
    
    print("✅ Parênteses duplicados corrigidos")
    
    # Escrever o arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("💾 Arquivo corrigido e salvo!")

if __name__ == "__main__":
    fix_syntax_errors()