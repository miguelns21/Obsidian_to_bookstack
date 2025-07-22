#!/usr/bin/env python3
"""
Ejemplo de uso del transferidor de Obsidian a BookStack

Este script muestra cómo usar la herramienta paso a paso y proporciona
ejemplos prácticos de configuración.

Autor: Miguel Navarro
Fecha: 2025
"""

import json
import os
from pathlib import Path


def crear_configuracion_ejemplo():
    """Crea un archivo de configuración de ejemplo personalizado"""
    
    print("=== Configurador de Obsidian to BookStack ===")
    print()
    
    # Recopilar información del usuario
    print("Por favor, proporciona la siguiente información:")
    print()
    
    # Configuración de BookStack
    bookstack_url = input("URL de tu BookStack (ej: https://mi-bookstack.com): ").strip()
    token_id = input("Token ID de BookStack: ").strip()
    token_secret = input("Token Secret de BookStack: ").strip()
    
    # Configuración de Obsidian
    print("\nRuta a tu bóveda de Obsidian:")
    print("(Puedes arrastrar la carpeta aquí o escribir la ruta completa)")
    vault_path = input("Ruta: ").strip().strip('"\'')
    
    # Configuración de transferencia
    book_name = input("\nNombre del libro en BookStack (ej: 'Mi Bóveda de Obsidian'): ").strip()
    if not book_name:
        book_name = "Mi Bóveda de Obsidian"
    
    shelf_name = input("Nombre del estante principal [Contenido de Obsidian]: ").strip()
    if not shelf_name:
        shelf_name = "Contenido de Obsidian"
    
    print("\n¿Quieres preservar la estructura de carpetas como capítulos? (s/n): ", end="")
    preserve_structure = input().strip().lower() in ['s', 'sí', 'si', 'y', 'yes']
    
    print("¿Crear capítulos basados en carpetas? (s/n): ", end="")
    create_chapters = input().strip().lower() in ['s', 'sí', 'si', 'y', 'yes']
    
    # Crear configuración
    config = {
        "bookstack": {
            "url": bookstack_url,
            "token_id": token_id,
            "token_secret": token_secret
        },
        "obsidian": {
            "vault_path": vault_path
        },
        "transfer": {
            "book_name": book_name,
            "shelf_name": shelf_name,
            "create_chapters_from_folders": create_chapters,
            "preserve_folder_structure": preserve_structure
        }
    }
    
    # Guardar configuración
    config_path = "mi_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuración guardada en: {config_path}")
    return config_path


def mostrar_pasos_uso():
    """Muestra los pasos para usar la herramienta"""
    
    print("\n=== Pasos para usar la herramienta ===")
    print()
    print("1. 📋 PREPARACIÓN:")
    print("   - Asegúrate de tener Python 3.7+ instalado")
    print("   - Instala dependencias: pip install -r requirements.txt")
    print("   - Ten listos tus tokens de API de BookStack")
    print()
    print("2. 🔧 CONFIGURACIÓN:")
    print("   - Ejecuta este script para crear tu configuración")
    print("   - O edita manualmente config.json.example")
    print()
    print("3. 🧪 PRUEBA DE CONEXIÓN:")
    print("   python obsidian_to_bookstack.py mi_config.json --test-connection")
    print()
    print("4. 🚀 TRANSFERENCIA:")
    print("   # Simulación (recomendado primero):")
    print("   python obsidian_to_bookstack.py mi_config.json --dry-run")
    print()
    print("   # Transferencia real:")
    print("   python obsidian_to_bookstack.py mi_config.json")
    print()
    print("5. ✅ VERIFICACIÓN:")
    print("   - Revisa tu BookStack para confirmar la transferencia")
    print("   - Verifica que el contenido se vea correctamente")
    print()


