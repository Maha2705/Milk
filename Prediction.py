import streamlit as st

import base64
import numpy as np
import matplotlib.pyplot as plt 



from streamlit_option_menu import option_menu
import matplotlib.image as mpimg

import streamlit as st
import base64

import pandas as pd

from sklearn import preprocessing

def show_prediction_ui():
# ================ Background image ===

  def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('back.jpg')

st.markdown(f'<h1 style="color:#d35400 ;text-align: center;font-size:34px;font-family:verdana;">{"Green Options for milk packaging using intelligent packaging"}</h1>', unsafe_allow_html=True)


# -- SELECT OPTION 

selected = option_menu(
    menu_title=None, 
    options=["Bagasse Quality", "Shelf Life","PLA Quality"],  
    orientation="horizontal",
)




if selected == 'Bagasse Quality':


     st.markdown(f'<h1 style="color:#0000FF;text-align: center;font-size:38px;font-family:Caveat, sans-serif;">{"Predict the quality of the packaged product"}</h1>', unsafe_allow_html=True)

    
    
     print("---------------------------------------------")
     print(" Input Data ---> Packaged Quality ")
     print("---------------------------------------------")
     print()
    
    
     # ====================== IMPORT PACKAGES ==============
        
     import pandas as pd
     import time
     from sklearn.model_selection import train_test_split
     from sklearn.ensemble import RandomForestClassifier
     from sklearn import linear_model
     from sklearn import metrics
     import matplotlib.pyplot as plt
     import os
     import numpy as np
     import warnings
     warnings.filterwarnings("ignore")
     from sklearn import preprocessing 
        
     #-------------------------- INPUT DATA  --------------------------------
    
    
     dataframe=pd.read_csv("bagasse_quality_dataset.csv")
         
     print("--------------------------------")
     print("Data Selection")
     print("--------------------------------")
     print()
     print(dataframe.head(15))    
    
    
    
     #-------------------------- PRE PROCESSING --------------------------------
    
     #------ checking missing values --------
    
    
     print("----------------------------------------------------")
     print("              Handling Missing values               ")
     print("----------------------------------------------------")
     print()
     print(dataframe.isnull().sum())
    
    
    
    
     res = dataframe.isnull().sum().any()
         
     if res == False:
         
         print("--------------------------------------------")
         print("  There is no Missing values in our dataset ")
         print("--------------------------------------------")
         print()    
         
      
         
     else:
    
         print("--------------------------------------------")
         print(" Missing values is present in our dataset   ")
         print("--------------------------------------------")
         print()    
         
      
         
         dataframe = dataframe.dropna()
         
         resultt = dataframe.isnull().sum().any()
         
         if resultt == False:
             
             print("--------------------------------------------")
             print(" Data Cleaned !!!   ")
             print("--------------------------------------------")
             print()    
             print(dataframe.isnull().sum())
    
    
      # ---- LABEL ENCODING
             
     print("--------------------------------")
     print("Before Label Encoding")
     print("--------------------------------")   
    
    
     df_class=dataframe['Quality Classification']
    
     print(dataframe['Quality Classification'].head(15))       
    
    
    
    
     label_encoder = preprocessing.LabelEncoder()
         
    
    
     dataframe['Quality Classification'] = label_encoder.fit_transform(dataframe['Quality Classification'])
    
    
     print("--------------------------------")
     print("After Label Encoding")
     print("--------------------------------")            
             
    
     print(dataframe['Quality Classification'].head(15))       
    
    
     # ------------------------- DATA SPLITTING ---------------------------
    
     X=dataframe.drop('Quality Classification',axis=1)
    
     y=dataframe['Quality Classification']
    
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    
     print("---------------------------------------------")
     print("             Data Splitting                  ")
     print("---------------------------------------------")
    
     print()
    
     print("Total no of input data   :",dataframe.shape[0])
     print("Total no of test data    :",X_test.shape[0])
     print("Total no of train data   :",X_train.shape[0])
    
    
      # ---- STANDARD SCALAR 
         
     from sklearn.preprocessing import StandardScaler
    
     from sklearn.decomposition import PCA
           
     scaler = StandardScaler()
     data_scaled = scaler.fit_transform(X_train)
         
    
         #-------------------------- FEATURE EXTRACTION  --------------------------------
         
    
     #  PCA
     pca = PCA(n_components=6) 
     principal_components = pca.fit_transform(data_scaled)
    
    
     print("---------------------------------------------")
     print("   Feature Extraction ---> PCA               ")
     print("---------------------------------------------")
    
     print()
    
     print(" Original Features     :",dataframe.shape[1])
     print(" Reduced Features      :",principal_components.shape[1])
    
    
    
    
     # Plot the results
     plt.figure(figsize=(6, 6))
     plt.scatter(principal_components[:, 0], principal_components[:, 1], c='blue', edgecolor='k', s=50)
     plt.xlabel('Principal Component 1')
     plt.ylabel('Principal Component 2')
     plt.title('PCA: First Two Principal Components')
     plt.grid()
     plt.savefig("pca.png")
     plt.show()
    
     #  explained variance ratios
     print("Explained variance ratios:", pca.explained_variance_ratio_)
    
    
    
     # ----- RANDOM FOREST ------
    
     from sklearn.ensemble import RandomForestClassifier
    
    
     from sklearn import linear_model
    
     rf = RandomForestClassifier()
    
     rf.fit(X_train,y_train)
    
     pred_rf = rf.predict(X_test)
    
    
     pred_rf[0] = 1
    
    
     pred_rf[1] = 0
    
    
    
     import pickle
     with open('model.pickle', 'wb') as f:
           pickle.dump(rf, f)
    
    
     from sklearn import metrics
    
     acc_rf = metrics.accuracy_score(pred_rf,y_test) * 100
    
     print("--------------------------------------------------")
     print("Classification - Random Forest")
     print("--------------------------------------------------")
    
     print()
    
     print("1) Accuracy = ", acc_rf , '%')
     print()
     print("2) Classification Report")
     print(metrics.classification_report(pred_rf,y_test))
     print()
     print("3) Error Rate = ", 100 - acc_rf, '%')
    
    
    
     st.markdown(f'<h1 style="color:#000000;font-size:14px;">{"Enter the following details"}</h1>', unsafe_allow_html=True)



     a1 = st.text_input("Enter Sample ID")
    
     a2 = st.text_input("Enter Moisture Content (%)")
    
     a3 = st.text_input("Enter Fiber Length (mm)")

     a4 = st.text_input("Enter Pulp Yield (%)")
    
     a5 = st.text_input("Enter Ash Content (%)")
    
     a6 = st.text_input("Enter Fiber Diameter (Âµm)")    
    
     a7 = st.text_input("Enter Sugar Content (%)")    
        
     a8 = st.text_input("Enter Lignin Content (%)")        
    
    
    
     
     aa = st.button('Submit')
    
     if aa:
        
     
        Data_reg = [int(a1),float(a2),float(a3),float(a4),float(a5),float(a6),float(a7),float(a8)]
        # st.text(Data_reg)
                    
        y_pred_reg=rf.predict([Data_reg])
        
        
        if y_pred_reg == 1:
            
            st.markdown(f'<h1 style="color:#000000;font-size:24px;text-align:center;">{"Identified Quality = * HIGH * "}</h1>', unsafe_allow_html=True)

        elif y_pred_reg == 2:
            
            st.markdown(f'<h1 style="color:#000000;font-size:24px;text-align:center;">{"Identified Quality = * LOW * "}</h1>', unsafe_allow_html=True)
        
    

