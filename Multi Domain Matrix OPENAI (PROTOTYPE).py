import tkinter as tk
from tkinter import ttk
import openai

# Set the OpenAI API Key
openai.api_key = ''

class MultiDomainMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Domain Matrix App @Eunsop JEONG")

        # Main frame for scrolling
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        left_container = ttk.Frame(self.frame)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        right_container = ttk.Frame(self.frame)
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.create_domain_frame(right_container)
        self.create_openai_frame(left_container)
        self.create_dependency_frame()
        self.create_matrix_frame()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_domain_frame(self, parent):
        domain_frame = ttk.LabelFrame(parent, text="Domains")
        domain_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.domain_entry = ttk.Entry(domain_frame)
        self.domain_entry.pack(padx=10, pady=5)

        self.domain_listbox = tk.Listbox(domain_frame)
        self.domain_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        domain_button_frame = ttk.Frame(domain_frame)
        domain_button_frame.pack(pady=5)

        ttk.Button(domain_button_frame, text="Add Domain", command=self.add_domain).pack(side="left", padx=5)
        ttk.Button(domain_button_frame, text="Delete Domain", command=self.delete_domain).pack(side="left", padx=5)

    def create_openai_frame(self, parent):
        openai_frame = ttk.LabelFrame(parent, text="Fetch from OpenAI")
        openai_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.search_entry = ttk.Entry(openai_frame)
        self.search_entry.pack(padx=10, pady=5)

        ttk.Button(openai_frame, text="Search & Display", command=self.fetch_from_openai).pack(pady=5)

        self.openai_listbox = tk.Listbox(openai_frame)
        self.openai_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.move_to_domain_button = ttk.Button(openai_frame, text="Move to Domain", command=self.move_to_domain)
        self.move_to_domain_button.pack(pady=10)

    def create_dependency_frame(self):
        dependency_frame = ttk.LabelFrame(self.frame, text="Dependency")
        dependency_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.domain1_combobox = ttk.Combobox(dependency_frame)
        self.domain2_combobox = ttk.Combobox(dependency_frame)
        self.interaction_entry = ttk.Entry(dependency_frame)

        self.domain1_combobox.pack(padx=10, pady=5)
        self.domain2_combobox.pack(padx=10, pady=5)
        self.interaction_entry.pack(padx=10, pady=5)

        dependency_button_frame = ttk.Frame(dependency_frame)
        dependency_button_frame.pack(pady=5)

        ttk.Button(dependency_button_frame, text="Add Interaction", command=self.add_interaction).pack(side="left", padx=5)
        ttk.Button(dependency_button_frame, text="Delete Interaction", command=self.delete_interaction).pack(side="left", padx=5)

        self.dependency_listbox = tk.Listbox(dependency_frame)
        self.dependency_listbox.pack(fill="both", expand=True, padx=10, pady=5)

    def create_matrix_frame(self):
        matrix_frame = ttk.LabelFrame(self.frame, text="Matrix Display")
        matrix_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.matrix_text = tk.Text(matrix_frame)
        self.matrix_text.pack(fill="both", expand=True, padx=10, pady=5)

        button_frame = ttk.Frame(matrix_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Generate Matrix", command=self.generate_matrix).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Reset Matrix", command=self.reset_matrix).pack(side="left", padx=10)

    def add_domain(self):
        domain = self.domain_entry.get()
        if domain:
            self.domain_listbox.insert(tk.END, domain)
            self.domain_entry.delete(0, tk.END)
            self.update_comboboxes()

    def delete_domain(self):
        selected_domain_index = self.domain_listbox.curselection()
        if selected_domain_index:
            self.domain_listbox.delete(selected_domain_index)
            self.update_comboboxes()

    def fetch_from_openai(self):
        query = self.search_entry.get()
        if query:
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                          messages=[
                                                              {"role": "system", "content": "You are to provide a list of Multi Domain Matrix's Component, Function, Parameter. List it with numbers."},
                                                              {"role": "user", "content": query}
                                                          ])
                response = completion.choices[0].message.content.split('\n')
                for item in response:
                    self.openai_listbox.insert(tk.END, item)
            except Exception as e:
                print(f"Error fetching data from OpenAI: {e}")

    def move_to_domain(self):
        try:
            index = self.openai_listbox.curselection()[0]
            item = self.openai_listbox.get(index)
            self.domain_listbox.insert(tk.END, item)
            self.openai_listbox.delete(index)
            self.update_comboboxes()
        except:
            pass

    def add_interaction(self):
        domain1 = self.domain1_combobox.get()
        domain2 = self.domain2_combobox.get()
        interaction = self.interaction_entry.get()

        if domain1 and domain2 and interaction:
            interaction_string = f"{domain1} -> {domain2}: {interaction}"
            self.dependency_listbox.insert(tk.END, interaction_string)
            self.interaction_entry.delete(0, tk.END)

    def delete_interaction(self):
        selected_interaction_index = self.dependency_listbox.curselection()
        if selected_interaction_index:
            self.dependency_listbox.delete(selected_interaction_index)

    def generate_matrix(self):
        self.matrix_text.delete(1.0, tk.END)
        domains = list(self.domain_listbox.get(0, tk.END))
        interactions = [self.dependency_listbox.get(i) for i in range(self.dependency_listbox.size())]

        domain_interaction_dict = {}
        for interaction in interactions:
            domain1, rest = interaction.split(" -> ")
            domain2, interaction_text = rest.split(": ")
            if domain1 not in domain_interaction_dict:
                domain_interaction_dict[domain1] = {}
            domain_interaction_dict[domain1][domain2] = interaction_text

        # Create the matrix
        matrix = [["" for _ in domains] for _ in domains]
        for i, domain_row in enumerate(domains):
            for j, domain_col in enumerate(domains):
                if domain_row == domain_col:
                    matrix[i][j] = "-"
                else:
                    if domain_row in domain_interaction_dict and domain_col in domain_interaction_dict[domain_row]:
                        matrix[i][j] = domain_interaction_dict[domain_row][domain_col]

        # Display the matrix
        header = "\t".join(domains)
        self.matrix_text.insert(tk.END, "\t" + header + "\n")
        for i, row in enumerate(matrix):
            row_text = "\t".join(row)
            self.matrix_text.insert(tk.END, f"{domains[i]}\t{row_text}\n")

    def reset_matrix(self):
        self.matrix_text.delete(1.0, tk.END)

    def update_comboboxes(self):
        domains = list(self.domain_listbox.get(0, tk.END))
        
        # Update domain1_combobox
        self.domain1_combobox["values"] = domains
        if domains:
            self.domain1_combobox.set(domains[0])

        # Update domain2_combobox
        self.domain2_combobox["values"] = domains
        if domains:
            self.domain2_combobox.set(domains[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiDomainMatrixApp(root)
    root.mainloop()
