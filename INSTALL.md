WINDOWS

cd "C:\Users\pro90\OneDrive\Документы\NetBeansProjects\TitanCoreFramework"

python -m venv venv
"venv\Scripts\activate"
pip install -r requirements.txt


# migration
python craft.py migrate
python craft.py db:seed

python -m uvicorn app.main:app --reload

Install nodejs https://nodejs.org/en/download/current
Windows Installer (.msi)




UBUNTU

sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential python3-pip python3.12-venv curl

cd /var/www/html/workpython/titanCoreFramework
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# migration
./craft.py migrate
./craft.py db:seed

curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install
npm run watch

-----------------------REACT-------------------------
cd /var/www/html/workpython/titanCoreFramework
sudo npm run watch


