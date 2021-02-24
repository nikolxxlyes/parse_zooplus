# parse_zooplus
Parse https://www.zooplus.de/

Instruction:
1. Download the project:
  
  git clone https://github.com/nikolxxlyes/parse_zooplus.git
  
2. Download webdriver selenium. For example, follows the link below download "chromedriver_win32.zip" and unpack "chromedriver.exe"
    
  https://chromedriver.storage.googleapis.com/index.html?path=89.0.4389.23/
  
  Download "chromedriver_win32.zip", unpack "chromedriver.exe"

3. Set varible in main.py like
  
  driver_file = r'D:\chromedriver.exe'  # path to file webdriver "chromedriver.exe" p.2
  
  webdriver_ = webdriver.Chrome         # choose respectively
  
4. Create and activate pythonvenv. For example, in Windows
  
  python3 -m venv \path\to\new\virtual\environment
  \path\to\new\virtual\environment\Scripts\activate.bat
  
5. Install Python packages:
  
  pip install -r requirements.txt
  