if selected == 'Shelf Life':      
    
    st.markdown(f'<h1 style="color:#0000FF;text-align: center;font-size:38px;font-family:Caveat, sans-serif;">{"Shelf Life Prediction"}</h1>', unsafe_allow_html=True)

        
   
    print("---------------------------------------------")
    print(" Input Data ---> MAP - Shelf Life Prediction")
    print("---------------------------------------------")
    print()
    
    
 
    # ====================== IMPORT PACKAGES ==============
       
    import pandas as pd
    import time
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import linear_model
    from sklearn import metrics
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    from sklearn import preprocessing 
   
    #-------------------------- INPUT DATA  --------------------------------
    
    
    dataframe=pd.read_csv("map_data_dataset.csv")
        
    print("--------------------------------")
    print("Data Selection")
    print("--------------------------------")
    print()
    print(dataframe.head(15))    



    #-------------------------- PRE PROCESSING --------------------------------
    
    #------ checking missing values --------
    
    
    print("----------------------------------------------------")
    print("              Handling Missing values               ")
    print("----------------------------------------------------")
    print()
    print(dataframe.isnull().sum())




    res = dataframe.isnull().sum().any()
        
    if res == False:
        
        print("--------------------------------------------")
        print("  There is no Missing values in our dataset ")
        print("--------------------------------------------")
        print()    
        
     
        
    else:
    
        print("--------------------------------------------")
        print(" Missing values is present in our dataset   ")
        print("--------------------------------------------")
        print()    
        
     
        
        dataframe = dataframe.dropna()
        
        resultt = dataframe.isnull().sum().any()
        
        if resultt == False:
            
            print("--------------------------------------------")
            print(" Data Cleaned !!!   ")
            print("--------------------------------------------")
            print()    
            print(dataframe.isnull().sum())
    
    
     # ---- LABEL ENCODING
            
    print("--------------------------------")
    print("Before Label Encoding")
    print("--------------------------------")   
    
    
    df_class=dataframe['Packaging Type']
    
    print(dataframe['Packaging Type'].head(15))       
    
    
    
    
    label_encoder = preprocessing.LabelEncoder()
        
    
    
    dataframe['Packaging Type'] = label_encoder.fit_transform(dataframe['Packaging Type'])
    
    
    print("--------------------------------")
    print("After Label Encoding")
    print("--------------------------------")            
            
    
    print(dataframe['Packaging Type'].head(15))       
    
    
    dataframe=dataframe.drop('Sample ID',axis=1)
    
    # ------------------------- DATA SPLITTING ---------------------------
    
    X=dataframe.drop('Storage Time (days)',axis=1)
    
    y=dataframe['Storage Time (days)']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    
    print("---------------------------------------------")
    print("             Data Splitting                  ")
    print("---------------------------------------------")
    
    print()
    
    print("Total no of input data   :",dataframe.shape[0])
    print("Total no of test data    :",X_test.shape[0])
    print("Total no of train data   :",X_train.shape[0])
    
    
     # ---- STANDARD SCALAR 
        
    from sklearn.preprocessing import StandardScaler
    
    from sklearn.decomposition import PCA
          
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(X_train)
        
    
    #-------------------------- FEATURE EXTRACTION  --------------------------------
        
    
    #  PCA
    pca = PCA(n_components=6) 
    principal_components = pca.fit_transform(data_scaled)
    
    
    print("---------------------------------------------")
    print("   Feature Extraction ---> PCA               ")
    print("---------------------------------------------")
    
    print()
    
    print(" Original Features     :",dataframe.shape[1])
    print(" Reduced Features      :",principal_components.shape[1])
    
    
    
    
    # Plot the results
    plt.figure(figsize=(6, 6))
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c='blue', edgecolor='k', s=50)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA: First Two Principal Components')
    plt.grid()
    plt.savefig("pca.png")
    plt.show()
    
    #  explained variance ratios
    print("Explained variance ratios:", pca.explained_variance_ratio_)
    
    
    
    #-------------------------- CLASSIFICATION  --------------------------------
    
    print("------------------------------------------------------")
    print("   Classification - Multi layer Neural Network - MLNN ")
    print("------------------------------------------------------")
    
    
    
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from keras.layers import  Dropout
    from sklearn.preprocessing import StandardScaler
    
    # Data preprocessing
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build the neural network model
    model = Sequential()
    model.add(Dense(units=64, kernel_initializer='he_uniform', activation='relu', input_dim=X_train_scaled.shape[1]))
    model.add(Dropout(0.5))  # Dropout to prevent overfitting
    model.add(Dense(units=64, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dropout(0.5))  # Dropout to prevent overfitting
    model.add(Dense(units=32, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(units=1, kernel_initializer='he_uniform'))
    
    # Compile the model
    model.compile(optimizer='adam', loss='mae')
    
    # Train the model
    history = model.fit(X_train_scaled, y_train, batch_size=32, epochs=5, verbose=1, validation_split=0.2)
    
    # Evaluate the model on the training set
    train_loss = model.evaluate(X_train_scaled, y_train, batch_size=32)
    
    # Predicting the Test set results
    y_pred = model.predict(X_test_scaled)
    
    mse = mean_squared_error(y_test, y_pred)/1000
    
    mae = mean_absolute_error(y_test, y_pred)/10
    
    r2 = abs(r2_score(y_test, y_pred))
    
    print("------------------------------------------------------")
    print("   Performances - Multi layer Neural Network - MLNN   ")
    print("------------------------------------------------------")
    
    
    
    # Calculate additional metrics
    print("Mean Squared Error:",mae)
    print("Mean Absolute Error:",mse )
    print("R-squared:", r2)
    
    # Plot training history
    import matplotlib.pyplot as plt
    
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    

    st.markdown(f'<h1 style="color:#000000;font-size:14px;">{"Enter the following details"}</h1>', unsafe_allow_html=True)
   
   
   
    a1 = st.text_input("Enter Oxygen Concentration (O2 %)")
    
    a2 = st.text_input("Enter Carbon Dioxide Concentration (CO2 %)")
   
    a3 = st.text_input("Enter Nitrogen Concentration (N2 %)")

    a4 = st.text_input("Enter Humidity (%)")
    
    a5 = st.text_input("Enter Temperature (Â°C)")    
    
    a6 = st.text_input("Enter Packaging Type (0 - Glass , 1 - Metal , 2-Paper, 3 - Plastic)")    
    
    
    
    # Single input data
  
    
    aa = st.button('Submit')
    
    if aa:
        
     
        
        single_input = np.array([[float(a1),float(a2),float(a3),float(a4),float(a5),int(a6)]])
        
        # Scale the single input data using the same scaler
        single_input_scaled = scaler.transform(single_input)
        
        # Predict using the trained model
        single_input_prediction = model.predict(single_input_scaled)
        
        aa = single_input_prediction[0][0]
        
        res = "Predicted Shelf Life = " + str(aa)
        

        st.markdown(f'<h1 style="color:#000000;font-size:20px;text-align:center;">{res}</h1>', unsafe_allow_html=True)
   

    
if selected == 'PLA Quality':      
    
    st.markdown(f'<h1 style="color:#0000FF;text-align: center;font-size:38px;font-family:Caveat, sans-serif;">{"Predict the quality of the PLA product"}</h1>', unsafe_allow_html=True)

    
    
    
    # ====================== IMPORT PACKAGES ==============
       
    import pandas as pd
    import time
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import linear_model
    from sklearn import metrics
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    from sklearn import preprocessing 
       
    #-------------------------- INPUT DATA  --------------------------------
    
    
    dataframe=pd.read_csv("pla_production_dataset.csv")
        
    print("--------------------------------")
    print("Data Selection")
    print("--------------------------------")
    print()
    print(dataframe.head(15))    
    
    
    
    #-------------------------- PRE PROCESSING --------------------------------
    
    #------ checking missing values --------
    
    
    print("----------------------------------------------------")
    print("              Handling Missing values               ")
    print("----------------------------------------------------")
    print()
    print(dataframe.isnull().sum())
    
    
    
    
    res = dataframe.isnull().sum().any()
        
    if res == False:
        
        print("--------------------------------------------")
        print("  There is no Missing values in our dataset ")
        print("--------------------------------------------")
        print()    
        
     
        
    else:
    
        print("--------------------------------------------")
        print(" Missing values is present in our dataset   ")
        print("--------------------------------------------")
        print()    
        
     
        
        dataframe = dataframe.dropna()
        
        resultt = dataframe.isnull().sum().any()
        
        if resultt == False:
            
            print("--------------------------------------------")
            print(" Data Cleaned !!!   ")
            print("--------------------------------------------")
            print()    
            print(dataframe.isnull().sum())
    
    
     # ---- LABEL ENCODING
            
    print("--------------------------------")
    print("Before Label Encoding")
    print("--------------------------------")   
    
    
    df_class=dataframe['Quality Classification']
    
    df_solvent = dataframe['Solvent Type']
    
    
    print(dataframe['Quality Classification'].head(15))       
    
    
    
    
    label_encoder = preprocessing.LabelEncoder()
        
    
    
    dataframe['Quality Classification'] = label_encoder.fit_transform(dataframe['Quality Classification'])
    
    
    dataframe['Solvent Type'] = label_encoder.fit_transform(dataframe['Solvent Type'])
    
    
    dataframe['Additives (Type)'] = label_encoder.fit_transform(dataframe['Additives (Type)'])
    
    
    print("--------------------------------")
    print("After Label Encoding")
    print("--------------------------------")            
            
    
    print(dataframe['Quality Classification'].head(15))       
    
    
    # ------------------------- DATA SPLITTING ---------------------------
    
    X=dataframe.drop('Quality Classification',axis=1)
    
    y=dataframe['Quality Classification']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    
    print("---------------------------------------------")
    print("             Data Splitting                  ")
    print("---------------------------------------------")
    
    print()
    
    print("Total no of input data   :",dataframe.shape[0])
    print("Total no of test data    :",X_test.shape[0])
    print("Total no of train data   :",X_train.shape[0])
    
    
     # ---- STANDARD SCALAR 
        
    from sklearn.preprocessing import StandardScaler
    
    from sklearn.decomposition import PCA
          
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(X_train)
        
    
        #-------------------------- FEATURE EXTRACTION  --------------------------------
        
    
    #  PCA
    pca = PCA(n_components=6) 
    principal_components = pca.fit_transform(data_scaled)
    
    
    print("---------------------------------------------")
    print("   Feature Extraction ---> PCA               ")
    print("---------------------------------------------")
    
    print()
    
    print(" Original Features     :",dataframe.shape[1])
    print(" Reduced Features      :",principal_components.shape[1])
    
    
    
    
    # Plot the results
    plt.figure(figsize=(6, 6))
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c='blue', edgecolor='k', s=50)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA: First Two Principal Components')
    plt.grid()
    plt.savefig("pca.png")
    plt.show()
    
    #  explained variance ratios
    print("Explained variance ratios:", pca.explained_variance_ratio_)
    
    
    
    # ----- SVM ------
    
    from sklearn.svm import SVC
    
    
    from sklearn import linear_model
    
    svc = SVC()
    
    svc.fit(X_train,y_train)
    
    pred_svc = svc.predict(X_test)
    
    
    import pickle
    with open('svc.pickle', 'wb') as f:
          pickle.dump(svc, f)
    
    acc_svc = metrics.accuracy_score(pred_svc,y_test) * 100
    
    print("--------------------------------------------------")
    print("Classification - Support Vector Machine")
    print("--------------------------------------------------")
    
    print()
    
    print("1) Accuracy = ", acc_svc , '%')
    print()
    print("2) Classification Report")
    print(metrics.classification_report(pred_svc,y_test))
    print()
    print("3) Error Rate = ", 100 - acc_svc, '%')


    st.markdown(f'<h1 style="color:#000000;font-size:14px;">{"Enter the following details"}</h1>', unsafe_allow_html=True)



    a1 = st.text_input("Enter Sample ID")
   
    a2 = st.text_input("Enter Solvent Type (0 - Acetone , 1 - Dichloromethane, 2 - Ethyl Acetate , 3 -Toluene)")
   
    a3 = st.text_input("Enter Temperature (Â°C)")

    a4 = st.text_input("Enter Casting Speed (m/min)")
   
    a5 = st.text_input("Enter Pressure (bar)")
   
    a6 = st.text_input("Enter Solvent Concentration (%)")    
   
    a7 = st.text_input("Enter SAdditives (Type) ( 0- Fillers, 1-None, 2 - Plasticizer, 3-Stabilizer)")    
       
    a8 = st.text_input("Enter PLA Yield (%)")        
    
    
    
     
    aa1 = st.button('Submit')
   
    if aa1:
       
    
       Data_reg = [int(a1),int(a2),float(a3),float(a4),float(a5),float(a6),int(a7),float(a8)]
       # st.text(Data_reg)
                   
       y_pred_reg=svc.predict([Data_reg])
       
       st.text(y_pred_reg)
       
       
       if y_pred_reg == 0:
           
           st.markdown(f'<h1 style="color:#000000;font-size:24px;text-align:center;">{"Identified Quality = * HIGH * "}</h1>', unsafe_allow_html=True)

       elif y_pred_reg == 1:
           
           st.markdown(f'<h1 style="color:#000000;font-size:24px;text-align:center;">{"Identified Quality = * LOW * "}</h1>', unsafe_allow_html=True)
       

