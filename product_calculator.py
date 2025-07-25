import tkinter as tk
from tkinter import ttk, messagebox

# Unit multipliers for conversion
unit_multipliers = {
    'mg': 0.001,
    'g': 1,
    'kg': 1000,
    'mL': 1,
    'L': 1000
}

# Classification cost multipliers
classification_multipliers = {
    "Non-Sterile": 1.0,
    "Sterile": 1.1,
    "High Risk": 1.25
}

class ProductCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Cost Calculator")
        self.geometry("750x500")
        self.resizable(False, False)

        self.frames = {}
        self.raw_materials = []
        self.labor_data = []
        self.additional_costs = {}

        for F in (RawMaterialPage, LaborPage, AdditionalCostsPage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RawMaterialPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class RawMaterialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Raw Materials Input", font=("Arial", 16)).pack(pady=10)

        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack()

        self.entries = []
        self.build_table_headers()
        for _ in range(5):
            self.add_row()

        ttk.Button(self, text="Add Row", command=self.add_row).pack(pady=5)
        ttk.Button(self, text="Next", command=self.save_and_continue).pack(pady=10)

    def build_table_headers(self):
        headers = ["Component", "Qty", "Unit", "Unit Cost ($)", "Waste %"]
        for col, text in enumerate(headers):
            ttk.Label(self.entries_frame, text=text).grid(row=0, column=col)

    def add_row(self):
        row = len(self.entries) + 1
        name = ttk.Entry(self.entries_frame, width=20)
        qty = ttk.Entry(self.entries_frame, width=10)
        unit = ttk.Combobox(self.entries_frame, values=list(unit_multipliers.keys()), width=6)
        unit.set("g")
        cost = ttk.Entry(self.entries_frame, width=10)
        waste = ttk.Entry(self.entries_frame, width=6)
        name.grid(row=row, column=0)
        qty.grid(row=row, column=1)
        unit.grid(row=row, column=2)
        cost.grid(row=row, column=3)
        waste.grid(row=row, column=4)
        self.entries.append((name, qty, unit, cost, waste))

    def save_and_continue(self):
        self.controller.raw_materials.clear()
        for name, qty, unit, cost, waste in self.entries:
            if name.get() and qty.get() and unit.get() and cost.get():
                try:
                    converted_qty = float(qty.get()) * unit_multipliers[unit.get()]
                    waste_factor = 1 + (float(waste.get() or 0) / 100)
                    total_qty = converted_qty * waste_factor
                    self.controller.raw_materials.append({
                        "component": name.get(),
                        "qty": total_qty,
                        "unit_cost": float(cost.get())
                    })
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid numeric values.")
                    return
        if not self.controller.raw_materials:
            messagebox.showerror("Input Error", "Please enter at least one material.")
            return
        self.controller.show_frame("LaborPage")
class LaborPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Labor & Machine Time", font=("Arial", 16)).pack(pady=10)

        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack()

        self.entries = []
        self.build_table_headers()
        for _ in range(5):
            self.add_row()

        ttk.Button(self, text="Add Row", command=self.add_row).pack(pady=5)
        ttk.Button(self, text="Next", command=self.save_and_continue).pack(pady=10)

    def build_table_headers(self):
        headers = ["Role", "Hours", "Hourly Rate", "Machine Hours", "Machine Rate"]
        for col, text in enumerate(headers):
            ttk.Label(self.entries_frame, text=text).grid(row=0, column=col)

    def add_row(self):
        row = len(self.entries) + 1
        role = ttk.Entry(self.entries_frame, width=20)
        hours = ttk.Entry(self.entries_frame, width=10)
        rate = ttk.Entry(self.entries_frame, width=10)
        machine_hours = ttk.Entry(self.entries_frame, width=10)
        machine_rate = ttk.Entry(self.entries_frame, width=10)
        role.grid(row=row, column=0)
        hours.grid(row=row, column=1)
        rate.grid(row=row, column=2)
        machine_hours.grid(row=row, column=3)
        machine_rate.grid(row=row, column=4)
        self.entries.append((role, hours, rate, machine_hours, machine_rate))

    def save_and_continue(self):
        self.controller.labor_data.clear()
        for role, hours, rate, machine_hours, machine_rate in self.entries:
            if role.get() and hours.get() and rate.get():
                try:
                    self.controller.labor_data.append({
                        "role": role.get(),
                        "hours": float(hours.get()),
                        "rate": float(rate.get()),
                        "machine_hours": float(machine_hours.get() or 0),
                        "machine_rate": float(machine_rate.get() or 0)
                    })
                except ValueError:
                    messagebox.showerror("Input Error", "Ensure all numeric values are valid.")
                    return
        if not self.controller.labor_data:
            messagebox.showerror("Input Error", "Please enter at least one labor row.")
            return
        self.controller.show_frame("AdditionalCostsPage")
class AdditionalCostsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Additional Costs & Assumptions", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=15)

        labels = [
            "R&D / Setup Cost ($):",
            "Lab Testing Cost ($):",
            "Units per Batch:",
            "Expected Units Sold:",
            "Price per Unit ($):",
            "Product Classification:"
        ]

        self.entries = {}
        for i, label in enumerate(labels[:-1]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky=tk.E, pady=4)
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, pady=4)
            self.entries[label] = entry

        # Product Classification dropdown
        ttk.Label(form, text=labels[-1]).grid(row=5, column=0, sticky=tk.E, pady=4)
        self.class_box = ttk.Combobox(form, values=list(classification_multipliers.keys()), state="readonly")
        self.class_box.set("Non-Sterile")
        self.class_box.grid(row=5, column=1, pady=4)

        ttk.Button(self, text="Calculate", command=self.save_and_continue).pack(pady=20)

    def save_and_continue(self):
        try:
            self.controller.additional_costs = {
                "rnd_cost": float(self.entries["R&D / Setup Cost ($):"].get()),
                "lab_cost": float(self.entries["Lab Testing Cost ($):"].get()),
                "units_per_batch": int(self.entries["Units per Batch:"].get()),
                "units_sold": int(self.entries["Expected Units Sold:"].get()),
                "price_per_unit": float(self.entries["Price per Unit ($):"].get()),
                "classification": self.class_box.get()
            }
            self.controller.show_frame("ResultsPage")
        except ValueError:
            messagebox.showerror("Input Error", "Please fill in all fields with valid numbers.")
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.result_text = tk.StringVar()

        ttk.Label(self, text="Financial Summary", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self, textvariable=self.result_text, font=("Courier", 11), justify="left").pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Start Over (Keep)", command=self.soft_restart).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Start Fresh", command=self.full_restart).pack(side=tk.LEFT, padx=10)

    def soft_restart(self):
        self.controller.show_frame("RawMaterialPage")

    def full_restart(self):
        self.controller.raw_materials.clear()
        self.controller.labor_data.clear()
        self.controller.additional_costs.clear()

        for entry_group in self.controller.frames["RawMaterialPage"].entries:
            for widget in entry_group:
                widget.delete(0, tk.END)

        for entry_group in self.controller.frames["LaborPage"].entries:
            for widget in entry_group:
                widget.delete(0, tk.END)

        add_page = self.controller.frames["AdditionalCostsPage"]
        for widget in add_page.entries.values():
            widget.delete(0, tk.END)
        add_page.class_box.set("Non-Sterile")

        self.controller.show_frame("RawMaterialPage")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.calculate()

    def calculate(self):
        rm_total = sum(item["qty"] * item["unit_cost"] for item in self.controller.raw_materials)
        labor_total = sum(item["hours"] * item["rate"] for item in self.controller.labor_data)
        machine_total = sum(item["machine_hours"] * item["machine_rate"] for item in self.controller.labor_data)

        ac = self.controller.additional_costs
        rnd = ac["rnd_cost"]
        lab = ac["lab_cost"]
        units_per_batch = ac["units_per_batch"]
        units_sold = ac["units_sold"]
        price = ac["price_per_unit"]
        classification = ac["classification"]
        multiplier = classification_multipliers[classification]

        total_batch_cost = (rm_total + labor_total + machine_total + rnd + lab) * multiplier
        cost_per_unit = total_batch_cost / units_per_batch if units_per_batch else 0
        total_cost = cost_per_unit * units_sold
        revenue = price * units_sold
        profit = revenue - total_cost
        roi = (profit / total_cost) * 100 if total_cost else 0
        breakeven_units = total_batch_cost / price if price else 0

        self.result_text.set(
            f"Raw Materials:       ${rm_total:,.2f}\n"
            f"Labor:               ${labor_total:,.2f}\n"
            f"Machine Time:        ${machine_total:,.2f}\n"
            f"R&D / Setup:         ${rnd:,.2f}\n"
            f"Lab Testing:         ${lab:,.2f}\n"
            f"Classification Adj.: x{multiplier}\n"
            f"-------------------------------\n"
            f"Total Batch Cost:    ${total_batch_cost:,.2f}\n"
            f"Cost per Unit:       ${cost_per_unit:,.2f}\n"
            f"Total Revenue:       ${revenue:,.2f}\n"
            f"Total Cost:          ${total_cost:,.2f}\n"
            f"Profit:              ${profit:,.2f}\n"
            f"ROI:                 {roi:.2f}%\n"
            f"Breakeven Units:     {breakeven_units:.0f}"
        )

if __name__ == "__main__":
    app = ProductCalculatorApp()
    app.mainloop()