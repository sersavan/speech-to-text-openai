#### ⭐ Support this repository by giving it a ⭐

## Script Overview

The script converts speech from audio file to text using the OpenAI API. It handles audio file splitting, sends parts to OpenAI for transcription, combines the text, and optionally creates summaries and timestamps. Supported file types include `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, and `webm`.

### Step 1: Install Python and Libraries

1. **Install Python**:
   - **macOS**: Open Terminal and run:
     ```sh
     brew install python
     ```
   - **Windows**: Download and install from [Python website](https://www.python.org/downloads/windows/), check "Add Python to PATH".

2. **Install Libraries**:
   ```sh
   pip install pydub openai
   ```

### Step 2: Get an OpenAI API Key

1. Sign up and log in at [OpenAI](https://platform.openai.com).
2. Generate a new API key in your dashboard.

### Step 3: Set API Key

**macOS:**
1. Open Terminal.
2. Edit your shell profile:
   ```sh
   nano ~/.bash_profile
   ```
3. Add:
   ```sh
   export OPENAI_API_KEY='your_openai_api_key'
   ```
4. Save and apply changes:
   ```sh
   source ~/.bash_profile
   ```

**Windows:**
1. Open Command Prompt.
2. Run:
   ```cmd
   setx OPENAI_API_KEY "your_openai_api_key"
   ```
3. Restart Command Prompt.

### Step 4: Run the Script

1. Save the script as `transcribe.py`.
2. Open Command Prompt or Terminal, navigate to the script directory.
3. Run:
   ```sh
   python transcribe.py path_to_your_audio_file
   ```
   For Python 3, use:
   ```sh
   python3 transcribe.py path_to_your_audio_file
   ```

Example:
```sh
python transcribe.py audio.m4a
```

### Optional Parameters

- `--sum`: Create a summary.
- `--time`: Include timestamps.

Example:
```sh
python transcribe.py audio.m4a --sum --time
```
