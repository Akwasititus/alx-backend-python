# Step 1: Use Python 3.10 as the base image
FROM python:3.10

# Step 2: Set environment variables to make Python run better
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 5: Install Python packages inside the container
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 6: Copy the rest of your app code into the container
COPY . /app/

# Step 7: Expose the port Django runs on
EXPOSE 8000

# Step 8: Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
