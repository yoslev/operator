# ---------- Stage 1: Builder ----------
FROM python:3 AS builder

# Install tools and Azure CLI
RUN apt-get update && \
    apt-get install -y curl apt-transport-https lsb-release gnupg && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install AzCopy (download and extract binary)
RUN curl -sL https://aka.ms/downloadazcopy-v10-linux -o azcopy.tar.gz && \
    mkdir /azcopy && \
    tar -xzf azcopy.tar.gz -C /azcopy --strip-components=1 && \
    rm azcopy.tar.gz
# ---------- Stage 2: Final Image ----------
FROM python:3

# Copy Azure CLI binaries from builder stage
COPY --from=builder /usr/bin/az /usr/bin/az
COPY --from=builder /opt/az /opt/az
COPY --from=builder /usr/share/az* /usr/share/

# Copy AzCopy binary
COPY --from=builder /azcopy/azcopy /usr/bin/azcopy

# Verify Azure CLI
RUN az version

# Set working directory
WORKDIR /app
COPY scripts/ ./scripts/
COPY requirements.txt .
COPY . .

# (Optional) Copy requirements and install Python deps
# COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "/app/main.py" ]
