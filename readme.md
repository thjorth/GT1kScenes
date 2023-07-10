Display resolution: 800 x 480

On raspberry pi:


sudo pip install python-rtmidi
sudo pip install --force-reinstall -v "pygame==2.5.0"
sudo apt-get install libsdl-ttf2.0-dev libsdl1.2-dev
sudo apt install libsdl2-ttf-2.0-0


/etc/dhcpcd.conf

interface wlan0                                        
static ip_address=192.168.8.88/24                      
static routers=192.168.8.1                             
static domain_name_servers=192.168.8.1 8.8.8.8


/boot/config.txt
# enabling the Hyper Pixel display
dtoverlay=vc4-kms-dpi-hyperpixel4
dtparam=rotate=270


/etc/xdg/lxsession/LXDE-pi/autostart

@sh <path to a shell scritp that changes to the project dir and runs "python main.py --fullscreen">