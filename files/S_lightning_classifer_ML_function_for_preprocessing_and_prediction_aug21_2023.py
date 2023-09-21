from gensim.parsing.preprocessing import preprocess_documents
from gensim.parsing.porter import PorterStemmer
from lightning.classification import CDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

import copy
import numpy as np
import os
import sklearn
import sys
import time

import mlflow
import mlflow.sklearn

#print('sklearn  version' , sklearn.__version__)
#print('python version is ', sys.version)
#print('path to python exe ' ,  sys.executable)

model_name = "model"
model_path = "trained_model"

# Start Logging
mlflow.start_run()

# enable autologging
mlflow.sklearn.autolog()

y_test_text_file  = open("y_test.txt", "r")
y_train_text_file = open("y_train.txt", "r")
X_test_text_file  = open("X_test.txt",  "r", encoding='latin-1')
X_train_text_file = open("X_train.txt", "r", encoding='latin-1')

X_test = X_test_text_file.readlines()    
X_train = X_train_text_file.readlines()

y_test = y_test_text_file.readlines()
y_test = [int(x) for x in y_test]
y_test = np.array( y_test )

y_train = y_train_text_file.readlines()
y_train = [int(x) for x in y_train]
y_train = np.array( y_train )

q = 0

def preprocessing_function(X_train, data_to_vectorize ):
    vectorizer = TfidfVectorizer( sublinear_tf=True, max_df=0.5, min_df=5, stop_words="english")    

    my_PorterStemmer = PorterStemmer()
    X_train =  my_PorterStemmer.stem_documents( X_train )
    X_train =  preprocess_documents(X_train)
    X_train = [" ".join(x) for x in X_train]
    vectorizer.fit(X_train)
    data_to_vectorize =  my_PorterStemmer.stem_documents( data_to_vectorize )
    data_to_vectorize =  preprocess_documents(data_to_vectorize)
    data_to_vectorize = [" ".join(x) for x in data_to_vectorize]  
    X_train_vectorised = vectorizer.transform(data_to_vectorize)

    return X_train_vectorised

def my_inference(my_text):
    test_vectorised =  preprocessing_function(X_train, [my_text])
    pred_test_lightning = clf_lightning.predict( test_vectorised   )
    print('for text => ', my_text )
    print('pred_test_lightning', pred_test_lightning[0])
    return pred_test_lightning

X_train_vectorised =  preprocessing_function(X_train, X_train )
test_data_vectorised =  preprocessing_function(X_train, X_test )

clf_lightning = CDClassifier(loss="squared_hinge",
                    penalty="l1",           
                    multiclass=False,
                    max_iter=20,
                    alpha=1e-4,
                    C=1.0 / X_train_vectorised.shape[0],
                    tol=1e-3,
                    n_jobs =5)

clf_lightning.fit(X_train_vectorised, y_train )
pred_train_lightning = [int(x) for x in clf_lightning.predict(X_train_vectorised)]   
original_targt_lightning = [int(x) for x in y_train]  
print('\n****                 train data lightning confusion_matrix     **************')
print(confusion_matrix( original_targt_lightning , pred_train_lightning)  )

pred_test_data_lightning      = [int(x) for x in clf_lightning.predict(test_data_vectorised)]   
original_test_targt_lightning = [int(x) for x in y_test]  
print('\n****                 test data lightning confusion_matrix     **************')
print(confusion_matrix( original_test_targt_lightning , pred_test_data_lightning)  )

my_text =  X_test[0]

my_inference = my_inference(my_text) 

mlflow.sklearn.log_model(sk_model=clf_lightning,  registered_model_name=model_name , artifact_path=model_path)
mlflow.sklearn.save_model(sk_model=clf_lightning, path=os.path.join(model_path))
mlflow.end_run()