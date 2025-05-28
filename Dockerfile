# Final Stage (Smaller Runtime Image)
FROM python:3.12-bookworm

WORKDIR /app

# Create a non-root user and group
RUN adduser --system --group appuser

# Change ownership of the WORKDIR to the new user *while still root*
RUN chown appuser:appuser /app

# Switch to the non-root user
USER appuser

# Create a temporary directory that the appuser can write to.
# This is crucial for pip's operations.
RUN mkdir -p /app/tmp && chmod 777 /app/tmp

# Set environment variables, including TMPDIR for pip's temporary files.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TMPDIR /app/tmp

# Install alembic
RUN pip install --no-cache-dir alembic

# Copy all your application code from the build context.
COPY --chown=appuser:appuser . .

# Ensure the entrypoint script is executable AFTER all files have been copied.
RUN chmod +x /app/entrypoint.sh

# Expose the application port (if applicable)
EXPOSE 8000

# Define the command to run your application
ENTRYPOINT ["/app/entrypoint.sh"]