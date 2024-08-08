# Base image
FROM vocodedev/vocode:latest

# Set working directory
WORKDIR /code

# Copy dependency files
COPY ./pyproject.toml ./poetry.lock /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy application files
COPY app /code/app

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["uvicorn", "inbound:app", "--host", "0.0.0.0", "--port", "3000"]
