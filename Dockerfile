FROM public.ecr.aws/lambda/python:3.12

# 2. Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}   
# 3. Install dependencies
# We use --extra-index-url for a CPU-only torch to save massive amounts of space
# We also explicitly install a pre-compiled version of pyarrow to avoid the build error
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pyarrow==15.0.0 && \
    pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# 4. Copy your application code
COPY . ${LAMBDA_TASK_ROOT} 

# 5. Set the Mangum handler
CMD [ "main.handler" ]