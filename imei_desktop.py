#!/usr/bin/env python3
"""
IMEI Studio Pro - Aplicación de Escritorio para Windows
======================================================
Herramienta nativa con interfaz gráfica moderna (Dark Mode) para:
1. Verificación de 14 dígitos (cálculo de 15º dígito por Algoritmo de Luhn).
2. Generación con desglose de TAC y FAC por marcas (Samsung, Xiaomi, Apple, etc.).
3. Gestión de modelos y TACs sin programar (editable desde la app o en tac_database.json).
"""

import os
import sys
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta de la base de datos de TACs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "tac_database.json")

# ==============================================================================
# LÓGICA DE NEGOCIO (LUHN MOD 10 Y DATOS)
# ==============================================================================

def calculate_luhn_check_digit(number_14: str) -> int:
    """Calcula el 15º dígito para 14 dígitos usando Luhn (Mod 10)."""
    if len(number_14) != 14 or not number_14.isdigit():
        return -1
    total = 0
    for idx, char in enumerate(number_14):
        digit = int(char)
        if idx % 2 == 1:
            doubled = digit * 2
            total += doubled if doubled < 10 else (doubled - 9)
        else:
            total += digit
    return (10 - (total % 10)) % 10


def validate_full_imei(number_15: str):
    """Retorna (es_valido, digito_esperado)."""
    if len(number_15) != 15 or not number_15.isdigit():
        return False, -1
    expected = calculate_luhn_check_digit(number_15[:14])
    actual = int(number_15[14])
    return (expected == actual), expected


def load_tac_db():
    if not os.path.exists(DB_FILE):
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
        save_tac_db(default_data)
        return default_data

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_tac_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudo guardar tac_database.json:\n{e}")
        return False


# ==============================================================================
# INTERFAZ GRÁFICA DE ESCRITORIO (MODERN DARK THEME)
# ==============================================================================

class ImeiDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GSM-POLAR - Escritorio")
        self.root.geometry("780x680")
        self.root.minsize(700, 600)
        self.root.configure(bg="#0b0f19")

        # Configuración de paleta de colores
        self.c_bg = "#0b0f19"
        self.c_surface = "#131b2e"
        self.c_card = "#1a243b"
        self.c_border = "#2a3754"
        self.c_accent = "#6366f1"
        self.c_accent_hover = "#4f46e5"
        self.c_text = "#f8fafc"
        self.c_muted = "#94a3b8"
        self.c_success = "#10b981"
        self.c_danger = "#f43f5e"

        self.tac_db = load_tac_db()

        self.setup_styles()
        self.create_header()
        self.create_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Notebook (Pestañas)
        style.configure("TNotebook", background=self.c_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background="#1a243b", foreground="#94a3b8",
                        padding=[18, 9], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", self.c_accent), ("active", "#2d3a5a")],
                  foreground=[("selected", "#ffffff"), ("active", "#f8fafc")])

        # Treeview (Tablas)
        style.configure("Treeview",
                        background=self.c_surface,
                        foreground=self.c_text,
                        fieldbackground=self.c_surface,
                        rowheight=28,
                        font=("Segoe UI", 9),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#1e293b",
                        foreground="#cbd5e1",
                        font=("Segoe UI", 9, "bold"),
                        padding=[6, 6],
                        borderwidth=0)
        style.map("Treeview",
                  background=[("selected", self.c_accent)],
                  foreground=[("selected", "#ffffff")])

        # Combobox
        style.configure("TCombobox",
                        fieldbackground=self.c_card,
                        background="#1e293b",
                        foreground=self.c_text,
                        darkcolor=self.c_border,
                        lightcolor=self.c_border)

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.c_surface, height=65, padx=20, pady=12)
        header_frame.pack(fill="x", side="top")

        # Logo / Badge o Avatar con la imagen de C:\Users\Jhose\Documents\videos
        self.header_img = None
        img_paths = [
            os.path.join(BASE_DIR, "videoframe_9214.png"),
            r"C:\Users\Jhose\Documents\videos\videoframe_9214.png",
        ]
        for p in img_paths:
            if os.path.exists(p) and p.endswith(".png"):
                try:
                    full_img = tk.PhotoImage(file=p)
                    self.header_img = full_img.subsample(6, 6)
                    break
                except Exception:
                    pass

        if self.header_img:
            badge = tk.Label(header_frame, image=self.header_img, bg=self.c_surface, relief="flat", bd=0)
            badge.pack(side="left", padx=(0, 12))
        else:
            badge = tk.Label(header_frame, text="GP", bg="#ff1744", fg="#ffffff",
                             font=("Segoe UI", 12, "bold"), width=3, height=1, relief="flat")
            badge.pack(side="left", padx=(0, 12))

        # Título y subtítulo
        title_box = tk.Frame(header_frame, bg=self.c_surface)
        title_box.pack(side="left")

        lbl_title = tk.Label(title_box, text="GSM-POLAR", bg=self.c_surface, fg=self.c_text,
                             font=("Segoe UI", 13, "bold"))
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(title_box, text="trabajando en nuevos procesos lo mejor en garantias polar",
                           bg=self.c_surface, fg=self.c_muted, font=("Segoe UI", 8))
        lbl_sub.pack(anchor="w")

        # Etiqueta de estado
        lbl_status = tk.Label(header_frame, text="● Sistema Listo", bg="#064e3b", fg="#34d399",
                              font=("Segoe UI", 8, "bold"), padx=10, pady=4)
        lbl_status.pack(side="right")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=14)

        # Tab 1: Verificador
        self.tab_verify = tk.Frame(self.notebook, bg=self.c_bg, padx=14, pady=14)
        self.notebook.add(self.tab_verify, text="🔍 Verificador (14 / 15 Dígitos)")
        self.build_verify_tab()

        # Tab 2: Generador
        self.tab_generate = tk.Frame(self.notebook, bg=self.c_bg, padx=14, pady=14)
        self.notebook.add(self.tab_generate, text="⚙️ Generador por Modelos")
        self.build_generate_tab()

        # Tab 3: Gestión de TACs
        self.tab_tacs = tk.Frame(self.notebook, bg=self.c_bg, padx=14, pady=14)
        self.notebook.add(self.tab_tacs, text="📱 Modelos y TACs (Sin Programar)")
        self.build_tacs_tab()

    # ==========================================================================
    # PESTAÑA 1: VERIFICADOR
    # ==========================================================================
    def build_verify_tab(self):
        container = tk.Frame(self.tab_verify, bg=self.c_bg)
        container.pack(fill="both", expand=True)

        # Instrucción
        lbl_info = tk.Label(container,
                            text="Escribe un IMEI de 14 dígitos para calcular automáticamente su 15º dígito de control,\n"
                                 "o escribe un IMEI completo de 15 dígitos para verificar su validez según el algoritmo de Luhn.",
                            bg=self.c_bg, fg=self.c_muted, font=("Segoe UI", 9), justify="left")
        lbl_info.pack(anchor="w", pady=(0, 12))

        # Entrada
        input_frame = tk.Frame(container, bg=self.c_surface, padx=16, pady=14,
                               highlightthickness=1, highlightbackground=self.c_border)
        input_frame.pack(fill="x", pady=(0, 16))

        lbl_entry = tk.Label(input_frame, text="INGRESA EL IMEI (14 O 15 DÍGITOS):", bg=self.c_surface,
                             fg=self.c_muted, font=("Segoe UI", 8, "bold"))
        lbl_entry.pack(anchor="w", pady=(0, 6))

        self.var_verify_input = tk.StringVar(value="35284011123456")
        self.entry_verify = tk.Entry(input_frame, textvariable=self.var_verify_input,
                                     bg=self.c_card, fg="#38bdf8", insertbackground="#38bdf8",
                                     font=("Consolas", 14, "bold"), relief="flat", bd=8)
        self.entry_verify.pack(fill="x")
        self.var_verify_input.trace_add("write", lambda *args: self.on_verify_change())

        # Resultado principal
        self.res_card = tk.Frame(container, bg=self.c_surface, padx=20, pady=16,
                                 highlightthickness=1, highlightbackground=self.c_border)
        self.res_card.pack(fill="x", pady=(0, 14))

        self.lbl_verify_status = tk.Label(self.res_card, text="ESTADO", bg=self.c_surface,
                                          fg=self.c_success, font=("Segoe UI", 10, "bold"))
        self.lbl_verify_status.pack(anchor="w")

        # Visor del número con destaque del dígito de control
        display_frame = tk.Frame(self.res_card, bg="#080c14", pady=10, padx=12)
        display_frame.pack(fill="x", pady=10)

        self.lbl_main_number = tk.Label(display_frame, text="", bg="#080c14", fg="#38bdf8",
                                        font=("Consolas", 18, "bold"))
        self.lbl_main_number.pack(side="left")

        self.lbl_cd_number = tk.Label(display_frame, text="", bg="#080c14", fg=self.c_danger,
                                      font=("Consolas", 18, "bold"))
        self.lbl_cd_number.pack(side="left")

        btn_copy = tk.Button(display_frame, text="📋 Copiar", bg=self.c_card, fg=self.c_text,
                             activebackground=self.c_accent, activeforeground="#ffffff",
                             font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4, cursor="hand2",
                             command=self.copy_verified_number)
        btn_copy.pack(side="right")

        # Desglose de campos (Grid)
        grid_frame = tk.Frame(self.res_card, bg=self.c_surface)
        grid_frame.pack(fill="x", pady=(6, 0))

        # Columna 1: TAC 8d
        self.card_tac8 = self.make_stat_box(grid_frame, "TAC (8 DÍGITOS GSMA)", "--", 0, 0)
        # Columna 2: TAC 6d + FAC 2d
        self.card_tacfac = self.make_stat_box(grid_frame, "TAC (6d) + FAC (2d)", "--", 0, 1)
        # Columna 3: SNR 6d
        self.card_snr = self.make_stat_box(grid_frame, "SNR (SERIE - 6d)", "--", 1, 0)
        # Columna 4: Check Digit
        self.card_cd = self.make_stat_box(grid_frame, "DÍGITO DE CONTROL", "--", 1, 1)

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Trigger inicial
        self.on_verify_change()

    def make_stat_box(self, parent, label_text, default_val, row, col):
        box = tk.Frame(parent, bg=self.c_card, padx=12, pady=8, highlightthickness=1, highlightbackground=self.c_border)
        box.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        lbl = tk.Label(box, text=label_text, bg=self.c_card, fg=self.c_muted, font=("Segoe UI", 7, "bold"))
        lbl.pack(anchor="w")

        val = tk.Label(box, text=default_val, bg=self.c_card, fg=self.c_text, font=("Consolas", 11, "bold"))
        val.pack(anchor="w", pady=(2, 0))
        return val

    def on_verify_change(self):
        raw = self.var_verify_input.get().strip().replace(" ", "").replace("-", "")
        if not raw.isdigit():
            self.lbl_verify_status.config(text="⚠️ Ingrese solo dígitos numéricos", fg=self.c_muted)
            self.lbl_main_number.config(text=raw)
            self.lbl_cd_number.config(text="")
            return

        if len(raw) == 14:
            cd = calculate_luhn_check_digit(raw)
            self.lbl_verify_status.config(
                text=f"✓ 14 DÍGITOS VÁLIDOS — DÍGITO 15º CALCULADO (LUHN): {cd}",
                fg=self.c_success
            )
            self.lbl_main_number.config(text=raw)
            self.lbl_cd_number.config(text=str(cd), fg=self.c_danger)

            self.card_tac8.config(text=raw[:8])
            self.card_tacfac.config(text=f"{raw[:6]} (TAC) + {raw[6:8]} (FAC)")
            self.card_snr.config(text=raw[8:14])
            self.card_cd.config(text=str(cd))

        elif len(raw) == 15:
            is_valid, expected_cd = validate_full_imei(raw)
            actual_cd = int(raw[14])
            if is_valid:
                self.lbl_verify_status.config(
                    text=f"✓ IMEI VÁLIDO (15 DÍGITOS) — Dígito de control ({actual_cd}) correcto",
                    fg=self.c_success
                )
                self.lbl_cd_number.config(text=str(actual_cd), fg=self.c_success)
            else:
                self.lbl_verify_status.config(
                    text=f"✗ IMEI INVÁLIDO — Dígito actual: {actual_cd} (Esperado según Luhn: {expected_cd})",
                    fg=self.c_danger
                )
                self.lbl_cd_number.config(text=str(actual_cd), fg=self.c_danger)

            self.lbl_main_number.config(text=raw[:14])
            self.card_tac8.config(text=raw[:8])
            self.card_tacfac.config(text=f"{raw[:6]} (TAC) + {raw[6:8]} (FAC)")
            self.card_snr.config(text=raw[8:14])
            self.card_cd.config(text=f"{actual_cd} (Esperado: {expected_cd})")

        else:
            self.lbl_verify_status.config(
                text=f"Longitud actual: {len(raw)} dígitos (se requieren 14 o 15)",
                fg=self.c_muted
            )
            self.lbl_main_number.config(text=raw)
            self.lbl_cd_number.config(text="")

    def copy_verified_number(self):
        raw = self.var_verify_input.get().strip().replace(" ", "")
        if len(raw) == 14 and raw.isdigit():
            cd = calculate_luhn_check_digit(raw)
            to_copy = raw + str(cd)
        elif len(raw) == 15 and raw.isdigit():
            to_copy = raw
        else:
            to_copy = raw

        if to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(to_copy)
            messagebox.showinfo("Copiado", f"IMEI copiado al portapapeles:\n{to_copy}")

    # ==========================================================================
    # PESTAÑA 2: GENERADOR
    # ==========================================================================
    def build_generate_tab(self):
        container = tk.Frame(self.tab_generate, bg=self.c_bg)
        container.pack(fill="both", expand=True)

        # Controles superiores
        ctrl_frame = tk.Frame(container, bg=self.c_surface, padx=16, pady=14,
                              highlightthickness=1, highlightbackground=self.c_border)
        ctrl_frame.pack(fill="x", pady=(0, 14))

        # Selector de Marca
        tk.Label(ctrl_frame, text="MARCA:", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=2)
        self.combo_brand = ttk.Combobox(ctrl_frame, state="readonly", width=18, font=("Segoe UI", 9))
        self.combo_brand.grid(row=1, column=0, padx=6, pady=(0, 8))
        self.combo_brand.bind("<<ComboboxSelected>>", self.on_gen_brand_change)

        # Selector de Modelo
        tk.Label(ctrl_frame, text="MODELO:", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).grid(row=0, column=1, sticky="w", padx=6, pady=2)
        self.combo_model = ttk.Combobox(ctrl_frame, state="readonly", width=26, font=("Segoe UI", 9))
        self.combo_model.grid(row=1, column=1, padx=6, pady=(0, 8))
        self.combo_model.bind("<<ComboboxSelected>>", self.on_gen_model_change)

        # Cantidad
        tk.Label(ctrl_frame, text="CANTIDAD:", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).grid(row=0, column=2, sticky="w", padx=6, pady=2)
        self.combo_qty = ttk.Combobox(ctrl_frame, state="readonly", width=8, values=["1", "3", "5", "10"], font=("Segoe UI", 9))
        self.combo_qty.set("3")
        self.combo_qty.grid(row=1, column=2, padx=6, pady=(0, 8))

        # TAC Preview
        self.lbl_gen_tac_preview = tk.Label(ctrl_frame, text="TAC: --", bg=self.c_surface, fg="#38bdf8",
                                            font=("Consolas", 10, "bold"))
        self.lbl_gen_tac_preview.grid(row=2, column=0, columnspan=2, sticky="w", padx=6, pady=(4, 0))

        # Botón Generar
        btn_gen = tk.Button(ctrl_frame, text="⚡ GENERAR CON LUHN", bg=self.c_accent, fg="#ffffff",
                            activebackground=self.c_accent_hover, activeforeground="#ffffff",
                            font=("Segoe UI", 10, "bold"), relief="flat", padx=16, pady=6, cursor="hand2",
                            command=self.execute_generate)
        btn_gen.grid(row=2, column=2, sticky="e", padx=6, pady=(4, 0))

        # Tabla de Resultados
        table_frame = tk.Frame(container, bg=self.c_surface, highlightthickness=1, highlightbackground=self.c_border)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        cols = ("imei", "tac8", "tac6", "fac2", "snr", "cd")
        self.tree_gen = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_gen.heading("imei", text="IMEI Completo (15 d.)")
        self.tree_gen.heading("tac8", text="TAC (8d)")
        self.tree_gen.heading("tac6", text="TAC (6d)")
        self.tree_gen.heading("fac2", text="FAC (2d)")
        self.tree_gen.heading("snr", text="SNR (6d)")
        self.tree_gen.heading("cd", text="Check Digit")

        self.tree_gen.column("imei", width=190, anchor="center")
        self.tree_gen.column("tac8", width=95, anchor="center")
        self.tree_gen.column("tac6", width=85, anchor="center")
        self.tree_gen.column("fac2", width=75, anchor="center")
        self.tree_gen.column("snr", width=95, anchor="center")
        self.tree_gen.column("cd", width=85, anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_gen.yview)
        self.tree_gen.configure(yscrollcommand=scroll.set)

        self.tree_gen.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Botones de acción inferiores
        btn_box = tk.Frame(container, bg=self.c_bg)
        btn_box.pack(fill="x")

        tk.Button(btn_box, text="📋 Copiar Seleccionado", bg=self.c_surface, fg=self.c_text,
                  activebackground=self.c_card, font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.copy_selected_generated).pack(side="left", padx=(0, 8))

        tk.Button(btn_box, text="📑 Copiar Todos", bg=self.c_surface, fg=self.c_text,
                  activebackground=self.c_card, font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.copy_all_generated).pack(side="left")

        tk.Button(btn_box, text="🗑️ Limpiar Lista", bg=self.c_surface, fg=self.c_muted,
                  activebackground=self.c_card, font=("Segoe UI", 9), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=lambda: self.tree_gen.delete(*self.tree_gen.get_children())).pack(side="right")

        self.refresh_generator_combos()

    def refresh_generator_combos(self):
        brands = list(self.tac_db.keys())
        self.combo_brand["values"] = brands
        if brands:
            self.combo_brand.set(brands[0])
            self.on_gen_brand_change()

    def on_gen_brand_change(self, event=None):
        brand = self.combo_brand.get()
        models = [m.get("model", "") for m in self.tac_db.get(brand, [])]
        self.combo_model["values"] = models
        if models:
            self.combo_model.set(models[0])
            self.on_gen_model_change()

    def on_gen_model_change(self, event=None):
        brand = self.combo_brand.get()
        idx = self.combo_model.current()
        models = self.tac_db.get(brand, [])
        if 0 <= idx < len(models):
            item = models[idx]
            tac = item.get("tac", item.get("tac_6", "") + item.get("fac_2", ""))
            tac6 = item.get("tac_6", tac[:6])
            fac2 = item.get("fac_2", tac[6:8])
            self.lbl_gen_tac_preview.config(text=f"TAC (8d): {tac}  |  TAC(6d): {tac6}  FAC(2d): {fac2}")

    def execute_generate(self):
        brand = self.combo_brand.get()
        idx = self.combo_model.current()
        models = self.tac_db.get(brand, [])
        if not (0 <= idx < len(models)):
            messagebox.showwarning("Atención", "Selecciona una marca y modelo válidos.")
            return

        item = models[idx]
        tac8 = item.get("tac", item.get("tac_6", "") + item.get("fac_2", ""))
        if len(tac8) != 8 or not tac8.isdigit():
            messagebox.showerror("Error", "El TAC de este modelo no tiene 8 dígitos válidos.")
            return

        qty = int(self.combo_qty.get() or "1")

        for _ in range(qty):
            snr = f"{random.randint(0, 999999):06d}"
            body14 = tac8 + snr
            cd = calculate_luhn_check_digit(body14)
            full_imei = body14 + str(cd)

            tac6 = tac8[:6]
            fac2 = tac8[6:8]

            self.tree_gen.insert("", 0, values=(full_imei, tac8, tac6, fac2, snr, cd))

    def copy_selected_generated(self):
        selected = self.tree_gen.selection()
        if not selected:
            messagebox.showinfo("Copiar", "Selecciona una fila de la lista para copiar.")
            return
        val = self.tree_gen.item(selected[0], "values")[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(val)
        messagebox.showinfo("Copiado", f"IMEI copiado:\n{val}")

    def copy_all_generated(self):
        children = self.tree_gen.get_children()
        if not children:
            messagebox.showinfo("Copiar", "No hay elementos en la lista.")
            return
        lines = [self.tree_gen.item(c, "values")[0] for c in children]
        text = "\n".join(lines)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copiado", f"Se copiaron {len(lines)} IMEIs al portapapeles.")

    # ==========================================================================
    # PESTAÑA 3: GESTIÓN DE MODELOS Y TACS (SIN PROGRAMAR)
    # ==========================================================================
    def build_tacs_tab(self):
        container = tk.Frame(self.tab_tacs, bg=self.c_bg)
        container.pack(fill="both", expand=True)

        lbl_desc = tk.Label(container,
                            text="Administra las marcas y códigos TAC/FAC. Puedes agregar o borrar modelos aquí mismo,\n"
                                 "o editar directamente el archivo 'tac_database.json' en el Bloc de Notas sin tocar código.",
                            bg=self.c_bg, fg=self.c_muted, font=("Segoe UI", 9), justify="left")
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Botones de barra superior
        bar = tk.Frame(container, bg=self.c_bg)
        bar.pack(fill="x", pady=(0, 10))

        tk.Button(bar, text="➕ Agregar Modelo", bg=self.c_accent, fg="#ffffff",
                  activebackground=self.c_accent_hover, font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.open_add_model_dialog).pack(side="left", padx=(0, 8))

        tk.Button(bar, text="🗑️ Eliminar Seleccionado", bg=self.c_surface, fg=self.c_danger,
                  activebackground=self.c_card, font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.delete_selected_model).pack(side="left", padx=(0, 8))

        tk.Button(bar, text="📂 Abrir en Bloc de Notas", bg=self.c_surface, fg=self.c_text,
                  activebackground=self.c_card, font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.open_in_notepad).pack(side="left", padx=(0, 8))

        tk.Button(bar, text="🔄 Recargar", bg=self.c_surface, fg=self.c_muted,
                  activebackground=self.c_card, font=("Segoe UI", 9), relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.reload_tac_database).pack(side="right")

        # Tabla de modelos
        table_frame = tk.Frame(container, bg=self.c_surface, highlightthickness=1, highlightbackground=self.c_border)
        table_frame.pack(fill="both", expand=True)

        cols = ("brand", "model", "tac8", "tac6", "fac2")
        self.tree_models = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_models.heading("brand", text="Marca")
        self.tree_models.heading("model", text="Modelo")
        self.tree_models.heading("tac8", text="TAC (8 Dígitos)")
        self.tree_models.heading("tac6", text="TAC (6d)")
        self.tree_models.heading("fac2", text="FAC (2d)")

        self.tree_models.column("brand", width=120, anchor="w")
        self.tree_models.column("model", width=220, anchor="w")
        self.tree_models.column("tac8", width=120, anchor="center")
        self.tree_models.column("tac6", width=100, anchor="center")
        self.tree_models.column("fac2", width=90, anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_models.yview)
        self.tree_models.configure(yscrollcommand=scroll.set)

        self.tree_models.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.populate_models_tree()

    def populate_models_tree(self):
        self.tree_models.delete(*self.tree_models.get_children())
        for brand, models in self.tac_db.items():
            for m in models:
                tac8 = m.get("tac", m.get("tac_6", "") + m.get("fac_2", ""))
                tac6 = m.get("tac_6", tac8[:6])
                fac2 = m.get("fac_2", tac8[6:8])
                self.tree_models.insert("", "end", values=(brand, m.get("model", ""), tac8, tac6, fac2))

    def open_add_model_dialog(self):
        diag = tk.Toplevel(self.root)
        diag.title("Agregar Nuevo Modelo / TAC")
        diag.geometry("380x360")
        diag.resizable(False, False)
        diag.configure(bg=self.c_surface)
        diag.transient(self.root)
        diag.grab_set()

        pad_f = tk.Frame(diag, bg=self.c_surface, padx=20, pady=18)
        pad_f.pack(fill="both", expand=True)

        tk.Label(pad_f, text="NUEVO MODELO Y TAC", bg=self.c_surface, fg=self.c_text,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 12))

        # Marca
        tk.Label(pad_f, text="Marca (ej: Samsung, Xiaomi, Apple):", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        e_brand = tk.Entry(pad_f, bg=self.c_card, fg=self.c_text, font=("Segoe UI", 10), bd=5, relief="flat")
        e_brand.pack(fill="x", pady=(2, 10))

        # Modelo
        tk.Label(pad_f, text="Nombre del Modelo (ej: Galaxy S24 Ultra):", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        e_model = tk.Entry(pad_f, bg=self.c_card, fg=self.c_text, font=("Segoe UI", 10), bd=5, relief="flat")
        e_model.pack(fill="x", pady=(2, 10))

        # TAC
        tk.Label(pad_f, text="TAC (8 dígitos numéricos o TAC 6d + FAC 2d):", bg=self.c_surface, fg=self.c_muted,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        e_tac = tk.Entry(pad_f, bg=self.c_card, fg="#38bdf8", font=("Consolas", 11, "bold"), bd=5, relief="flat")
        e_tac.pack(fill="x", pady=(2, 16))

        def save_action():
            brand = e_brand.get().strip()
            model = e_model.get().strip()
            tac = e_tac.get().strip().replace(" ", "")

            if not brand or not model or len(tac) != 8 or not tac.isdigit():
                messagebox.showerror("Campos Inválidos", "Completa la marca, el modelo y un TAC numérico de exactamente 8 dígitos.")
                return

            if brand not in self.tac_db:
                self.tac_db[brand] = []

            self.tac_db[brand].append({
                "model": model,
                "tac": tac,
                "tac_6": tac[:6],
                "fac_2": tac[6:8]
            })

            save_tac_db(self.tac_db)
            self.populate_models_tree()
            self.refresh_generator_combos()
            diag.destroy()
            messagebox.showinfo("Éxito", f"Modelo '{model}' agregado correctamente.")

        btn_save = tk.Button(pad_f, text="Guardar Modelo", bg=self.c_accent, fg="#ffffff",
                             font=("Segoe UI", 10, "bold"), relief="flat", pady=6, cursor="hand2", command=save_action)
        btn_save.pack(fill="x")

    def delete_selected_model(self):
        sel = self.tree_models.selection()
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona un modelo de la lista para eliminar.")
            return

        values = self.tree_models.item(sel[0], "values")
        brand = values[0]
        model_name = values[1]

        if messagebox.askyesno("Confirmar", f"¿Deseas eliminar el modelo '{model_name}' de la marca '{brand}'?"):
            if brand in self.tac_db:
                self.tac_db[brand] = [m for m in self.tac_db[brand] if m.get("model") != model_name]
                if not self.tac_db[brand]:
                    del self.tac_db[brand]
                save_tac_db(self.tac_db)
                self.populate_models_tree()
                self.refresh_generator_combos()

    def open_in_notepad(self):
        try:
            os.startfile(DB_FILE)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def reload_tac_database(self):
        self.tac_db = load_tac_db()
        self.populate_models_tree()
        self.refresh_generator_combos()
        messagebox.showinfo("Recargado", "La base de datos de modelos y TACs fue recargada.")


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================
def main():
    root = tk.Tk()
    app = ImeiDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
