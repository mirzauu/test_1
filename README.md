# Image Upload and Description API

This project provides a RESTful API built using Django and Django REST Framework (DRF) to upload images, generate descriptions using an external Large Language Model (LLM), and return the image with categorized descriptions.

## Features

### 1. Image Upload
- Accepts image files through a `POST` request.
- Validates the uploaded images (e.g., file size, type, and resolution).

### 2. Integration with Gemini LLM API
- Processes the uploaded image using an external LLM (e.g., Gemini API).
- Generates descriptions in three tones:
  - **Formal**
  - **Humorous**
  - **Critical**

### 3. API Response
- Returns a JSON response containing:
  - The uploaded image URL.
  - An array of descriptions categorized by tone.

## Requirements

### Prerequisites
- Python 3.8+
- Django 4.2+
- Django REST Framework
- External dependencies (installed via `pip`):
  - `requests`
  - `boto3` (if using AWS for storage)
  - `Pillow` (for image handling)

### Environment Variables
Create a `.env` file in the root directory and add the following keys:
```env
SECRET_KEY=django-insecure-!e#p-307msd%47vpac1ai^9tv*25m13j_n)79e$%&q$3#x0v0x
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_NAME=test1
DATABASE_USER=postgres
DATABASE_PASSWORD=alimirsa1
DATABASE_HOST=localhost
DATABASE_PORT=5432

AWS_ACCESS_KEY_ID=AKIAZQ3DTQE3ICSXLYZJ
AWS_SECRET_ACCESS_KEY=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
AWS_STORAGE_BUCKET_NAME=machinetest12
AWS_S3_REGION_NAME=us-east-1
AWS_QUERYSTRING_AUTH=False

GEMINI_API_KEY=AIzaSyCNdJFrGBa8sS7A_aqf19BDiuuLKZEOIOI
```

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mirzauu/test_1
   cd test_1
   ```

2. **Create a Virtual Environment and Install Dependencies**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Ensure the `.env` file is properly configured as mentioned above.

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. **Upload Image**
- **URL**: `/api/upload-image/`
- **Method**: `POST`
- **Request Body**:
  - `image` (file): The image file to upload.

- **Response**:
  ```json
  {
    "id": 1,
    "image": "https://<bucket-name>/<image-path>",
    "descriptions": {
        "formal": "A formal description of the image.",
        "humorous": "A humorous description of the image.",
        "critical": "A critical description of the image."
    }
  }
  ```

### Error Handling
- Returns appropriate HTTP status codes and error messages for invalid requests or unexpected failures.

## Testing

Run tests using Django's built-in test framework:
```bash
python manage.py test
```

## Deployment

1. Set up the production environment with proper database and storage configurations.
2. Configure the server (e.g., Gunicorn and Nginx) for deployment.
3. Use `AWS S3` or another cloud storage service for handling uploaded images.

## Additional Details

- **Code Structure**:
  - `views.py`: Contains the API view logic.
  - `models.py`: Defines the `UploadedImage` and `ImageDescription` models.
  - `serializers.py`: Handles the serialization of model data.
  - `urls.py`: Maps API endpoints to views.

- **LLM Integration**: Utilizes the Gemini API to analyze images and generate descriptions based on specific prompts.

## Future Improvements
- Add authentication for secured API access.
- Support additional tones or description styles.
- Include advanced image validation (e.g., resolution checks).

## Contribution

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License.

