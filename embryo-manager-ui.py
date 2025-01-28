import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import random
from datetime import datetime
import sys
import importlib.util
from typing import Dict, List, Any
from embryo_manager_extensions import EmbryoManagerExtensions
class EmbryoManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Embryo Management System")
        self.root.geometry("1200x800")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.creation_tab = ttk.Frame(self.notebook)
        self.training_tab = ttk.Frame(self.notebook)
        self.monitoring_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.creation_tab, text="Embryo Creation")
        self.notebook.add(self.training_tab, text="Training Programs")
        self.notebook.add(self.monitoring_tab, text="Monitoring")
        
        # Initialize components
        self.setup_creation_tab()
        self.setup_training_tab()
        self.setup_monitoring_tab()
        
        # Load existing embryos
        self.load_existing_embryos()
        
    def setup_creation_tab(self):
        # Left panel for creation options
        left_panel = ttk.LabelFrame(self.creation_tab, text="Creation Options")
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        
        # Creation type selection
        ttk.Label(left_panel, text="Creation Type:").pack(pady=5)
        self.creation_type = tk.StringVar(value="random")
        ttk.Radiobutton(left_panel, text="Random", variable=self.creation_type, 
                       value="random").pack()
        ttk.Radiobutton(left_panel, text="Inherited", variable=self.creation_type, 
                       value="inherited").pack()
        
        # Parent selection (for inherited creation)
        self.parent_frame = ttk.LabelFrame(left_panel, text="Parent Selection")
        self.parent_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(self.parent_frame, text="Parent 1:").pack()
        self.parent1_var = tk.StringVar()
        self.parent1_combo = ttk.Combobox(self.parent_frame, textvariable=self.parent1_var)
        self.parent1_combo.pack(pady=5)
        
        ttk.Label(self.parent_frame, text="Parent 2:").pack()
        self.parent2_var = tk.StringVar()
        self.parent2_combo = ttk.Combobox(self.parent_frame, textvariable=self.parent2_var)
        self.parent2_combo.pack(pady=5)
        
        # Create button
        ttk.Button(left_panel, text="Create Embryo", 
                  command=self.create_embryo).pack(pady=20)
        
        # Right panel for embryo list
        right_panel = ttk.LabelFrame(self.creation_tab, text="Existing Embryos")
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Embryo list with scrollbar
        self.embryo_list = ttk.Treeview(right_panel, columns=("ID", "Type", "Created"), 
                                      show="headings")
        self.embryo_list.heading("ID", text="Embryo ID")
        self.embryo_list.heading("Type", text="Creation Type")
        self.embryo_list.heading("Created", text="Creation Date")
        
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", 
                                command=self.embryo_list.yview)
        self.embryo_list.configure(yscrollcommand=scrollbar.set)
        
        self.embryo_list.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def setup_training_tab(self):
        # Left panel for embryo selection and program list
        left_panel = ttk.LabelFrame(self.training_tab, text="Training Configuration")
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        
        # Embryo selection
        ttk.Label(left_panel, text="Select Embryo:").pack(pady=5)
        self.training_embryo_var = tk.StringVar()
        self.training_embryo_combo = ttk.Combobox(left_panel, 
                                                textvariable=self.training_embryo_var)
        self.training_embryo_combo.pack(pady=5)
        
        # Training program selection
        ttk.Label(left_panel, text="Training Program:").pack(pady=5)
        self.program_list = ttk.Treeview(left_panel, columns=("Name", "Duration"), 
                                       show="headings", height=10)
        self.program_list.heading("Name", text="Program Name")
        self.program_list.heading("Duration", text="Duration")
        self.program_list.pack(pady=5)
        
        # Start training button
        ttk.Button(left_panel, text="Start Training", 
                  command=self.start_training).pack(pady=20)
        
        # Right panel for training progress
        right_panel = ttk.LabelFrame(self.training_tab, text="Training Progress")
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Progress indicators
        self.progress_frame = ttk.Frame(right_panel)
        self.progress_frame.pack(fill='both', expand=True)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill='x', pady=10)
        
        self.progress_label = ttk.Label(self.progress_frame, text="No training in progress")
        self.progress_label.pack()
        
    def setup_monitoring_tab(self):
        # Left panel for embryo selection
        left_panel = ttk.LabelFrame(self.monitoring_tab, text="Embryo Selection")
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        
        ttk.Label(left_panel, text="Select Embryo:").pack(pady=5)
        self.monitor_embryo_var = tk.StringVar()
        self.monitor_embryo_combo = ttk.Combobox(left_panel, 
                                               textvariable=self.monitor_embryo_var)
        self.monitor_embryo_combo.pack(pady=5)
        
        ttk.Button(left_panel, text="Refresh Data", 
                  command=self.refresh_monitoring).pack(pady=20)
        
        # Right panel for stats and graphs
        right_panel = ttk.LabelFrame(self.monitoring_tab, text="Embryo Statistics")
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Stats display
        self.stats_tree = ttk.Treeview(right_panel, columns=("Metric", "Value"), 
                                     show="headings")
        self.stats_tree.heading("Metric", text="Metric")
        self.stats_tree.heading("Value", text="Value")
        self.stats_tree.pack(fill='both', expand=True)
        
    def load_existing_embryos(self):
        """Load existing embryos from the embryos directory"""
        embryo_dir = Path("embryos")
        if not embryo_dir.exists():
            return
            
        for embryo_file in embryo_dir.glob("embryo_*.py"):
            embryo_id = embryo_file.stem.split('_')[1]
            creation_time = datetime.fromtimestamp(embryo_file.stat().st_ctime)
            
            # Determine creation type from conception records
            creation_type = "Random"
            conception_record = Path(f"conception_records/conception_{embryo_id}.json")
            if conception_record.exists():
                with open(conception_record) as f:
                    data = json.load(f)
                    if data.get("parentage"):
                        creation_type = "Inherited"
            
            self.embryo_list.insert("", "end", values=(
                embryo_id,
                creation_type,
                creation_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
    
    def create_embryo(self):
        """Handle embryo creation based on selected options"""
        try:
            if self.creation_type.get() == "random":
                embryo_id = self.create_random_embryo()
            else:
                parent1 = self.parent1_var.get()
                parent2 = self.parent2_var.get()
                if not parent1 or not parent2:
                    messagebox.showerror("Error", "Please select both parents")
                    return
                embryo_id = self.create_inherited_embryo(parent1, parent2)
            
            messagebox.showinfo("Success", f"Created embryo with ID: {embryo_id}")
            self.load_existing_embryos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create embryo: {str(e)}")
    
    def create_random_embryo(self):
        """Create a random embryo"""
        # Import and use the genetic inheritance module
        spec = importlib.util.spec_from_file_location("genetic_inheritance",
                                                    "genetic-inheritance.py")
        genetic_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(genetic_module)
        
        return genetic_module.conceive_embryo()
    
    def create_inherited_embryo(self, parent1_id, parent2_id):
        """Create an inherited embryo from selected parents"""
        spec = importlib.util.spec_from_file_location("genetic_inheritance",
                                                    "genetic-inheritance.py")
        genetic_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(genetic_module)
        
        return genetic_module.conceive_embryo(parent1_id, parent2_id)
    
    def start_training(self):
        """Start the selected training program"""
        embryo_id = self.training_embryo_var.get()
        selected_items = self.program_list.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a training program")
            return
            
        program_name = self.program_list.item(selected_items[0])['values'][0]
        
        try:
            # Import and use the embryo school module
            spec = importlib.util.spec_from_file_location("embryo_school",
                                                        "embryo-school.py")
            school_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(school_module)
            
            school = school_module.EmbryoSchool()
            embryo = school.load_embryo(f"embryos/embryo_{embryo_id}.py")
            
            # Start training in a separate thread to not block UI
            import threading
            def training_thread():
                try:
                    result = school.train_embryo(embryo, program_name)
                    self.root.after(0, self.training_completed, result)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                                  f"Training failed: {str(e)}"))
            
            thread = threading.Thread(target=training_thread)
            thread.start()
            
            self.progress_bar['value'] = 0
            self.progress_label['text'] = f"Training in progress: {program_name}"
            self.simulate_progress()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start training: {str(e)}")
    
    def simulate_progress(self):
        """Simulate training progress"""
        if self.progress_bar['value'] < 100:
            self.progress_bar['value'] += 1
            self.root.after(100, self.simulate_progress)
    
    def training_completed(self, result):
        """Handle training completion"""
        self.progress_bar['value'] = 100
        self.progress_label['text'] = "Training completed"
        self.refresh_monitoring()
        messagebox.showinfo("Success", "Training program completed successfully")
    
    def refresh_monitoring(self):
        """Refresh monitoring data for selected embryo"""
        embryo_id = self.monitor_embryo_var.get()
        if not embryo_id:
            return
            
        try:
            # Load embryo and get status
            spec = importlib.util.spec_from_file_location("embryo_school",
                                                        "embryo-school.py")
            school_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(school_module)
            
            school = school_module.EmbryoSchool()
            embryo = school.load_embryo(f"embryos/embryo_{embryo_id}.py")
            status = embryo.get_status()
            
            # Clear existing stats
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            # Update stats display
            self.stats_tree.insert("", "end", values=("Development Stage", 
                                                    f"{status['development_stage']:.2f}"))
            self.stats_tree.insert("", "end", values=("Age", status['age']))
            self.stats_tree.insert("", "end", values=("Experiences", 
                                                    status['experiences_count']))
            
            # Add neural connections
            for conn_type, value in status['neural_connections'].items():
                self.stats_tree.insert("", "end", values=(f"Neural Connections - {conn_type}", 
                                                        value))
            
            # Add specializations
            self.stats_tree.insert("", "end", values=("Specializations", 
                                                    ", ".join(status['specializations'])))
            
            self.extensions = EmbryoManagerExtensions(self)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh monitoring: {str(e)}")

def main():
    root = tk.Tk()
    app = EmbryoManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
