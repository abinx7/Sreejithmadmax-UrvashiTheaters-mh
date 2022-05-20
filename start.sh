if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Sreejithmadmax/Cinderella2022Sub.git /Cinderella2022Sub
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Cinderella2022Sub
fi
cd /Cinderella2022Sub
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
