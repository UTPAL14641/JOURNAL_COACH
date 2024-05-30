echo [$(date)]: "START"


echo [$(date)]: "creating env with latest python version" 


conda create --prefix ./Intern_Emo_b_j python -y


echo [$(date)]: "activating the environment" 

source activate ./Intern_Emo_b_j

echo [$(date)]: "installing the dev requirements" 

pip install -r requirements.txt

echo [$(date)]: "END" 
