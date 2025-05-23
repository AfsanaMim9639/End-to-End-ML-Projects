import sys
import os
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor,)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression



##Import All the Files
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts",'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Spliting Training and Test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models={
                "Random Forest Regressor":RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
}
            

            params={
                "Decision Tree":{'criterion':['squared_error','friedman_mse','absolute_error','poisson']},
                "Random Forest Regressor":{'n_estimators':[8,16,32,64,128,256]},
                "Gradient Boosting":{'learning_rate':[.1,.01,.05,.001],
                                     'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                                     'n_estimators':[8,16,32,64,128,256]
                                     },
                "Linear Regression":{},
                "K-Neighbors Regressor":{'n_neighbors':[5,7,9,11]},
                "XGBRegressor":{'learning_rate':[.1,.01,.05,.001],
                                'n_estimators':[8,16,32,64,128,256]
                                },
                "CatBoosting Regressor":{'depth':[6,8,10],
                                         'learning_rate':[.1,.01,.05,.001],
                                         'iterations':[30,50,100]
                                         },
                "AdaBoost Regressor":{'learning_rate':[.1,.01,.05,.001],
                                      'n_estimators':[8,16,32,64,128,256]
                                      }
}

            
            





            model_report:dict=evaluate_model(x_train=X_train,y_train=y_train,x_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
            ## To get best model score from dict
            best_model_score=max(sorted(model_report.values()))

            ## To get best model name from dict
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]

            if best_model_score  < 0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing datsets")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            prediced=best_model.predict(X_test)
            r2_square=r2_score(y_test,prediced)
            return r2_square
            
        except Exception as e:

            raise CustomException(e,sys)