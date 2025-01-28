import json
import random
import numpy as np
from pathlib import Path
import importlib.util
from datetime import datetime

class EmbryoSchool:
    def __init__(self):
        self.training_programs = {
            # Basic Programs
            "basic_cognition": {
                "experiences": [
                    {"type": "pattern", "complexity": 0.3, "data": "sequential_learning"},
                    {"type": "logical", "complexity": 0.2, "data": "basic_reasoning"},
                    {"type": "visual", "complexity": 0.25, "data": "pattern_matching"}
                ],
                "duration": 5,
                "required_stage": 0,
                "metrics": ["pattern_recognition", "learning_capacity"]
            },
            "social_adaptation": {
                "experiences": [
                    {"type": "social", "complexity": 0.3, "data": "basic_interaction"},
                    {"type": "emotional", "complexity": 0.25, "data": "response_patterns"},
                    {"type": "collaborative", "complexity": 0.2, "data": "group_dynamics"}
                ],
                "duration": 6,
                "required_stage": 2,
                "metrics": ["social_interaction", "adaptability"]
            },
            "resource_efficiency": {
                "experiences": [
                    {"type": "optimization", "complexity": 0.4, "data": "resource_allocation"},
                    {"type": "management", "complexity": 0.35, "data": "efficiency_patterns"},
                    {"type": "analytical", "complexity": 0.3, "data": "usage_analysis"}
                ],
                "duration": 7,
                "required_stage": 3,
                "metrics": ["resource_management", "energy_efficiency"]
            },
            
            # Advanced Programs
            "advanced_patterns": {
                "experiences": [
                    {"type": "pattern", "complexity": 0.7, "data": "complex_patterns"},
                    {"type": "logical", "complexity": 0.6, "data": "pattern_analysis"},
                    {"type": "visual", "complexity": 0.65, "data": "visual_patterns"},
                    {"type": "temporal", "complexity": 0.7, "data": "sequence_prediction"}
                ],
                "duration": 8,
                "required_stage": 5,
                "metrics": ["pattern_recognition", "processing_speed"]
            },
            "decision_mastery": {
                "experiences": [
                    {"type": "decision", "complexity": 0.75, "data": "complex_choices"},
                    {"type": "analysis", "complexity": 0.7, "data": "outcome_prediction"},
                    {"type": "strategic", "complexity": 0.8, "data": "strategy_formation"}
                ],
                "duration": 9,
                "required_stage": 6,
                "metrics": ["decision_making", "adaptability"]
            },
            "parallel_processing": {
                "experiences": [
                    {"type": "multi_task", "complexity": 0.8, "data": "simultaneous_processing"},
                    {"type": "coordination", "complexity": 0.75, "data": "task_coordination"},
                    {"type": "efficiency", "complexity": 0.7, "data": "resource_distribution"}
                ],
                "duration": 8,
                "required_stage": 7,
                "metrics": ["parallel_processing", "processing_speed"]
            },
            
            # Specialization Programs
            "pattern_analysis_specialist": {
                "experiences": [
                    {"type": "pattern", "complexity": 0.9, "data": "advanced_pattern_recognition"},
                    {"type": "analysis", "complexity": 0.85, "data": "pattern_interpretation"},
                    {"type": "synthesis", "complexity": 0.95, "data": "pattern_synthesis"},
                    {"type": "application", "complexity": 0.9, "data": "pattern_application"}
                ],
                "duration": 10,
                "required_stage": 8,
                "metrics": ["pattern_recognition", "processing_speed", "learning_capacity"]
            },
            "decision_optimization_specialist": {
                "experiences": [
                    {"type": "optimization", "complexity": 0.95, "data": "decision_optimization"},
                    {"type": "analysis", "complexity": 0.9, "data": "outcome_analysis"},
                    {"type": "strategy", "complexity": 0.85, "data": "strategy_optimization"}
                ],
                "duration": 10,
                "required_stage": 8,
                "metrics": ["decision_making", "adaptability", "processing_speed"]
            },
            "multi_task_specialist": {
                "experiences": [
                    {"type": "parallel", "complexity": 0.95, "data": "advanced_parallel_processing"},
                    {"type": "coordination", "complexity": 0.9, "data": "advanced_coordination"},
                    {"type": "optimization", "complexity": 0.85, "data": "task_optimization"}
                ],
                "duration": 10,
                "required_stage": 8,
                "metrics": ["parallel_processing", "task_specialization", "energy_efficiency"]
            },
            "adaptive_learning_specialist": {
                "experiences": [
                    {"type": "adaptation", "complexity": 0.95, "data": "advanced_adaptation"},
                    {"type": "learning", "complexity": 0.9, "data": "learning_optimization"},
                    {"type": "integration", "complexity": 0.85, "data": "knowledge_integration"}
                ],
                "duration": 10,
                "required_stage": 8,
                "metrics": ["learning_capacity", "adaptability", "memory_capacity"]
            }
        }
        
        self.curriculum_paths = {
            "pattern_analysis": [
                "basic_cognition",
                "advanced_patterns",
                "parallel_processing",
                "pattern_analysis_specialist"
            ],
            "decision_optimization": [
                "basic_cognition",
                "resource_efficiency",
                "decision_mastery",
                "decision_optimization_specialist"
            ],
            "multi_task_processing": [
                "basic_cognition",
                "parallel_processing",
                "advanced_patterns",
                "multi_task_specialist"
            ],
            "adaptive_learning": [
                "basic_cognition",
                "social_adaptation",
                "advanced_patterns",
                "adaptive_learning_specialist"
            ]
        }
        
        # Performance assessment criteria
        self.assessment_criteria = {
            "learning_efficiency": {
                "weight": 0.3,
                "metrics": ["learning_capacity", "memory_capacity"]
            },
            "processing_capability": {
                "weight": 0.25,
                "metrics": ["processing_speed", "parallel_processing"]
            },
            "adaptation_rate": {
                "weight": 0.25,
                "metrics": ["adaptability", "error_tolerance"]
            },
            "specialization_progress": {
                "weight": 0.2,
                "metrics": ["task_specialization", "pattern_recognition"]
            }
        }
        
    def load_embryo(self, embryo_file):
        """Load an embryo from its Python file"""
        spec = importlib.util.spec_from_file_location("embryo_module", embryo_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.embryo
        
    def evaluate_embryo(self, embryo):
        """Evaluate embryo's current capabilities and recommend training"""
        status = embryo.get_status()
        
        evaluation = {
            "development_stage": status["development_stage"],
            "experience_level": status["experiences_count"],
            "specializations": status["specializations"],
            "performance_metrics": self._calculate_performance_metrics(status),
            "recommended_programs": [],
            "readiness_assessment": {}
        }
        
        # Assess readiness for each program
        for program, details in self.training_programs.items():
            readiness = self._assess_program_readiness(status, program, details)
            evaluation["readiness_assessment"][program] = readiness
            if readiness["ready"]:
                evaluation["recommended_programs"].append(program)
        
        return evaluation
    
    def _calculate_performance_metrics(self, status):
        """Calculate detailed performance metrics"""
        metrics = {}
        
        for criterion, details in self.assessment_criteria.items():
            score = 0
            for metric in details["metrics"]:
                if metric in status["neural_connections"]:
                    score += status["neural_connections"][metric]
                elif metric in status["potential_capabilities"]:
                    score += status["potential_capabilities"][metric] * 100
            
            metrics[criterion] = (score / len(details["metrics"])) * details["weight"]
        
        metrics["overall_score"] = sum(metrics.values())
        return metrics
    
    def _assess_program_readiness(self, status, program, details):
        """Assess if embryo is ready for a specific program"""
        if status["development_stage"] < details["required_stage"]:
            return {
                "ready": False,
                "reason": "Insufficient development stage",
                "requirements": {
                    "current_stage": status["development_stage"],
                    "required_stage": details["required_stage"]
                }
            }
        
        # Check required metrics
        metric_requirements = {}
        for metric in details["metrics"]:
            current_value = status["neural_connections"].get(metric, 0)
            required_value = 100 * (details["required_stage"] / 10)
            metric_requirements[metric] = {
                "current": current_value,
                "required": required_value,
                "met": current_value >= required_value
            }
        
        ready = all(req["met"] for req in metric_requirements.values())
        
        return {
            "ready": ready,
            "reason": "Ready for training" if ready else "Insufficient metrics",
            "requirements": metric_requirements
        }

    def train_embryo(self, embryo, program_name):
        """Put an embryo through a specific training program"""
        if program_name not in self.training_programs:
            raise ValueError(f"Unknown training program: {program_name}")
            
        program = self.training_programs[program_name]
        training_log = []
        performance_history = []
        
        # Initial assessment
        initial_status = embryo.get_status()
        initial_metrics = self._calculate_performance_metrics(initial_status)
        
        # Run the training program
        for day in range(program["duration"]):
            daily_performance = {
                "day": day + 1,
                "experiences": []
            }
            
            # Apply experiences
            for experience in program["experiences"]:
                # Add some randomization to experience complexity
                modified_experience = experience.copy()
                modified_experience["complexity"] *= random.uniform(0.9, 1.1)
                
                result = embryo.learn_from_experience(modified_experience)
                training_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "program": program_name,
                    "day": day + 1,
                    "experience": modified_experience,
                    "result": result
                })
                daily_performance["experiences"].append({
                    "type": modified_experience["type"],
                    "performance": result["processing_quality"]
                })
            
            # Development step
            embryo.develop()
            
            # Calculate daily performance
            status = embryo.get_status()
            daily_performance["metrics"] = self._calculate_performance_metrics(status)
            performance_history.append(daily_performance)
        
        # Final assessment
        final_status = embryo.get_status()
        final_metrics = self._calculate_performance_metrics(final_status)
        
        # Calculate improvement
        improvement = {
            metric: final_metrics[metric] - initial_metrics[metric]
            for metric in initial_metrics
        }
        
        # Save training log
        log_dir = Path("training_logs")
        log_dir.mkdir(exist_ok=True)
        
        training_record = {
            "program": program_name,
            "embryo_id": embryo.embryo_id,
            "training_log": training_log,
            "performance_history": performance_history,
            "initial_metrics": initial_metrics,
            "final_metrics": final_metrics,
            "improvement": improvement
        }
        
        log_file = log_dir / f"training_{embryo.embryo_id}_{program_name}.json"
        log_file.write_text(json.dumps(training_record, indent=2))
        
        return training_record
    
    def create_curriculum(self, embryo):
        """Create a personalized curriculum based on embryo's specializations"""
        status = embryo.get_status()
        curriculum = []
        specialization_paths = []
        
        # Find relevant curriculum paths based on specializations
        for specialization in status["specializations"]:
            if specialization in self.curriculum_paths:
                specialization_paths.append({
                    "specialization": specialization,
                    "path": self.curriculum_paths[specialization]
                })
        
        # Create ordered curriculum considering prerequisites
        seen_programs = set()
        for path in specialization_paths:
            for program in path["path"]:
                if program not in seen_programs:
                    curriculum.append(program)
                    seen_programs.add(program)
        
        # Calculate estimated metrics
        total_duration = sum(self.training_programs[p]["duration"] for p in curriculum)
        estimated_completion_stage = status["development_stage"]
        for program in curriculum:
            estimated_completion_stage += self.training_programs[program]["duration"] * 0.5
        
        return {
            "embryo_id": embryo.embryo_id,
            "current_stage": status["development_stage"],
            "recommended_curriculum": curriculum,
            "specialization_paths": specialization_paths,
            "estimated_duration": total_duration,
            "estimated_completion_stage": estimated_completion_stage,
            "program_details": {
                program: {
                    "duration": self.training_programs[program]["duration"],
                    "required_stage": self.training_programs[program]["required_stage"],
                    "focus_metrics": self.training_programs[program]["metrics"]
                }
                for program in curriculum
            }
        }

def main():
    # Example usage
    school = EmbryoSchool()
    
    # Load an embryo (you'll need to provide a valid embryo file path)
    embryo_files = list(Path("embryos").glob("embryo_*.py"))
    if not embryo_files:
        print("No embryo files found in 'embryos' directory")
        return
        
    embryo = school.load_embryo(embryo_files[0])
    
    # Evaluate the embryo
    evaluation = school.evaluate_embryo(embryo)
    print("\nEmbryo Evaluation:")
    print(json.dumps(evaluation, indent=2))
    
    # Create a curriculum
    curriculum = school.create_curriculum(embryo)
    print("\nRecommended Curriculum:")
    print(json.dumps(curriculum, indent=2))
    
    # Train the embryo through recommended programs
    for program in curriculum["recommended_curriculum"]:
        try:
            result = school.train_embryo(embryo, program)
            print(f"\nCompleted {program}:")
            print(json.dumps(result, indent=2))
        except ValueError as e:
            print(f"\nCannot complete {program}: {e}")

if __name__ == "__main__":
    main()
