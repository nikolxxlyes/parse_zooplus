# parse_zooplus
#Describe

    Parse https://www.zooplus.de/

#Instruction:
1. ###Download the project:
  
        git clone https://github.com/nikolxxlyes/parse_zooplus.git
  
2. ###Download webdriver selenium. 
   
   We using Google Chrome in this example. Follows the link below, 
   download "chromedriver_win32.zip" and unpack "chromedriver.exe"
   
        https://chromedriver.storage.googleapis.com/index.html?path=89.0.4389.23/

3. ###Set variables in main.py like:
    - [REQUIRED] Path to webdriver file from p.2
     
          driver_file = r'D:\chromedriver.exe'          

    - [REQUIRED] Your browser respectively 
          
          webdriver_ = webdriver.Chrome       
      
    - [OPTIONAL] Your start browser options respectively. 
      
      Hide Google Chrome with option "--headless" 
      
          driver_hide_option.add_argument("--headless")   

          

  
4. ###Create and activate pythonvenv. 
   https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
  
5. ###Install Python packages:
  
        pip install -r requirements.txt

6. ###Run file app/main.py
