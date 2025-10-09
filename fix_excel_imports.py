#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_excel_imports():
    """Corrige os imports do ExcelExporter no arquivo api.py"""
    
    file_path = r"c:\Users\landr\Eng. Software\UniProjs\web-scrapper\src\api.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📝 Arquivo lido com sucesso")
    
    # Substituir os imports
    old_import = "from src.export.excel_exporter import ExcelExporter"
    new_import = "from src.export.excel_exporter import ProfessionalExcelExporter"
    
    content = content.replace(old_import, new_import)
    print(f"✅ Import substituído: {old_import} -> {new_import}")
    
    # Substituir as instanciações
    old_instantiation = "exporter = ExcelExporter()"
    new_instantiation = "exporter = ProfessionalExcelExporter()"
    
    content = content.replace(old_instantiation, new_instantiation)
    print(f"✅ Instanciação substituída: {old_instantiation} -> {new_instantiation}")
    
    # Substituir as chamadas de método
    old_method_pattern = r'filename = exporter\.export_publications_to_excel\([^)]+\)'
    new_method_call = "filename = exporter.export_research_data(result)"
    
    content = re.sub(old_method_pattern, new_method_call, content)
    print(f"✅ Chamadas de método substituídas para export_research_data")
    
    # Escrever o arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("💾 Arquivo corrigido e salvo!")
    
    # Contar as mudanças
    with open(file_path, 'r', encoding='utf-8') as f:
        final_content = f.read()
    
    professional_count = final_content.count('ProfessionalExcelExporter')
    research_data_count = final_content.count('export_research_data')
    
    print(f"📊 Verificação final:")
    print(f"  - ProfessionalExcelExporter encontrado: {professional_count} vezes")
    print(f"  - export_research_data encontrado: {research_data_count} vezes")

if __name__ == "__main__":
    fix_excel_imports()