# what is a virtual environment
# how to create virtual environment (pip)
python -m venv my_venv
python -m venv ../my_venv
python -m venv ../../my_venv
# how to activate/deactivate virtual environment
source my_venv/bin/activate
deactivate
# how to see what are the packages/libraries in the current environment
pip list [--format=freeze]
pip freeze
# how to export requirements.txt
pip freeze > requirements.txt
pip list --format=freeze > requirements.txt 

# pip freeze
# typing_extensions==4.16.0@SDFDS@xcfda/dfskljfslk  
# pip list --format=freeze
# typing_extensions==4.16.0
# how to install packages/libraries to the env
pip install -r requirements.txt
