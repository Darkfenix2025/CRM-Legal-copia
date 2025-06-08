#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRADOR SEGURO DE BASE DE DATOS - CRM LEGAL
=========================================

Este script migra de forma segura la base de datos existente del CRM Legal
a la nueva versión que incluye:
1. Sistema de Etiquetas Globales
2. Módulo Financiero Completo

CARACTERÍSTICAS:
✅ Backup automático antes de migrar
✅ Verificación de integridad de datos
✅ Migración incremental (solo agrega lo necesario)
✅ Rollback automático en caso de error
✅ Validación completa post-migración

USO:
cd CRM-Legal/
python3 migrar_bd_crm_legal.py
"""

import sqlite3
import os
import shutil
import json
from datetime import datetime
import sys

class MigradorBDCRMLegal:
    def __init__(self, db_path='crm_legal.db'):
        self.db_path = db_path
        self.backup_path = f"backup_{db_path}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conn = None
        self.versiones_aplicadas = []
        
    def conectar(self):
        """Conecta a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON")
            print(f"✅ Conectado a base de datos: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a BD: {e}")
            return False
    
    def crear_backup(self):
        """Crea backup de seguridad de la BD"""
        try:
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, self.backup_path)
                print(f"✅ Backup creado: {self.backup_path}")
                return True
            else:
                print(f"❌ Archivo de BD no encontrado: {self.db_path}")
                return False
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return False
    
    def verificar_estado_actual(self):
        """Verifica el estado actual de la BD"""
        print("\n🔍 VERIFICANDO ESTADO ACTUAL DE LA BASE DE DATOS")
        print("=" * 55)
        
        try:
            cursor = self.conn.cursor()
            
            # Obtener tablas existentes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tablas_existentes = [row[0] for row in cursor.fetchall()]
            
            print(f"📋 Tablas existentes ({len(tablas_existentes)}):")
            for tabla in tablas_existentes:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   📄 {tabla}: {count} registros")
            
            # Verificar si ya tiene las nuevas tablas
            tablas_nuevas = [
                'etiquetas_globales', 'caso_etiquetas', 'cliente_etiquetas',
                'presupuestos', 'items_presupuesto', 'facturas', 'items_factura',
                'pagos', 'conceptos_facturacion'
            ]
            
            tablas_faltantes = [t for t in tablas_nuevas if t not in tablas_existentes]
            tablas_existentes_nuevas = [t for t in tablas_nuevas if t in tablas_existentes]
            
            if tablas_existentes_nuevas:
                print(f"\n✅ Tablas nuevas ya existentes ({len(tablas_existentes_nuevas)}):")
                for tabla in tablas_existentes_nuevas:
                    print(f"   🔄 {tabla}")
            
            if tablas_faltantes:
                print(f"\n⏳ Tablas a crear ({len(tablas_faltantes)}):")
                for tabla in tablas_faltantes:
                    print(f"   🆕 {tabla}")
            else:
                print("\n🎉 ¡Todas las tablas nuevas ya están creadas!")
            
            return tablas_faltantes
            
        except Exception as e:
            print(f"❌ Error verificando estado: {e}")
            return None
    
    def aplicar_migracion_etiquetas(self):
        """Aplica la migración del sistema de etiquetas"""
        print("\n🏷️  APLICANDO MIGRACIÓN: SISTEMA DE ETIQUETAS")
        print("=" * 50)
        
        try:
            cursor = self.conn.cursor()
            
            # 1. Crear tabla etiquetas_globales
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etiquetas_globales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT,
                    color TEXT DEFAULT '#3498db',
                    categoria TEXT NOT NULL,
                    activa INTEGER DEFAULT 1,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    creado_por TEXT DEFAULT 'Sistema'
                )
            """)
            print("✅ Tabla etiquetas_globales creada")
            
            # 2. Crear tabla caso_etiquetas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS caso_etiquetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caso_id INTEGER NOT NULL,
                    etiqueta_id INTEGER NOT NULL,
                    fecha_asignacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    asignado_por TEXT DEFAULT 'Usuario',
                    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE,
                    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas_globales(id) ON DELETE CASCADE,
                    UNIQUE(caso_id, etiqueta_id)
                )
            """)
            print("✅ Tabla caso_etiquetas creada")
            
            # 3. Crear tabla cliente_etiquetas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cliente_etiquetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    etiqueta_id INTEGER NOT NULL,
                    fecha_asignacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    asignado_por TEXT DEFAULT 'Usuario',
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas_globales(id) ON DELETE CASCADE,
                    UNIQUE(cliente_id, etiqueta_id)
                )
            """)
            print("✅ Tabla cliente_etiquetas creada")
            
            # 4. Crear índices optimizados
            indices_etiquetas = [
                "CREATE INDEX IF NOT EXISTS idx_etiquetas_globales_categoria ON etiquetas_globales(categoria)",
                "CREATE INDEX IF NOT EXISTS idx_etiquetas_globales_activa ON etiquetas_globales(activa)",
                "CREATE INDEX IF NOT EXISTS idx_caso_etiquetas_caso ON caso_etiquetas(caso_id)",
                "CREATE INDEX IF NOT EXISTS idx_caso_etiquetas_etiqueta ON caso_etiquetas(etiqueta_id)",
                "CREATE INDEX IF NOT EXISTS idx_cliente_etiquetas_cliente ON cliente_etiquetas(cliente_id)",
                "CREATE INDEX IF NOT EXISTS idx_cliente_etiquetas_etiqueta ON cliente_etiquetas(etiqueta_id)"
            ]
            
            for indice in indices_etiquetas:
                cursor.execute(indice)
            
            print("✅ Índices de etiquetas creados")
            
            self.conn.commit()
            self.versiones_aplicadas.append("etiquetas_v1.0")
            return True
            
        except Exception as e:
            print(f"❌ Error en migración de etiquetas: {e}")
            self.conn.rollback()
            return False
    
    def aplicar_migracion_financiero(self):
        """Aplica la migración del sistema financiero"""
        print("\n💰 APLICANDO MIGRACIÓN: SISTEMA FINANCIERO")
        print("=" * 50)
        
        try:
            cursor = self.conn.cursor()
            
            # 1. Crear tabla conceptos_facturacion
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conceptos_facturacion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    categoria TEXT NOT NULL,
                    tarifa_sugerida REAL DEFAULT 0,
                    moneda TEXT DEFAULT 'COP',
                    activo INTEGER DEFAULT 1,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Tabla conceptos_facturacion creada")
            
            # 2. Crear tabla presupuestos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS presupuestos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caso_id INTEGER NOT NULL,
                    numero TEXT UNIQUE NOT NULL,
                    estado TEXT DEFAULT 'Borrador',
                    moneda TEXT DEFAULT 'COP',
                    subtotal REAL DEFAULT 0,
                    iva REAL DEFAULT 0,
                    total REAL DEFAULT 0,
                    notas TEXT,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    fecha_envio TEXT,
                    fecha_aprobacion TEXT,
                    creado_por TEXT,
                    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
                )
            """)
            print("✅ Tabla presupuestos creada")
            
            # 3. Crear tabla items_presupuesto
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items_presupuesto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    presupuesto_id INTEGER NOT NULL,
                    concepto_id INTEGER,
                    descripcion TEXT NOT NULL,
                    cantidad REAL DEFAULT 1,
                    precio_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (presupuesto_id) REFERENCES presupuestos(id) ON DELETE CASCADE,
                    FOREIGN KEY (concepto_id) REFERENCES conceptos_facturacion(id)
                )
            """)
            print("✅ Tabla items_presupuesto creada")
            
            # 4. Crear tabla facturas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    presupuesto_id INTEGER,
                    caso_id INTEGER NOT NULL,
                    numero TEXT UNIQUE NOT NULL,
                    estado TEXT DEFAULT 'Pendiente',
                    moneda TEXT DEFAULT 'COP',
                    subtotal REAL DEFAULT 0,
                    iva REAL DEFAULT 0,
                    total REAL DEFAULT 0,
                    saldo_pendiente REAL DEFAULT 0,
                    fecha_emision TEXT DEFAULT CURRENT_TIMESTAMP,
                    fecha_vencimiento TEXT,
                    notas TEXT,
                    creado_por TEXT,
                    FOREIGN KEY (presupuesto_id) REFERENCES presupuestos(id),
                    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
                )
            """)
            print("✅ Tabla facturas creada")
            
            # 5. Crear tabla items_factura
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items_factura (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER NOT NULL,
                    concepto_id INTEGER,
                    descripcion TEXT NOT NULL,
                    cantidad REAL DEFAULT 1,
                    precio_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
                    FOREIGN KEY (concepto_id) REFERENCES conceptos_facturacion(id)
                )
            """)
            print("✅ Tabla items_factura creada")
            
            # 6. Crear tabla pagos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER NOT NULL,
                    monto REAL NOT NULL,
                    fecha_pago TEXT DEFAULT CURRENT_TIMESTAMP,
                    metodo_pago TEXT,
                    referencia TEXT,
                    notas TEXT,
                    registrado_por TEXT,
                    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
                )
            """)
            print("✅ Tabla pagos creada")
            
            # 7. Crear índices financieros
            indices_financieros = [
                "CREATE INDEX IF NOT EXISTS idx_conceptos_categoria ON conceptos_facturacion(categoria)",
                "CREATE INDEX IF NOT EXISTS idx_presupuestos_caso ON presupuestos(caso_id)",
                "CREATE INDEX IF NOT EXISTS idx_presupuestos_estado ON presupuestos(estado)",
                "CREATE INDEX IF NOT EXISTS idx_facturas_caso ON facturas(caso_id)",
                "CREATE INDEX IF NOT EXISTS idx_facturas_estado ON facturas(estado)",
                "CREATE INDEX IF NOT EXISTS idx_pagos_factura ON pagos(factura_id)"
            ]
            
            for indice in indices_financieros:
                cursor.execute(indice)
            
            print("✅ Índices financieros creados")
            
            self.conn.commit()
            self.versiones_aplicadas.append("financiero_v1.0")
            return True
            
        except Exception as e:
            print(f"❌ Error en migración financiera: {e}")
            self.conn.rollback()
            return False
    
    def cargar_datos_predefinidos(self):
        """Carga datos predefinidos (etiquetas y conceptos)"""
        print("\n📊 CARGANDO DATOS PREDEFINIDOS")
        print("=" * 40)
        
        try:
            cursor = self.conn.cursor()
            
            # Cargar etiquetas predefinidas
            etiquetas_predefinidas = [
                # Prioridad
                ('Urgente', 'Casos que requieren atención inmediata', '#e74c3c', 'Prioridad'),
                ('Alta', 'Casos de alta prioridad', '#f39c12', 'Prioridad'),
                ('Media', 'Casos de prioridad media', '#f1c40f', 'Prioridad'),
                ('Baja', 'Casos de baja prioridad', '#2ecc71', 'Prioridad'),
                
                # Estado
                ('En Proceso', 'Casos actualmente en tramitación', '#3498db', 'Estado'),
                ('Finalizado', 'Casos terminados exitosamente', '#27ae60', 'Estado'),
                ('Suspendido', 'Casos temporalmente suspendidos', '#95a5a6', 'Estado'),
                ('Apelación', 'Casos en proceso de apelación', '#9b59b6', 'Estado'),
                
                # Tipo de Caso
                ('Civil', 'Casos de derecho civil', '#34495e', 'Tipo de Caso'),
                ('Penal', 'Casos de derecho penal', '#c0392b', 'Tipo de Caso'),
                ('Laboral', 'Casos de derecho laboral', '#16a085', 'Tipo de Caso'),
                ('Familia', 'Casos de derecho de familia', '#e67e22', 'Tipo de Caso'),
                ('Comercial', 'Casos de derecho comercial', '#8e44ad', 'Tipo de Caso'),
                ('Administrativo', 'Casos de derecho administrativo', '#2c3e50', 'Tipo de Caso'),
                
                # Cliente
                ('VIP', 'Cliente de alta importancia', '#f39c12', 'Cliente'),
                ('Empresarial', 'Cliente empresarial', '#3498db', 'Cliente'),
                ('Particular', 'Cliente particular', '#95a5a6', 'Cliente'),
                
                # Complejidad
                ('Alta Complejidad', 'Casos complejos que requieren especialización', '#e74c3c', 'Complejidad'),
                ('Media Complejidad', 'Casos de complejidad moderada', '#f39c12', 'Complejidad'),
                ('Baja Complejidad', 'Casos simples y rutinarios', '#27ae60', 'Complejidad'),
                
                # Especialidad
                ('Constitucional', 'Casos de derecho constitucional', '#9b59b6', 'Especialidad'),
                ('Internacional', 'Casos con componente internacional', '#1abc9c', 'Especialidad'),
                ('Tributario', 'Casos de derecho tributario', '#e67e22', 'Especialidad'),
                
                # Demo
                ('Demo', 'Etiqueta de demostración', '#bdc3c7', 'Demo')
            ]
            
            etiquetas_insertadas = 0
            for nombre, desc, color, categoria in etiquetas_predefinidas:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO etiquetas_globales 
                        (nombre, descripcion, color, categoria, activa, creado_por)
                        VALUES (?, ?, ?, ?, 1, 'Sistema')
                    """, (nombre, desc, color, categoria))
                    if cursor.rowcount > 0:
                        etiquetas_insertadas += 1
                except:
                    pass
            
            print(f"✅ Etiquetas predefinidas cargadas: {etiquetas_insertadas}")
            
            # Cargar conceptos de facturación
            conceptos_predefinidos = [
                # Consultas
                ('Consulta Inicial', 'Primera consulta con el cliente', 'Consultas', 300000, 'COP'),
                ('Consulta de Seguimiento', 'Consulta posterior al caso', 'Consultas', 200000, 'COP'),
                ('Consulta Especializada', 'Consulta en área específica', 'Consultas', 450000, 'COP'),
                ('Consulta Virtual', 'Consulta por videoconferencia', 'Consultas', 250000, 'COP'),
                
                # Audiencias
                ('Representación en Audiencia', 'Representación legal en audiencia', 'Audiencias', 800000, 'COP'),
                ('Audiencia de Conciliación', 'Participación en audiencia conciliatoria', 'Audiencias', 600000, 'COP'),
                ('Audiencia de Juicio', 'Representación en audiencia de juicio', 'Audiencias', 1200000, 'COP'),
                ('Audiencia Virtual', 'Participación en audiencia virtual', 'Audiencias', 700000, 'COP'),
                
                # Redacciones
                ('Redacción de Demanda', 'Elaboración de demanda civil', 'Redacciones', 800000, 'COP'),
                ('Redacción de Contestación', 'Contestación de demanda', 'Redacciones', 600000, 'COP'),
                ('Redacción de Recurso', 'Elaboración de recurso de apelación', 'Redacciones', 500000, 'COP'),
                ('Redacción de Contrato', 'Elaboración de contrato', 'Redacciones', 400000, 'COP'),
                ('Redacción de Escritos', 'Escritos procesales diversos', 'Redacciones', 300000, 'COP'),
                
                # Gestiones
                ('Gestión Administrativa', 'Trámites y gestiones administrativas', 'Gestiones', 150000, 'COP'),
                ('Notificaciones', 'Gestión de notificaciones judiciales', 'Gestiones', 100000, 'COP'),
                ('Certificaciones', 'Obtención de certificaciones', 'Gestiones', 80000, 'COP'),
                ('Copias y Fotocopias', 'Gestión documental', 'Gestiones', 50000, 'COP'),
                
                # Investigación
                ('Investigación Jurídica', 'Investigación legal especializada', 'Investigación', 400000, 'COP'),
                ('Análisis de Caso', 'Análisis detallado del caso', 'Investigación', 350000, 'COP'),
                ('Investigación Documental', 'Búsqueda y análisis de documentos', 'Investigación', 250000, 'COP'),
                
                # Asesoría
                ('Asesoría Legal General', 'Asesoría legal integral', 'Asesoría', 500000, 'COP'),
                ('Asesoría Empresarial', 'Asesoría legal empresarial', 'Asesoría', 700000, 'COP'),
                ('Asesoría Fiscal', 'Asesoría en temas tributarios', 'Asesoría', 600000, 'COP'),
                ('Asesoría Laboral', 'Asesoría en derecho laboral', 'Asesoría', 550000, 'COP'),
                
                # Representación
                ('Representación Legal', 'Representación general del cliente', 'Representación', 1000000, 'COP'),
                ('Poder Especial', 'Otorgamiento de poder especial', 'Representación', 200000, 'COP'),
                ('Representación en Notaría', 'Actos notariales', 'Representación', 300000, 'COP'),
                
                # Trámites
                ('Trámite Registral', 'Gestiones en registros públicos', 'Trámites', 250000, 'COP'),
                ('Trámite Notarial', 'Gestiones notariales', 'Trámites', 200000, 'COP'),
                ('Trámite Administrativo', 'Gestiones ante entidades públicas', 'Trámites', 180000, 'COP'),
                
                # Otros
                ('Viáticos', 'Gastos de transporte y estadía', 'Otros', 100000, 'COP'),
                ('Gastos Procesales', 'Gastos inherentes al proceso', 'Otros', 150000, 'COP'),
                ('Horas Adicionales', 'Trabajo fuera de horario normal', 'Otros', 80000, 'COP'),
                ('Revisión de Documentos', 'Revisión y análisis documental', 'Otros', 200000, 'COP'),
                ('Seguimiento de Caso', 'Seguimiento periódico del caso', 'Otros', 150000, 'COP'),
                ('Traducción de Documentos', 'Servicios de traducción', 'Otros', 100000, 'COP'),
                ('Peritajes', 'Coordinación de peritajes', 'Otros', 300000, 'COP'),
                ('Mediación', 'Servicios de mediación', 'Otros', 400000, 'COP'),
                ('Arbitraje', 'Participación en arbitraje', 'Otros', 800000, 'COP'),
                ('Capacitación Legal', 'Capacitación al cliente', 'Otros', 250000, 'COP')
            ]
            
            conceptos_insertados = 0
            for nombre, desc, categoria, tarifa, moneda in conceptos_predefinidos:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO conceptos_facturacion 
                        (nombre, descripcion, categoria, tarifa_sugerida, moneda, activo)
                        VALUES (?, ?, ?, ?, ?, 1)
                    """, (nombre, desc, categoria, tarifa, moneda))
                    if cursor.rowcount > 0:
                        conceptos_insertados += 1
                except:
                    pass
            
            print(f"✅ Conceptos de facturación cargados: {conceptos_insertados}")
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos predefinidos: {e}")
            self.conn.rollback()
            return False
    
    def verificar_migracion(self):
        """Verifica que la migración se haya completado correctamente"""
        print("\n🔍 VERIFICANDO MIGRACIÓN COMPLETADA")
        print("=" * 45)
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar tablas nuevas
            tablas_esperadas = [
                'etiquetas_globales', 'caso_etiquetas', 'cliente_etiquetas',
                'presupuestos', 'items_presupuesto', 'facturas', 'items_factura',
                'pagos', 'conceptos_facturacion'
            ]
            
            print("📋 Verificando tablas creadas:")
            for tabla in tablas_esperadas:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
                if cursor.fetchone():
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                    count = cursor.fetchone()[0]
                    print(f"   ✅ {tabla}: {count} registros")
                else:
                    print(f"   ❌ {tabla}: NO ENCONTRADA")
                    return False
            
            # Verificar datos predefinidos
            cursor.execute("SELECT COUNT(*) FROM etiquetas_globales WHERE activa = 1")
            etiquetas_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM conceptos_facturacion WHERE activo = 1")
            conceptos_count = cursor.fetchone()[0]
            
            print(f"\n📊 Datos predefinidos:")
            print(f"   🏷️ Etiquetas activas: {etiquetas_count}")
            print(f"   💰 Conceptos de facturación: {conceptos_count}")
            
            if etiquetas_count >= 20 and conceptos_count >= 30:
                print("\n✅ ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
                return True
            else:
                print("\n⚠️ Migración incompleta - faltan datos predefinidos")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando migración: {e}")
            return False
    
    def migrar(self):
        """Ejecuta el proceso completo de migración"""
        print("🚀 INICIANDO MIGRACIÓN SEGURA DE BASE DE DATOS")
        print("=" * 60)
        print("CRM Legal v2.0 - Sistema de Etiquetas + Módulo Financiero")
        print("=" * 60)
        
        # 1. Verificar si existe la BD
        if not os.path.exists(self.db_path):
            print(f"❌ Base de datos no encontrada: {self.db_path}")
            print("   Asegúrate de estar en el directorio correcto del CRM Legal")
            return False
        
        # 2. Crear backup
        if not self.crear_backup():
            return False
        
        # 3. Conectar a BD
        if not self.conectar():
            return False
        
        try:
            # 4. Verificar estado actual
            tablas_faltantes = self.verificar_estado_actual()
            if tablas_faltantes is None:
                return False
            
            if not tablas_faltantes:
                print("\n🎉 ¡La base de datos ya está actualizada!")
                respuesta = input("\n¿Deseas recargar los datos predefinidos? (s/N): ").lower()
                if respuesta == 's':
                    self.cargar_datos_predefinidos()
                    self.verificar_migracion()
                return True
            
            # 5. Confirmar migración
            print(f"\n⚠️ Se van a crear {len(tablas_faltantes)} nuevas tablas.")
            print(f"📁 Backup guardado en: {self.backup_path}")
            respuesta = input("\n¿Proceder con la migración? (s/N): ").lower()
            
            if respuesta != 's':
                print("❌ Migración cancelada por el usuario")
                return False
            
            # 6. Aplicar migraciones
            exito = True
            
            if any('etiqueta' in t for t in tablas_faltantes):
                if not self.aplicar_migracion_etiquetas():
                    exito = False
            
            if any(t in ['presupuestos', 'facturas', 'pagos', 'conceptos_facturacion'] for t in tablas_faltantes):
                if not self.aplicar_migracion_financiero():
                    exito = False
            
            if not exito:
                print("\n❌ Error en migración - Restaurando backup...")
                self.conn.close()
                shutil.copy2(self.backup_path, self.db_path)
                return False
            
            # 7. Cargar datos predefinidos
            if not self.cargar_datos_predefinidos():
                print("⚠️ Error cargando datos predefinidos, pero migración exitosa")
            
            # 8. Verificar migración
            if not self.verificar_migracion():
                return False
            
            print(f"\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
            print(f"📊 Versiones aplicadas: {', '.join(self.versiones_aplicadas)}")
            print(f"💾 Backup disponible en: {self.backup_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante migración: {e}")
            print("🔄 Restaurando backup...")
            self.conn.close()
            shutil.copy2(self.backup_path, self.db_path)
            return False
        
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Función principal"""
    print("🔧 MIGRADOR DE BASE DE DATOS - CRM LEGAL v2.0")
    print("=" * 50)
    
    # Verificar directorio
    if not os.path.exists('crm_legal.db'):
        print("❌ Base de datos 'crm_legal.db' no encontrada")
        print("   Asegúrate de ejecutar desde el directorio del CRM Legal")
        print("   O ejecuta primero la aplicación principal para crear la BD")
        return
    
    # Ejecutar migración
    migrador = MigradorBDCRMLegal()
    exito = migrador.migrar()
    
    if exito:
        print("\n✅ PRÓXIMOS PASOS:")
        print("1. Ejecuta: python3 main_app.py")
        print("2. Explora las nuevas pestañas: 'Etiquetas' y 'Financiero'")
        print("3. Revisa la documentación en docs/")
        print("\n🚀 ¡Tu CRM Legal está listo con las nuevas funcionalidades!")
    else:
        print("\n❌ Migración fallida")
        print("📧 Contacta al desarrollador si el problema persiste")

if __name__ == "__main__":
    main()
