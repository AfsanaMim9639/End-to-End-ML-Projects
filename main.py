import os
import sys

# ✅ Add root folder to sys.path so `src` is accessible
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# ✅ Imports from src
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    try:
        # Step 1: Data ingestion
        ingestion = DataIngestion()
        train_data, test_data = ingestion.initiate_data_ingestion()

        # Step 2: Data transformation
        transformation = DataTransformation()
        train_arr, test_arr, _ = transformation.initiate_data_transformation(
            train_data, test_data
        )

        # Step 3: Model training
        trainer = ModelTrainer()
        print(trainer.initiate_model_trainer(train_arr, test_arr))

    except Exception as e:
        print("❌ Error:", e)
