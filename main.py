# main.py - Entry point
# from src.data_ingestion import fetch_and_save_data
from src.data_preparation import prepare_dataset
from src.model_training import train_and_save_model

if __name__ == "__main__":
    # fetch_and_save_data()
    prepare_dataset()
    train_and_save_model()
