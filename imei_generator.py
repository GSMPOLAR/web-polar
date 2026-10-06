#!/usr/bin/env python3
"""
Herramienta de Verificación y Generación de Estructura IMEI (Algoritmo de Luhn)
--------------------------------------------------------------------------------
Este script implementa el estándar 3GPP / GSMA para la validación y cálculo
del dígito de control de identificadores IMEI (15 dígitos) utilizando el
algoritmo de Luhn (Módulo 10).

Los códigos TAC/FAC se cargan desde 'tac_database.json' para permitir modificaciones
fáciles sin necesidad de editar el código fuente.
"""

import os
import sys
import json
import random
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_FILENAME = "tac_database.json"


# ==============================================================================
# ALGORITMO DE LUHN (CÁLCULO Y VALIDACIÓN DE DÍGITO VERIFICADOR)
# ==============================================================================

def calculate_luhn_check_digit(number_14: str) -> int:
    """
    Calcula el 15º dígito (dígito de control) para una cadena de 14 dígitos numéricos
    utilizando el algoritmo de Luhn (Mod 10).
    """
    if len(number_14) != 14 or not number_14.isdigit():
        raise ValueError("Se requieren exactamente 14 dígitos numéricos.")

    total_sum = 0
    for idx, char in enumerate(number_14):
        digit = int(char)
        # Las posiciones impares en índice base 1 (índices 1, 3, 5, 7, 9, 11, 13 base 0)
        # se multiplican por 2
        if idx % 2 == 1:
            doubled = digit * 2
            total_sum += doubled if doubled < 10 else (doubled - 9)
        else:
            total_sum += digit

    check_digit = (10 - (total_sum % 10)) % 10
    return check_digit


def validate_full_imei(imei_15: str) -> Tuple[bool, str]:
    """
    Verifica si un IMEI de 15 dígitos cumple con el algoritmo de Luhn.
    Retorna (es_valido, mensaje_descriptivo).
    """
    clean_imei = "".join(imei_15.split())
    if len(clean_imei) != 15 or not clean_imei.isdigit():
        return False, "El IMEI debe contener exactamente 15 dígitos numéricos."

    body_14 = clean_imei[:14]
    expected_check_digit = calculate_luhn_check_digit(body_14)
    actual_check_digit = int(clean_imei[14])

    if expected_check_digit == actual_check_digit:
        return True, f"IMEI válido. El dígito de verificación ({actual_check_digit}) coincide."
    else:
        return False, f"IMEI inválido. El dígito actual es {actual_check_digit}, pero según Luhn debe ser {expected_check_digit}."


def decompose_imei(imei_str: str) -> Dict[str, str]:
    """
    Desglosa un IMEI (14 o 15 dígitos) en sus componentes según la norma histórica y moderna:
    - TAC Moderno (8 dígitos): Type Allocation Code asignado por GSMA
    - TAC Clásico (6 dígitos) + FAC (2 dígitos): Final Assembly Code (anterior a 2004)
    - SNR (6 dígitos): Serial Number
    - CD (1 dígito): Check Digit (Luhn)
    """
    clean = "".join(imei_str.split())
    if len(clean) < 14:
        raise ValueError("El número debe tener al menos 14 dígitos.")

    tac_full = clean[:8]
    tac_classic = clean[:6]
    fac_classic = clean[6:8]
    snr = clean[8:14]
    cd = str(calculate_luhn_check_digit(clean[:14]))

    provided_cd = clean[14] if len(clean) >= 15 else None

    return {
        "tac_full": tac_full,
        "tac_classic": tac_classic,
        "fac_classic": fac_classic,
        "snr": snr,
        "calculated_cd": cd,
        "provided_cd": provided_cd,
        "full_imei_15": clean[:14] + cd
    }


# ==============================================================================
# GESTIÓN DE BASE DE DATOS DE TACS (SIN PROGRAMAR)
# ==============================================================================

def get_db_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DB_FILENAME)


