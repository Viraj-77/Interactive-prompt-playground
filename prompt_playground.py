import os
import time
from datetime import datetime
from dotenv import load_dotenv
import openai
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Load environment variables
load_dotenv()

class PromptPlayground:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.experiments = []
        self.available_models = ["gpt-3.5-turbo"]  # Default to gpt-3.5-turbo only
        
        # Test if GPT-4 is available
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            self.available_models.append("gpt-4")
        except:
            pass  # GPT-4 not available, stick with gpt-3.5-turbo
        
    def get_user_input(self, prompt, default=None, type_func=str):
        """Get user input with optional default value and type conversion."""
        if default is not None:
            prompt = f"{prompt} (default: {default}): "
        else:
            prompt = f"{prompt}: "
            
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input == "" and default is not None:
                    return default
                return type_func(user_input)
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")

    def get_float_input(self, prompt, min_val, max_val, default=None):
        """Get float input within specified range."""
        while True:
            value = self.get_user_input(prompt, default, float)
            if min_val <= value <= max_val:
                return value
            print(f"{Fore.RED}Please enter a value between {min_val} and {max_val}{Style.RESET_ALL}")

    def get_stop_sequences(self):
        """Get stop sequences from user."""
        sequences = []
        while True:
            seq = input("Enter a stop sequence (or press Enter to finish): ").strip()
            if not seq:
                break
            sequences.append(seq)
        return sequences if sequences else None

    def select_model(self):
        """Let user select the model."""
        print("\nAvailable models:")
        for i, model in enumerate(self.available_models, 1):
            print(f"{i}. {model}")
        
        while True:
            try:
                choice = int(input("\nSelect model number: ")) - 1
                if 0 <= choice < len(self.available_models):
                    return self.available_models[choice]
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")

    def get_parameters(self):
        """Get all parameters from user."""
        print(f"\n{Fore.CYAN}=== Parameter Selection ==={Style.RESET_ALL}")
        
        model = self.select_model()
        temperature = self.get_float_input("Temperature (0.0 - 2.0)", 0.0, 2.0, 0.7)
        max_tokens = int(self.get_float_input("Max tokens (1 - 4096)", 1, 4096, 150))
        presence_penalty = self.get_float_input("Presence penalty (-2.0 to 2.0)", -2.0, 2.0, 0.0)
        frequency_penalty = self.get_float_input("Frequency penalty (-2.0 to 2.0)", -2.0, 2.0, 0.0)
        
        print("\nStop sequences (press Enter with no input to finish)")
        stop = self.get_stop_sequences()
        
        return {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "stop": stop,
            "model": model  # Keep model separate from other params
        }

    def estimate_cost(self, model, max_tokens):
        """Estimate the cost of the API call."""
        # Approximate costs per 1K tokens (input + output)
        costs = {
            "gpt-3.5-turbo": 0.0015,
            "gpt-4": 0.03
        }
        # Rough estimation assuming input is about 50 tokens
        total_tokens = 50 + max_tokens
        cost = (total_tokens / 1000) * costs.get(model, 0.0015)
        return cost

    def generate_description(self, product, params):
        """Generate product description using OpenAI API."""
        try:
            estimated_cost = self.estimate_cost(params["model"], params["max_tokens"])
            print(f"\n{Fore.YELLOW}Estimated cost: ${estimated_cost:.4f}{Style.RESET_ALL}")
            
            if not input("\nPress Enter to proceed (or 'q' to quit): ").lower().startswith('q'):
                # Separate model from other parameters
                model = params.pop("model")
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional product copywriter."},
                        {"role": "user", "content": f"Write a product description for: {product}"}
                    ],
                    **params
                )
                # Put model back in params
                params["model"] = model
                
                output = response.choices[0].message['content'].strip()
                
                # Save experiment
                experiment = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "product": product,
                    **params,
                    "output": output,
                    "tokens_used": response.usage.total_tokens,
                    "actual_cost": (response.usage.total_tokens / 1000) * self.estimate_cost(params["model"], 1000)
                }
                self.experiments.append(experiment)
                
                return output
            
            return None
            
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            return None

    def generate_reflection(self):
        """Generate a reflection on parameter effects using GPT."""
        if len(self.experiments) < 2:
            return None
            
        try:
            # Prepare experiment data for analysis
            experiment_data = []
            for exp in self.experiments:
                experiment_data.append(
                    f"Parameters: model={exp['model']}, temp={exp['temperature']}, "
                    f"presence_penalty={exp['presence_penalty']}, frequency_penalty={exp['frequency_penalty']}\n"
                    f"Output: {exp['output']}\n"
                )
            
            # Generate reflection
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI researcher analyzing how different parameters affect AI outputs."},
                    {"role": "user", "content": f"Analyze these outputs and explain in two paragraphs how the different parameters affected the responses:\n\n{''.join(experiment_data)}"}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message['content'].strip()
            
        except Exception as e:
            print(f"{Fore.RED}Error generating reflection: {str(e)}{Style.RESET_ALL}")
            return None

    def display_comparison_grid(self):
        """Display a comparison grid of experiments in the console."""
        if not self.experiments:
            return
            
        print(f"\n{Fore.CYAN}=== Parameter Comparison Grid ==={Style.RESET_ALL}")
        
        # Create comparison table
        headers = ["Model", "Temp", "P.Penalty", "F.Penalty", "Tokens", "Cost", "Output Preview"]
        table_data = []
        
        for exp in self.experiments:
            # Truncate output for preview
            output_preview = exp['output'][:50] + "..." if len(exp['output']) > 50 else exp['output']
            
            table_data.append([
                exp['model'],
                exp['temperature'],
                exp['presence_penalty'],
                exp['frequency_penalty'],
                exp['tokens_used'],
                f"${exp['actual_cost']:.4f}",
                output_preview
            ])
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def save_results(self):
        """Save experiments to a markdown file."""
        if not self.experiments:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Prompt Playground Results\n\n")
            
            # Write experiment table
            headers = ["Timestamp", "Product", "Model", "Temp", "Max Tokens", "P.Penalty", "F.Penalty", "Stop", "Tokens", "Cost"]
            table_data = []
            
            for exp in self.experiments:
                table_data.append([
                    exp["timestamp"],
                    exp["product"],
                    exp["model"],
                    exp["temperature"],
                    exp["max_tokens"],
                    exp["presence_penalty"],
                    exp["frequency_penalty"],
                    exp["stop"],
                    exp["tokens_used"],
                    f"${exp['actual_cost']:.4f}"
                ])
            
            f.write(tabulate(table_data, headers=headers, tablefmt="pipe"))
            f.write("\n\n## Generated Outputs\n\n")
            
            # Write detailed outputs
            for i, exp in enumerate(self.experiments, 1):
                f.write(f"### Experiment {i}\n")
                f.write(f"- **Product:** {exp['product']}\n")
                f.write(f"- **Parameters:**\n")
                f.write(f"  - Model: {exp['model']}\n")
                f.write(f"  - Temperature: {exp['temperature']}\n")
                f.write(f"  - Max Tokens: {exp['max_tokens']}\n")
                f.write(f"  - Presence Penalty: {exp['presence_penalty']}\n")
                f.write(f"  - Frequency Penalty: {exp['frequency_penalty']}\n")
                f.write(f"  - Stop Sequences: {exp['stop']}\n")
                f.write(f"- **Output:**\n\n```\n{exp['output']}\n```\n\n")
            
            # Add reflection if we have multiple experiments
            reflection = self.generate_reflection()
            if reflection:
                f.write("\n## Parameter Effect Analysis\n\n")
                f.write(reflection)

    def run(self):
        """Main interaction loop."""
        print(f"{Fore.GREEN}Welcome to the Interactive Prompt Playground!{Style.RESET_ALL}")
        print("Test different OpenAI API parameters and see their effects on product descriptions.")
        
        product = input("\nEnter the product name to describe: ").strip()
        
        while True:
            params = self.get_parameters()
            output = self.generate_description(product, params)
            
            if output:
                print(f"\n{Fore.GREEN}Generated Description:{Style.RESET_ALL}")
                print(output)
                
                print(f"\n{Fore.CYAN}Tokens used: {self.experiments[-1]['tokens_used']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Actual cost: ${self.experiments[-1]['actual_cost']:.4f}{Style.RESET_ALL}")
                
                # Show comparison grid after each successful generation
                self.display_comparison_grid()
            
            choice = input("\nOptions:\n1. Try different parameters\n2. Try different product\n3. Save and quit\nYour choice (1-3): ")
            
            if choice == "2":
                product = input("\nEnter the new product name: ").strip()
            elif choice == "3":
                break
                
        if self.experiments:
            self.save_results()
            print(f"\n{Fore.GREEN}Results saved to results_[timestamp].md{Style.RESET_ALL}")
            print("The results file includes a detailed analysis of how parameters affected the outputs.")

if __name__ == "__main__":
    playground = PromptPlayground()
    playground.run() 