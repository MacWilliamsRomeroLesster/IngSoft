import sys

def install(package):
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verificar e instalar las librerías necesarias
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    install('tkinter')
    import tkinter as tk
    from tkinter import ttk,messagebox, filedialog

try:
    import json
except ImportError:
    install('json')
    import json

try:
    import os
except ImportError:
    install('os')
    import os

try:
    from datetime import datetime
except ImportError:
    install('datetime')
    from datetime import datetime

try:
    from collections import defaultdict
except ImportError:
    install('collections')
    from collections import defaultdict

try:
    import matplotlib.pyplot as plt
except ImportError:
    install('matplotlib')
    import matplotlib.pyplot as plt

class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fitness App")
        self.attributes("-fullscreen", True)

        # Botón de cierre
        self.close_button = ttk.Button(self, text="Cerrar App", command=self.quit)
        self.close_button.place(x=10, y=10)

        # Botón para ver información de usuario
        self.info_button = ttk.Button(self, text="Ver Info", command=self.show_user_info)
        self.info_button.place(x=100, y=10)

        self.current_view = None
        self.user_info = self.load_user_info()

        self.user_info_label = tk.Label(self, bg="#f0f0f0", font=("Arial", 14))
        self.user_info_label.pack(side="top", anchor="ne", padx=20, pady=10)

        self.register_file_path = "registerroutines.txt"
        if not os.path.exists(self.register_file_path):
            with open(self.register_file_path, "w") as file:
                file.write("")

        if self.user_info['nombre']:
            self.show_main_screen()
        else:
            self.show_login_screen()
   
    def show_user_info(self):
        messagebox.showinfo("Información del Usuario", 
                            f"Nombre: {self.user_info['nombre']}\n"
                            f"Peso: {self.user_info['peso']}\n"
                            f"Altura: {self.user_info['altura']}")

    def show_login_screen(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Inicio de Sesión", font=("Arial", 24), bg="#f0f0f0").pack(pady=(100, 20))

        login_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        login_frame.pack()

        tk.Label(login_frame, text="Nombre de Usuario:", bg="#f0f0f0", font=("Arial", 14)).grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(login_frame, text="Peso:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.weight_entry = tk.Entry(login_frame, font=("Arial", 14))
        self.weight_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(login_frame, text="Altura:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, pady=10)
        self.height_entry = tk.Entry(login_frame, font=("Arial", 14))
        self.height_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(self.current_view, text="Iniciar Sesión", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=20)

    def show_main_screen(self):

        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Bienvenido, " + self.user_info['nombre'], font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        options_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        options_frame.pack()

        tk.Button(options_frame, text="Rutinas", command=self.manage_routines, bg="#008CBA", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Editar Información del Usuario", command=self.edit_user_info, bg="#008CBA", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Registrar Ejercicio Realizado", command=self.register_exercise_window, bg="#008CBA", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Ver Progreso", command=self.view_progress, bg="#008CBA", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Salir", command=self.quit_app, bg="#f44336", fg="white", font=("Arial", 18)).pack(pady=10)

    def load_user_info(self):
        try:
            with open("user_info.json", "r") as file:
                user_info = json.load(file)
                return user_info
        except FileNotFoundError:
            return {
                "nombre": "",
                "edad": "",
                "altura": "",
                "peso": ""
            }

    def save_user_info(self):
        self.user_info["nombre"] = self.username_entry.get()
        self.user_info["peso"] = self.weight_entry.get()
        self.user_info["altura"] = self.height_entry.get()

        with open("user_info.json", "w") as file:
            json.dump(self.user_info, file)

        messagebox.showinfo("Información del Usuario", "Información actualizada con éxito!")

    def login(self):
        self.save_user_info()
        self.show_main_screen()

    def manage_routines(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Rutinas", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        options_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        options_frame.pack()

        tk.Button(options_frame, text="Registrar Rutinas", command=self.register_routines, bg="#4CAF50", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Ver Rutinas", command=self.view_routines, bg="#4CAF50", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(options_frame, text="Eliminar Rutinas", command=self.delete_routines, bg="#4CAF50", fg="white", font=("Arial", 18)).pack(pady=10)
        tk.Button(self.current_view, text="Atrás", command=self.show_main_screen, bg="#FF5722", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")

    def register_routines(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Registrar Rutinas", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        register_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        register_frame.pack()

        tk.Label(register_frame, text="Ejercicio:", bg="#f0f0f0", font=("Arial", 14)).grid(row=0, column=0, pady=10)
        self.exercise_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.exercise_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(register_frame, text="Repeticiones:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.reps_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.reps_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(register_frame, text="Series:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, pady=10)
        self.sets_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.sets_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(register_frame, text="Descripción:", bg="#f0f0f0", font=("Arial", 14)).grid(row=3, column=0, pady=10)
        self.description_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.description_entry.grid(row=3, column=1, pady=10, padx=10)

        tk.Button(self.current_view, text="Guardar Rutina", command=self.save_routine, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")
        tk.Button(self.current_view, text="Atrás", command=self.manage_routines, bg="#FF5722", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")

    def save_routine(self):
        exercise = self.exercise_entry.get()
        reps = self.reps_entry.get()
        sets = self.sets_entry.get()
        description = self.description_entry.get()

        routine = f"Usuario: {self.user_info['nombre']}, Ejercicio: {exercise}, Repeticiones: {reps}, Series: {sets}, Descripción: {description}\n"

        with open("routines.txt", "a") as file:
            file.write(routine)

        messagebox.showinfo("Registro de Rutina", "Rutina guardada con éxito!")

    def view_routines(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Ver Rutinas", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        try:
            with open("routines.txt", "r") as file:
                routines = file.readlines()
                for routine in routines:
                    routine_data = routine.strip().split(", ")
                    username = routine_data[0].split(": ")[1]
                    exercise_info = ", ".join(routine_data[1:])
                    routine_frame = tk.Frame(self.current_view, bg="white", bd=2, relief="groove", padx=20, pady=10)
                    routine_frame.pack(pady=5, fill="x")

                    tk.Label(routine_frame, text=f"Usuario: {username}, {exercise_info}", bg="white", font=("Arial", 14)).pack()

        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "No hay rutinas registradas.")

        tk.Button(self.current_view, text="Atrás", command=self.manage_routines, bg="#FF5722", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")

    def delete_routines(self):
        try:
            with open("routines.txt", "r") as file:
                routines = file.readlines()
            if not routines:
                messagebox.showinfo("Eliminar Rutinas", "No hay rutinas para eliminar.")
                return

            self.current_view.destroy()

            self.current_view = tk.Frame(self, bg="#f0f0f0")
            self.current_view.pack(expand=True, fill="both")

            tk.Label(self.current_view, text="Eliminar Rutinas", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

            for routine in routines:
                routine_data = routine.strip().split(", ")
                username = routine_data[0].split(": ")[1]
                exercise_info = ", ".join(routine_data[1:])
                routine_frame = tk.Frame(self.current_view, bg="white", bd=2, relief="groove", padx=20, pady=10)
                routine_frame.pack(pady=5, fill="x")

                tk.Label(routine_frame, text=f"Usuario: {username}, {exercise_info}", bg="white", font=("Arial", 14)).pack(side="left")

                tk.Button(routine_frame, text="Eliminar", command=lambda r=routine: self.delete_selected_routine(r), bg="#FF5722", fg="white", font=("Arial", 14)).pack(side="right")

            tk.Button(self.current_view, text="Atrás", command=self.manage_routines, bg="#FF5722", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")

        except FileNotFoundError:
            messagebox.showinfo("Eliminar Rutinas", "No hay rutinas para eliminar.")

    def delete_selected_routine(self, routine):
        try:
            with open("routines.txt", "r") as file:
                lines = file.readlines()
            with open("routines.txt", "w") as file:
                for line in lines:
                    if line.strip() != routine.strip():
                        file.write(line)

            messagebox.showinfo("Eliminar Rutina", "Rutina eliminada exitosamente.")
            self.delete_routines()  # Actualizar la vista de eliminación de rutinas

        except FileNotFoundError:
            messagebox.showinfo("Eliminar Rutina", "No hay rutinas para eliminar.")

    def edit_user_info(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Editar Información del Usuario", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        edit_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        edit_frame.pack()

        tk.Label(edit_frame, text="Nombre de Usuario:", bg="#f0f0f0", font=("Arial", 14)).grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(edit_frame, font=("Arial", 14))
        self.username_entry.insert(0, self.user_info['nombre'])
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(edit_frame, text="Peso:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.weight_entry = tk.Entry(edit_frame, font=("Arial", 14))
        self.weight_entry.insert(0, self.user_info['peso'])
        self.weight_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(edit_frame, text="Altura:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, pady=10)
        self.height_entry = tk.Entry(edit_frame, font=("Arial", 14))
        self.height_entry.insert(0, self.user_info['altura'])
        self.height_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(self.current_view, text="Guardar Cambios", command=self.save_user_info, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")
        tk.Button(self.current_view, text="Atrás", command=self.show_main_screen, bg="#FF5722", fg="white", font=("Arial", 14)).pack(pady=20, side="bottom")

    def quit_app(self):
        self.destroy()

    def register_exercise_window(self):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = tk.Frame(self, bg="#f0f0f0")
        self.current_view.pack(expand=True, fill="both")

        tk.Label(self.current_view, text="Registrar Ejercicio Realizado", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)
        
        # Campo de entrada para la fecha
        date_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        date_frame.pack(pady=10)
        tk.Label(date_frame, text="Fecha (dd/mm/yyyy):", font=("Arial", 14), bg="#f0f0f0").pack(side="left")
        self.date_entry = tk.Entry(date_frame, font=("Arial", 12))
        self.date_entry.pack(side="left", padx=10)

        # Campo de entrada para el peso
        weight_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        weight_frame.pack(pady=10)
        tk.Label(weight_frame, text="Peso (kg):", font=("Arial", 14), bg="#f0f0f0").pack(side="left")
        self.weight_entry = tk.Entry(weight_frame, font=("Arial", 12))
        self.weight_entry.pack(side="left", padx=10)

        # Campo de entrada para la altura
        height_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        height_frame.pack(pady=10)
        tk.Label(height_frame, text="Altura (cm):", font=("Arial", 14), bg="#f0f0f0").pack(side="left")
        self.height_entry = tk.Entry(height_frame, font=("Arial", 12))
        self.height_entry.pack(side="left", padx=10)

        # Botón para guardar el ejercicio
        tk.Button(self.current_view, text="Guardar", command=self.save_exercise, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=10, side="bottom")

        # Botón Atrás
        tk.Button(self.current_view, text="Atrás", command=self.show_main_screen, bg="#FF5722", fg="white", font=("Arial", 14)).pack(side="bottom", pady=20)

        # Obtener ejercicios disponibles del archivo routines.txt
        exercise_options = self.get_available_exercises()

        # Menú desplegable para seleccionar el ejercicio
        exercise_frame = tk.Frame(self.current_view, bg="#f0f0f0")
        exercise_frame.pack(pady=10)
        tk.Label(exercise_frame, text="Seleccione el Ejercicio:", font=("Arial", 14), bg="#f0f0f0").pack(side="left")
        self.exercise_selection = tk.StringVar(self.current_view)
        self.exercise_selection.set("Seleccionar ejercicio")
        self.exercise_menu = tk.OptionMenu(exercise_frame, self.exercise_selection, *exercise_options)
        self.exercise_menu.pack(side="left", padx=10)



    def get_available_exercises(self):
        exercise_options = []
        try:
            with open("routines.txt", "r") as file:
                for line in file:
                    if "Ejercicio:" in line:
                        exercise_info = line.strip()
                        exercise_options.append(exercise_info)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'routines.txt'")
            return
        return exercise_options

    def save_exercise(self):
        exercise_name = self.exercise_selection.get()
        date_str = self.date_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()

        # Verificar si se ingresó una fecha válida
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Por favor, use el formato dd/mm/yyyy")
            return

        # Obtener la fecha en formato dd/mm/yyyy
        formatted_date = date.strftime("%d/%m/%Y")

        # Guardar el ejercicio y la fecha en el archivo registerroutines.txt
        try:
            with open("registerroutines.txt", "a") as file:
                file.write(f"Ejercicio Registrado: {exercise_name}, Fecha: {formatted_date}, Peso: {weight} kg, Altura: {height} cm\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el ejercicio: {str(e)}")
        else:
            messagebox.showinfo("Éxito", "Ejercicio registrado correctamente.")

    def view_progress(self):
        try:
            with open("registerroutines.txt", "r") as file:
                exercises = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'registerroutines.txt'")
            return

        # Diccionario para almacenar el peso y la altura por fecha
        weight_by_date = defaultdict(list)
        height_by_date = defaultdict(list)

        for exercise in exercises:
            parts = exercise.split(", ")
            date_str = None
            weight = None
            height = None
            for part in parts:
                if "Fecha:" in part:
                    date_str = part.split(": ")[1]
                elif "Peso:" in part:
                    weight = float(part.split(": ")[1].split()[0])
                elif "Altura:" in part:
                    height = float(part.split(": ")[1].split()[0])
            if date_str and weight:
                date = datetime.strptime(date_str, "%d/%m/%Y")
                weight_by_date[date].append(weight)
            if date_str and height:
                date = datetime.strptime(date_str, "%d/%m/%Y")
                height_by_date[date].append(height)

        # Extraer las fechas ordenadas
        sorted_dates_weight = sorted(weight_by_date.keys())
        sorted_dates_height = sorted(height_by_date.keys())

        # Preparar los datos para la gráfica de peso
        weights = [sum(weight_by_date[date]) / len(weight_by_date[date]) for date in sorted_dates_weight]

        # Configurar la gráfica de peso
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_dates_weight, weights, marker='o', linestyle='-')
        for i, date in enumerate(sorted_dates_weight):
            plt.text(date, weights[i], f'{weights[i]} kg', fontsize=9, ha='center', va='bottom')
        plt.title('Progreso de Peso por Fecha')
        plt.xlabel('Fecha')
        plt.ylabel('Peso')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Preparar los datos para la gráfica de altura
        heights = [sum(height_by_date[date]) / len(height_by_date[date]) for date in sorted_dates_height]

        # Configurar la gráfica de altura
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_dates_height, heights, marker='o', linestyle='-')
        for i, date in enumerate(sorted_dates_height):
            plt.text(date, heights[i], f'{heights[i]} cm', fontsize=9, ha='center', va='bottom')
        plt.title('Progreso de Altura por Fecha')
        plt.xlabel('Fecha')
        plt.ylabel('Altura')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