def load_tac_database() -> Dict[str, List[Dict[str, str]]]:
    """Carga los modelos y TACs desde el archivo JSON editable."""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        default_data = {
            "Samsung": [
                {"model": "Galaxy S23 Ultra", "tac": "35284011", "tac_6": "352840", "fac_2": "11"},
                {"model": "Galaxy S22", "tac": "35165438", "tac_6": "351654", "fac_2": "38"},
                {"model": "Galaxy A54 5G", "tac": "35912448", "tac_6": "359124", "fac_2": "48"}
            ],
            "Xiaomi": [
                {"model": "Redmi Note 12", "tac": "86420106", "tac_6": "864201", "fac_2": "06"},
                {"model": "Xiaomi 13 Pro", "tac": "86940205", "tac_6": "869402", "fac_2": "05"},
                {"model": "POCO X5 Pro", "tac": "86311006", "tac_6": "863110", "fac_2": "06"}
            ],
            "Apple": [
                {"model": "iPhone 14 Pro", "tac": "35384139", "tac_6": "353841", "fac_2": "39"},
                {"model": "iPhone 13", "tac": "35613867", "tac_6": "356138", "fac_2": "67"},
                {"model": "iPhone 12", "tac": "35304611", "tac_6": "353046", "fac_2": "11"}
            ],
            "Motorola": [
                {"model": "Moto G84", "tac": "35741029", "tac_6": "357410", "fac_2": "29"},
                {"model": "Edge 40 Neo", "tac": "35890214", "tac_6": "358902", "fac_2": "14"}
            ]
        }
        save_tac_database(default_data)
        return default_data

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al leer '{DB_FILENAME}': {e}. Usando base vacía.")
        return {}


def save_tac_database(data: Dict[str, List[Dict[str, str]]]) -> bool:
    """Guarda las modificaciones en el archivo JSON."""
    db_path = get_db_path()
    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar base de datos: {e}")
        return False


# ==============================================================================
# GENERADOR DE EJEMPLOS DE PRUEBA
# ==============================================================================

def generate_random_imei(tac_8: str, custom_snr: Optional[str] = None) -> Dict[str, str]:
    """Genera un IMEI válido de 15 dígitos a partir de un TAC de 8 dígitos."""
    if len(tac_8) != 8 or not tac_8.isdigit():
        raise ValueError("El TAC debe tener exactamente 8 dígitos numéricos.")

    if custom_snr:
        if len(custom_snr) != 6 or not custom_snr.isdigit():
            raise ValueError("El SNR debe tener 6 dígitos numéricos.")
        snr = custom_snr
    else:
        snr = f"{random.randint(0, 999999):06d}"

    body_14 = tac_8 + snr
    cd = calculate_luhn_check_digit(body_14)
    full_imei = body_14 + str(cd)

    return {
        "imei": full_imei,
        "tac": tac_8,
        "tac_6": tac_8[:6],
        "fac_2": tac_8[6:8],
        "snr": snr,
        "check_digit": str(cd)
    }


# ==============================================================================
# INTERFAZ INTERACTIVA DE CONSOLA
# ==============================================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 65)
    print("      HERRAMIENTA EDUCATIVA Y DE VERIFICACIÓN DE IMEI")
    print("           (Estándar 3GPP / Algoritmo de Luhn Mod-10)")
    print("=" * 65)


def menu_verificar():
    print("\n--- [1] VERIFICADOR DE IMEI (14 o 15 dígitos) ---")
    imei_input = input("Ingrese el número a verificar (14 o 15 dígitos): ").strip()
    clean = "".join(imei_input.split())

    if len(clean) == 14 and clean.isdigit():
        cd = calculate_luhn_check_digit(clean)
        full = clean + str(cd)
        dec = decompose_imei(clean)
        print("\nResultado:")
        print(f"  • Entrada de 14 dígitos : {clean}")
        print(f"  • 15º Dígito calculado  : {cd} (Algoritmo de Luhn)")
        print(f"  • IMEI completo (15 d.) : {full}")
        print("\nDesglose de campos:")
        print(f"  - TAC (8 dígitos)       : {dec['tac_full']}")
        print(f"    ├─ TAC clásico (6 d.) : {dec['tac_classic']}")
        print(f"    └─ FAC clásico (2 d.) : {dec['fac_classic']}")
        print(f"  - SNR (Serie, 6 d.)     : {dec['snr']}")
        print(f"  - Check Digit (1 d.)    : {cd}")

    elif len(clean) == 15 and clean.isdigit():
        is_valid, msg = validate_full_imei(clean)
        dec = decompose_imei(clean)
        status = "VÁLIDO [OK]" if is_valid else "INVÁLIDO [FALLO]"
        print(f"\nEstado: {status}")
        print(f"Detalle: {msg}")
        print("\nDesglose:")
        print(f"  - TAC (8 dígitos)       : {dec['tac_full']}")
        print(f"    ├─ TAC clásico (6 d.) : {dec['tac_classic']}")
        print(f"    └─ FAC clásico (2 d.) : {dec['fac_classic']}")
        print(f"  - SNR (Serie, 6 d.)     : {dec['snr']}")
        print(f"  - Dígito proporcionado  : {clean[14]}")
        print(f"  - Dígito esperado (Luhn): {dec['calculated_cd']}")
    else:
        print("\nError: Debe ingresar exactamente 14 o 15 dígitos numéricos.")


