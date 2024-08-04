import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
import pickle as pickle

def create_model(data):
    X = data.drop(['diagnosis'],axis=1)
    Y = data['diagnosis']
    
    scalar=StandardScaler()
    X = scalar.fit_transform(X)
    X_train,X_test,Y_train,Y_test = train_test_split(
        X,Y,test_size=0.2,random_state=42
    )
    
    model =LogisticRegression()
    model.fit(X_train,Y_train)
    
    y_pred=model.predict(X_test)
    print("Accuracy of our model :",accuracy_score(Y_test,y_pred))
    print("Classification report :\n",classification_report(Y_test,y_pred))
    
    return model,scalar

    
def get_clean_data():
    data = pd.read_csv("D:\\python\\Cancer Project\\data\\Cancer_Data.csv")
    
    data=data.drop(['Unnamed: 32','id'],axis=1)
    data['diagnosis']=data['diagnosis'].map({'M':1,'B':0})
    return data
    
def main():
    data =get_clean_data()
    
    
    model,scalar=create_model(data)
    
    with open('model/model.pkl','wb') as f:
        pickle.dump(model,f)
    with open('model/scaler.pkl','wb') as f:
        pickle.dump(scalar,f)
        
    
    
if __name__ =='__main__':
    main()
    