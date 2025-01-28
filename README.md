# OrbAI

Welcome to OrbAI, the AI-driven Twitch streamer that revolutionizes viewer interaction. OrbAI isn't just a bot; it's a fully dynamic AI that can chat, react, and adapt to live stream activities in real-time.

## Features

- **Dynamic AI Streaming**: Engage with viewers using an AI that learns and adapts during the stream.
- **Interactive Commands**: Let viewers shape the stream through AI-driven interactions.
- **Concurrent Frontend and Backend**: Smooth simultaneous operation of React and Python components for a seamless user experience.
- **Secure API Integration**: Uses Twitch and OpenAI APIs securely to enhance capabilities.

## Getting Started

Follow these steps to set up and run OrbAI on your Twitch channel:

### Prerequisites

Make sure you have Node.js, npm, and Python installed on your system. You will also need Twitch account credentials and an OpenAI API key.

### Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/OrbAI.git
   ```
2. **Navigate to the project directory**:
   ```
   cd OrbAI
   ```
3. **Install JavaScript dependencies**:
   ```
   npm install
   ```
4. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. **Set up the `.env` file**:
   Create a `.env` file in the root directory and add your Twitch and OpenAI API keys:
   ```
   TWITCH_API_KEY=your_twitch_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
2. **Configure additional settings** (optional) in the `.env` file as needed.

### Running the Application

To run both the frontend and backend concurrently:

1. **Start the React frontend**:
   ```
   npm start
   ```
2. **In another terminal, launch the Python backend**:
   ```
   python app.py
   ```

These commands will start the services needed for OrbAI to operate on your Twitch channel. Ensure both services are running to handle interactions fully.

## Usage

With OrbAI active, viewers can start interacting through the chat. Customize commands and responses within the project to tailor the AI's personality and interaction style.

## Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. I would greatly appreciate any contributions you make.

## License

Distributed under the MIT License. See `LICENSE` for more information.



Thank you for exploring OrbAI. Happy streaming!

