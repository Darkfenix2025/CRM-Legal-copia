#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN SIMPLE DEL LAYOUT - CRM LEGAL
=======================================

Corrección rápida del problema donde no se ven los clientes
porque el panel izquierdo es demasiado angosto.
"""

import os

def fix_layout_simple():
    """Corrección simple del layout"""
    
    try:
        # Leer archivo
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup rápido
        with open('backup_layout.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Backup creado")
        
        # Corrección simple: cambiar weight=0 a weight=1
        content = content.replace(
            'main_frame.columnconfigure(0, weight=0)  # Panel izquierdo',
            'main_frame.columnconfigure(0, weight=1, minsize=400)  # Panel izquierdo MÁS ANCHO'
        )
        
        # Escribir archivo corregido
        with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Layout corregido")
        print("📏 Panel izquierdo ahora se expandirá apropiadamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 CORRECCIÓN SIMPLE DE LAYOUT")
    print("=" * 40)
    
    if fix_layout_simple():
        print("\n🎉 ¡CORREGIDO!")
        print("🚀 Ejecuta ahora: python main_app_refactorizado.py")
        print("📋 Ahora deberías ver los clientes en el panel izquierdo")
    else:
        print("\n❌ Error en corrección")

if __name__ == "__main__":
    main()
