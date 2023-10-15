
pip install requests
pip install customtkinter
pip install fast-file-encryption
pip install wmi

if exist port.txt (
	start Broadcaster.bat
	start syncVault.bat
	python serverMenu.py
) else (
	python serverInit.py
)

timeout /t 10
exit