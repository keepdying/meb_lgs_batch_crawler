@echo off
cls

if exist .\venv\ (
	echo Program calistiriliyor
	call .\venv\Scripts\activate
	py main.py
) else (
	echo Gerekli kutuphaneler kuruluyor
	py -m venv venv
	call .\venv\Scripts\activate
	py -m pip install -r requirements.txt
	echo Program calistiriliyor
	py main.py
)