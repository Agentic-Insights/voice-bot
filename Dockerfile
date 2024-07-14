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
COPY main.py speller_agent.py prompt_handler.py system_prompt.md /code/

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