def menu_generar():
    db = load_tac_database()
    brands = list(db.keys())

    print("\n--- [2] GENERADOR CON TAC Y FAC ---")
    if not brands:
        print("No hay marcas configuradas en la base de datos.")
        return

    print("Marcas disponibles:")
    for idx, brand in enumerate(brands, 1):
        print(f"  {idx}. {brand}")
    print(f"  {len(brands) + 1}. [Ingresar TAC / FAC manualmente]")

    try:
        choice = int(input("\nSeleccione una opción: ").strip())
    except ValueError:
        print("Opción inválida.")
        return

    selected_tac = ""
    model_name = ""

    if 1 <= choice <= len(brands):
        brand_name = brands[choice - 1]
        models = db[brand_name]
        print(f"\nModelos de {brand_name}:")
        for m_idx, m in enumerate(models, 1):
            tac_info = m.get("tac", m.get("tac_6", "") + m.get("fac_2", ""))
            fac_info = m.get("fac_2", tac_info[6:8] if len(tac_info) >= 8 else "--")
            print(f"  {m_idx}. {m.get('model', 'Sin nombre')} (TAC: {tac_info} | TAC 6d: {tac_info[:6]}, FAC: {fac_info})")

        try:
            m_choice = int(input("\nSeleccione el modelo: ").strip())
            if 1 <= m_choice <= len(models):
                selected = models[m_choice - 1]
                model_name = f"{brand_name} - {selected.get('model')}"
                selected_tac = selected.get("tac", selected.get("tac_6", "") + selected.get("fac_2", ""))
            else:
                print("Modelo inválido.")
                return
        except ValueError:
            print("Entrada inválida.")
            return

    elif choice == len(brands) + 1:
        print("\nFormato: puede ingresar el TAC directo de 8 dígitos, o TAC de 6 + FAC de 2.")
        modo = input("¿Desea ingresar TAC(6) + FAC(2)? (s/n, defecto: no): ").strip().lower()
        if modo == "s":
            t6 = input("Ingrese TAC (6 dígitos): ").strip()
            f2 = input("Ingrese FAC (2 dígitos): ").strip()
            if len(t6) == 6 and len(f2) == 2 and t6.isdigit() and f2.isdigit():
                selected_tac = t6 + f2
                model_name = "Personalizado (TAC 6 + FAC 2)"
            else:
                print("Error: TAC debe ser de 6 dígitos y FAC de 2 dígitos.")
                return
        else:
            t8 = input("Ingrese TAC de 8 dígitos: ").strip()
            if len(t8) == 8 and t8.isdigit():
                selected_tac = t8
                model_name = "Personalizado (TAC 8)"
            else:
                print("Error: El TAC debe tener exactamente 8 dígitos.")
                return
    else:
        print("Opción no válida.")
        return

    try:
        qty_str = input("¿Cuántos ejemplos desea generar? (1 a 10, defecto 1): ").strip()
        qty = int(qty_str) if qty_str else 1
        qty = max(1, min(qty, 20))
    except ValueError:
        qty = 1

    print(f"\nGenerando {qty} IMEI(s) para: {model_name} (TAC: {selected_tac})")
    print("-" * 65)
    for i in range(qty):
        res = generate_random_imei(selected_tac)
        print(f"[{i + 1}] IMEI: {res['imei']}")
        print(f"    Desglose -> TAC(6): {res['tac_6']} | FAC(2): {res['fac_2']} | SNR: {res['snr']} | CheckDigit: {res['check_digit']}")
    print("-" * 65)


