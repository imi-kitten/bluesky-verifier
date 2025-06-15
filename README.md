# Bluesky Verifier

An automated verification bot for [Bluesky](https://bsky.app) that monitors likes on a specific post and issues verification records to users who interact with it.

## ✨ Features

- **Post Monitoring**: Continuously watches a specified Bluesky post via its `at://` URI
- **Automatic Verification**: Generates verification records for users who like the monitored post
- **Change Detection**: Tracks changes in user handles and display names, updating verification records accordingly
- **Efficient Caching**: Uses Redis to cache user data, minimizing API calls and enabling fast change detection
- **Docker Ready**: Fully containerized for easy deployment

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose plugin installed
- A Bluesky account with an app password
- The `at://` URI of the post you want to monitor

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/imi-kitten/bluesky-verifier.git
   cd bluesky-verifier
   ```

2. **Configure environment variables:**
   ```bash
   cp example.docker-compose.yml docker-compose.yml
   ```

   Edit `docker-compose.yml` and update the environment variables with your values.

3. **Deploy the bot:**
   ```bash
   docker compose up -d
   ```

The bot will start monitoring your specified post and automatically manage verification records!

## ⚙️ Configuration

Configure the bot by setting these environment variables in your `docker-compose.yml`:

| Variable | Description | Required |
|----------|-------------|----------|
| `BSKY_HANDLE` | Your Bluesky handle (e.g., `user.bsky.social`) | ✅ |
| `BSKY_APP_PASSWORD` | Your Bluesky app password | ✅ |
| `POST_URI` | The `at://` URI of the post to monitor | ✅ |
| `REDIS_HOST` | Redis hostname (default: `redis`) | ❌ |
| `REDIS_PORT` | Redis port (default: `6379`) | ❌ |

### Getting Your App Password

1. Go to [Bluesky Settings](https://bsky.app/settings)
2. Navigate to "App Passwords"
3. Create a new app password for this bot
4. Use this password (not your account password) in the configuration

### Finding a Post URI

The post URI format is: `at://did:plc:USER_ID/app.bsky.feed.post/POST_ID`

You can find this in the post's URL or by using Bluesky's API tools.

## 🔧 Development

### Local Development

1. **Clone and build locally:**
   ```bash
   git clone https://github.com/imi-kitten/bluesky-verifier.git
   cd bluesky-verifier
   docker build -t bluesky-verifier:dev .
   ```

2. **Update docker-compose.yml for local development:**
   ```yaml
   services:
     bluesky-verifier:
       build: .
       # Remove or comment out the 'image:' line
   ```

3. **Run with live logs:**
   ```bash
   docker compose up
   ```

4. **Rebuild after code changes:**
   ```bash
   docker compose build
   docker compose up
   ```

### Interactive Development

For debugging or interactive development:

```bash
docker compose run --rm bluesky-verifier
```

### Cleanup

To stop and remove all containers:

```bash
docker compose down
```

## 🏗️ Architecture

The bot consists of:

- **Python Application**: Core verification logic and Bluesky API integration
- **Redis Cache**: Stores user data and tracks changes efficiently
- **Docker Container**: Ensures consistent deployment across environments

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Issues

Found a bug or have a feature request? Please [open an issue](https://github.com/imi-kitten/bluesky-verifier/issues) with:

- Clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (OS, Docker version, etc.)
