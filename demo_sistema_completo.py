#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMOSTRACIÓN COMPLETA DEL CRM LEGAL EXPANDIDO
===========================================

Este script demuestra las nuevas funcionalidades implementadas:
1. Sistema de Etiquetas Globales
2. Módulo Financiero Completo

Ejecutar desde el directorio CRM-Legal:
python3 demo_sistema_completo.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'CRM-Legal'))

import sqlite3
from datetime import datetime
import json

def conectar_bd():
    """Conecta a la base de datos del CRM"""
    try:
        db_path = 'CRM-Legal/crm_legal.db'
        if not os.path.exists(db_path):
            print("❌ Base de datos no encontrada. Ejecuta primero la aplicación principal.")
            return None
        
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

def verificar_sistema_etiquetas():
    """Verifica que el sistema de etiquetas esté funcionando"""
    print("\n🏷️  VERIFICANDO SISTEMA DE ETIQUETAS")
    print("=" * 50)
    
    conn = conectar_bd()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar tabla de etiquetas globales
        cursor.execute("SELECT COUNT(*) FROM etiquetas_globales WHERE activa = 1")
        count_etiquetas = cursor.fetchone()[0]
        
        # Verificar categorías
        cursor.execute("""
            SELECT categoria, COUNT(*) 
            FROM etiquetas_globales 
            WHERE activa = 1 
            GROUP BY categoria 
            ORDER BY categoria
        """)
        categorias = cursor.fetchall()
        
        print(f"✅ Etiquetas activas: {count_etiquetas}")
        print(f"✅ Categorías disponibles: {len(categorias)}")
        
        for categoria, count in categorias:
            print(f"   📁 {categoria}: {count} etiquetas")
        
        # Mostrar algunas etiquetas ejemplo
        cursor.execute("""
            SELECT nombre, categoria, color, descripcion 
            FROM etiquetas_globales 
            WHERE activa = 1 
            LIMIT 5
        """)
        etiquetas_ejemplo = cursor.fetchall()
        
        print("\n📋 Etiquetas de ejemplo:")
        for nombre, categoria, color, desc in etiquetas_ejemplo:
            print(f"   🔖 {nombre} ({categoria}) - {desc}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando etiquetas: {e}")
        conn.close()
        return False

def verificar_sistema_financiero():
    """Verifica que el sistema financiero esté funcionando"""
    print("\n💰 VERIFICANDO SISTEMA FINANCIERO")
    print("=" * 50)
    
    conn = conectar_bd()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar conceptos de facturación
        cursor.execute("SELECT COUNT(*) FROM conceptos_facturacion WHERE activo = 1")
        count_conceptos = cursor.fetchone()[0]
        
        # Verificar categorías de conceptos
        cursor.execute("""
            SELECT categoria, COUNT(*) 
            FROM conceptos_facturacion 
            WHERE activo = 1 
            GROUP BY categoria 
            ORDER BY categoria
        """)
        categorias_conceptos = cursor.fetchall()
        
        print(f"✅ Conceptos de facturación: {count_conceptos}")
        print(f"✅ Categorías de servicios: {len(categorias_conceptos)}")
        
        for categoria, count in categorias_conceptos:
            print(f"   💼 {categoria}: {count} conceptos")
        
        # Mostrar algunos conceptos ejemplo
        cursor.execute("""
            SELECT nombre, categoria, tarifa_sugerida, moneda 
            FROM conceptos_facturacion 
            WHERE activo = 1 
            LIMIT 5
        """)
        conceptos_ejemplo = cursor.fetchall()
        
        print("\n📋 Conceptos de ejemplo:")
        for nombre, categoria, tarifa, moneda in conceptos_ejemplo:
            print(f"   💰 {nombre} ({categoria}) - {tarifa:,.0f} {moneda}")
        
        # Verificar tablas de presupuestos y facturas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%presupuesto%'")
        tablas_presupuesto = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%factura%'")
        tablas_factura = [row[0] for row in cursor.fetchall()]
        
        print(f"\n✅ Tablas de presupuestos: {', '.join(tablas_presupuesto)}")
        print(f"✅ Tablas de facturación: {', '.join(tablas_factura)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando sistema financiero: {e}")
        conn.close()
        return False

