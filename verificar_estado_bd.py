#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE ESTADO - BASE DE DATOS CRM LEGAL
==============================================

Este script verifica el estado actual de la base de datos del CRM Legal
sin hacer modificaciones. Te permite saber qué tienes y qué necesitas.

USO:
cd CRM-Legal/
python3 verificar_estado_bd.py
"""

import sqlite3
import os
from datetime import datetime

def verificar_base_datos():
    """Verifica el estado completo de la base de datos"""
    
    db_path = 'crm_legal.db'
    
    print("🔍 VERIFICADOR DE ESTADO - CRM LEGAL")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗄️ Base de datos: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"\n❌ Base de datos no encontrada: {db_path}")
        print("   Ejecuta primero main_app.py para crear la base de datos")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. INFORMACIÓN GENERAL
        print(f"\n📊 INFORMACIÓN GENERAL")
        print("-" * 30)
        
        file_size = os.path.getsize(db_path)
        print(f"💾 Tamaño archivo: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        # 2. TABLAS EXISTENTES
        print(f"\n📋 TABLAS EXISTENTES")
        print("-" * 25)
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = cursor.fetchall()
        
        datos_tablas = []
        for (tabla,) in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            datos_tablas.append((tabla, count))
            print(f"📄 {tabla:<20} {count:>8} registros")
        
        total_registros = sum(count for _, count in datos_tablas)
        print(f"\n📊 TOTAL: {len(datos_tablas)} tablas, {total_registros:,} registros")
        
        # 3. VERIFICAR FUNCIONALIDADES NUEVAS
        print(f"\n🚀 FUNCIONALIDADES NUEVAS")
        print("-" * 30)
        
        # Sistema de Etiquetas
        tablas_etiquetas = ['etiquetas_globales', 'caso_etiquetas', 'cliente_etiquetas']
        etiquetas_completas = True
        
        print("🏷️  Sistema de Etiquetas Globales:")
        for tabla in tablas_etiquetas:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {tabla}: {count} registros")
            else:
                print(f"   ❌ {tabla}: NO EXISTE")
                etiquetas_completas = False
        
        # Sistema Financiero
        tablas_financiero = ['presupuestos', 'items_presupuesto', 'facturas', 'items_factura', 'pagos', 'conceptos_facturacion']
        financiero_completo = True
        
        print("\n💰 Sistema Financiero:")
        for tabla in tablas_financiero:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {tabla}: {count} registros")
            else:
                print(f"   ❌ {tabla}: NO EXISTE")
                financiero_completo = False
        
        # 4. DATOS PREDEFINIDOS
        print(f"\n📊 DATOS PREDEFINIDOS")
        print("-" * 25)
        
        if etiquetas_completas:
            cursor.execute("SELECT COUNT(*) FROM etiquetas_globales WHERE activa = 1")
            etiquetas_activas = cursor.fetchone()[0]
            
            cursor.execute("SELECT categoria, COUNT(*) FROM etiquetas_globales WHERE activa = 1 GROUP BY categoria ORDER BY categoria")
            categorias_etiquetas = cursor.fetchall()
            
            print(f"🏷️  Etiquetas activas: {etiquetas_activas}")
            for categoria, count in categorias_etiquetas:
                print(f"   📁 {categoria}: {count}")
        else:
            print("🏷️  Sistema de etiquetas: NO CONFIGURADO")
        
        if financiero_completo:
            cursor.execute("SELECT COUNT(*) FROM conceptos_facturacion WHERE activo = 1")
            conceptos_activos = cursor.fetchone()[0]
            
            cursor.execute("SELECT categoria, COUNT(*) FROM conceptos_facturacion WHERE activo = 1 GROUP BY categoria ORDER BY categoria")
            categorias_conceptos = cursor.fetchall()
            
            print(f"\n💰 Conceptos facturación: {conceptos_activos}")
            for categoria, count in categorias_conceptos:
                print(f"   💼 {categoria}: {count}")
        else:
            print("\n💰 Sistema financiero: NO CONFIGURADO")
        
        # 5. DATOS DEL USUARIO
        print(f"\n👥 DATOS DEL USUARIO")
        print("-" * 25)
        
        cursor.execute("SELECT COUNT(*) FROM clientes")
        clientes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM casos")
        casos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM audiencias")
        audiencias = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM actividades")
        actividades = cursor.fetchone()[0]
        
        print(f"👤 Clientes: {clientes}")
        print(f"📁 Casos: {casos}")
        print(f"🎯 Audiencias: {audiencias}")
        print(f"📝 Actividades: {actividades}")
        
        # 6. ESTADO Y RECOMENDACIONES
        print(f"\n🎯 ESTADO Y RECOMENDACIONES")
        print("-" * 35)
        
        if etiquetas_completas and financiero_completo:
            print("✅ ¡Base de datos COMPLETAMENTE ACTUALIZADA!")
            print("🎉 Todas las funcionalidades nuevas están disponibles")
            
            if datos_tablas:
                print("\n📋 Funcionalidades disponibles:")
                print("   🏷️ Sistema de Etiquetas Globales")
                print("   💰 Módulo Financiero Completo")
                print("   📊 Presupuestos y Facturación")
                print("   💳 Control de Pagos")
        
        elif not etiquetas_completas and not financiero_completo:
            print("⏳ Base de datos REQUIERE MIGRACIÓN COMPLETA")
            print("📋 Funcionalidades pendientes:")
            print("   🏷️ Sistema de Etiquetas Globales")
            print("   💰 Módulo Financiero Completo")
            print("\n🔧 Ejecuta: python3 migrar_bd_crm_legal.py")
        
        elif not etiquetas_completas:
            print("⏳ Falta SISTEMA DE ETIQUETAS")
            print("🔧 Ejecuta: python3 migrar_bd_crm_legal.py")
        
        elif not financiero_completo:
            print("⏳ Falta SISTEMA FINANCIERO")
            print("🔧 Ejecuta: python3 migrar_bd_crm_legal.py")
        
        else:
            print("⚠️ Estado parcial - verifica configuración")
        
        # 7. INTEGRIDAD DE DATOS
        print(f"\n🔒 VERIFICACIÓN DE INTEGRIDAD")
        print("-" * 35)
        
        try:
            cursor.execute("PRAGMA integrity_check")
            integridad = cursor.fetchone()[0]
            if integridad == 'ok':
                print("✅ Integridad de datos: OK")
            else:
                print(f"⚠️ Problemas de integridad: {integridad}")
        except:
            print("⚠️ No se pudo verificar integridad")
        
        try:
            cursor.execute("PRAGMA foreign_key_check")
            fk_errors = cursor.fetchall()
            if not fk_errors:
                print("✅ Claves foráneas: OK")
            else:
                print(f"⚠️ Errores en claves foráneas: {len(fk_errors)}")
        except:
            print("⚠️ No se pudieron verificar claves foráneas")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    """Función principal"""
    resultado = verificar_base_datos()
    
    if resultado:
        print(f"\n✅ VERIFICACIÓN COMPLETADA")
        print("=" * 30)
        print("📋 Próximos pasos:")
        print("   1. Si necesitas migrar: python3 migrar_bd_crm_legal.py")
        print("   2. Para usar el CRM: python3 main_app.py")
        print("   3. Para demo: python3 demo_sistema_completo.py")
    else:
        print(f"\n❌ VERIFICACIÓN FALLIDA")

if __name__ == "__main__":
    main()
