import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM
from lightning import LightningApp, LightningFlow
from lit_server import LitServer, module

# Define a simple neural network model for demonstration
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(1000, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Define LLAMA Inference Module
class LLAMAModule(LightningFlow):
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load the LLAMA model and tokenizer from HuggingFace Transformers
        model_name = "huggingface/llama"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    @module
    def llama_inference(self, prompt: str = "Hello, this is a test"):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(inputs["input_ids"], max_length=50)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Define tasks to be exposed by the LitServer
class ComputeModule(LightningFlow):

    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SimpleNN().to(self.device)

    @module
    def matrix_multiplication(self):
        a = torch.randn((1000, 1000), device=self.device)
        b = torch.randn((1000, 1000), device=self.device)
        result = torch.mm(a, b)
        return result[0][0].item()

    @module
    def neural_network_inference(self):
        input_data = torch.randn(1, 1000, device=self.device)
        with torch.no_grad():
            output = self.model(input_data)
        return output[0].cpu().numpy().tolist()

# The main LitServer app
class LitServeApp(LightningApp):
    def __init__(self):
        super().__init__()
        self.compute_module = ComputeModule()
        self.llama_module = LLAMAModule()

# Run LitServer
if __name__ == "__main__":
    app = LitServeApp()
    LitServer(app).start(host="0.0.0.0", port=5000)
