#PI SHUTDOWN
=======
##Brand New Edit with Detailed DIrections
==
I got this idea from a fellow rpi enthusiast his github is https://github.com/gilyes/pi-shutdown


we will need a pushbutton on pin 5 and ground. We will use a script and call it to sleep until pin 5 is set to high.

The reason this works is because we are using pin 5. you may use others to call the shutdown or restart script but It will be the only combination that I have found to acctually star the PI from a shutdown mode. Sense shortneing Pin 5  will cause the pi to start up. So we are taking advantage of that. 

Youll want to set the pin and subscribe than we'll set an object to sleep until the button is Held for 3 secs + causing a shutdown, or pressed momentarily for a restart 

```

def buttonStateChanged(pin):
global buttonPressedTime

if not (GPIO.input(pin)):
# button is down
buttonPressedTime = datetime.now()
else:
# button is up
if buttonPressedTime is not None:
if (datetime.now() - buttonPressedTime).total_seconds() >= shutdownMinSeconds:
# button pressed for more than specified time, shutdown
call(['shutdown', '-h', 'now'], shell=False)
else:
# button pressed for a shorter time, reboot
call(['shutdown', '-r', 'now'], shell=False)
```
Using this code, if the button is pressed for more than a few seconds then the Raspberry Pi *shuts down*, otherwise it *reboots*.


We will want this added to our startup so the bother of loading it will not be needed :D 

CD to /etc/systemd/system/ 

create a service 

```
sudo nano rpi-push-shutdown.service
```

I called mine rpi-push-shutdown You are free to name it as you please. Just remember it for our next steps.
You'll want to replace the ExecStart pointing to the Shutdown File and WorkingDirectory to the relative path of the saved script from earlier.

```
[Service]
ExecStart=/usr/bin/python /path_to_script/rpi-push-shutdown.py
WorkingDirectory=/path_to_script/
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=pishutdown
User=root
Group=root

[Install]
WantedBy=multi-user.target
```
Now we will Enable and Run the Service and once you reboot it will be automatically started. 

```
sudo systemctl enable rpi-push-shutdown.service
sudo systemctl start rpi-push-shutdown.service
```
Now we will check and see if the script is enabled 

```
sudo systemctl list-unit-files | grep enabled
```
Check for any errors [ a little debugging I like to do on all my scripts ] Preventive maintenance is the key to being a successful IT GURU 😀 

```
sudo systemctl status rpi-push-shutdown.service
```
 rpi-push-shutdown.service
   Loaded: loaded (/etc/systemd/system/rpishutdown.service; enabled)
   Active: active (running) since Thu 2017-04-25 21:20:31 EDT; 1s ago

You'll see something like this If it's successful with a few more lines with the output of the script   

Now you can test your button and enjoy your never thought possible pushbutton restart/shutdown/start With the fraction of cost of the PowerBoard addons :D



