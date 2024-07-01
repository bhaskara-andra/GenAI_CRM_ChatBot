import os
 
current_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_folder)
streamlit_command = f"python -m streamlit run final_crm_chatbot.py"
os.system(streamlit_command)


#C:\Users\BHASKARASUBBARAO\OneDrive - Virtusa\DesktopFiles\z_CRM_usecase\final_crm_chatbot.py