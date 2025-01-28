# embryo_manager_extensions.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Any

class EmbryoManagerExtensions:
    def __init__(self, manager_ui):
        self.manager = manager_ui
        self.setup_additional_ui_components()
        self.initialize_training_programs()
        self.setup_monitoring_graphs()
        self.bind_events()
        
    def setup_additional_ui_components(self):
        """Add additional UI components to existing tabs"""
        # Creation Tab Extensions
        self.add_genetic_preview(self.manager.creation_tab)
        
        # Training Tab Extensions
        self.add_training_metrics(self.manager.training_tab)
        
        # Monitoring Tab Extensions
        self.add_monitoring_graphs(self.manager.monitoring_tab)
        
    def add_genetic_preview(self, parent):
        """Add genetic preview panel to creation tab"""
        preview_frame = ttk.LabelFrame(parent, text="Genetic Preview")
        preview_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Genetic traits preview
        self.preview_tree = ttk.Treeview(preview_frame, columns=("Trait", "Value"), 
                                       show="headings", height=6)
        self.preview_tree.heading("Trait", text="Genetic Trait")
        self.preview_tree.heading("Value", text="Predicted Value")
        self.preview_tree.pack(fill='x', padx=5, pady=5)
        
        # Preview update button
        ttk.Button(preview_frame, text="Update Preview", 
                  command=self.update_genetic_preview).pack(pady=5)
        
    def add_training_metrics(self, parent):
        """Add real-time training metrics panel"""
        metrics_frame = ttk.LabelFrame(self.manager.progress_frame, text="Training Metrics")
        metrics_frame.pack(fill='x', pady=10)
        
        # Training metrics display
        self.metrics_display = {}
        metrics = ["Learning Rate", "Error Rate", "Accuracy", "Iterations"]
        
        for metric in metrics:
            frame = ttk.Frame(metrics_frame)
            frame.pack(fill='x', padx=5, pady=2)
            ttk.Label(frame, text=f"{metric}:").pack(side='left')
            value_label = ttk.Label(frame, text="0.0")
            value_label.pack(side='right')
            self.metrics_display[metric] = value_label
            
        # Add training log
        log_frame = ttk.LabelFrame(self.manager.progress_frame, text="Training Log")
        log_frame.pack(fill='both', expand=True, pady=10)
        
        self.training_log = tk.Text(log_frame, height=8, width=40)
        scrollbar = ttk.Scrollbar(log_frame, command=self.training_log.yview)
        self.training_log.configure(yscrollcommand=scrollbar.set)
        
        self.training_log.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def add_monitoring_graphs(self, parent):
        """Add graphical monitoring components"""
        graphs_frame = ttk.Frame(parent)
        graphs_frame.pack(side='bottom', fill='both', expand=True)
        
        # Create matplotlib figures
        self.setup_development_graph(graphs_frame)
        self.setup_neural_graph(graphs_frame)
        
    def setup_development_graph(self, parent):
        """Setup development progress graph"""
        fig, self.dev_ax = plt.subplots(figsize=(6, 4))
        self.dev_canvas = FigureCanvasTkAgg(fig, master=parent)
        self.dev_canvas.get_tk_widget().pack(side='left', fill='both', expand=True)
        
        self.dev_ax.set_title('Development Progress')
        self.dev_ax.set_xlabel('Time')
        self.dev_ax.set_ylabel('Development Stage')
        
    def setup_neural_graph(self, parent):
        """Setup neural connections graph"""
        fig, self.neural_ax = plt.subplots(figsize=(6, 4))
        self.neural_canvas = FigureCanvasTkAgg(fig, master=parent)
        self.neural_canvas.get_tk_widget().pack(side='right', fill='both', expand=True)
        
        self.neural_ax.set_title('Neural Connections')
        self.neural_ax.set_xlabel('Connection Type')
        self.neural_ax.set_ylabel('Connection Count')
        
    def initialize_training_programs(self):
        """Initialize available training programs"""
        programs = [
            ("Basic Pattern Recognition", "2 hours", "pattern_recognition"),
            ("Advanced Problem Solving", "4 hours", "problem_solving"),
            ("Neural Network Growth", "3 hours", "neural_growth"),
            ("Specialization Training", "5 hours", "specialization"),
            ("Adaptive Learning", "6 hours", "adaptive")
        ]
        
        for program in programs:
            self.manager.program_list.insert("", "end", values=program[:2])
            
    def bind_events(self):
        """Bind event handlers"""
        self.manager.embryo_list.bind('<<TreeviewSelect>>', self.on_embryo_select)
        self.manager.program_list.bind('<<TreeviewSelect>>', self.on_program_select)
        self.manager.monitor_embryo_combo.bind('<<ComboboxSelected>>', 
                                             self.on_monitor_embryo_change)
        
    def update_genetic_preview(self):
        """Update genetic preview based on current selection"""
        self.preview_tree.delete(*self.preview_tree.get_children())
        
        if self.manager.creation_type.get() == "inherited":
            # Calculate predicted traits from parents
            parent1 = self.manager.parent1_var.get()
            parent2 = self.manager.parent2_var.get()
            if parent1 and parent2:
                predicted_traits = self.calculate_inherited_traits(parent1, parent2)
                for trait, value in predicted_traits.items():
                    self.preview_tree.insert("", "end", values=(trait, f"{value:.2f}"))
        else:
            # Show random trait ranges
            traits = [
                ("Learning Capacity", "1.5 - 3.0"),
                ("Pattern Recognition", "1.5 - 3.0"),
                ("Adaptability", "1.5 - 3.0"),
                ("Processing Speed", "1.5 - 3.0"),
                ("Error Tolerance", "1.5 - 3.0")
            ]
            for trait, range_val in traits:
                self.preview_tree.insert("", "end", values=(trait, range_val))
                
    def calculate_inherited_traits(self, parent1_id: str, parent2_id: str) -> Dict[str, float]:
        """Calculate predicted traits for inherited embryo"""
        try:
            p1_data = self.load_parent_data(parent1_id)
            p2_data = self.load_parent_data(parent2_id)
            
            predicted = {}
            for trait in p1_data['genetic_traits']:
                # Calculate weighted average with random variation
                base_value = (p1_data['genetic_traits'][trait] + 
                            p2_data['genetic_traits'][trait]) / 2
                variation = np.random.normal(0, 0.1)  # Small random variation
                predicted[trait] = max(1.5, min(3.0, base_value + variation))
                
            return predicted
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate inherited traits: {str(e)}")
            return {}
            
    def load_parent_data(self, parent_id: str) -> Dict[str, Any]:
        """Load parent embryo data"""
        conception_file = Path(f"conception_records/conception_{parent_id}.json")
        if conception_file.exists():
            with open(conception_file) as f:
                return json.load(f)
        raise ValueError(f"Parent data not found for ID: {parent_id}")
        
    def update_training_metrics(self, metrics: Dict[str, float]):
        """Update training metrics display"""
        for metric, value in metrics.items():
            if metric in self.metrics_display:
                self.metrics_display[metric]['text'] = f"{value:.3f}"
                
    def log_training_event(self, message: str):
        """Add message to training log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.training_log.insert('end', f"[{timestamp}] {message}\n")
        self.training_log.see('end')
        
    def update_monitoring_graphs(self, embryo_data: Dict[str, Any]):
        """Update monitoring graphs with new data"""
        # Update development progress graph
        self.dev_ax.clear()
        times = [i for i in range(len(embryo_data['development_history']))]
        stages = [d['stage'] for d in embryo_data['development_history']]
        
        self.dev_ax.plot(times, stages)
        self.dev_ax.set_title('Development Progress')
        self.dev_ax.set_xlabel('Time')
        self.dev_ax.set_ylabel('Development Stage')
        self.dev_canvas.draw()
        
        # Update neural connections graph
        self.neural_ax.clear()
        conn_types = list(embryo_data['neural_connections'].keys())
        conn_values = list(embryo_data['neural_connections'].values())
        
        self.neural_ax.bar(conn_types, conn_values)
        self.neural_ax.set_title('Neural Connections')
        self.neural_ax.tick_params(axis='x', rotation=45)
        self.neural_canvas.draw()
        
    def on_embryo_select(self, event):
        """Handle embryo selection in list"""
        selection = self.manager.embryo_list.selection()
        if selection:
            embryo_id = self.manager.embryo_list.item(selection[0])['values'][0]
            self.update_genetic_preview()
            
    def on_program_select(self, event):
        """Handle training program selection"""
        selection = self.manager.program_list.selection()
        if selection:
            program = self.manager.program_list.item(selection[0])['values'][0]
            self.show_program_details(program)
            
    def on_monitor_embryo_change(self, event):
        """Handle monitored embryo change"""
        embryo_id = self.manager.monitor_embryo_var.get()
        if embryo_id:
            self.refresh_monitoring_data(embryo_id)
            
    def show_program_details(self, program: str):
        """Show details for selected training program"""
        details = {
            "Basic Pattern Recognition": {
                "description": "Fundamental pattern recognition training",
                "prerequisites": "None",
                "expected_outcomes": ["Improved pattern matching", "Basic classification skills"]
            },
            "Advanced Problem Solving": {
                "description": "Complex problem-solving scenarios",
                "prerequisites": "Basic Pattern Recognition",
                "expected_outcomes": ["Strategic thinking", "Solution optimization"]
            }
            # Add other program details here
        }
        
        if program in details:
            info = details[program]
            messagebox.showinfo("Program Details",
                              f"Program: {program}\n\n"
                              f"Description: {info['description']}\n"
                              f"Prerequisites: {info['prerequisites']}\n"
                              f"Expected Outcomes:\n" +
                              "\n".join(f"- {outcome}" for outcome in info['expected_outcomes']))
            
    def refresh_monitoring_data(self, embryo_id: str):
        """Refresh monitoring data for selected embryo"""
        try:
            # Load embryo data
            embryo_data = self.load_embryo_data(embryo_id)
            
            # Update graphs
            self.update_monitoring_graphs(embryo_data)
            
            # Update stats tree
            self.manager.refresh_monitoring()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh monitoring data: {str(e)}")
            
    def load_embryo_data(self, embryo_id: str) -> Dict[str, Any]:
        """Load complete embryo data including history"""
        # Load development logs
        log_file = Path(f"development_logs/{embryo_id}.json")
        if not log_file.exists():
            raise ValueError(f"No development logs found for embryo: {embryo_id}")
            
        with open(log_file) as f:
            return json.load(f)
