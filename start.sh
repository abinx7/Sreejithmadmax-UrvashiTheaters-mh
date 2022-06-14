if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Sreejithmadmax/UrvashiTheaters.git /UrvashiTheaters
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /UrvashiTheaters
fi
cd /UrvashiTheaters
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
