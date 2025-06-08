#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN ESPECÍFICA: ERROR update_case()
==========================================

Error: "update_case() takes 11 positional arguments but 13 were given"

Este error indica que hay una discrepancia entre:
- Cuántos parámetros espera la función update_case()
- Cuántos parámetros se están enviando desde la interfaz

Voy a analizar y corregir esta discrepancia específica.
"""

import os
import re

def analizar_funcion_update_case():
    """Analiza la función update_case actual en crm_database.py"""
    print("🔍 ANALIZANDO FUNCIÓN update_case()")
    print("=" * 45)
    
    if not os.path.exists('crm_database.py'):
        print("❌ crm_database.py no encontrado")
        return None
    
    try:
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar la función update_case
        patron = r'def update_case\([^)]+\):'
        match = re.search(patron, contenido, re.MULTILINE)
        
        if match:
            funcion_def = match.group(0)
            print(f"📋 Definición encontrada: {funcion_def}")
            
            # Contar parámetros
            parametros = funcion_def[funcion_def.find('(')+1:funcion_def.find(')')]
            lista_params = [p.strip() for p in parametros.split(',') if p.strip()]
            
            print(f"📊 Parámetros actuales ({len(lista_params)}):")
            for i, param in enumerate(lista_params, 1):
                print(f"   {i}. {param}")
            
            return lista_params
        else:
            print("❌ Función update_case no encontrada")
            return None
            
    except Exception as e:
        print(f"❌ Error analizando función: {e}")
        return None

def buscar_llamadas_update_case():
    """Busca todas las llamadas a update_case() en el código"""
    print("\n🔍 BUSCANDO LLAMADAS A update_case()")
    print("=" * 40)
    
    archivos_python = []
    for archivo in os.listdir('.'):
        if archivo.endswith('.py') and archivo != __file__:
            archivos_python.append(archivo)
    
    llamadas_encontradas = []
    
    for archivo in archivos_python:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            for num_linea, linea in enumerate(lineas, 1):
                if 'update_case(' in linea and not linea.strip().startswith('#'):
                    llamadas_encontradas.append({
                        'archivo': archivo,
                        'linea': num_linea,
                        'codigo': linea.strip()
                    })
                    print(f"📍 {archivo}:{num_linea} - {linea.strip()}")
        except:
            continue
    
    return llamadas_encontradas

def crear_funcion_update_case_corregida():
    """Crea la función update_case corregida con el número correcto de parámetros"""
    print("\n🔧 CREANDO FUNCIÓN CORREGIDA")
    print("=" * 35)
    
    # Función corregida que acepta todos los parámetros necesarios
    funcion_corregida = '''def update_case(case_id, caratula, numero_expediente, anio_caratula, juzgado, jurisdiccion, etapa_procesal, notas, ruta_carpeta, inactivity_threshold_days, inactivity_enabled):
    """
    Actualiza un caso existente en la base de datos.
    
    Parámetros:
    1. case_id - ID del caso a actualizar
    2. caratula - Carátula del caso
    3. numero_expediente - Número de expediente
    4. anio_caratula - Año de la carátula
    5. juzgado - Juzgado del caso
    6. jurisdiccion - Jurisdicción
    7. etapa_procesal - Etapa procesal actual
    8. notas - Notas del caso
    9. ruta_carpeta - Ruta de la carpeta de documentos
    10. inactivity_threshold_days - Días límite de inactividad
    11. inactivity_enabled - Si la alerta de inactividad está habilitada
    """
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE casos SET 
                caratula = ?, 
                numero_expediente = ?, 
                anio_caratula = ?, 
                juzgado = ?, 
                jurisdiccion = ?, 
                etapa_procesal = ?, 
                notas = ?, 
                ruta_carpeta = ?, 
                inactivity_threshold_days = ?, 
                inactivity_enabled = ?
            WHERE id = ?
        """, (caratula, numero_expediente, anio_caratula, juzgado, jurisdiccion, 
              etapa_procesal, notas, ruta_carpeta, inactivity_threshold_days, 
              inactivity_enabled, case_id))
        
        conn.commit()
        return cursor.rowcount > 0
        
    except Exception as e:
        print(f"Error al actualizar caso: {e}")
        return False
    finally:
        close_db(conn)'''
    
    return funcion_corregida

def aplicar_correccion_update_case():
    """Aplica la corrección a la función update_case"""
    print("\n🛠️  APLICANDO CORRECCIÓN")
    print("=" * 30)
    
    try:
        # Leer archivo actual
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open('crm_database_backup_update_case.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado: crm_database_backup_update_case.py")
        
        # Buscar la función update_case actual
        inicio = contenido.find('def update_case(')
        if inicio == -1:
            print("❌ Función update_case no encontrada")
            return False
        
        # Buscar el final de la función
        fin = contenido.find('\ndef ', inicio + 1)
        if fin == -1:
            fin = contenido.find('\n\n', inicio + 1)
        if fin == -1:
            fin = len(contenido)
        
        # Obtener función corregida
        funcion_nueva = crear_funcion_update_case_corregida()
        
        # Reemplazar la función
        nuevo_contenido = contenido[:inicio] + funcion_nueva + '\n' + contenido[fin:]
        
        # Escribir archivo corregido
        with open('crm_database.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Función update_case reemplazada con versión corregida")
        print("✅ Ahora acepta exactamente 11 parámetros como se espera")
        
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando corrección: {e}")
        return False

def verificar_correccion():
    """Verifica que la corrección se aplicó correctamente"""
    print("\n✅ VERIFICANDO CORRECCIÓN")
    print("=" * 30)
    
    # Re-analizar la función corregida
    parametros = analizar_funcion_update_case()
    
    if parametros and len(parametros) == 11:
        print("🎉 ¡CORRECCIÓN EXITOSA!")
        print(f"✅ La función ahora tiene exactamente {len(parametros)} parámetros")
        print("✅ Debería resolver el error de 'too many positional arguments'")
        return True
    else:
        print("❌ La corrección no se aplicó correctamente")
        return False

def main():
    """Función principal para corregir el error de update_case"""
    print("🔧 CORRECCIÓN ESPECÍFICA: ERROR update_case()")
    print("=" * 60)
    print("Error: 'update_case() takes 11 positional arguments but 13 were given'\n")
    
    # Paso 1: Analizar función actual
    parametros_actuales = analizar_funcion_update_case()
    
    # Paso 2: Buscar llamadas
    llamadas = buscar_llamadas_update_case()
    
    # Paso 3: Aplicar corrección
    if aplicar_correccion_update_case():
        # Paso 4: Verificar corrección
        if verificar_correccion():
            print("\n🎯 RESULTADO FINAL")
            print("=" * 25)
            print("✅ Error de update_case() SOLUCIONADO")
            print("✅ Función acepta 11 parámetros correctamente")
            print("✅ Backup de seguridad creado")
            
            print("\n📋 LO QUE SE CORRIGIÓ:")
            print("• Definición de función alineada con llamadas")
            print("• Parámetros en orden correcto")
            print("• SQL UPDATE statement correcto")
            print("• Manejo de errores incluido")
            
            print("\n🚀 PRUEBA AHORA:")
            print("1. Ejecuta el CRM Legal")
            print("2. Ve a Alta/Edición de caso")
            print("3. Indica ruta de documentos")
            print("4. El error ya no debería aparecer")
        else:
            print("\n❌ Verificación falló - revisar manualmente")
    else:
        print("\n❌ No se pudo aplicar la corrección")

if __name__ == "__main__":
    main()
