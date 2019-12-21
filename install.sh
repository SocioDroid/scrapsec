echo Enter SENDGRIP API KEY
read api_key
export SENGRID_API_KEY=$api_key
echo "export SENDGRID_API_KEY=$api_key" > /etc/profile.d/send.sh
chmod +x /etc/profile.d/send.sh
pip3 install sendgrid
pip3 install argparse
pip3 install apscheduler
pip3 install bs4
