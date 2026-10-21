FROM python:3.9-slim

# Working directory inside the container
WORKDIR /app

# Copy everything in backend_files (app.py, model, requirements) into /app
COPY . .

# Install the pinned dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the API with Gunicorn: 4 workers, listening on port 7860 on all interfaces
# "app:superkart_api" = file app.py, Flask object named superkart_api
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
