//Install what you'll need and set up a python vertual env. Adjust for your mqtt server.<br>

sudo apt update<br>
sudo apt install mosquitto-clients python3 python3-pip<br>
sudo apt install python3.11-venv<br>
python3 -m venv /opt/mqtt_sniffer_env<br>
source /opt/mqtt_sniffer_env/bin/activate<br>
pip install "paho-mqtt<2.0"<br>
<br>
//create and install python script<br>
mkdir /etc/mqttsniffer<br>
cd /etc/mqttsniffer<br>
nano mqttsniffer.py<br>
<br>
//create and install the service<br>
sudo nano /etc/systemd/system/mqtt-sniffer.service<br>
<br>
sudo systemctl daemon-reload<br>
sudo systemctl enable mqtt-listener<br>
sudo systemctl start mqtt-listener<br>
<br>
//To check the status:<br>
sudo systemctl status mqtt-sniffer<br>
<br>
//Log output<br>
sudo journalctl -u mqtt-sniffer -f<br>
<br>
//Home assistant, create sensor:<br>
