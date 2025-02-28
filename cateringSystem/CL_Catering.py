from tkinter import *
from tkinter import messagebox, ttk
from fpdf import FPDF
from datetime import datetime

# Function to generate invoice using FPDF
def generate_invoice(customer_name, phone_number, address, items, is_taxable):
    invoice_number = datetime.now().strftime("%Y%m%d%H%M%S")
    subtotal = sum(item['Total'] for item in items)
    tax_rate = 0.0825  # 8.25% tax
    tax_amount = subtotal * tax_rate if is_taxable else 0
    total_amount = subtotal + tax_amount

    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add logo at the top (replace with the full path to your logo file)
    pdf.image('C:/Users/12146/Desktop/elCielitoLindo/cateringSystem/logo.png', x=50, y=10, w=110)  # Centered and bigger logo
    pdf.ln(40)  # Move down to leave space after the logo

    # Add invoice title
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    pdf.ln(10)

    # Add invoice details (customer info on the left, invoice number and date on the right)
    pdf.set_font("Arial", "", 12)
    
    # Left side: Customer information
    pdf.cell(100, 10, txt=f"BILLED TO:", ln=0, align="L")
    # Right side: Invoice number and date
    pdf.cell(100, 10, txt=f"Invoice Number: {invoice_number}", ln=1, align="R")
    
    pdf.cell(100, 10, txt=f"Customer Name: {customer_name}", ln=0, align="L")
    pdf.cell(100, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align="R")
    
    pdf.cell(100, 10, txt=f"Phone Number: {phone_number}", ln=0, align="L")
    pdf.cell(100, 10, txt="", ln=1, align="R")  # Empty cell for alignment
    
    pdf.cell(100, 10, txt=f"Address: {address}", ln=0, align="L")
    pdf.cell(100, 10, txt="", ln=1, align="R")  # Empty cell for alignment
    
    pdf.ln(10)  # Add some space before the table

    # Add table headers
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)  # Light blue background for headers
    pdf.cell(80, 10, txt="Item", border=1, fill=True, align="C")
    pdf.cell(30, 10, txt="Quantity", border=1, fill=True, align="C")
    pdf.cell(30, 10, txt="Price", border=1, fill=True, align="C")
    pdf.cell(30, 10, txt="Total", border=1, fill=True, align="C", ln=True)

    # Add table rows
    pdf.set_font("Arial", "", 12)
    for item in items:
        pdf.cell(80, 10, txt=item['Item'], border=1, align="L")
        pdf.cell(30, 10, txt=str(item['Quantity']), border=1, align="C")
        pdf.cell(30, 10, txt=f"${item['Price']:.2f}", border=1, align="C")
        pdf.cell(30, 10, txt=f"${item['Total']:.2f}", border=1, align="C", ln=True)

    # Add subtotal, tax, and total amount
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Subtotal: ${subtotal:.2f}", ln=True, align="R")
    pdf.cell(200, 10, txt=f"Tax (8.25%): ${tax_amount:.2f}", ln=True, align="R")  # Always show tax
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Total Amount: ${total_amount:.2f}", ln=True, align="R")

    # Add a thank-you message
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, txt="Thank you for choosing El Cielito Lindo Catering!", ln=True, align="C")
    pdf.cell(200, 10, txt="Contact us at (682) 250-2443  or elCielitoLindoDFW@gmail.com", ln=True, align="C")

    # Save the PDF
    invoice_filename = f"Invoice_{invoice_number}.pdf"
    pdf.output(invoice_filename)
    messagebox.showinfo("Success", f"Invoice generated: {invoice_filename}")

# Function to handle the "Submit Order" button click
def submit_order():
    customer_name = entry_name.get()
    phone_number = entry_phone.get()
    address = entry_address.get()
    items = []
    is_taxable = tax_var.get()  # Get the value of the tax checkbox

    # Get items from the listbox
    for item in listbox_items.get(0, END):
        item_name, quantity, price = item.split(" - ")
        items.append({
            'Item': item_name,
            'Quantity': int(quantity),
            'Price': float(price),
            'Total': int(quantity) * float(price)
        })

    if customer_name and phone_number and address and items:
        generate_invoice(customer_name, phone_number, address, items, is_taxable)
        listbox_items.delete(0, END)  # Clear the listbox after submission
    else:
        messagebox.showwarning("Input Error", "Please enter customer name, phone number, address, and at least one item.")

# Function to add an item to the listbox
def add_item():
    item_name = entry_item.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    # Validate inputs
    try:
        quantity = int(quantity)
        price = float(price)
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive numbers.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numbers for quantity and price.")
        return

    if item_name and quantity and price:
        listbox_items.insert(END, f"{item_name} - {quantity} - {price}")
        entry_item.delete(0, END)
        entry_quantity.delete(0, END)
        entry_price.delete(0, END)
    else:
        messagebox.showwarning("Input Error", "Please fill in all item fields.")

# Create the main window
root = Tk()
root.title("El Cielito Lindo Catering")
root.geometry("400x600")

# Use ttk for themed widgets
style = ttk.Style()
style.theme_use("clam")  # Choose a theme: 'clam', 'alt', 'default', etc.

# Customer Name
ttk.Label(root, text="Customer Name:").grid(row=0, column=0, padx=10, pady=10)
entry_name = ttk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=10)

# Customer Phone Number
ttk.Label(root, text="Phone Number:").grid(row=1, column=0, padx=10, pady=10)
entry_phone = ttk.Entry(root, width=30)
entry_phone.grid(row=1, column=1, padx=10, pady=10)

# Customer Address
ttk.Label(root, text="Address:").grid(row=2, column=0, padx=10, pady=10)
entry_address = ttk.Entry(root, width=30)
entry_address.grid(row=2, column=1, padx=10, pady=10)

# Item Details
ttk.Label(root, text="Item:").grid(row=3, column=0, padx=10, pady=10)
entry_item = ttk.Entry(root, width=30)
entry_item.grid(row=3, column=1, padx=10, pady=10)

ttk.Label(root, text="Quantity:").grid(row=4, column=0, padx=10, pady=10)
entry_quantity = ttk.Entry(root, width=30)
entry_quantity.grid(row=4, column=1, padx=10, pady=10)

ttk.Label(root, text="Price:").grid(row=5, column=0, padx=10, pady=10)
entry_price = ttk.Entry(root, width=30)
entry_price.grid(row=5, column=1, padx=10, pady=10)

# Add Item Button
ttk.Button(root, text="Add Item", command=add_item).grid(row=6, column=1, padx=10, pady=10)

# Listbox to display items
listbox_items = Listbox(root, width=50, height=10)
listbox_items.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Tax Checkbox
tax_var = BooleanVar()  # Variable to store the checkbox state
ttk.Checkbutton(root, text="Taxable Order (8.25% tax)", variable=tax_var).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Submit Order Button
ttk.Button(root, text="Submit Order", command=submit_order).grid(row=9, column=0, padx=10, pady=10)

# Exit Button
ttk.Button(root, text="Exit", command=root.quit).grid(row=9, column=1, padx=10, pady=10)

# Run the application
root.mainloop()