def crear_datos_demo():
    """Crea datos de demostración para mostrar el sistema"""
    print("\n🎯 CREANDO DATOS DE DEMOSTRACIÓN")
    print("=" * 50)
    
    conn = conectar_bd()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Obtener un caso existente para demo
        cursor.execute("SELECT id, caratula FROM casos LIMIT 1")
        caso_demo = cursor.fetchone()
        
        if not caso_demo:
            print("❌ No hay casos disponibles para demo")
            return False
        
        caso_id, caso_caratula = caso_demo
        print(f"📁 Usando caso: {caso_caratula}")
        
        # Asignar algunas etiquetas al caso demo
        etiquetas_para_asignar = ['Urgente', 'En Proceso', 'Civil', 'Particular']
        
        for etiqueta_nombre in etiquetas_para_asignar:
            # Buscar la etiqueta
            cursor.execute("SELECT id FROM etiquetas_globales WHERE nombre = ? AND activa = 1", (etiqueta_nombre,))
            etiqueta = cursor.fetchone()
            
            if etiqueta:
                etiqueta_id = etiqueta[0]
                # Verificar si ya está asignada
                cursor.execute("SELECT 1 FROM caso_etiquetas WHERE caso_id = ? AND etiqueta_id = ?", (caso_id, etiqueta_id))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO caso_etiquetas (caso_id, etiqueta_id, fecha_asignacion)
                        VALUES (?, ?, ?)
                    """, (caso_id, etiqueta_id, datetime.now().isoformat()))
                    print(f"   🏷️ Etiqueta '{etiqueta_nombre}' asignada")
        
        # Crear un presupuesto demo
        cursor.execute("""
            INSERT INTO presupuestos (
                caso_id, numero, estado, moneda, subtotal, iva, total,
                notas, fecha_creacion, creado_por
            ) VALUES (?, 'PRES-2024-0001', 'Borrador', 'COP', 2000000, 380000, 2380000,
                     'Presupuesto de demostración para caso civil', ?, 'Admin')
        """, (caso_id, datetime.now().isoformat()))
        
        presupuesto_id = cursor.lastrowid
        
        # Agregar items al presupuesto
        items_demo = [
            ('Consulta Inicial', 1, 300000, 300000),
            ('Redacción de Demanda', 1, 800000, 800000),
            ('Representación en Audiencia', 2, 450000, 900000)
        ]
        
        for descripcion, cantidad, precio, subtotal in items_demo:
            cursor.execute("""
                INSERT INTO items_presupuesto (
                    presupuesto_id, descripcion, cantidad, precio_unitario, subtotal
                ) VALUES (?, ?, ?, ?, ?)
            """, (presupuesto_id, descripcion, cantidad, precio, subtotal))
        
        print(f"   💰 Presupuesto PRES-2024-0001 creado con 3 items")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos demo: {e}")
        conn.rollback()
        conn.close()
        return False

def mostrar_estadisticas_finales():
    """Muestra estadísticas finales del sistema"""
    print("\n📊 ESTADÍSTICAS FINALES DEL SISTEMA")
    print("=" * 50)
    
    conn = conectar_bd()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Estadísticas de etiquetas
        cursor.execute("SELECT COUNT(*) FROM etiquetas_globales WHERE activa = 1")
        total_etiquetas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM caso_etiquetas")
        total_asignaciones_caso = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cliente_etiquetas")
        total_asignaciones_cliente = cursor.fetchone()[0]
        
        # Estadísticas financieras
        cursor.execute("SELECT COUNT(*) FROM conceptos_facturacion WHERE activo = 1")
        total_conceptos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM presupuestos")
        total_presupuestos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM facturas")
        total_facturas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pagos")
        total_pagos = cursor.fetchone()[0]
        
        print("🏷️  SISTEMA DE ETIQUETAS:")
        print(f"   📋 Etiquetas disponibles: {total_etiquetas}")
        print(f"   🔗 Asignaciones a casos: {total_asignaciones_caso}")
        print(f"   🔗 Asignaciones a clientes: {total_asignaciones_cliente}")
        
        print("\n💰 SISTEMA FINANCIERO:")
        print(f"   📝 Conceptos de facturación: {total_conceptos}")
        print(f"   📄 Presupuestos creados: {total_presupuestos}")
        print(f"   🧾 Facturas emitidas: {total_facturas}")
        print(f"   💳 Pagos registrados: {total_pagos}")
        
        # Calcular totales financieros si hay presupuestos
        if total_presupuestos > 0:
            cursor.execute("SELECT SUM(total) FROM presupuestos")
            total_presupuestado = cursor.fetchone()[0] or 0
            print(f"   💵 Total presupuestado: ${total_presupuestado:,.0f} COP")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error calculando estadísticas: {e}")
        conn.close()
        return False

def main():
    """Función principal de demostración"""
    print("🚀 DEMOSTRACIÓN COMPLETA - CRM LEGAL EXPANDIDO")
    print("=" * 60)
    print("Verificando las nuevas funcionalidades implementadas...")
    
    # Verificar directorio
    if not os.path.exists('CRM-Legal'):
        print("❌ Directorio CRM-Legal no encontrado.")
        print("   Asegúrate de ejecutar desde el directorio correcto.")
        return
    
    # Cambiar al directorio del CRM
    os.chdir('CRM-Legal')
    
    # Verificaciones
    etiquetas_ok = verificar_sistema_etiquetas()
    financiero_ok = verificar_sistema_financiero()
    
    if etiquetas_ok and financiero_ok:
        print("\n🎉 ¡TODOS LOS SISTEMAS OPERATIVOS!")
        
        # Crear datos demo
        demo_ok = crear_datos_demo()
        
        if demo_ok:
            mostrar_estadisticas_finales()
            
            print("\n✅ IMPLEMENTACIÓN COMPLETADA CON ÉXITO")
            print("=" * 50)
            print("🎯 Módulos implementados:")
            print("   🏷️ Sistema de Etiquetas Globales")
            print("   💰 Módulo Financiero Completo")
            print("\n📝 Próximos pasos:")
            print("   1. Ejecutar: python3 main_app.py")
            print("   2. Explorar nuevas pestañas: Etiquetas y Financiero")
            print("   3. Revisar documentación en docs/")
            print("\n🚀 ¡Tu CRM Legal está listo para uso profesional!")
        
    else:
        print("\n❌ Algunos sistemas requieren configuración adicional")
        print("   Ejecuta los scripts de inicialización:")
        print("   - python3 init_etiquetas_predefinidas.py")
        print("   - python3 init_conceptos_facturacion.py")

if __name__ == "__main__":
    main()
