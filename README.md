#### ⭐ Please, give this repository a ⭐! Your support motivates me to create more! ⭐

## Script Description and Setup

The script converts audio files into text using the OpenAI API. It takes an audio file, splits it into parts if it's too long, sends these parts to OpenAI for transcription, and then combines the resulting text into one file.

### Step 1: Install Python on Your Computer (if necessary)

1. **Install Python**:
   - **On macOS**: Open Terminal and run:
     ```sh
     brew install python
     ```
   - **On Windows**: Download the installer from the [official Python website](https://www.python.org/downloads/windows/), run it, and follow the instructions (make sure to check "Add Python to PATH").


3. **Install Required Libraries**:
   - Open Command Prompt (or Terminal) and run:
     ```sh
     pip install pydub openai
     ```

### Step 2: Get an OpenAI API Key

1. Sign up on the [OpenAI website](https://platform.openai.com) and log in.
2. Go to the API keys section in your OpenAI dashboard.
3. Generate a new API key and copy it.

### Step 3: Set the API Key Globally on Your System

**On macOS:**
1. Open Terminal.
2. Open your shell profile file (for example, for bash, open `.bash_profile`):
   ```sh
   nano ~/.bash_profile
   ```
3. Add the following line:
   ```sh
   export OPENAI_API_KEY='your_openai_api_key'
   ```
4. Save the file and close the editor (Ctrl + X, then Y, then Enter).
5. Apply the changes:
   ```sh
   source ~/.bash_profile
   ```

**On Windows:**
1. Open Command Prompt.
2. Run the command:
   ```cmd
   setx OPENAI_API_KEY "your_openai_api_key"
   ```
3. Restart Command Prompt to use the new environment variable.

### Step 4: Run the Script with the Audio File Path

1. Copy and past file named `transcribe.py` on Your Computer (change the file name if you want)
2. Open Command Prompt or Terminal.
3. Navigate to the directory where your script is located.
4. Run the command:
   ```sh
   python your_script_name.py path_to_your_audio_file
   ```
   Example:
   ```sh
   python transcribe.py my_audio_file.m4a
   ```

### Optionaly Modify the Script

**Choosing the Transcription Model**:
- The script currently uses the `"whisper-1"` model. You can change this value in the line:
  ```python
  response = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
  )
  ```
  For example, to use a different model, replace `"whisper-1"` with the desired model name.

**Adding Post-Processing**:
- To add post-processing, such as creating meeting notes or summaries, modify the `main` function or add a new function to process the text after it is obtained. Example:

  ```python
  def create_summary(transcript):
    # Пример постобработки для создания резюме
    summary = f"Summary of the meeting:\n{transcript[:200]}..."
    return summary

  def main(speech_file):
    full_transcription = transcribe_audio(speech_file)
    summary = create_summary(full_transcription)
    
    with open("transcription.txt", "w") as file:
        file.write(full_transcription)
    
    with open("summary.txt", "w") as file:
        file.write(summary)
  ```
