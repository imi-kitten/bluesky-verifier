# 🦋 Bluesky Verifier Bot

An automated tool to manage user verification on [Bluesky](https://bsky.app) by monitoring likes on a specific post and issuing verification records to everyone that likes the watched post

---

## 🔍 Features

- **Post Monitoring**: Watches a specified Bluesky post via its `at://` URI.  
- **User Verification**: Generates verification records for users who like the monitored post.  
- **Change Detection**: Tracks changes in user handles or display names and updates verification records when changes are detected.  
- **Efficient Data Handling**: Utilizes Redis to cache user data, reducing API calls and enabling quick change detection.

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose plugin installed on your system.

### Setup Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/imi-kitten/bluesky-verifier.git
   cd bluesky-verifier
   ```

2. **Configure Environment Variables**:

   Copy the example Docker Compose file and replace the environment variables with your own values.

   ```bash
   cp example.docker-compose.yml docker-compose.yml
   ```

   Edit `docker-compose.yml` and set the following environment variables:

   - `BSKY_HANDLE`: Your Bluesky handle.  
   - `BSKY_APP_PASSWORD`: Your Bluesky app password.  
   - `POST_URI`: The `at://` URI of the post to monitor.  
   - `REDIS_HOST`: Hostname for your Redis instance (default: `redis`).  
   - `REDIS_PORT`: Port for your Redis instance (default: `6379`).

3. **Deploy the Bot**:

   Start the services using Docker Compose:

   ```bash
   docker compose up -d
   ```

   The bot will now monitor the specified post and manage verification records for users who like it.

---

## ⚙️ Environment Variables

| Variable            | Description                                         |
|---------------------|-----------------------------------------------------|
| `BSKY_HANDLE`       | Your Bluesky handle.                                |
| `BSKY_APP_PASSWORD` | Your Bluesky app password.                          |
| `POST_URI`          | The `at://` URI of the post to monitor.             |
| `REDIS_HOST`        | Hostname for your Redis instance (default: `redis`).|
| `REDIS_PORT`        | Port for your Redis instance (default: `6379`).     |

---

## 🐳 Docker Notes

- The provided `Dockerfile` will build the required container, and is the basis for the live container
- The `example.docker-compose.yml` file demonstrates how to configure and deploy the bot along with a Redis instance.

---

## 🛠️ Development & Local Building

### Running Locally for Development

1. **Clone the repository and install dependencies locally (optional):**

   ```bash
   git clone https://github.com/imi-kitten/bluesky-verifier.git
   cd bluesky-verifier
   ```

2. **Build the Docker container locally:**

   ```bash
   docker build -t bluesky-verifier:dev .
   ```

3. **Update your `docker-compose.yml` to use the local image:**

   Change the `image:` line to:  
   ```
   image: bluesky-verifier:dev
   ```
   Or remove the `image:` line and uncomment/add the `build:` section:  
   ```
   build: .
   ```

4. **(Optional) If editing Python files, rebuild the image to include your changes:**

   ```bash
   docker compose build
   ```

5. **Start the services (including Redis):**

   ```bash
   docker compose up
   ```

6. **For interactive development, you can run the container in the foreground:**

   ```bash
   docker compose run --rm bluesky-verifier
   ```

7. **Stop and clean up:**

   ```bash
   docker compose down
   ```

---


## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
