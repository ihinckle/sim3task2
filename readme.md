
---

## 4. Running the Project

### Phase A: Model Training (Optional)
If the `model/ai-text-detector-model.pkl` file is not present, or if you wish to retrain the model:
1.  Open the `ai-text-detector.ipynb` file in a Jupyter environment.
2.  Run all cells sequentially.
3.  The notebook will unzip the data, clean it, evaluate accuracy, and export the trained model to the `/model` folder.

### Phase B: Launching the Web Application
To start the interactive data product:
1.  Ensure your virtual environment is active.
2.  Execute the following command in the root directory:
    ```bash
    python app.py
    ```
3.  The application will initialize the database and start a local development server at `http://127.0.0.1:5000`.

---

## 5. Using the Product

### Testing with Example Manuscripts
To facilitate immediate testing, **two example manuscripts** are included in the `/model` folder:
*   **Example 1:** Use this to verify the detection of human-authored linguistic patterns.
*   **Example 2:** Use this to verify the detection of machine-generated content.

### Uploading a Manuscript
1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Use the **Upload** tool to select an EPUB file (you may use the files from the `/model` folder).
3.  Click **Predict**.
4.  The system will display the result:
    *   **AI Detected:** High probability of being machine-generated.
    *   **Human Authored:** Linguistic patterns consistent with human writing.

### Monitoring and Auditing
*   **Logs:** Navigate to the `/monitor` tab to view processing exceptions.
*   **Database:** IT professionals can audit raw prediction records using the following SQL command in a database console:
    ```sql
    SELECT * FROM sos_prediction;
    ```

---

## 6. Troubleshooting
*   **Missing Model:** Ensure `ai-text-detector-model.pkl` exists in the `model/` directory.
*   **Corrupt EPUBs:** If a file fails to parse, check the `/monitor` page for detailed error logs.
*   **Port Conflicts:** If port 5000 is occupied, modify the `app.run()` line in `app.py`.