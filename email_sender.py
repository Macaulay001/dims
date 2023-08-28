import tkinter as tk
from tkinter import ttk, filedialog
import email, smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from tkinter import messagebox



def send_emails():
    
    sender_email = username_entry.get()
    password = password_entry.get()
    email_subject = subject_entry.get()
    body = body_text.get("1.0", tk.END).strip()
    emails = email_list_text.get("1.0", tk.END).strip().split('\n')
    
    if not (sender_email and password and body and emails and documents_paths):
        messagebox.showerror("Error", "Please provide all necessary inputs.")
        return
    messagebox.showerror("Success", "Press Okay to confirm sending emails.")
    context = ssl._create_default_https_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        total_emails = len(emails)
        for index, receiver_email in enumerate(emails):
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = email_subject if email_subject else "Interest in Advertised Job Position"
            message.attach(MIMEText(body, "plain"))
            for doc_path in documents_paths:
                with open(doc_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(doc_path)}",)
                message.attach(part)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            progress_text = f"{index + 1} emails of {total_emails} emails sent"
            progress_label["text"] = progress_text
            root.update_idletasks()
            time.sleep(1)
    messagebox.showinfo("Success", "Emails sent successfully!")

def select_documents():
    file_paths = filedialog.askopenfilenames(title="Select documents")
    documents_paths.extend(file_paths)
    docs_names = ', '.join(os.path.basename(fp) for fp in file_paths)
    existing_text = documents_label["text"]
    if existing_text:
        documents_label["text"] = existing_text + ', ' + docs_names
    else:
        documents_label["text"] = docs_names

def toggle_password_visibility():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        show_pass_button.configure(text="Hide Password")
    else:
        password_entry.configure(show="*")
        show_pass_button.configure(text="Show Password")

def update_line_count(event=None):
    line_count = email_list_text.index(tk.END).split('.')[0]
    line_count = int(line_count) - 1 
    line_count_label["text"] = f"Lines: {line_count}"

documents_paths = []

root = tk.Tk()
root.title("Email Sender App")
root.geometry("700x500")

root.configure(bg="#e6f7ff")

style = ttk.Style()
style.configure("TButton", background="blue", foreground="white")

content_frame = ttk.Frame(root)
content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

username_label = ttk.Label(content_frame, text="Username:", background="#e6f7ff")
username_label.grid(row=0, column=0, sticky='w', pady=5)
username_entry = ttk.Entry(content_frame, width=40, background="white")
username_entry.grid(row=0, column=1, pady=5)

password_label = ttk.Label(content_frame, text="Password:", background="#e6f7ff")
password_label.grid(row=1, column=0, sticky='w', pady=5)
password_entry = ttk.Entry(content_frame, show="*", width=30, background="white")
password_entry.grid(row=1, column=1, pady=5, sticky='w')
show_pass_button = ttk.Button(content_frame, text="Show Password", command=toggle_password_visibility)
show_pass_button.grid(row=1, column=2, pady=5, sticky='w')

subject_label = ttk.Label(content_frame, text="Email Subject:", background="#e6f7ff")
subject_label.grid(row=2, column=0, sticky='w', pady=5)
subject_entry = ttk.Entry(content_frame, width=40, background="white")
subject_entry.grid(row=2, column=1, pady=5)

body_label = ttk.Label(content_frame, text="Email Body:", background="#e6f7ff")
body_label.grid(row=3, column=0, sticky='w', pady=5)
body_text = tk.Text(content_frame, height=5, width=40, background="black")
body_text.grid(row=3, column=1, pady=5)

email_list_label = ttk.Label(content_frame, text="Email List:", background="#e6f7ff")
email_list_label.grid(row=4, column=0, sticky='w', pady=5)
email_list_text = tk.Text(content_frame, height=5, width=40, background="black")
email_list_text.grid(row=4, column=1, pady=5)
email_list_text.bind("<KeyRelease>", update_line_count)

line_count_label = ttk.Label(content_frame, text="Lines: 0", background="#e6f7ff")
line_count_label.grid(row=5, column=1, sticky="w")

documents_button = ttk.Button(content_frame, text="Add attachments", command=select_documents)
documents_button.grid(row=6, column=0, pady=5, sticky='w')
documents_label = ttk.Label(content_frame, text="", background="#e6f7ff")
documents_label.grid(row=6, column=1, pady=5, sticky="w")

send_button = ttk.Button(content_frame, text="Send", command=send_emails)
send_button.grid(row=7, column=2, pady=5, sticky='w')
progress_label = ttk.Label(content_frame, text="", background="#e6f7ff")
progress_label.grid(row=8, column=1, pady=5, sticky='w')

root.mainloop()
