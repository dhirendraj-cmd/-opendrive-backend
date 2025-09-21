pip install "fastapi[standard]"
pip install sqlmodel
pip install "python-jose[cryptography]"
pip install bcrypt==3.2.2
pip install passlib
pip install python-multipart
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf