import sqlite3
from datasets import Dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer, TrainingArguments, Trainer

# Function to load data from the database
def load_data_from_db(db_name, table_name):
    """
    Load data from the SQLite database.
    
    Parameters:
        db_name (str): Name of the SQLite database file.
        table_name (str): Name of the table to load data from.
    
    Returns:
        list: A list of (input_text, target_text) pairs.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Fetch data from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    # Convert rows to (input_text, target_text) pairs
    data = []
    for row in rows:
        # Assuming the first column is the natural language query and the second is the SQL query
        input_text = row[0]  # Natural language query
        target_text = row[1]  # SQL query
        data.append((input_text, target_text))
    
    conn.close()
    return data

# Tokenize the dataset
def preprocess_function(examples):
    """
    Tokenize the input and target texts.
    """
    inputs = [f"translate English to SQL: {text}" for text in examples["input_text"]]
    targets = examples["target_text"]
    
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    labels = tokenizer(targets, max_length=512, truncation=True)
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Main function to fine-tune the model
def fine_tune_model():
    # Load train data from the database
    train_data = load_data_from_db("banking.db", "transactions")  # Replace "train" with your table name

    # Convert train data to Hugging Face Dataset format
    train_dataset = Dataset.from_dict({
        "input_text": [item[0] for item in train_data],
        "target_text": [item[1] for item in train_data]
    })

    # Load the tokenizer
    tokenizer = T5Tokenizer.from_pretrained("tscholak/cxmefzzi")

    # Tokenize the dataset
    train_dataset = train_dataset.map(preprocess_function, batched=True)

    # Load the model
    model = T5ForConditionalGeneration.from_pretrained("tscholak/cxmefzzi")

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./fine-tuned-model",  # Directory to save the fine-tuned model
        evaluation_strategy="epoch",     # Evaluate after each epoch
        learning_rate=5e-5,              # Learning rate
        per_device_train_batch_size=8,   # Batch size for training
        per_device_eval_batch_size=8,    # Batch size for evaluation
        num_train_epochs=3,              # Number of training epochs
        save_steps=10_000,               # Save checkpoint every 10,000 steps
        save_total_limit=2,              # Keep only the last 2 checkpoints
        logging_dir="./logs",            # Directory for logs
        logging_steps=500,               # Log every 500 steps
        load_best_model_at_end=True,     # Load the best model at the end of training
    )

    # Define the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
    )

    # Fine-tune the model
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("./fine-tuned-model")
    tokenizer.save_pretrained("./fine-tuned-model")
    print("Fine-tuning complete! Model saved to './fine-tuned-model'.")

if __name__ == "__main__":
    fine_tune_model()