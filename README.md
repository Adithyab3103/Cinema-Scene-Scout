# 🦇 Cinema Scene Scout: The Batman Edition

This project allows you to find specific scenes in the movie "The Batman (2022)" by describing them in natural language. It uses a Retrieval-Augmented Generation (RAG) pipeline to search through the movie's subtitles.

### Project Files

-   `ingest.py`: Script to process the subtitle file. **Run this first.**
-   `app.py`: The main web application. **Run this second.**
-   `TheBatman2022.srt`: Your subtitle file for the movie.
-   `requirements.txt`: A list of all required Python packages.
-   `.env`: A file you will create to store your API key.

---

## 🚀 How to Run This Project

Follow these steps exactly to get the application working.

### Step 1: Set Up Your Environment

1.  **Activate Conda:** Open your terminal and activate the conda environment you prepared (e.g., `scene-scout`).
    ```bash
    conda activate scene-scout
    ```

2.  **Install Dependencies:** Make sure you are in the project directory and run the following command to install all necessary packages from the requirements file.
    ```bash
    pip install -r requirements.txt
    ```

### Step 2: Add Your API Key

1.  **Create a `.env` file:** In the same project folder, create a new file and name it exactly `.env`.

2.  **Add your key:** Open the `.env` file and add your OpenAI API key like this. Replace `your-key-goes-here` with your actual secret key.
    ```
    GOOGLE_API_KEY="your-key-goes-here"
    ```
    Save and close the file. The Python scripts will automatically load this key.

### Step 3: Process the Subtitle File (Ingestion)

1.  **Run the Ingestion Script:** In your terminal, run the `ingest.py` script. This will read your `TheBatman2022.srt` file, create the embeddings, and build the local database in a new `db` folder.
    ```bash
    python ingest.py
    ```
    > **Note:** You only need to do this step **once**. If you ever change or update your SRT file, you will need to delete the `db` folder and run this script again.

### Step 4: Launch the Web App

1.  **Run Streamlit:** After the ingestion is complete, launch the web application.
    ```bash
    streamlit run app.py
    ```

2.  **Open in Browser:** Your web browser should automatically open with the application running. You can now start searching for scenes!