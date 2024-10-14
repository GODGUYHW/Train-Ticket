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
        
        # เก็บสถิติของสถานีต้นทางและปลายทางเป็น tuple
        self.history = []  # List to store (start_station, end_station) as tuples
        
        # เก็บรายรับและเงินทอน
        self.revenue_list = []  # List to store total revenue from transactions
        self.change_list = []   # List to store change given to customers
        self.ticket_count_list = []  # List to store the number of tickets per transaction
        self.total_payment = 0  # Track total amount paid

        # สร้างหน้าต่างหลักของโปรแกรม
        self.root = tk.Tk()
        self.root.title("ระบบขายตั๋วรถไฟ")

        # สถานีต้นทาง
        tk.Label(self.root, text="สถานีต้นทาง:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_station_var = tk.StringVar()
        self.start_combobox = ttk.Combobox(self.root, textvariable=self.start_station_var)
        self.start_combobox['values'] = self.stations
        self.start_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.start_combobox.bind("<<ComboboxSelected>>", self.update_end_stations)

        # สถานีปลายทาง
        tk.Label(self.root, text="สถานีปลายทาง:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_station_var = tk.StringVar()
        self.end_combobox = ttk.Combobox(self.root, textvariable=self.end_station_var)
        self.end_combobox['values'] = self.stations
        self.end_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.end_combobox.bind("<<ComboboxSelected>>", self.show_distance_and_fare)

        # แสดงระยะทาง
        self.distance_label = tk.Label(self.root, text="ระยะทาง: -")
        self.distance_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # แสดงค่าโดยสาร
        self.fare_label = tk.Label(self.root, text="ค่าโดยสาร: -")
        self.fare_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # เลือกจำนวนตั๋ว (จำกัดจำนวนสูงสุด 4 ใบ)
        tk.Label(self.root, text="จำนวนตั๋ว:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.ticket_count_var = tk.IntVar(value=1)
        
        # Set validation to limit the Spinbox to a maximum of 4 tickets
        self.ticket_count_spinbox = ttk.Spinbox(self.root, from_=1, to=4, textvariable=self.ticket_count_var, width=5, 
                                                command=self.show_distance_and_fare, validate="key", validatecommand=(self.root.register(self.validate_ticket_count), '%P'))
        self.ticket_count_spinbox.grid(row=4, column=1, padx=10, pady=5)

        # จำนวนเงินที่จ่าย
        tk.Label(self.root, text="จำนวนเงินที่จ่าย:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.payment_var = tk.StringVar()
        self.payment_entry = ttk.Entry(self.root, textvariable=self.payment_var)
        self.payment_entry.grid(row=5, column=1, padx=10, pady=5)

        # แสดงยอดเงินที่ยังขาดอยู่
        self.remaining_label = tk.Label(self.root, text="ยอดที่ยังขาดอยู่: -")
        self.remaining_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # แสดงสถานะการซื้อตั๋ว
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # ปุ่มซื้อตั๋ว
        self.buy_button = ttk.Button(self.root, text="ซื้อตั๋ว", command=self.buy_ticket)
        self.buy_button.grid(row=8, column=0, columnspan=2, pady=10)

        # ปุ่มดูประวัติ
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

    def show_distance_and_fare(self, event=None):
        start = self.start_station_var.get()
        end = self.end_station_var.get()
        if start and end:
            distance = self.distances.get((start, end)) or self.distances.get((end, start))
            if distance:
                fare = distance * 2 * self.ticket_count_var.get()  # ค่าโดยสาร = ระยะทาง x 2 บาท x จำนวนตั๋ว
                self.distance_label.config(text=f"ระยะทาง: {distance} กม.")
                self.fare_label.config(text=f"ค่าโดยสาร: {fare} บาท")
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

        # ตรวจสอบการกรอกข้อมูล
        if not payment.isdigit():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่จำนวนเงินที่เป็นตัวเลข")
            return

        payment = int(payment)
        self.total_payment += payment  # Add to the total payment
        price = self.get_ticket_price(start, end)

        if price == 0:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่มีเส้นทางจาก {start} ไปยัง {end}")
        elif self.total_payment < price:
            remaining = price - self.total_payment
            self.remaining_label.config(text=f"ยอดที่ยังขาดอยู่: {remaining} บาท")
            messagebox.showinfo("เพิ่มเงิน", f"คุณต้องเพิ่มอีก {remaining} บาท")
        else:
            change = self.total_payment - price
            # เก็บสถิติการเดินทาง
            self.history.append((start, end))  # Store (start_station, end_station) as a tuple
            # เก็บรายรับและเงินทอน
            self.revenue_list.append(price)
            self.change_list.append(change)
            self.ticket_count_list.append(self.ticket_count_var.get())  # Save number of tickets

            # บันทึกข้อมูลประวัติการเดินทางลงในไฟล์ .txt
            self.write_history_to_file(start, end, price, self.total_payment, change, self.ticket_count_var.get())

            # Update UI to show success status
            self.status_label.config(text="ซื้อตั๋วสำเร็จ!", fg="green")
            self.total_payment = 0  # Reset total payment
            self.payment_var.set("")  # ล้างข้อมูลการจ่ายเงิน
            self.remaining_label.config(text="ยอดที่ยังขาดอยู่: -")  # Reset remaining label

    def write_history_to_file(self, start, end, price, payment, change, ticket_count):
        with open("history.txt", "a", encoding="utf-8") as file:
            file.write(f"สถานีต้นทาง: {start}, สถานีปลายทาง: {end}, จำนวนตั๋ว: {ticket_count}, ราคา: {price} บาท, ชำระเงิน: {payment} บาท, ทอนเงิน: {change} บาท\n")

    def show_history(self):
        # Create a new window to show the history
        history_window = tk.Toplevel(self.root)
        history_window.title("ประวัติการซื้อตั๋ว")

        # Add a listbox to show history details
        history_listbox = tk.Listbox(history_window, width=80, height=20)
        history_listbox.pack(padx=10, pady=10)

        # Populate the listbox with the history
        for i, (route, revenue, change, ticket_count) in enumerate(zip(self.history, self.revenue_list, self.change_list, self.ticket_count_list)):
            start, end = route
            history_listbox.insert(tk.END, f"{i+1}. สถานีต้นทาง: {start}, สถานีปลายทาง: {end}, จำนวนตั๋ว: {ticket_count}, ราคา: {revenue} บาท, ทอนเงิน: {change} บาท")

if __name__ == "__main__":
    TrainTicketSystem()
