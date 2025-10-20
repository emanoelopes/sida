
### 7. Verificar compatibilidade:

#!/usr/bin/env python3
"""
Script para verificar se o ambiente está configurado corretamente
"""

import sys
import importlib

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python {version.major}.{version.minor} não é suportado. Use Python 3.9+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'sklearn', 'plotly', 'pygwalker', 'missingno'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO INSTALADO")
            missing.append(package)
    
    return len(missing) == 0, missing

if __name__ == "__main__":
    print("Verificando ambiente SIDA...")
    print("=" * 40)
    
    python_ok = check_python_version()
    deps_ok, missing = check_dependencies()
    
    print("=" * 40)
    if python_ok and deps_ok:
        print("✅ Ambiente configurado corretamente!")
    else:
        print("❌ Problemas encontrados:")
        if not python_ok:
            print("  - Versão do Python incompatível")
        if missing:
            print(f"  - Dependências ausentes: {', '.join(missing)}")
        print("\nExecute: pip install -r requirements.txt")
