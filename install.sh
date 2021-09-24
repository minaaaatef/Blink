green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}>>> Update apt ${reset}"
sudo apt update
echo "${green}>>> install nodejs & npm & python ${reset}"
sudo apt install nodejs npm python3-pip

echo "${green}>>> install virtualenv ${reset}"
pip3 install virtualenv 

echo "${green}>>> clone git repo ${reset}"

git clone https://github.com/minaaaatef/blink
cd blink
cd BackEnd
echo "${green}>>> Creating virtualenv${reset}"
virtualenv venv
sleep 2
echo "${green}>>> activate the venv.${reset}"
source venv/bin/activate
echo "${green}>>> Installing the requirements${reset}"
pip install -r requirements.txt 
echo "${green}>>> Installing honcho to run ProcFile${reset}"
pip install honcho
echo "${green}>>> Installing npm packages${reset}"
cd ../FrontEnd/vuetify-basic-components-master
npm install
echo "${green}>>> Running ProcFile ${reset}"
cd ../../
pwd
honcho start
