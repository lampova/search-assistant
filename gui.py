import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from main import PriceManager
from tkinter import ttk


COLORS = {
    'primary': '#2C3E50',      # Темно-синий
    'secondary': '#3498DB',    # Голубой
    'accent': '#E74C3C',       # Красный
    'success': '#27AE60',      # Зеленый
    'warning': '#F39C12',      # Оранжевый
    'light': '#ECF0F1',        # Светло-серый
    'dark': '#2C3E50',         # Темный
    'background': '#F8F9FA',   # Фон
    'text': '#2C3E50'          # Текст
}

class PriceManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Система анализа прайсов")
        self.root.geometry("600x500")

        self.manager = PriceManager()

        self.create_main_menu()

    def create_main_menu(self):
        """Создает главное меню"""

        self.clear_window()

        # Заголовок
        title_label = ttk.Label(self.root, text="Система анализа прайсов",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Информация о местоположении
        self.location_label = ttk.Label(
            self.root,
            text=f"Ваше местоположение:\n{self.manager.get_user_location_info()}",
            font=("Arial", 12)
        )
        self.location_label.pack(pady=10)

        # Кнопки меню
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=20)

        button_style = {"width": 40, "padding": 10}

        ttk.Button(buttons_frame, text="Загрузить прайс предприятия",
                   command=self.open_add_company_window, **button_style).pack(pady=5)

        ttk.Button(buttons_frame, text="Поиск товара",
                   command=self.open_search_window, **button_style).pack(pady=5)

        ttk.Button(buttons_frame, text="Задать мое местоположение",
                   command=self.open_location_window, **button_style).pack(pady=5)

        ttk.Button(buttons_frame, text="Показать все предприятия",
                   command=self.open_companies_window, **button_style).pack(pady=5)

        ttk.Button(buttons_frame, text="Выход",
                   command=self.root.quit, **button_style).pack(pady=5)

    # В методе open_add_company_window добавляем поле для адреса:
    def open_add_company_window(self):
        """Окно добавления предприятия"""
        self.clear_window()
        self.root.configure(bg=COLORS['background'])

        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        # Заголовок
        title_label = ttk.Label(main_frame,
                                text="📁 Загрузка прайса предприятия",
                                font=("Arial", 18, "bold"),
                                foreground=COLORS['primary'],
                                background=COLORS['background'])
        title_label.pack(pady=20)

        # Поля ввода в рамке
        input_frame = ttk.LabelFrame(main_frame,
                                     text="Данные предприятия",
                                     padding=20,
                                     style='TFrame')
        input_frame.pack(pady=20, padx=20, fill="x")

        # Название предприятия
        ttk.Label(input_frame,
                  text="Название предприятия:",
                  font=("Arial", 11),
                  foreground=COLORS['dark']).grid(row=0, column=0, sticky="w", pady=10)

        company_name_var = tk.StringVar()
        company_entry = ttk.Entry(input_frame,
                                  textvariable=company_name_var,
                                  width=40,
                                  font=("Arial", 11))
        company_entry.grid(row=0, column=1, pady=10, padx=10, columnspan=2)

        # Адрес предприятия
        ttk.Label(input_frame,
                  text="Адрес предприятия:",
                  font=("Arial", 11),
                  foreground=COLORS['dark']).grid(row=1, column=0, sticky="w", pady=10)

        address_var = tk.StringVar()
        address_entry = ttk.Entry(input_frame,
                                  textvariable=address_var,
                                  width=40,
                                  font=("Arial", 11))
        address_entry.grid(row=1, column=1, pady=10, padx=10, columnspan=2)

        # Файл прайса
        ttk.Label(input_frame,
                  text="Файл прайса (DOCX):",
                  font=("Arial", 11),
                  foreground=COLORS['dark']).grid(row=2, column=0, sticky="w", pady=10)

        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(input_frame,
                               textvariable=self.file_path_var,
                               width=30,
                               state="readonly",
                               font=("Arial", 10))
        file_entry.grid(row=2, column=1, pady=10, padx=10)

        ttk.Button(input_frame,
                   text="📂 Выбрать файл",
                   command=self.select_file,
                   style='Secondary.TButton').grid(row=2, column=2, pady=10, padx=10)

        # Подсказка о формате файла
        help_label = ttk.Label(input_frame,
                               text="Формат файла: каждая строка - 'Название товара, Цена'",
                               font=("Arial", 9),
                               foreground=COLORS['secondary'],
                               background=COLORS['background'])
        help_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=5)

        # Кнопки действий
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=30)

        ttk.Button(button_frame,
                   text="✅ Загрузить",
                   command=lambda: self.add_company(company_name_var.get(), address_var.get()),
                   style='Primary.TButton').pack(side="left", padx=15)

        ttk.Button(button_frame,
                   text="↩️ Назад",
                   command=self.create_main_menu,
                   style='Secondary.TButton').pack(side="left", padx=15)

    # Обновляем метод select_file для фильтрации DOCX
    def select_file(self):
        """Выбор DOCX файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл прайса",
            filetypes=[("Excel documents", "*.xlxs"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

    # Обновляем метод add_company
    def add_company(self, company_name, address):
        """Добавление предприятия"""
        if not company_name:
            messagebox.showerror("Ошибка", "Введите название предприятия")
            return

        if not self.file_path_var.get():
            messagebox.showerror("Ошибка", "Выберите файл прайса")
            return

        # Если адрес не указан, используем значение по умолчанию
        if not address:
            address = "Адрес не указан"

        # Вызываем метод с тремя аргументами
        result = self.manager.add_company_from_file(company_name, self.file_path_var.get(), address)
        messagebox.showinfo("Результат", result)
        self.create_main_menu()

    def open_search_window(self):
        """Окно поиска товара"""
        self.clear_window()

        ttk.Label(self.root, text="Поиск товара",
                  font=("Arial", 14, "bold")).pack(pady=20)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill="x")

        # Используем grid для всех виджетов в search_frame
        ttk.Label(search_frame, text="Название товара:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(search_frame, text="Вес расстояния:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.distance_weight_var = tk.DoubleVar(value=10)
        distance_entry = ttk.Entry(search_frame, textvariable=self.distance_weight_var, width=10)
        distance_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Поиск",
                   command=lambda: self.search_product(search_var.get())).pack(side="left", padx=10)

        ttk.Button(button_frame, text="Назад",
                   command=self.create_main_menu).pack(side="left", padx=10)

        # Область для результатов
        self.results_text = scrolledtext.ScrolledText(self.root, height=15, width=70)
        self.results_text.pack(pady=10, padx=20, fill="both", expand=True)
        self.results_text.config(state="disabled")

    def search_product(self, search_term):
        """Поиск товара"""
        if not search_term:
            messagebox.showerror("Ошибка", "Введите название товара")
            return

        results = self.manager.search_products(search_term)
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)

        if not results:
            self.results_text.insert(tk.END, "Товары не найдены.")
        else:


            for i, item in enumerate(results, 1):
                self.results_text.insert(tk.END, f"{i}. {item['name']} - {item['price']} руб.\n")
                self.results_text.insert(tk.END, f"   Магазин: {item['company']}\n")
                self.results_text.insert(tk.END, f"   Расстояние: {item['distance']:.2f} км\n")
                self.results_text.insert(tk.END, f"   Общий балл: {item['total_score']:.2f}\n")
                self.results_text.insert(tk.END, "-" * 50 + "\n\n")

        self.results_text.config(state="disabled")

    def open_location_window(self):
        """Окно установки местоположения"""
        self.clear_window()

        ttk.Label(self.root, text="Задать мое местоположение",
                  font=("Arial", 14, "bold")).pack(pady=20)

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Город:").grid(row=0, column=0, sticky="w", pady=5)
        city_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=city_var, width=30).grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Улица и дом:").grid(row=1, column=0, sticky="w", pady=5)
        street_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=street_var, width=30).grid(row=1, column=1, pady=5, padx=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Сохранить",
                   command=lambda: self.save_location(city_var.get(), street_var.get())).pack(side="left", padx=10)

        ttk.Button(button_frame, text="Назад",
                   command=self.create_main_menu).pack(side="left", padx=10)

    def save_location(self, city, street):
        """Сохранение местоположения"""
        if not city or not street:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        success = self.manager.set_user_location(city, street)
        if success:
            messagebox.showinfo("Успех", "Местоположение успешно сохранено!")
            self.create_main_menu()
        else:
            messagebox.showerror("Ошибка", "Не удалось определить координаты по этому адресу")

    def open_companies_window(self):
        """Окно просмотра предприятий"""
        self.clear_window()

        ttk.Label(self.root, text="Все предприятия",
                  font=("Arial", 14, "bold")).pack(pady=20)

        companies = self.manager.get_all_companies()

        # Создаем Treeview для таблицы
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("name", "address", "distance")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        tree.heading("name", text="Название")
        tree.heading("address", text="Адрес")
        tree.heading("distance", text="Расстояние (км)")

        tree.column("name", width=150)
        tree.column("address", width=200)
        tree.column("distance", width=100)

        for company in companies:
            distance = company['distance'] if isinstance(company['distance'], float) else company['distance']
            tree.insert("", "end", values=(company['name'], company['address'], distance))

        # Добавляем scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка назад
        ttk.Button(self.root, text="Назад",
                   command=self.create_main_menu).pack(pady=10)

    def clear_window(self):
        """Очищает окно от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def save_location(self, city, street):
        if not city or not street:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        success = self.manager.set_user_location(city, street)
        if success:
            messagebox.showinfo("Успех", "Местоположение успешно сохранено!")
            self.create_main_menu()  # пересоздаем меню вместе с актуальной меткой
        else:
            messagebox.showerror("Ошибка", "Не удалось определить координаты по этому адресу")


