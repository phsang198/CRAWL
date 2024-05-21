import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from urllib.parse import urlparse, urljoin
class WebCloneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web Clone & Viewer")

        if not os.path.exists("clones"):
            os.makedirs("clones")

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        url_label = tk.Label(input_frame, text="URL:", font=("Arial", 12))
        url_label.grid(row=0, column=0, padx=(0, 5))
        self.url_entry = tk.Entry(input_frame, width=50, font=("Arial", 12))
        self.url_entry.grid(row=0, column=1)

        file_name_label = tk.Label(input_frame, text="File Name:", font=("Arial", 12))
        file_name_label.grid(row=1, column=0, padx=(0, 5), pady=5)
        self.file_name_entry = tk.Entry(input_frame, width=50, font=("Arial", 12))
        self.file_name_entry.grid(row=1, column=1)

        clone_button = tk.Button(input_frame, text="Clone & View Offline", command=self.on_clone_click, font=("Arial", 12), bg="green", fg="white")
        clone_button.grid(row=2, columnspan=2, pady=(5, 0))
        clone_button = tk.Button(input_frame, text="Extract Image", command=self.on_extract_image_click, font=("Arial", 12), bg="green", fg="white")
        clone_button.grid(row=3, columnspan=3, pady=(5, 0))
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        search_label = tk.Label(search_frame, text="Search:", font=("Arial", 12))
        search_label.grid(row=0, column=0, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind("<KeyRelease>", self.on_search_click)

        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=10)

        self.selectedl = tk.Label(button_frame, text="Selected File:", anchor="w", padx=10, font=("Arial", 12))
        self.selectedl.pack(side="left", fill="x", padx=(0, 10))
        self.selected_file_label = tk.Label(button_frame, text="None", anchor="w", padx=10, font=("Arial", 12))
        self.selected_file_label.pack(side="left", fill="x", padx=(0, 10))

        self.show_button = tk.Button(button_frame, text="Show", command=self.on_show_click, state=tk.DISABLED, font=("Arial", 12), fg="black")
        self.show_button.pack(side="left", pady=(5, 0))

        self.tree = ttk.Treeview(self, columns=("ID", "File Name", "Size"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("File Name", text="File Name", anchor="center")
        self.tree.heading("Size", text="Size", anchor="center")
        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)
        self.tree.pack(side="left", expand=True, fill="both")
        self.data = self.load_data()
        self.update_table()

    def on_clone_click(self):
        url = self.url_entry.get()
        file_name = self.file_name_entry.get()
        if url and file_name:
            hostname = urlparse(url).hostname
            self.clone_and_open(url,hostname, file_name)
        else:
            messagebox.showwarning("Warning", "Please enter both URL and File Name.")

    def clone_web(self, url, folder_path, hostname):
        try:
            response = requests.get(url)
            web_content = response.content

            soupAll = BeautifulSoup(web_content, 'html.parser')

            links = soupAll.find_all('a')
            count = 0 
            for link in links:
                href = link.get('href')
                if href:

                    absolute_href = urljoin(url, href)
                    parsed_href = urlparse(absolute_href)

                    if parsed_href.scheme and parsed_href.netloc :

                        try:
                            count += 1 
                            new_link = str(count) + ".html" ; 
                            file_path = os.path.join(folder_path, new_link)
                            
                            if not os.path.exists(file_path):
                                soup = self.get_soup(absolute_href)
                                with open(file_path, 'w', encoding='utf-8') as file:
                                    file.write(str(soup))
                                    
                        except Exception as e:
                            a = 0

                    link['href'] = "./" + hostname + "/" + new_link 
                    
            css = soupAll.find_all('link')
            for link in css:
                href = link.get('href')
                if href:

                    absolute_href = urljoin(url, href)
                    parsed_href = urlparse(absolute_href)
                    if href.endswith('.css'):
                        link['href'] = absolute_href

            images = soupAll.find_all('img')
            for link in images:
                href = link.get('src')
                if href:

                    absolute_href = urljoin(url, href)
                    
                    link['src'] = absolute_href

            return soupAll           

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clone_and_open(self, url, hostname, file_name):
        try:
            root_path = os.path.realpath(__file__)

            folder_path = os.path.dirname(root_path) +"\\clones\\" + hostname

            file_path = os.path.join("clones", file_name + ".html")
            if os.path.exists(file_path):
                messagebox.showwarning("Warning", "File with this name already exists. Please choose a different name.")
                return
            else:
                os.makedirs(folder_path)

            soup = self.clone_web(url,folder_path,hostname)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            webbrowser.open(file_path)
            self.data = self.load_data()
            self.update_table()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_soup(self, url):
        try:
            response = requests.get(url)
            web_content = response.content

            soupAll = BeautifulSoup(web_content, 'html.parser')

            links = soupAll.find_all('a')
            count = 0 
            for link in links:
                href = link.get('href')
                if href:
                    absolute_href = urljoin(url, href)
                    link['href'] = absolute_href
                    
            css = soupAll.find_all('link')
            for link in css:
                href = link.get('href')
                if href:
                    absolute_href = urljoin(url, href)
                    if href.endswith('.css'):
                        link['href'] = absolute_href

            images = soupAll.find_all('img')
            for link in images:
                href = link.get('src')
                if href:
                    absolute_href = urljoin(url, href)
                    link['src'] = absolute_href

            return soupAll           
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_search_click(self,event):
        search_text = self.search_entry.get()
        if search_text == "":
            self.data = self.load_data()
            self.update_table()
            return
        try:
            self.data = [item for item in self.data if search_text in item['file_name']]
            self.update_table()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, record in enumerate(self.data, start=1):
            self.tree.insert("", "end", values=(idx, record["file_name"], f"{record['file_size_kb']:.2f} KB"))

    def on_show_click(self):
        try:
            file_name = self.selected_file_label.cget("text")
            file_path = os.path.join("clones", file_name)
            webbrowser.open(file_path)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a file.")

    def on_item_selected(self, event):
        item = self.tree.selection()
        file_name = self.tree.item(item, "values")[1]
        if file_name:
            self.show_button.configure(state="normal")
        self.selected_file_label.configure(text=f"{file_name}")

    def load_data(self):
        clones_dir = "clones"
        files = os.listdir(clones_dir)
        file_info_list = []

        for file in files:
            file_path = os.path.join(clones_dir, file)
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024
            file_info_list.append({"file_name": file, "file_size_kb": file_size_kb})

        return file_info_list

    def on_extract_image_click(self):
        url = self.url_entry.get()
        if url:
            self.extract_images(url)
        else:
            messagebox.showwarning("Warning", "Please enter a URL.")

    def extract_images(self, url):
        try:
            soup = self.get_soup(url)
            img_tags = soup.find_all("img")
            img_urls = [tag.get("src") for tag in img_tags]
            img_urls.extend([tag.get("data-original") for tag in img_tags])
            hostname = urlparse(url).hostname
            self.save_images(img_urls,hostname)

            messagebox.showinfo("Extracted Images", "Images saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_images(self, img_urls,hostname):
        images_dir = os.path.join("clones\\"+hostname, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        for i, url in enumerate(img_urls, start=1):
            try:
                response = requests.get(url)
                timestamp = int(datetime.datetime.now().timestamp())
                
                _, ext = os.path.splitext(urlparse(url).path)
                file_path = os.path.join(images_dir, f"{timestamp}_{i}"+ext)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Image saved successfully: {file_path}")
            except Exception as e:
                print(f"Error saving image: {e}")

if __name__ == "__main__":
    app = WebCloneApp()
    app.mainloop()
