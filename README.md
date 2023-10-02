# StickerRefacerBot Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Project Overview](#project-overview)
   - [Pipeline Stages](#pipeline-stages)
   - [Configuration](#configuration)
4. [Usage](#usage)
   - [Running Locally](#running-locally)
   - [Deployment on Google Cloud Compute Engine](#deployment-on-google-cloud-compute-engine)
5. [Contributing](#contributing)
6. [License](#license)

---

## 1. Introduction <a name="introduction"></a>

**StickerRefacerBot** is a Python-based chatbot project that leverages the Telegram API through the pyTelegramBotAPI library. It allows users to upload images, detect faces, overlay stickers, and modify them before finalizing the image. The project also utilizes Google Cloud for storage and the Google Image Search API for testing image downloads. Additionally, it employs OpenCV for Haar Cascade face detection and Pillow (PIL) for image manipulation.

## 2. Getting Started <a name="getting-started"></a>

### Prerequisites <a name="prerequisites"></a>

Before using StickerRefacerBot, ensure you have the following prerequisites installed and set up:

- Python 3.6 or higher
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library
- Google Cloud credentials and storage bucket
- Google Image Search API key
- OpenCV (cv2)
- Pillow (PIL)

### Installation <a name="installation"></a>

1. Clone the StickerRefacerBot repository from GitHub:

   ```bash
   git clone https://github.com/yourusername/StickerRefacerBot.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## 3. Project Overview <a name="project-overview"></a>

### Pipeline Stages <a name="pipeline-stages"></a>

StickerRefacerBot operates in a pipeline with the following stages:

1. **START**: Captures user data from Telegram messages and prompts the user to upload a PNG image.

2. **UPLOAD**: Checks the uploaded image's compatibility, downloads it using the bot's download link specified in `CONFIG.py`, and informs the user of success or failure.

3. **DETECT**: Allows the user to detect faces in the uploaded image using Haar Cascade, with three different thresholds represented by colored squares (R, G, B) over the faces in the preview image.

4. **MATCH**: Prompts the user to provide a sticker and match it to a numerically labeled face in the preview image, with options to match to multiple or match to all.

5. **MODIFY**: Lets the user flip or scale the selected sticker by clicking the keypad number corresponding to the detected face it overlays. The preview image updates as the user makes modifications.

6. **FINALIZE**: Previews the final image with matched, modified, and overlaid stickers and prompts the user to confirm or return to a previous stage.

### Configuration <a name="configuration"></a>

The project includes a configuration file called `CONFIG.py` with key-value pairs for various settings:

```python
gis = {
    "api_key": "",  # Google Image Search API key
    "project_id": "",  # Google Cloud Project ID
}

gcp = {
    "conn": "",  # Google Cloud connection string
    "user": "",
    "password": "",
    "driver": "",
    "db": "",
    "bucket": "",  # Google Cloud Storage bucket name
    "iam_command": "",  # Google Cloud IAM command
}

telegram = {
    "token": "",  # Telegram API token
    "download_link": "",  # Bot's download link for uploaded content
}
```

You need to fill in these values with your own API keys, project IDs, and other necessary information.

## 4. Usage <a name="usage"></a>

### Running Locally <a name="running-locally"></a>

To run StickerRefacerBot locally, follow these steps:

1. Ensure you have filled in the required values in `CONFIG.py`.

2. Run the bot using the following command:

   ```bash
   SSB_BOT.py
   ```

3. Start a chat with your bot on Telegram and follow the prompts to upload an image, detect faces, match stickers, modify them, and finalize the image.

### Deployment on Google Cloud Compute Engine <a name="deployment-on-google-cloud-compute-engine"></a>

To deploy StickerRefacerBot on a Google Cloud Compute Engine instance, you can follow these general steps:

1. Set up a Compute Engine instance with the necessary configurations.

2. Clone the StickerRefacerBot repository onto the instance.

3. Install the required dependencies as specified in the "Installation" section.

4. Configure the `CONFIG.py` file with the appropriate values for the Compute Engine environment.

5. Run the bot on the Compute Engine instance.

6. Set up any necessary firewall rules to allow communication with the bot.

7. Start a chat with the bot on Telegram and use it as described in the "Running Locally" section.

## 5. Contributing <a name="contributing"></a>

Contributions to StickerRefacerBot are welcome! Feel free to fork the repository, make improvements, and submit pull requests. Be sure to follow the project's coding and documentation guidelines.

---

Thank you for using StickerRefacerBot! If you have any questions or encounter any issues, please refer to the GitHub repository's issue tracker or reach out to the project maintainers. Enjoy using the bot for image manipulation and sticker creation!