def menu_gestionar_tacs():
    db = load_tac_database()
    db_path = get_db_path()

    print("\n--- [3] GESTIÓN DE TACs Y MODELOS (SIN PROGRAMAR) ---")
    print(f"Ubicación del archivo de configuración editable:")
    print(f"-> {db_path}\n")
    print("Opciones:")
    print("  1. Ver todos los modelos y TACs registrados")
    print("  2. Agregar un nuevo modelo / TAC desde aquí")
    print("  3. Cómo editar 'tac_database.json' directamente en Bloc de Notas")

    opc = input("\nSeleccione una opción: ").strip()

    if opc == "1":
        for brand, models in db.items():
            print(f"\n[{brand}]")
            for m in models:
                tac = m.get("tac", m.get("tac_6", "") + m.get("fac_2", ""))
                fac = m.get("fac_2", tac[6:8] if len(tac) >= 8 else "--")
                print(f"  • {m.get('model')}: TAC={tac} (TAC 6d: {tac[:6]}, FAC: {fac})")

    elif opc == "2":
        brand = input("Marca (ej: Samsung, Xiaomi, Apple): ").strip()
        model = input("Modelo (ej: Galaxy S24, Redmi Note 13): ").strip()
        print("¿Desea ingresar TAC(6) + FAC(2) o TAC completo de 8 dígitos?")
        tipo = input("Escriba '1' para TAC(8) o '2' para TAC(6) + FAC(2): ").strip()

        if tipo == "2":
            t6 = input("TAC (6 dígitos): ").strip()
            f2 = input("FAC (2 dígitos): ").strip()
            if len(t6) != 6 or len(f2) != 2 or not t6.isdigit() or not f2.isdigit():
                print("Error: formato inválido.")
                return
            t8 = t6 + f2
        else:
            t8 = input("TAC (8 dígitos): ").strip()
            if len(t8) != 8 or not t8.isdigit():
                print("Error: debe ser de 8 dígitos numéricos.")
                return
            t6 = t8[:6]
            f2 = t8[6:8]

        if brand not in db:
            db[brand] = []

        db[brand].append({
            "model": model,
            "tac": t8,
            "tac_6": t6,
            "fac_2": f2
        })

        if save_tac_database(db):
            print(f"\n¡Modelo '{model}' guardado exitosamente en '{DB_FILENAME}'!")

    elif opc == "3":
        print("\nPara modificar los TACs sin programar:")
        print(f"1. Abra el archivo '{DB_FILENAME}' con cualquier editor de texto (Bloc de Notas, VS Code).")
        print("2. Cada elemento tiene el formato:")
        print('   {\n     "model": "Nombre del Teléfono",\n     "tac": "8 DÍGITOS",\n     "tac_6": "6 DÍGITOS",\n     "fac_2": "2 DÍGITOS"\n   }')
        print("3. Guarde el archivo y este programa cargará los cambios automáticamente.")


def main():
    while True:
        print_header()
        print("\nSeleccione una opción:")
        print("  1. Verificador de IMEI (Calcula dígito 15 para 14 dígitos o valida 15 dígitos)")
        print("  2. Generador de IMEI con marcas (TAC y FAC)")
        print("  3. Gestionar o ver lista de TACs y modelos (tac_database.json)")
        print("  4. Explicación técnica y aviso legal")
        print("  5. Salir")

        opt = input("\nOpción [1-5]: ").strip()

        if opt == "1":
            menu_verificar()
        elif opt == "2":
            menu_generar()
        elif opt == "3":
            menu_gestionar_tacs()
        elif opt == "4":
            print("\n" + "=" * 65)
            print("INFORMACIÓN TÉCNICA Y MARCO REGULATORIO:")
            print("=" * 65)
            print("1. ¿Qué es el TAC y FAC?")
            print("   - Históricamente (GSM pre-2004), los primeros 8 dígitos del IMEI se")
            print("     dividían en TAC (6 dígitos) y FAC (Final Assembly Code, 2 dígitos).")
            print("   - Desde 2004, 3GPP/GSMA unificó ambos en un TAC de 8 dígitos.")
            print("2. Algoritmo de Luhn (Módulo 10):")
            print("   - El dígito 15 es una suma de verificación que valida la integridad")
            print("     contra errores de tecleo al transferir el número.")
            print("3. Advertencia Legal:")
            print("   - Modificar, clonar o sustituir el IMEI en dispositivos móviles físicos")
            print("     para evadir bloqueos de operadora o listas negras (Blacklist) es un")
            print("     delito tipificado en numerosos países (fraude de telecomunicaciones).")
            print("   - Este software está destinado exclusivamente a fines académicos,")
            print("     pruebas de software, validación de formularios y testing de QA.")
            print("=" * 65)
        elif opt == "5":
            print("\nHasta pronto.")
            sys.exit(0)
        else:
            print("\nOpción no válida.")

        input("\nPresione [Enter] para continuar...")
        clear_screen()


if __name__ == "__main__":
    # Soporte para argumentos de línea de comandos directos
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg in ("--help", "-h"):
            print("Uso:")
            print("  python imei_generator.py                   (Inicia el menú interactivo)")
            print("  python imei_generator.py <14_o_15_digitos> (Verifica o calcula check digit)")
        elif len(arg) == 14 and arg.isdigit():
            cd = calculate_luhn_check_digit(arg)
            print(f"Entrada: {arg} -> Dígito verificador: {cd} -> IMEI completo: {arg}{cd}")
        elif len(arg) == 15 and arg.isdigit():
            val, msg = validate_full_imei(arg)
            print(f"IMEI {arg}: {'VÁLIDO' if val else 'INVÁLIDO'} ({msg})")
        else:
            print(f"Argumento no reconocido: {arg}. Ejecute sin argumentos para ver el menú.")
    else:
        main()
