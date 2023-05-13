import os
import shutil
import zipfile
from tkinter.ttk import Combobox, Label, Button, Radiobutton, Spinbox

from tkinter import filedialog, StringVar, IntVar, Tk, W, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from constants import FILE_TYPES, BrowserType, CreateType


class GenerateProfileBrowser:
    def __init__(self, master):
        self.folder_extracted = None
        self.master = master
        master.title("Generate Profile Browsers")
        master.geometry("400x200")
        self.profiles = []
        self.root_folder = os.path.dirname(os.path.abspath(__file__))
        self.rar_file_name = "import.zip"
        self.import_file = os.path.join(self.root_folder, self.rar_file_name)
        if not os.path.isfile(self.import_file):
            messagebox.showinfo(
                title=None, message="Không tồn tại file ZIP. Hãy import"
            )
            self.do_import_file()
        self.do_get_folder_extract_rar()

        self.browser_var = StringVar()
        self.type_var = IntVar()
        self.amount_var = IntVar()

    def init_ui(self):
        # Tạo label và combobox chọn loại browser
        browser_label = Label(self.master, text="Loại browser:")
        browser_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        browser_combobox = Combobox(
            self.master,
            textvariable=self.browser_var,
            values=BrowserType.to_list(),
            state="readonly",
        )
        browser_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        # import profile có sẵn
        import_button = Button(
            self.master, text="Import Profile", command=self.do_import_file
        )
        import_button.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        # Tạo label và radiobutton chọn kiểu tạo
        type_label = Label(self.master, text="Kiểu tạo:")
        type_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        new_profile_radio = Radiobutton(
            self.master,
            text="Tạo profile mới",
            variable=self.type_var,
            value=CreateType.CREATE_NEW_PROFILE,
        )
        new_profile_radio.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        add_profile_radio = Radiobutton(
            self.master,
            text="Tạo thêm profile",
            variable=self.type_var,
            value=CreateType.ADD_PROFILE,
        )
        add_profile_radio.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        # Tạo label và spinbox chọn số lượng
        amount_label = Label(self.master, text="Số lượng:")
        amount_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        amount_spinbox = Spinbox(
            self.master, from_=0, to=100, width=5, textvariable=self.amount_var
        )
        amount_spinbox.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Tạo nút Enter
        enter_button = Button(
            self.master, text="Enter", command=self.do_generate_profiles
        )
        enter_button.grid(row=3, column=0, padx=10, pady=10, sticky=W)

    def do_generate_profiles(self):
        # Get selected browser
        browser = self.browser_var.get()
        # Get number of profiles to generate
        num_profiles = self.amount_var.get()

        if not browser:
            messagebox.showinfo(title=None, message="Hãy chọn loại trình duyệt")
            return
        # Initialize Chrome driver
        if BrowserType.is_chrome(browser):
            self.do_create_chrome_profile(num_profiles=num_profiles)

        messagebox.showinfo("Thông báo", "Đã tạo và import các profile thành công!")

        # Hiển thị thông báo thành công và xóa dữ liệu trên các widget
        # messagebox.showinfo('Thông báo', 'Đã tạo {} profile thành công'.format(amount))
        # self.browser_var.set('')
        # self.type_var.set(1)
        # self.amount_var.set(0)

    def do_import_file(self):
        self.import_file = filedialog.askopenfilename(
            title="Chọn file .zip", filetypes=FILE_TYPES, initialdir=self.root_folder
        )
        self.do_get_folder_extract_rar()

    def do_get_folder_extract_rar(self):
        with zipfile.ZipFile(self.import_file) as zip_file:
            extracted_files = zip_file.infolist()
            self.folder_extracted = os.path.join(
                self.root_folder, extracted_files[0].filename.split("/")[0]
            )
            self.profiles = [
                fd
                for fd in os.listdir(self.folder_extracted)
                if fd.startswith("Profile ")
            ]

    def do_create_chrome_profile(self, num_profiles):
        total_profiles = len(self.profiles)
        if CreateType.is_create_new(self.type_var.get()):
            # Copy imported file to new profiles
            for i in range(total_profiles, total_profiles + num_profiles):
                # Set up Chrome driver options
                chrome_options = Options()
                # Profile name
                profile_name = f"Profile {i}"
                profile_path = os.path.join(self.folder_extracted, profile_name)
                # Set user data dir to import folder
                chrome_options.add_argument(f"--headless")
                chrome_options.add_argument(f"--disable-gpu")
                chrome_options.add_argument(f"--user-data-dir={profile_path}")
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=chrome_options,
                )
                driver.quit()
                os.makedirs(profile_path, exist_ok=True)
                self.profiles.append(profile_name)

        elif CreateType.is_add_profile(self.type_var.get()):
            ...
            # # Copy imported file to existing profiles and create new profiles
            # existing_profiles = os.listdir(self.import_file)
            # num_existing_profiles = len(existing_profiles)
            #
            # for i in range(num_existing_profiles, num_existing_profiles + num_profiles):
            #     profile_folder = os.path.join(
            #         self.import_file, "Profile {}".format(i + 1)
            #     )
            #     os.makedirs(profile_folder, exist_ok=True)
            #     for member in rar_file.infolist():
            #         rar_file.extract(member, profile_folder)

        self.do_zip_folder()

    def do_zip_folder(self):
        os.remove(self.import_file)
        shutil.make_archive(self.import_file, 'zip', self.folder_extracted)


if __name__ == "__main__":
    root = Tk()
    GenerateProfileBrowser(root).init_ui()
    root.mainloop()
