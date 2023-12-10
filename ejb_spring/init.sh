python3 -m venv venv

source ./venv/bin/activate

pip3 install -r ./server/ejb_spring_boot/requirements.txt

python3 -c "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data')" ]

deactivate