import streamlit as st
import pickle
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
import sklearn
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import random
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import sklearn.model_selection as model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import RandomOverSampler

#应用标题
st.title('Application of Machine Learning Methods to Predict Bone Metastases in Breast Infiltrating Ductal Carcinoma Patients')



# conf
st.sidebar.markdown('## Variables')
Age = st.sidebar.selectbox('Age',('<55','>=55'),index=0)
Sex = st.sidebar.selectbox('Sex',('Female','Male'),index=0)
Race = st.sidebar.selectbox("Race",('American Indian/Alaska Native','Asian or Pacific Islander','Black','White'),index=3)
Grade = st.sidebar.selectbox("Grade",('Ⅰ','Ⅱ','Ⅲ','Ⅳ'),index=0)
Breast_subtype = st.sidebar.selectbox("Breast subtype",('HR-/HER2- (Triple Negative)','HR-/HER2+ (HER2 enriched)'
                                                        ,'HR+/HER2- (Luminal A)','HR+/HER2+ (Luminal B)'),index=0)
T_stage = st.sidebar.selectbox("T stage",('T1','T2','T3','T4'))
N_stage = st.sidebar.selectbox("N stage",('N0','N1','N2','N3'))
Marital_status = st.sidebar.selectbox("Marital status",('Married','Unmarried'))

# str_to_int

map = {'<55':1,'>=55':2,'Female':1,'Male':2,'American Indian/Alaska Native':1,'Asian or Pacific Islander':2,'Black':3,
       'White':4,'Ⅰ':1,'Ⅱ':2,'Ⅲ':3,'Ⅳ':4,'T1':1,'T2':2,'T3':3,'T4':4,
       'N0':0,'N1':1,'N2':2,'N3':3,
       'HR-/HER2- (Triple Negative)':1,'HR-/HER2+ (HER2 enriched)':2,
       'HR+/HER2- (Luminal A)':3,'HR+/HER2+ (Luminal B)':4,
       'Married':1,'Unmarried':2}
Age =map[Age]
Race =map[Race]
Sex =map[Sex]
Grade =map[Grade]
Breast_subtype =map[Breast_subtype]
T_stage =map[T_stage]
N_stage =map[N_stage]
Marital_status =map[Marital_status]

# 数据读取，特征标注
thyroid_train = pd.read_csv('train.csv', low_memory=False)
thyroid_train['BM'] = thyroid_train['BM'].apply(lambda x : +1 if x==1 else 0)
thyroid_test = pd.read_csv('test.csv', low_memory=False)
thyroid_test['BM'] = thyroid_test['BM'].apply(lambda x : +1 if x==1 else 0)
features = ['T_stage','N_stage','Age','Race','Sex','Grade','Breast_subtype','Marital_status']
target = 'BM'

#处理数据不平衡
ros = RandomOverSampler(random_state=12, sampling_strategy='auto')
X_ros, y_ros = ros.fit_resample(thyroid_train[features], thyroid_train[target])

#train and predict
#RF = sklearn.ensemble.RandomForestClassifier(n_estimators=7,criterion='entropy',max_features='log2',max_depth=5,random_state=12)
#RF.fit(thyroid_train[features],thyroid_train[target])
XGB = XGBClassifier(random_state=32,max_depth=3,n_estimators=36)
XGB.fit(X_ros, y_ros)
#读之前存储的模型

#with open('RF.pickle', 'rb') as f:
#    RF = pickle.load(f)


sp = 0.5
#figure
is_t = (XGB.predict_proba(np.array([[Age,Race,Sex,Grade,T_stage,N_stage,Breast_subtype,Marital_status]]))[0][1])> sp
prob = (XGB.predict_proba(np.array([[Age,Race,Sex,Grade,T_stage,N_stage,Breast_subtype,Marital_status]]))[0][1])*1000//1/10

#st.write('is_t:',is_t,'prob is ',prob)
#st.markdown('## is_t:'+' '+str(is_t)+' prob is:'+' '+str(prob))

if is_t:
    result = 'High Risk'
else:
    result = 'Low Risk'
if st.button('Predict'):
    st.markdown('## Risk grouping for bone metastases:  '+str(result))
    if result == 'Low Risk':
        st.balloons()
    st.markdown('## Probability of BM:  '+str(prob)+'%')
#st.markdown('## The risk of bone metastases is '+str(prob/0.0078*1000//1/1000)+' times higher than the average risk .')

#排版占行



st.title("")
st.title("")
st.title("")
st.title("")
#st.warning('This is a warning')
#st.error('This is an error')

#st.info('Information of the model: Auc: 0.882 ;Accuracy: 0.802 ;Sensitivity(recall): 0.811 ;Specificity :0.801 ')
#st.success('Affiliation: The First Affiliated Hospital of Nanchang University, Nanchnag university. ')





