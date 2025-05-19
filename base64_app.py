#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import base64
import random
import string
import csv
from datetime import datetime
import os
import subprocess
import platform

class Base64ToolApp:
    STATUS_SUCCESS_COLOR = "green"
    STATUS_ERROR_COLOR = "red"
    STATUS_DEFAULT_COLOR = "black"
    def __init__(self, master):
        self.master = master
        master.title("非常母牛-密码生成器")
        master.geometry("600x500") # Increased height for status bar

        self.notebook = ttk.Notebook(master)

        # Base64 Tab
        self.base64_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.base64_frame, text='Base64 编解码')
        self.create_base64_widgets()

        # Password Generator Tab
        self.password_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.password_frame, text='密码生成器')
        self.create_password_widgets()

        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)

        # Status Bar
        self.status_bar = tk.Label(master, text="准备就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_base64_widgets(self):
        # Input Label and Text Area
        ttk.Label(self.base64_frame, text="输入文本:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.base64_input_text = tk.Text(self.base64_frame, height=5, width=60)
        self.base64_input_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Buttons
        self.encode_button = ttk.Button(self.base64_frame, text="编码 (Encode)", command=self.encode_base64)
        self.encode_button.grid(row=2, column=0, padx=5, pady=10, sticky='ew') # Adjusted row

        self.decode_button = ttk.Button(self.base64_frame, text="解码 (Decode)", command=self.decode_base64)
        self.decode_button.grid(row=2, column=1, padx=5, pady=10, sticky='ew') # Adjusted row

        # Output Label and Text Area
        ttk.Label(self.base64_frame, text="输出结果:").grid(row=3, column=0, padx=5, pady=5, sticky='w') # Adjusted row
        self.base64_output_text = tk.Text(self.base64_frame, height=5, width=60, state='disabled')
        self.base64_output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5) # Adjusted row
        
        # Clear Button
        self.clear_base64_button = ttk.Button(self.base64_frame, text="清空", command=self.clear_base64_fields)
        self.clear_base64_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky='ew') # Adjusted row

    def encode_base64(self):
        try:
            input_string = self.base64_input_text.get("1.0", tk.END).strip()
            if not input_string:
                messagebox.showwarning("输入错误", "请输入需要编码的文本")
                return
            encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
            encoded_string = encoded_bytes.decode('utf-8')
            self.base64_output_text.config(state='normal')
            self.base64_output_text.delete("1.0", tk.END)
            self.base64_output_text.insert(tk.END, encoded_string)
            self.base64_output_text.config(state='disabled')
            self.update_status_bar("编码成功")
        except Exception as e:
            messagebox.showerror("编码错误", f"发生错误: {e}")

    def decode_base64(self):
        try:
            input_string = self.base64_input_text.get("1.0", tk.END).strip()

            if not input_string:
                messagebox.showwarning("输入错误", "请输入需要解码的文本")
                return

            # Add padding if necessary for base64 decoding
            missing_padding = len(input_string) % 4
            if missing_padding:
                input_string += '=' * (4 - missing_padding)

            decoded_bytes = base64.b64decode(input_string.encode('utf-8'))
            decoded_string = decoded_bytes.decode('utf-8')
            self.base64_output_text.config(state='normal')
            self.base64_output_text.delete("1.0", tk.END)
            self.base64_output_text.insert(tk.END, decoded_string)
            self.base64_output_text.config(state='disabled')
            self.update_status_bar("解码成功")
        except base64.binascii.Error:
            messagebox.showerror("解码错误", "无效的Base64编码字符串")
            self.update_status_bar("解码错误: 无效的Base64编码字符串", is_error=True)
        except UnicodeDecodeError:
            messagebox.showerror("解码错误", "解码后的文本不是有效的UTF-8编码")
            self.update_status_bar("解码错误: 解码后的文本不是有效的UTF-8编码", is_error=True)
        except Exception as e:
            messagebox.showerror("解码错误", f"发生未知错误: {e}")
            self.update_status_bar(f"解码错误: {e}", is_error=True)

    def clear_base64_fields(self):
        self.base64_input_text.delete("1.0", tk.END)
        self.base64_input_text.delete("1.0", tk.END)
        self.base64_output_text.config(state='normal')
        self.base64_output_text.delete("1.0", tk.END)
        self.base64_output_text.config(state='disabled')
        self.update_status_bar("Base64字段已清空")

    def create_password_widgets(self):
        options_frame = ttk.LabelFrame(self.password_frame, text="密码选项")
        options_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="包含大写字母 (A-Z)", variable=self.use_uppercase).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(options_frame, text="包含小写字母 (a-z)", variable=self.use_lowercase).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(options_frame, text="包含数字 (0-9)", variable=self.use_digits).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(options_frame, text="包含特殊字符 (!@#$%^&*)", variable=self.use_special).grid(row=3, column=0, sticky='w', padx=5, pady=2)

        ttk.Label(options_frame, text="密码长度:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.password_length = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(options_frame, from_=4, to_=64, textvariable=self.password_length, width=5)
        self.length_spinbox.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        self.generate_button = ttk.Button(self.password_frame, text="生成10个密码", command=self.generate_passwords_batch)
        self.generate_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        # Frame for displaying multiple passwords
        self.passwords_display_frame = ttk.Frame(self.password_frame)
        self.passwords_display_frame.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        self.password_frame.grid_rowconfigure(2, weight=1)
        self.password_frame.grid_columnconfigure(0, weight=1)

        # Canvas and Scrollbar for password list
        self.passwords_canvas = tk.Canvas(self.passwords_display_frame)
        self.passwords_scrollbar = ttk.Scrollbar(self.passwords_display_frame, orient="vertical", command=self.passwords_canvas.yview)
        self.scrollable_passwords_frame = ttk.Frame(self.passwords_canvas)

        self.scrollable_passwords_frame.bind(
            "<Configure>",
            lambda e: self.passwords_canvas.configure(
                scrollregion=self.passwords_canvas.bbox("all")
            )
        )

        self.passwords_canvas.create_window((0, 0), window=self.scrollable_passwords_frame, anchor="nw")
        self.passwords_canvas.configure(yscrollcommand=self.passwords_scrollbar.set)

        self.passwords_canvas.pack(side="left", fill="both", expand=True)
        self.passwords_scrollbar.pack(side="right", fill="y")

        self.generated_password_widgets = [] # To store (entry, strength_label, copy_button) tuples

        # CSV file path
        self.csv_file_path = os.path.join(os.path.dirname(__file__), "generated_passwords.csv")

        # Open CSV Button
        self.open_csv_button = ttk.Button(self.password_frame, text="打开CSV文件", command=self.open_csv_file)
        self.open_csv_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    def _generate_single_password(self): # Renamed from generate_password
        length = self.password_length.get()
        if length <= 0:
            # This case should ideally be handled by spinbox validation or a check before calling
            return None

        character_set = ""
        if self.use_uppercase.get():
            character_set += string.ascii_uppercase
        if self.use_lowercase.get():
            character_set += string.ascii_lowercase
        if self.use_digits.get():
            character_set += string.digits
        if self.use_special.get():
            character_set += string.punctuation

        if not character_set:
            # This case should ideally be handled by a check before calling
            return None

        password_chars = []
        # Ensure all selected character types are included if possible
        temp_set = list(character_set)
        
        if self.use_uppercase.get() and string.ascii_uppercase in character_set:
            password_chars.append(random.choice(string.ascii_uppercase))
        if self.use_lowercase.get() and string.ascii_lowercase in character_set:
            password_chars.append(random.choice(string.ascii_lowercase))
        if self.use_digits.get() and string.digits in character_set:
            password_chars.append(random.choice(string.digits))
        if self.use_special.get() and string.punctuation in character_set:
            password_chars.append(random.choice(string.punctuation))
        
        # Remove duplicates if length is very small and all types are selected
        password_chars = list(dict.fromkeys(password_chars))
        
        current_len = len(password_chars)
        if current_len > length:
            random.shuffle(password_chars)
            password_chars = password_chars[:length]
        else:
            for _ in range(length - current_len):
                password_chars.append(random.choice(character_set))
        
        random.shuffle(password_chars)
        return "".join(password_chars)

    def check_password_strength(self, password):
        length = len(password)
        score = 0
        feedback = []

        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            feedback.append("太短")

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)

        if has_upper:
            score += 1
        else:
            feedback.append("无大写")
        if has_lower:
            score += 1
        else:
            feedback.append("无小写")
        if has_digit:
            score += 1
        else:
            feedback.append("无数字")
        if has_special:
            score += 1
        else:
            feedback.append("无特殊字符")
        
        num_char_types = sum([has_upper, has_lower, has_digit, has_special])
        if num_char_types >= 3:
            score +=1
        if num_char_types == 4:
            score +=1

        if score >= 7:
            strength = "强"
            color = "green"
        elif score >= 4:
            strength = "中"
            color = "orange"
        else:
            strength = "弱"
            color = "red"
        
        if not feedback and strength == "弱": # Default for very short or simple passwords
             feedback.append("种类单一")

        strength_text = f"{strength} ({', '.join(feedback)})" if feedback else strength
        return strength_text, color

    def save_passwords_to_csv(self, passwords_with_strength):
        file_exists = os.path.isfile(self.csv_file_path)
        try:
            with open(self.csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists or os.path.getsize(self.csv_file_path) == 0:
                    writer.writerow(['日期时间', '密码', '强度'])
                
                now = datetime.now()
                datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
                for password_text, strength in passwords_with_strength:
                    writer.writerow([datetime_str, password_text, strength.split(' ')[0]]) # Save only strength level e.g. "强"
            self.update_status_bar(f"密码已保存到 {os.path.basename(self.csv_file_path)}")
        except IOError as e:
            messagebox.showerror("保存失败", f"无法写入CSV文件: {e}")
            self.update_status_bar(f"CSV保存失败: {e}", is_error=True)

    def generate_passwords_batch(self):
        # Clear previous password widgets
        for widget_set in self.generated_password_widgets:
            widget_set[0].destroy() # Entry
            widget_set[1].destroy() # Strength Label
            widget_set[2].destroy() # Copy Button
        self.generated_password_widgets.clear()
        self.passwords_canvas.yview_moveto(0) # Reset scroll position

        if not (self.use_uppercase.get() or self.use_lowercase.get() or self.use_digits.get() or self.use_special.get()):
            messagebox.showwarning("选项错误", "请至少选择一种字符类型")
            return
        
        if self.password_length.get() <= 0:
            messagebox.showwarning("长度错误", "密码长度必须大于0")
            return

        passwords_for_csv = [] # List of (password, strength_text) tuples
        for i in range(10):
            password = self._generate_single_password()
            if password:
                strength_text, strength_color = self.check_password_strength(password)
                passwords_for_csv.append((password, strength_text))

                row_frame = ttk.Frame(self.scrollable_passwords_frame)
                row_frame.pack(fill='x', pady=2)

                entry = ttk.Entry(row_frame, width=40, font=('TkFixedFont',))
                entry.insert(0, password)
                entry.config(state='readonly')
                entry.pack(side=tk.LEFT, padx=(0,5), expand=True, fill='x')

                strength_label = ttk.Label(row_frame, text=strength_text, foreground=strength_color, width=15, anchor='w')
                strength_label.pack(side=tk.LEFT, padx=5)

                copy_btn = ttk.Button(row_frame, text="复制", width=5, command=lambda p=password: self.copy_individual_password(p))
                copy_btn.pack(side=tk.LEFT, padx=5)
                
                self.generated_password_widgets.append((entry, strength_label, copy_btn))
        
        if passwords_for_csv:
            self.save_passwords_to_csv(passwords_for_csv)
            self.update_status_bar("10个密码已生成并保存到CSV")
        else:
            messagebox.showwarning("生成失败", "未能生成任何密码，请检查选项。")
            self.update_status_bar("密码生成失败，请检查选项", is_error=True)

    def copy_individual_password(self, password_text):
        if password_text:
            self.master.clipboard_clear()
            self.master.clipboard_append(password_text)
            # messagebox.showinfo("已复制", f"密码 '{password_text[:10]}...' 已复制到剪贴板", parent=self.master) # parent to ensure on top
            self.update_status_bar(f"密码 '{password_text[:10]}...' 已复制到剪贴板")
        else:
            messagebox.showwarning("无密码", "无法复制空密码", parent=self.master)
            self.update_status_bar("无法复制空密码", is_error=True)

    def copy_password(self):
        # This method is now obsolete due to individual copy buttons.
        # Kept for now to avoid breaking if called, but should be removed or repurposed.
        # messagebox.showinfo("提示", "请使用密码旁边的复制按钮。")
        pass # Or remove this method entirely

        length = self.password_length.get()
        if length <= 0:
            messagebox.showwarning("长度错误", "密码长度必须大于0")
            return

        character_set = ""
        if self.use_uppercase.get():
            character_set += string.ascii_uppercase
        if self.use_lowercase.get():
            character_set += string.ascii_lowercase
        if self.use_digits.get():
            character_set += string.digits
        if self.use_special.get():
            character_set += string.punctuation

        if not character_set:
            messagebox.showwarning("选项错误", "请至少选择一种字符类型")
            return

        password = []
        # Ensure all selected character types are included
        if self.use_uppercase.get():
            password.append(random.choice(string.ascii_uppercase))
        if self.use_lowercase.get():
            password.append(random.choice(string.ascii_lowercase))
        if self.use_digits.get():
            password.append(random.choice(string.digits))
        if self.use_special.get():
            password.append(random.choice(string.punctuation))
        
        # Fill the rest of the password length
        remaining_length = length - len(password)
        if remaining_length < 0: # If length is too short for all selected types
            password = password[:length] # Truncate to desired length
        else:
            for _ in range(remaining_length):
                password.append(random.choice(character_set))
        
        random.shuffle(password)
        final_password = "".join(password)

        self.generated_password_entry.config(state='normal')
        self.generated_password_entry.delete(0, tk.END)
        self.generated_password_entry.insert(0, final_password)
        self.generated_password_entry.config(state='readonly')

    def copy_password(self):
        password = self.generated_password_entry.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            # messagebox.showinfo("已复制", "密码已复制到剪贴板") # Replaced with status bar
            self.update_status_bar("密码已复制到剪贴板")
        else:
            messagebox.showwarning("无密码", "请先生成密码")
            self.update_status_bar("请先生成密码后再复制", is_error=True)

    def update_status_bar(self, message, is_error=False):
        self.status_bar.config(text=message)
        if is_error:
            self.status_bar.config(fg=self.STATUS_ERROR_COLOR)
        else:
            self.status_bar.config(fg=self.STATUS_SUCCESS_COLOR) # Default to success color for non-error messages
        # Reset to default color after a few seconds
        self.master.after(5000, lambda: self.status_bar.config(text="准备就绪", fg=self.STATUS_DEFAULT_COLOR))

    def open_csv_file(self):
        if not os.path.exists(self.csv_file_path):
            self.update_status_bar(f"CSV文件 '{os.path.basename(self.csv_file_path)}' 不存在", is_error=True)
            messagebox.showwarning("文件未找到", f"文件 {self.csv_file_path} 不存在。请先生成一些密码。")
            return

        try:
            current_platform = platform.system()
            if current_platform == "Windows":
                os.startfile(self.csv_file_path)
            elif current_platform == "Darwin":  # macOS
                subprocess.call(['open', self.csv_file_path])
            else:  # Linux and other Unix-like
                subprocess.call(['xdg-open', self.csv_file_path])
            self.update_status_bar(f"正在尝试打开 {os.path.basename(self.csv_file_path)}")
        except Exception as e:
            self.update_status_bar(f"打开CSV文件失败: {e}", is_error=True)
            messagebox.showerror("打开失败", f"无法打开CSV文件: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Base64ToolApp(root)
    root.mainloop()