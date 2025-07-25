import tkinter as tk
from tkinter import ttk, messagebox

class ProductCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Calculator")
        self.geometry("600x400")
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

        ttk.Label(self, text="Raw Materials", font=("Arial", 16)).pack(pady=10)
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(pady=10)

        self.entries = []
        self.build_initial_rows()

        ttk.Button(self, text="Add Row", command=self.add_row).pack(pady=5)
        ttk.Button(self, text="Next", command=self.save_and_continue).pack(pady=10)

    def build_initial_rows(self):
        headers = ["Component", "Qty per Batch", "Unit Cost"]
        for col, text in enumerate(headers):
            ttk.Label(self.entries_frame, text=text).grid(row=0, column=col)

        for _ in range(5):
            self.add_row()

    def add_row(self):
        row = len(self.entries) + 1
        component = ttk.Entry(self.entries_frame, width=20)
        qty = ttk.Entry(self.entries_frame, width=10)
        cost = ttk.Entry(self.entries_frame, width=10)
        component.grid(row=row, column=0, padx=5, pady=2)
        qty.grid(row=row, column=1, padx=5, pady=2)
        cost.grid(row=row, column=2, padx=5, pady=2)
        self.entries.append((component, qty, cost))

    def save_and_continue(self):
        self.controller.raw_materials = []
        for comp, qty, cost in self.entries:
            if comp.get() and qty.get() and cost.get():
                try:
                    self.controller.raw_materials.append({
                        "component": comp.get(),
                        "qty": float(qty.get()),
                        "cost": float(cost.get())
                    })
                except ValueError:
                    messagebox.showerror("Input Error", "All material quantities and costs must be numbers.")
                    return
        if not self.controller.raw_materials:
            messagebox.showerror("Input Error", "Please enter at least one valid material row.")
            return
        self.controller.show_frame("LaborPage")

class LaborPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Allocated Labor", font=("Arial", 16)).pack(pady=10)
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(pady=10)

        self.entries = []
        self.build_initial_rows()

        ttk.Button(self, text="Add Row", command=self.add_row).pack(pady=5)
        ttk.Button(self, text="Next", command=self.save_and_continue).pack(pady=10)

    def build_initial_rows(self):
        headers = ["Position", "Hours per Batch", "Hourly Rate"]
        for col, text in enumerate(headers):
            ttk.Label(self.entries_frame, text=text).grid(row=0, column=col)

        for _ in range(5):
            self.add_row()

    def add_row(self):
        row = len(self.entries) + 1
        position = ttk.Entry(self.entries_frame, width=20)
        hours = ttk.Entry(self.entries_frame, width=10)
        rate = ttk.Entry(self.entries_frame, width=10)
        position.grid(row=row, column=0, padx=5, pady=2)
        hours.grid(row=row, column=1, padx=5, pady=2)
        rate.grid(row=row, column=2, padx=5, pady=2)
        self.entries.append((position, hours, rate))

    def save_and_continue(self):
        self.controller.labor_data = []
        for pos, hrs, rate in self.entries:
            if pos.get() and hrs.get() and rate.get():
                try:
                    self.controller.labor_data.append({
                        "position": pos.get(),
                        "hours": float(hrs.get()),
                        "rate": float(rate.get())
                    })
                except ValueError:
                    messagebox.showerror("Input Error", "All hours and rates must be numbers.")
                    return
        if not self.controller.labor_data:
            messagebox.showerror("Input Error", "Please enter at least one valid labor row.")
            return
        self.controller.show_frame("AdditionalCostsPage")

class AdditionalCostsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Additional Inputs", font=("Arial", 16)).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="R&D / Setup Cost ($):").grid(row=0, column=0, sticky=tk.E)
        self.rnd_entry = ttk.Entry(form_frame)
        self.rnd_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Units per Batch:").grid(row=1, column=0, sticky=tk.E)
        self.units_entry = ttk.Entry(form_frame)
        self.units_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Price per Unit ($):").grid(row=2, column=0, sticky=tk.E)
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Expected Units Sold:").grid(row=3, column=0, sticky=tk.E)
        self.sold_entry = ttk.Entry(form_frame)
        self.sold_entry.grid(row=3, column=1)

        ttk.Button(self, text="Calculate", command=self.save_and_continue).pack(pady=10)

    def save_and_continue(self):
        try:
            self.controller.additional_costs = {
                "rnd_cost": float(self.rnd_entry.get()),
                "units_per_batch": int(self.units_entry.get()),
                "price_per_unit": float(self.price_entry.get()),
                "units_sold": int(self.sold_entry.get())
            }
            self.controller.show_frame("ResultsPage")
        except ValueError:
            messagebox.showerror("Input Error", "Please fill in all fields with valid numbers.")

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.result_text = tk.StringVar()

        ttk.Label(self, text="Financial Results", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self, textvariable=self.result_text, font=("Courier", 12), justify="left").pack(pady=10)
        ttk.Button(self, text="Restart", command=self.prompt_restart).pack(pady=10)

    def prompt_restart(self):
        response = messagebox.askquestion("Restart", "Would you like to start fresh?")
        if response == 'yes':
            self.clear_all_inputs()
        self.controller.show_frame("RawMaterialPage")

    def clear_all_inputs(self):
        # Clear stored data
        self.controller.raw_materials.clear()
        self.controller.labor_data.clear()
        self.controller.additional_costs.clear()

        # Clear input fields on all pages
        for entry_group in self.controller.frames['RawMaterialPage'].entries:
            for entry in entry_group:
                entry.delete(0, tk.END)

        for entry_group in self.controller.frames['LaborPage'].entries:
            for entry in entry_group:
                entry.delete(0, tk.END)

        add_page = self.controller.frames['AdditionalCostsPage']
        add_page.rnd_entry.delete(0, tk.END)
        add_page.units_entry.delete(0, tk.END)
        add_page.price_entry.delete(0, tk.END)
        add_page.sold_entry.delete(0, tk.END)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.calculate_results()

    def calculate_results(self):
        materials_cost = sum(item['qty'] * item['cost'] for item in self.controller.raw_materials)
        labor_cost = sum(item['hours'] * item['rate'] for item in self.controller.labor_data)
        rnd_cost = self.controller.additional_costs["rnd_cost"]
        units_per_batch = self.controller.additional_costs["units_per_batch"]
        price_per_unit = self.controller.additional_costs["price_per_unit"]
        units_sold = self.controller.additional_costs["units_sold"]

        total_batch_cost = materials_cost + labor_cost + rnd_cost
        cost_per_unit = total_batch_cost / units_per_batch
        total_cost = units_sold * cost_per_unit
        revenue = units_sold * price_per_unit
        profit = revenue - total_cost
        roi = (profit / total_cost) * 100 if total_cost else 0
        breakeven_units = total_batch_cost / price_per_unit if price_per_unit else 0

        self.result_text.set(
            f"Total Batch Cost:   ${total_batch_cost:,.2f}\n"
            f"Cost per Unit:      ${cost_per_unit:,.2f}\n"
            f"Total Revenue:      ${revenue:,.2f}\n"
            f"Total Cost:         ${total_cost:,.2f}\n"
            f"Profit:             ${profit:,.2f}\n"
            f"ROI:                {roi:.2f}%\n"
            f"Breakeven Units:    {breakeven_units:.0f}"
        )

# Run the app
if __name__ == "__main__":
    app = ProductCalculatorApp()
    app.mainloop()
