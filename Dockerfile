FROM nvidia/cuda-ppc64le:base

# Set environment variables for CUDA
ENV PATH /usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Install necessary dependencies
RUN yum update && apt-get install -y python3-devel

# Install PyTorch for ppc64le architecture with CUDA support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117/ppc64le

# Install Lightning, LitServer, transformers, pandas, matplotlib
RUN pip3 install lightning lit-server pandas matplotlib transformers sentencepiece

# Create a working directory
WORKDIR /workspace

# Copy the LitServer app code into the container
COPY . /workspace

# Expose the port for LitServer
EXPOSE 5000

# Run the LitServer
CMD ["lit-server", "--app", "litserve_app.py", "--host", "0.0.0.0", "--port", "5000"]
