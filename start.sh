if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Sreejithmadmax/CINDERELLARUNNING.git /CINDERELLARUNNING
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /CINDERELLARUNNING
fi
cd /CINDERELLARUNNING
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