def mostrar_ejemplos_configuracion():
    """Muestra ejemplos de diferentes configuraciones"""
    
    print("\n=== Ejemplos de configuración ===")
    print()
    
    print("📄 EJEMPLO 1: Configuración básica")
    ejemplo1 = {
        "bookstack": {
            "url": "https://mi-bookstack.com",
            "token_id": "tu_token_id",
            "token_secret": "tu_token_secret"
        },
        "obsidian": {
            "vault_path": "/Users/usuario/Documents/MiVault"
        },
        "transfer": {
            "book_name": "Conocimiento Personal",
            "shelf_name": "Contenido de Obsidian"
        }
    }
    print(json.dumps(ejemplo1, indent=2, ensure_ascii=False))
    print()
    
    print("📄 EJEMPLO 2: Configuración para empresa")
    ejemplo2 = {
        "bookstack": {
            "url": "https://docs.empresa.com",
            "token_id": "token123",
            "token_secret": "secret456"
        },
        "obsidian": {
            "vault_path": "/home/user/obsidian-vault"
        },
        "transfer": {
            "book_name": "Documentación Técnica",
            "shelf_name": "Documentación Empresa"
        }
    }
    print(json.dumps(ejemplo2, indent=2, ensure_ascii=False))
    print()


def verificar_requisitos():
    """Verifica que los requisitos estén instalados"""
    
    print("\n=== Verificando requisitos ===")
    print()
    
    # Verificar Python
    import sys
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Verificar módulos
    modulos_requeridos = ['requests', 'pathlib']
    modulos_opcionales = ['frontmatter']
    
    for modulo in modulos_requeridos:
        try:
            __import__(modulo)
            print(f"✅ {modulo}")
        except ImportError:
            print(f"❌ {modulo} - Instalar con: pip install {modulo}")
    
    for modulo in modulos_opcionales:
        try:
            __import__(modulo)
            print(f"✅ {modulo} (opcional)")
        except ImportError:
            print(f"⚠️  {modulo} (opcional) - Instalar con: pip install python-{modulo}")
    
    print()


def main():
    """Función principal del ejemplo"""
    
    print("🚀 Bienvenido al configurador de Obsidian to BookStack")
    print("Este script te ayudará a configurar y usar la herramienta.")
    print()
    
    while True:
        print("¿Qué quieres hacer?")
        print("1. Crear configuración personalizada")
        print("2. Ver pasos de uso")
        print("3. Ver ejemplos de configuración")
        print("4. Verificar requisitos")
        print("5. Ver opciones avanzadas")
        print("6. Salir")
        print()
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == '1':
            config_path = crear_configuracion_ejemplo()
            print("\n🎯 Próximos pasos recomendados:")
            print(f"1. python obsidian_to_bookstack.py {config_path} --test-connection")
            print(f"2. python obsidian_to_bookstack.py {config_path} --dry-run")
            print(f"3. python obsidian_to_bookstack.py {config_path}")
            
        elif opcion == '2':
            mostrar_pasos_uso()
            
        elif opcion == '3':
            mostrar_ejemplos_configuracion()
            
        elif opcion == '4':
            verificar_requisitos()
            
        elif opcion == '5':
            mostrar_opciones_avanzadas()
            
        elif opcion == '6':
            print("\n¡Hasta luego! 👋")
            break
            
        else:
            print("\n❌ Opción no válida. Por favor, selecciona 1-6.")
        
        print("\n" + "="*60 + "\n")


def mostrar_opciones_avanzadas():
    """Muestra opciones avanzadas de la herramienta"""
    print("\n=== Opciones Avanzadas ===")
    print()
    print("🔧 PRUEBA DE CONEXIÓN DETALLADA:")
    print("   python obsidian_to_bookstack.py config.json --test-connection")
    print("   - Verifica conectividad con BookStack")
    print("   - Prueba permisos de API")
    print("   - Valida configuración antes de transferir")
    print()
    print("🧪 MODO SIMULACIÓN (DRY-RUN):")
    print("   python obsidian_to_bookstack.py config.json --dry-run")
    print("   - Muestra qué se transferirá sin hacer cambios")
    print("   - Detecta imágenes y adjuntos")
    print("   - Reporta archivos no encontrados")
    print("   - Proporciona estadísticas detalladas")
    print()
    print("📊 FUNCIONALIDADES INCLUIDAS:")
    print("   ✅ Transferencia automática de imágenes")
    print("   ✅ Transferencia automática de adjuntos (PDF, DOCX, etc.)")
    print("   ✅ Soporte para sintaxis Obsidian ![[archivo]] y [[archivo]]")
    print("   ✅ Soporte para sintaxis Markdown ![](imagen) y [](archivo)")
    print("   ✅ Resolución automática de rutas relativas y absolutas")
    print("   ✅ Estadísticas detalladas con colores")
    print("   ✅ Reporte de errores completo")

if __name__ == "__main__":
    main()