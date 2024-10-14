import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TrainTicketSystem:
    def __init__(self):
        self.stations = ["สถานี A", "สถานี B", "สถานี C", "สถานี D"]
        self.distances = {
            ("สถานี A", "สถานี B"): 10,
            ("สถานี B", "สถานี C"): 15,
            ("สถานี C", "สถานี D"): 20,
            ("สถานี A", "สถานี C"): 25,
            ("สถานี A", "สถานี D"): 45,
            ("สถานี B", "สถานี D"): 35,
        }
        
        # Store history as an empty tuple
        self.history = ()  # Tuple to store (start_station, end_station, ticket_count, fare, payment, change)
        
        # Initialize total payment and histories
        self.total_payment = 0
        self.income_history = []  # List to store income
        self.change_history = []  # List to store change
        
        # Create the main window of the program
        self.root = tk.Tk()
        self.root.title("ระบบขายตั๋วรถไฟ")

        # Start Station
        tk.Label(self.root, text="สถานีต้นทาง:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_station_var = tk.StringVar()
        self.start_combobox = ttk.Combobox(self.root, textvariable=self.start_station_var)
        self.start_combobox['values'] = self.stations
        self.start_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.start_combobox.bind("<<ComboboxSelected>>", self.update_end_stations)

        # End Station
        tk.Label(self.root, text="สถานีปลายทาง:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_station_var = tk.StringVar()
        self.end_combobox = ttk.Combobox(self.root, textvariable=self.end_station_var)
        self.end_combobox['values'] = self.stations
        self.end_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.end_combobox.bind("<<ComboboxSelected>>", self.show_distance_and_fare)

        # Show distance
        self.distance_label = tk.Label(self.root, text="ระยะทาง: -")
        self.distance_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Show fare
        self.fare_label = tk.Label(self.root, text="ค่าโดยสาร: -")
        self.fare_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Select number of tickets (max 4)
        tk.Label(self.root, text="จำนวนตั๋ว:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.ticket_count_var = tk.IntVar(value=1)
        
        # Set validation to limit the Spinbox to a maximum of 4 tickets
        self.ticket_count_spinbox = ttk.Spinbox(self.root, from_=1, to=4, textvariable=self.ticket_count_var, width=5, 
                                                command=self.show_distance_and_fare, validate="key", validatecommand=(self.root.register(self.validate_ticket_count), '%P'))
        self.ticket_count_spinbox.grid(row=4, column=1, padx=10, pady=5)

        # Amount paid
        tk.Label(self.root, text="จำนวนเงินที่จ่าย:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.payment_var = tk.StringVar()
        self.payment_entry = ttk.Entry(self.root, textvariable=self.payment_var)
        self.payment_entry.grid(row=5, column=1, padx=10, pady=5)

        # Show remaining amount
        self.remaining_label = tk.Label(self.root, text="ยอดที่ยังขาดอยู่: -")
        self.remaining_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Show purchase status
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # Buy ticket button
        self.buy_button = ttk.Button(self.root, text="ซื้อตั๋ว", command=self.buy_ticket)
        self.buy_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Show history button
        self.history_button = ttk.Button(self.root, text="ดูประวัติการซื้อตั๋ว", command=self.show_history)
        self.history_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def validate_ticket_count(self, value):
        """ Validate that ticket count doesn't exceed 4 and is a valid number """
        if value.isdigit():
            count = int(value)
            return 1 <= count <= 4
        return False

    def update_end_stations(self, event=None):
        start = self.start_station_var.get()
        if start:
            end_stations = [station for station in self.stations if station != start]
            self.end_combobox['values'] = end_stations
            self.end_station_var.set('')
            self.distance_label.config(text="ระยะทาง: -")
            self.fare_label.config(text="ค่าโดยสาร: -")
            self.remaining_label.config(text="ยอดที่ยังขาดอยู่: -")
            self.status_label.config(text="")  # Reset status label
            self.total_payment = 0  # Reset total payment when changing stations

    def show_distance_and_fare(self, event=None):
        start = self.start_station_var.get()
        end = self.end_station_var.get()
        if start and end:
            distance = self.distances.get((start, end)) or self.distances.get((end, start))
            if distance:
                fare = distance * 2 * self.ticket_count_var.get()  # ค่าโดยสาร = ระยะทาง x 2 บาท x จำนวนตั๋ว
                self.distance_label.config(text=f"ระยะทาง: {distance} กม.")
                self.fare_label.config(text=f"ค่าโดยสาร: {fare} บาท")
                self.status_label.config(text="")  # Clear status label when distance or fare changes
            else:
                self.distance_label.config(text="ระยะทาง: ไม่พบเส้นทาง")
                self.fare_label.config(text="ค่าโดยสาร: -")

    def get_ticket_price(self, start, end):
        if (start, end) in self.distances:
            return self.distances[(start, end)] * 2 * self.ticket_count_var.get()  # จำนวนตั๋ว * ค่าโดยสารต่อใบ
        elif (end, start) in self.distances:
            return self.distances[(end, start)] * 2 * self.ticket_count_var.get()
        return 0

    def buy_ticket(self):
        start = self.start_station_var.get()
        end = self.end_station_var.get()
        payment = self.payment_var.get()

        # Validate input
        if not payment.isdigit():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่จำนวนเงินที่เป็นตัวเลข")
            return

        payment = int(payment)
        price = self.get_ticket_price(start, end)

        if price == 0:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่มีเส้นทางจาก {start} ไปยัง {end}")
            return

        # Update total payment
        self.total_payment += payment
        
        # Check if total payment is less than required
        if self.total_payment < price:
            remaining = price - self.total_payment
            self.remaining_label.config(text=f"ยอดที่ยังขาดอยู่: {remaining} บาท")
            messagebox.showinfo("เพิ่มเงิน", f"คุณต้องเพิ่มอีก {remaining} บาท")
            self.payment_var.set("")  # Clear the payment field for new entry
            return

        # If total payment exceeds price, calculate change
        change = self.total_payment - price
        
        # Add to income and change histories
        self.income_history.append(price)
        self.change_history.append(change)

        # Create a new history tuple that includes the new transaction
        self.history += ((start, end, self.ticket_count_var.get(), price, self.total_payment, change),)

        # Save the transaction to the history file
        self.write_history_to_file(start, end, price, self.total_payment, change, self.ticket_count_var.get())

        # Update UI to show success status
        self.status_label.config(text="ซื้อตั๋วสำเร็จ!", fg="green")
        self.remaining_label.config(text="ยอดที่ยังขาดอยู่: -")
        messagebox.showinfo("การชำระเงิน", f"คุณได้ทอนเงิน {change} บาท")

        # Reset total payment after successful transaction
        self.total_payment = 0
        self.payment_var.set("")  # Clear the payment field

    def write_history_to_file(self, start, end, fare, payment, change, ticket_count):
        with open("ticket_history.txt", "a", encoding="utf-8") as file:
            file.write(f"สถานีต้นทาง: {start}, สถานีปลายทาง: {end}, จำนวนตั๋ว: {ticket_count}, ราคา: {fare} บาท, ชำระเงิน: {payment} บาท, ทอนเงิน: {change} บาท\n")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("ประวัติการซื้อตั๋ว")
        
        # If history is empty
        if not self.history:
            messagebox.showinfo("ประวัติการซื้อตั๋ว", "ยังไม่มีประวัติการซื้อตั๋ว")
            return
        
        # Display history
        history_text = "\n".join([
            f"สถานีต้นทาง: {entry[0]}, สถานีปลายทาง: {entry[1]}, จำนวนตั๋ว: {entry[2]}, ราคา: {entry[3]} บาท, ชำระเงิน: {entry[4]} บาท, ทอนเงิน: {entry[5]} บาท"
            for entry in self.history
        ])
        
        history_label = tk.Label(history_window, text=history_text, justify="left")
        history_label.pack(padx=10, pady=10)

        # Button to close the history window
        close_button = ttk.Button(history_window, text="ปิด", command=history_window.destroy)
        close_button.pack(pady=5)

if __name__ == "__main__":
    TrainTicketSystem()
