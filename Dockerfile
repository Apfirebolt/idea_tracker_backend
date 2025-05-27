# Final Stage (Smaller Runtime Image)
FROM python:3.12-slim

WORKDIR /app

# Install alembic BEFORE switching to the non-root user
RUN pip install --no-cache-dir alembic

# Copy Alembic configuration and scripts
COPY ./alembic.ini .
COPY ./alembic /app/alembic
COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

# Copy all your application code from the build context
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the application port (if applicable)
EXPOSE 8000

# Define the command to run your application
ENTRYPOINT ["/app/entrypoint.sh"]