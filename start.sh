if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/abinx7/Sreejithmadmax-UrvashiTheaters-mh.git /MoviesHubGroup2
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /MoviesHubGroup2
fi
cd /MoviesHubGroup2
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
