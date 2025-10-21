# DockerFile to create a Container Image for lambda 

FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

# Install required tools using microdnf (Amazon Linux 2023)
RUN microdnf update -y && \
    microdnf install -y tar gzip && \
    microdnf clean all

# Install crane binary instead of Docker
RUN curl -L "https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz" | \
    tar xz -C /usr/local/bin crane && \
    chmod +x /usr/local/bin/crane

# Install Python dependencies
RUN pip install boto3

# Copy Lambda function code
COPY crane-app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["crane-app.lambda_handler"]
