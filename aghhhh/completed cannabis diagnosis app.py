import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class CannabisDiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cannabis Plant Diagnosis Tool")
        self.root.configure(background="#0d0d0d")  # Set background color to #0d0d0d

        self.current_question = 0
        self.responses = []
        self.diagnoses = []
        self.email_list = []
        self.life_stage = ""

        self.setup_styles()
        self.create_widgets()
        self.load_question()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        common_settings = {"font": ("Helvetica", 12), "padding": 10, "background": "#444444", "foreground": "#ffffff"}
        style.configure("TButton", **common_settings)
        style.configure("TLabel", font=("Helvetica", 14), padding=10, background="#0d0d0d", foreground="#ffffff")
        style.configure("TEntry", font=("Helvetica", 12), padding=10, fieldbackground="#444444", foreground="#ffffff")
        style.configure("TFrame", background="#0d0d0d")
        style.configure("TLabelFrame", background="#0d0d0d", foreground="#ffffff", padding=10)
        style.configure("TLabelFrame.Label", background="#0d0d0d", foreground="#ffffff")
        style.configure("TCheckbutton", background="#0d0d0d", font=("Helvetica", 12), foreground="#ffffff")
        style.map("TButton", background=[('active', '#555555')], foreground=[('active', '#ffffff')])

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        self.question_label = ttk.Label(self.main_frame, text="", wraplength=500)
        self.question_label.pack(pady=10)

        self.image_label = ttk.Label(self.main_frame)
        self.image_label.pack(pady=10)

        self.entry = ttk.Entry(self.main_frame)
        self.npk_entry = [ttk.Entry(self.main_frame) for _ in range(3)]

        self.ph_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.water_ph_label = ttk.Label(self.ph_frame, text="Water pH:", style="TLabel")
        self.water_ph_entry = ttk.Entry(self.ph_frame, style="TEntry")
        self.soil_ph_label = ttk.Label(self.ph_frame, text="Soil pH:", style="TLabel")
        self.soil_ph_entry = ttk.Entry(self.ph_frame, style="TEntry")

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)

        self.create_buttons()

        self.questions = [
            ("What stage of growth is your plant in? (Seedling, Vegetative, Flowering)", None, "stage"),
            ("Is your plant drooping?", "drooping.jpg"),
            ("Are the leaves yellowing?", "yellowing_leaves.jpg"),
            ("Are the leaves curling?", "curling_leaves.jpg"),
            ("Are there brown spots on the leaves?", "brown_spots.jpg"),
            ("Are the leaves turning purple?", "purple_leaves.jpg"),
            ("Is the growth stunted?", "stunted_growth.jpg"),
            ("Do you see pests on the plant?", "pests.jpg"),
            ("Are there whiteflies on the plant?", "whiteflies.jpg"),
            ("Are there spider mites on the plant?", "spider_mites.jpg"),
            ("Are there aphids on the plant?", "aphids.jpg"),
            ("Are there thrips on the plant?", "thrips.jpg"),
            ("Do the leaves have powdery mildew?", "powdery_mildew.jpg"),
            ("Is there bud rot (gray mold) on the plant?", "bud_rot.jpg"),
            ("Are there signs of root rot?", "root_rot.jpg"),
            ("What is your fertilizer NPK? (Enter N, P, and K values)", None, "npk_input"),
            ("What is the pH of the water and soil? (Enter water pH and soil pH)", None, "ph_input"),
            ("Is the temperature in the grow space above 85°F (30°C)?", None),
            ("Is the temperature in the grow space below 70°F (20°C)?", None),
            ("Is the relative humidity above 60%?", None),
            ("Is the relative humidity below 40%?", None),
            ("Are you using cannabis-specific nutrients?", "cannabis_nutrients.jpg"),
            ("Are you using reverse osmosis (RO) water?", "ro_water.jpg", "cal_mag"),
            ("Are you using coco coir as a growing medium?", "coco_coir.jpg", "cal_mag"),
        ]

        self.deficiency_images = [
            ("Nitrogen deficiency", "nitrogen_deficiency.jpg"),
            ("Potassium deficiency", "potassium_deficiency.jpg"),
            ("Magnesium deficiency", "magnesium_deficiency.jpg"),
            ("Phosphorus deficiency", "phosphorus_deficiency.jpg")
        ]

    def create_buttons(self):
        self.yes_button = ttk.Button(self.button_frame, text="Yes", command=lambda: self.record_response("yes"))
        self.no_button = ttk.Button(self.button_frame, text="No", command=lambda: self.record_response("no"))
        self.not_sure_button = ttk.Button(self.button_frame, text="Not Sure",
                                          command=lambda: self.record_response("not_sure"))
        self.na_button = ttk.Button(self.button_frame, text="Not Applicable",
                                    command=lambda: self.record_response("not_applicable"))

        self.seedling_button = ttk.Button(self.button_frame, text="Seedling",
                                          command=lambda: self.record_response("seedling"))
        self.veg_button = ttk.Button(self.button_frame, text="Vegetative",
                                     command=lambda: self.record_response("vegetative"))
        self.flower_button = ttk.Button(self.button_frame, text="Flowering",
                                        command=lambda: self.record_response("flowering"))

        self.submit_button = ttk.Button(self.button_frame, text="Submit", command=self.submit_input)

    def load_question(self):
        self.hide_buttons()  # Hide all buttons initially
        self.hide_inputs()  # Hide all input fields initially
        if self.current_question < len(self.questions):
            question, image_path, *input_type = self.questions[self.current_question]
            self.question_label.config(text=question)
            if image_path:
                self.load_image(image_path)
                self.show_buttons()
            elif input_type:
                self.image_label.config(image='', text='')
                if input_type[0] == "stage":
                    self.seedling_button.pack(side=tk.LEFT, padx=10, pady=10)
                    self.veg_button.pack(side=tk.LEFT, padx=10, pady=10)
                    self.flower_button.pack(side=tk.LEFT, padx=10, pady=10)
                elif input_type[0] == "npk_input":
                    for entry in self.npk_entry:
                        entry.pack(side=tk.LEFT, padx=5)
                    self.submit_button.pack(side=tk.LEFT, padx=10, pady=10)
                    self.not_sure_button.pack(side=tk.LEFT, padx=10, pady=10)
                elif input_type[0] == "ph_input":
                    self.ph_frame.pack()
                    self.water_ph_label.pack(side=tk.LEFT, padx=5)
                    self.water_ph_entry.pack(side=tk.LEFT, padx=5)
                    self.soil_ph_label.pack(side=tk.LEFT, padx=5)
                    self.soil_ph_entry.pack(side=tk.LEFT, padx=5)
                    self.submit_button.pack(side=tk.LEFT, padx=10, pady=10)
                    self.not_sure_button.pack(side=tk.LEFT, padx=10, pady=10)
                elif input_type[0] == "image_check":
                    self.show_deficiency_image()
                elif input_type[0] == "cal_mag":
                    self.show_cal_mag_buttons()
            else:
                self.image_label.config(image='', text='')
                self.show_buttons()
        else:
            self.evaluate_responses()
            self.show_results()

    def hide_inputs(self):
        self.entry.pack_forget()
        for entry in self.npk_entry:
            entry.pack_forget()
        self.ph_frame.pack_forget()
        self.water_ph_label.pack_forget()
        self.water_ph_entry.pack_forget()
        self.soil_ph_label.pack_forget()
        self.soil_ph_entry.pack_forget()
        self.submit_button.pack_forget()
        self.na_button.pack_forget()
        self.seedling_button.pack_forget()
        self.veg_button.pack_forget()
        self.flower_button.pack_forget()

    def evaluate_responses(self):
        self.diagnoses.clear()
        # Check each response and append corresponding diagnoses with solutions and images
        if len(self.responses) > 1 and self.responses[1] == "yes":
            self.diagnoses.append(("Drooping",
                                   "Check for overwatering or underwatering. Adjust watering schedule accordingly.",
                                   "drooping.jpg"))
        if len(self.responses) > 2 and self.responses[2] == "yes":
            self.diagnoses.append(("Yellowing Leaves",
                                   "Possible nitrogen deficiency. Natural solution: Compost tea. Chemical solution: Nitrogen-rich fertilizer.",
                                   "yellowing_leaves.jpg"))
        if len(self.responses) > 3 and self.responses[3] == "yes":
            self.diagnoses.append(("Curling Leaves",
                                   "Check for heat stress or overfeeding. Adjust light distance and nutrient levels.",
                                   "curling_leaves.jpg"))
        if len(self.responses) > 4 and self.responses[4] == "yes":
            self.diagnoses.append(("Brown Spots",
                                   "Possible calcium or magnesium deficiency. Natural solution: Epsom salts. Chemical solution: Cal-Mag supplement.",
                                   "brown_spots.jpg"))
        if len(self.responses) > 5 and self.responses[5] == "yes":
            self.diagnoses.append(("Purple Leaves",
                                   "Could be due to genetics or phosphorus deficiency. Ensure proper phosphorus levels.",
                                   "purple_leaves.jpg"))
        if len(self.responses) > 6 and self.responses[6] == "yes":
            self.diagnoses.append(("Stunted Growth",
                                   "Check for root-bound plants or nutrient deficiencies. Repot if necessary, and adjust feeding schedule.",
                                   "stunted_growth.jpg"))
        if len(self.responses) > 7 and self.responses[7] == "yes":
            self.diagnoses.append(("Pests",
                                   "Identify the pest and treat accordingly. Natural solution: Neem oil. Chemical solution: Insecticidal soap.",
                                   "pests.jpg"))
        if len(self.responses) > 8 and self.responses[8] == "yes":
            self.diagnoses.append(
                ("Whiteflies", "Treat with yellow sticky traps and insecticidal soap.", "whiteflies.jpg"))
        if len(self.responses) > 9 and self.responses[9] == "yes":
            self.diagnoses.append(("Spider Mites",
                                   "Increase humidity and treat with miticides. Natural solution: Neem oil.",
                                   "spider_mites.jpg"))
        if len(self.responses) > 10 and self.responses[10] == "yes":
            self.diagnoses.append(
                ("Aphids", "Natural solution: Ladybugs. Chemical solution: Insecticidal soap.", "aphids.jpg"))
        if len(self.responses) > 11 and self.responses[11] == "yes":
            self.diagnoses.append(("Thrips", "Use blue sticky traps and insecticidal soap.", "thrips.jpg"))
        if len(self.responses) > 12 and self.responses[12] == "yes":
            self.diagnoses.append(("Powdery Mildew",
                                   "Increase air circulation and treat with fungicides. Natural solution: Milk spray.",
                                   "powdery_mildew.jpg"))
        if len(self.responses) > 13 and self.responses[13] == "yes":
            self.diagnoses.append(("Bud Rot", "Remove affected buds and increase air circulation.", "bud_rot.jpg"))
        if len(self.responses) > 14 and self.responses[14] == "yes":
            self.diagnoses.append(("Root Rot",
                                   "Check for overwatering and ensure proper drainage. Treat with beneficial bacteria.",
                                   "root_rot.jpg"))

    def load_image(self, image_path):
        try:
            image = Image.open(f"images/{image_path}")
            image = image.resize((300, 200), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except FileNotFoundError:
            self.image_label.config(image='', text='Image not found.')
        except Exception as e:
            self.image_label.config(image='', text=f'Error loading image: {e}')

    def record_response(self, response):
        if self.current_question == 0:
            self.life_stage = response.lower()
            self.responses.append(response)
        elif self.current_question < len(self.questions) and len(self.questions[self.current_question]) > 2 and \
                self.questions[self.current_question][2] == "image_check":
            if response == "yes":
                self.diagnoses.append(f"Possible {self.deficiency_images[self.deficiency_index][0]}")
            self.deficiency_index += 1
            if self.deficiency_index < len(self.deficiency_images):
                self.show_deficiency_image()
                return
            else:
                self.deficiency_index = 0  # Reset for future use
        else:
            self.responses.append(response)
        self.current_question += 1
        self.load_question()

    def show_deficiency_image(self):
        deficiency_name, image_path = self.deficiency_images[self.deficiency_index]
        self.question_label.config(text=f"Does this photo look like your leaves? ({deficiency_name})")
        self.load_image(image_path)
        self.show_buttons()
        self.entry.pack_forget()
        for entry in self.npk_entry:
            entry.pack_forget()
        self.ph_frame.pack_forget()
        self.submit_button.pack_forget()

    def handle_not_sure(self):
        self.responses.append("not_sure")
        self.current_question += 1
        self.load_question()

    def submit_input(self):
        if self.current_question < len(self.questions):
            if self.current_question == 0:
                response = self.entry.get().lower()
                if response in ["seedling", "vegetative", "flowering"]:
                    self.life_stage = response
                    self.responses.append(response)
                    self.entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Input required",
                                           "Please enter a valid life stage: Seedling, Vegetative, or Flowering.")
                    return
            elif len(self.questions[self.current_question]) > 2 and self.questions[self.current_question][
                2] == "npk_input":
                npk_values = [entry.get() for entry in self.npk_entry]
                if all(npk_values):
                    self.responses.append(" ".join(npk_values))
                    for entry in self.npk_entry:
                        entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Input required", "Please enter all NPK values.")
                    return
            elif len(self.questions[self.current_question]) > 2 and self.questions[self.current_question][
                2] == "ph_input":
                water_ph = self.water_ph_entry.get()
                soil_ph = self.soil_ph_entry.get()
                if water_ph and soil_ph:
                    self.responses.append(f"Water pH: {water_ph}, Soil pH: {soil_ph}")
                    self.water_ph_entry.delete(0, tk.END)
                    self.soil_ph_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Input required", "Please enter both water pH and soil pH values.")
                    return
            elif len(self.questions[self.current_question]) > 2 and self.questions[self.current_question][2] == "input":
                response = self.entry.get()
                if response:
                    self.responses.append(response)
                    self.entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Input required", "Please enter a value.")
                    return
            else:
                response = None
                self.responses.append(response)
            self.current_question += 1
            self.load_question()

    def show_buttons(self):
        self.yes_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.no_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.not_sure_button.pack(side=tk.LEFT, padx=10, pady=10)

    def hide_buttons(self):
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.not_sure_button.pack_forget()
        self.na_button.pack_forget()

    def show_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Diagnosis Results")
        result_window.configure(background="#0d0d0d")

        result_frame = ttk.Frame(result_window, padding=20)
        result_frame.pack(fill=tk.BOTH, expand=True)

        diagnosis_label = ttk.Label(result_frame, text="Diagnosis:", style="TLabel")
        diagnosis_label.grid(row=0, column=0, sticky="w")

        result_textbox = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20)
        result_textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        for index, (diagnosis, solution, image_filename) in enumerate(self.diagnoses):
            diagnosis_text = f"{diagnosis}:\n{solution}\n\n"
            result_textbox.insert(tk.END, diagnosis_text)

            image_path = f"images/{image_filename}"
            try:
                image = Image.open(image_path)
                image = image.resize((150, 100), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
                photo = ImageTk.PhotoImage(image)
                image_label = ttk.Label(result_frame, image=photo)
                image_label.image = photo  # Keep a reference to avoid garbage collection
                result_textbox.window_create(tk.END, window=image_label)
                result_textbox.insert(tk.END, "\n\n")
            except FileNotFoundError:
                result_textbox.insert(tk.END, "Image not found.\n\n")
            except Exception as e:
                result_textbox.insert(tk.END, f"Error loading image: {e}\n\n")

        result_textbox.configure(state="disabled")

        stage_label = ttk.Label(result_frame, text="Plant Stage:", style="TLabel")
        stage_label.grid(row=2, column=0, sticky="w")

        stage_value_label = ttk.Label(result_frame, text=self.life_stage.capitalize(), style="TLabel")
        stage_value_label.grid(row=2, column=1, sticky="w")

        self.email_var = tk.BooleanVar()
        email_checkbox = ttk.Checkbutton(result_frame, text="Send results via email", variable=self.email_var,
                                         command=self.toggle_email_input, style="TCheckbutton")
        email_checkbox.grid(row=3, columnspan=2, pady=10)

        self.email_entry_label = ttk.Label(result_frame, text="Email:", style="TLabel")
        self.email_entry = ttk.Entry(result_frame, style="TEntry")

        email_button = ttk.Button(result_frame, text="Send Email",
                                  command=lambda: self.send_email(result_textbox.get("1.0", tk.END)))
        email_button.grid(row=5, columnspan=2)

    def toggle_email_input(self):
        if self.email_var.get():
            self.email_entry_label.grid(row=4, column=0, sticky="w")
            self.email_entry.grid(row=4, column=1, sticky="w")
        else:
            self.email_entry_label.grid_forget()
            self.email_entry.grid_forget()

    def send_email(self, diagnosis_text):
        email_address = self.email_entry.get()
        if not email_address:
            messagebox.showwarning("Email Error", "Please provide an email address.")
            return

        sender_email = "your-email@example.com"  # Replace with your email
        sender_password = "your-password"  # Replace with your password

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email_address
        message["Subject"] = "Cannabis Plant Diagnosis Results"

        message.attach(MIMEText(diagnosis_text, "plain"))

        try:
            with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_address, message.as_string())
                messagebox.showinfo("Email Sent", "Diagnosis results sent successfully.")
        except Exception as e:
            messagebox.showerror("Email Error", f"An error occurred while sending the email: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CannabisDiagnosisApp(root)
    root.mainloop()
