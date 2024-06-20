# Leyline Image2Video

This project is a web application that allows users to upload an image and receive a generated video based on that
image.

The system simulates an artificial intelligence (AI) model that processes each image to generate a video. The AI
model is resource-intensive and has a fixed processing time (30 seconds).

## Features

- Users can see the current status of their video generation task, including real-time progress.
- The AI model simulation takes 30 seconds to process each image and can only handle one image at a time.

## Tech Stack

- **Backend**: Flask
- **Task Queue**: Celery with Redis as the message broker
- **Storage**: Local file storage for images and generated videos
- **Containerization**: Docker and Docker Compose

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sergioasantiago/leyline-image2video.git
   cd leyline-image2video
   ```

2. **Build and start the containers:**

   ```bash
   docker-compose build
   docker-compose up
   ```

This will start 3 containers:

- redis: used by Celery to store the tasks and share the progress as well as the result
- worker: Celery worker responsible to simulate the job that generate the video based on the tasks in Redis
- image2video: Web application responsible to receive the image, create a new task in Redis and serve the status and
  video result

3. **Backend will accessible through:**
    - Backend: `http://localhost:8080`

### API Endpoints

#### 1. Upload an Image

**Endpoint:**

```plaintext
POST /upload
```

**Description:**
Upload an image to start the video generation process.

**Request:**

- `image`: The image file to upload.

**Response:**

- `task_id`: The ID of the video generation task.

**Example:**

```bash
curl -X POST -F "image=@examples/image.png" http://localhost:8080/upload
```

#### 2. Check Task Status

**Endpoint:**

```plaintext
GET /status/<task_id>
```

**Description:**
Check the status and progress of the video generation task.

**Response:**

- `state`: The current state of the task (e.g., PENDING, PROCESSING, SUCCESS).
- `progress`: The progress percentage of the task.
- `video_url`: The URL of the generated video (if the task is completed).

**Example:**

```bash
curl http://localhost:8080/status/<task_id>
```

#### 3. View Generated Video

**Endpoint:**

```plaintext
GET /video/<filename>
```

**Description:**
View the generated video.

**Example:**

```bash
curl http://localhost:8080/video/<filename>
```

### Celery Configuration

Celery is used to handle the background tasks for processing images.
The configuration is set up in `tasks.py` and `docker-compose.yml`.

### Notes

- Due to time constraints, no frontend was implemented. Currently, user can download the video via api, but that must be
  controlled by the frontend to make the video read-only.
- The simulated AI model processing time is set to 30 seconds.
- Only one image can be processed at a time due to the simulated AI model's constraints.
- If it is required to have parallel processing, more Celery workers can be created.

### What's Next

Following are some ideas for future improvements to the project:

- Long term storage: The current setup uses a docker volume to share the uploaded images and generated videos. Use a
  more scalable storage solution like AWS S3 for storing images and videos.
- Real AI Model Integration: Replace the simulated AI model with a real AI model for image-to-video generation.
- User Authentication: Implement user authentication to allow users to track their video generation history. Secure
  endpoints to ensure that only authenticated users can upload images and view generated videos.
- Add email or SMS notifications to inform users when their video is ready.
- Error Handling and Logging: Improve error handling and coverage on edge cases, e.g: big images.
- Implement copyright check on images and abusive content.