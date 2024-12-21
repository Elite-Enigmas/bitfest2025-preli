# Challenge 1 Solution

Run the code on kaggle

# **1. Data Preparation**
- **Task**: Load and preprocess the dataset.
- **Process**:
  1. **Dataset Loading**: The dataset is loaded from Hugging Face (`SKNahin/bengali-transliteration-data`) using the `load_dataset` function.
  2. **Splitting**: The dataset is split into training and testing subsets with an 80:20 ratio to ensure the model generalizes well.


  - **Justification**:
    - The 80:20 split ensures sufficient data for both training and evaluation.
    - Hugging Face's `datasets` library simplifies data handling and supports preprocessing pipelines.

---



# **2. Data Preprocessing**
- **Task**: Tokenize and clean the data.
- **Process**:
  1. **Removing Null or Corrupted Entries**: Null or empty rows are filtered out to avoid errors during training.
  2. **Tokenization**: Both Banglish (input) and Bengali (output) text are tokenized using the UMT5-Base tokenizer.

  

  - **Justification**:
    - The UMT5 tokenizer perfect with the pretrained UMT5-Base model, ensuring consistent input-output transformations.
    .

---


# **3. Model Selection**
- **Task**: Choose a suitable model for transliteration.
- **Choice**: `google/umt5-base`
- **Justification**:
  - **Performance**:
    - UMT5 is a multilingual model designed for sequence-to-sequence tasks like translation and transliteration.
    - It has shown robust performance on low-resource languages.
  - **Suitability**:
    - UMT5 supports Bengali and Roman script, making it ideal for Banglish-to-Bengali transliteration.
  - **Efficiency**:
    - The model is lightweight compared to larger models like mT5-Large or mBART, making it suitable for faster training and inference without sacrificing accuracy.

---


# **4. Training the Model**
- **Task**: Fine-tune the UMT5-Base model on the processed dataset.
- **Setup**:
  1. Define training arguments.
  2. Use `Seq2SeqTrainer` for fine-tuning.
  3. Monitor metrics such as WER (Word Error Rate) during evaluation.


  - **Hyperparameter Justification**:
    - **Batch Sizes**: Small batch sizes (4 for training, 8 for evaluation) are chosen to handle memory constraints.
    - **Learning Rate**: `5e-4` is used for stable convergence.
    - **Epochs**: `15` epochs allow the model sufficient time to learn patterns.
    - **Weight Decay**: `1e-2` helps prevent overfitting.
    - **Metric**: WER is chosen as the primary evaluation metric for transliteration tasks.

---

