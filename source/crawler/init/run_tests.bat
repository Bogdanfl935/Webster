cd ../core/Scripts
powershell "& "".\Activate.ps1"""
cd ..
cd tests
python -m pytest -s
pause