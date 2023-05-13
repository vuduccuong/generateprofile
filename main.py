import os
import json
import shutil
import rarfile
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox

class GenerateProfileBrowser:
    def __init__(self, master):
        self.master = master
        master.title('Generate Profile Browsers')
        master.geometry('400x200')
        self.profiles = []
        self.root_folder = os.path.dirname(os.path.abspath(__file__))
        self.import_file = os.path.join(self.root_folder, 'import')
        os.makedirs(self.import_file, exist_ok=True)

        # Tạo label và combobox chọn loại browser
        browser_label = Label(master, text='Loại browser:')
        browser_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.browser_var = StringVar()
        browser_combobox = Combobox(master, textvariable=self.browser_var, values=['Chrome', 'Firefox', 'Edge Dev'], state='readonly')
        browser_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        # import profile có sẵn
        import_button = Button(master, text='Import Profile', command=self.import_file)
        import_button.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        # Tạo label và radiobutton chọn kiểu tạo
        type_label = Label(master, text='Kiểu tạo:')
        type_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.type_var = IntVar()
        new_profile_radio = Radiobutton(master, text='Tạo profile mới', variable=self.type_var, value=1)
        new_profile_radio.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        add_profile_radio = Radiobutton(master, text='Tạo thêm profile', variable=self.type_var, value=2)
        add_profile_radio.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        # Tạo label và spinbox chọn số lượng
        amount_label = Label(master, text='Số lượng:')
        amount_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.amount_var = IntVar()
        amount_spinbox = Spinbox(master, from_=0, to=100, width=5, textvariable=self.amount_var)
        amount_spinbox.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Tạo nút Enter
        enter_button = Button(master, text='Enter', command=self.generate_profiles)
        enter_button.grid(row=3, column=0, padx=10, pady=10, sticky=W)

    def generate_profiles(self):
        # Get selected browser
        browser = self.browser_var.get()

        # Get number of profiles to generate
        num_profiles = self.amount_var.get()

        # Set up Chrome driver options
        chrome_options = Options()

        # Set user data dir to import folder
        chrome_options.add_argument("--user-data-dir={}".format(self.import_file))

        # Initialize Chrome driver
        if browser == "Chrome":
            driver_path = os.path.join(self.root_folder, "chromedriver")
            driver = webdriver.Chrome(driver_path, options=chrome_options)

            # Create new Chrome profiles
            for i in range(num_profiles):
                driver.get("chrome://settings/createProfile")
                profile_name_input = driver.find_element_by_css_selector(
                    "input[placeholder='Tên']")
                profile_name_input.send_keys("Profile {}".format(i + 1))
                create_button = driver.find_element_by_css_selector(
                    "button#create-profile-button")
                create_button.click()

            driver.quit()

        # Import RAR file into new profiles or existing profiles
        if os.path.exists(self.import_file):
            rar_file = rarfile.RarFile(self.import_file)

            if self.type_var.get() == 1:
                # Copy imported file to new profiles
                for i in range(num_profiles):
                    profile_folder = os.path.join(self.import_file,
                                                  "Profile {}".format(i + 1))
                    os.makedirs(profile_folder, exist_ok=True)
                    for member in rar_file.infolist():
                        rar_file.extract(member, profile_folder)

            elif self.type_var.get() == 2:
                # Copy imported file to existing profiles and create new profiles
                existing_profiles = os.listdir(self.import_file)
                num_existing_profiles = len(existing_profiles)

                for i in range(num_existing_profiles, num_existing_profiles + num_profiles):
                    profile_folder = os.path.join(self.import_file,
                                                  "Profile {}".format(i + 1))
                    os.makedirs(profile_folder, exist_ok=True)
                    for member in rar_file.infolist():
                        rar_file.extract(member, profile_folder)

            rar_file.close()

        messagebox.showinfo("Thông báo", "Đã tạo và import các profile thành công!")

        # Hiển thị thông báo thành công và xóa dữ liệu trên các widget
        # messagebox.showinfo('Thông báo', 'Đã tạo {} profile thành công'.format(amount))
        # self.browser_var.set('')
        # self.type_var.set(1)
        # self.amount_var.set(0)


root = Tk()
GenerateProfileBrowser(root)
root.mainloop()
