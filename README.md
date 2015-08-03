# Pool Monitor
Originally developed as a django website hosted locally, now simply reports temperatures to www.initialstate.com

## Requirements
1. Sensors as described in next section
2. RaspberryPi compatible with sensor
3. InitialState.com account, and api key

## Sensor Install/Configure
This should be used as a general overview of adding the water proof temperature sensor: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

## Physical Install
You should have a water tight box if your RaspberryPi will sit outside.  I opted for a clear top to show of my nerd skills to other nerds.
The case will need 2 holes: 1 for power (microUSB) and one for the sensor wire.
![Case Holes 1](https://github.com/h00die/poolmonitor/blob/master/docs/drill%20case.png)
![Case Holes 2](https://github.com/h00die/poolmonitor/blob/master/docs/drill%20case2.png)
These holes will need to be sealed with caulk/silicon to prevent water from getting in.
I placed a paper towel in there under the pi to catch any water that may get in, hopefully before it gets to the rPi.
I also, later, placed tin foil over the top, as well as heat sinks, to prevent the temperature from getting too hot.  After I baked my first rPi.
![deployed](https://github.com/h00die/poolmonitor/blob/master/docs/raspberrypi.png)
![deployed 2](https://github.com/h00die/poolmonitor/blob/master/docs/raspberrypi2.png)
I dropped my sensor in about a foot, in the shallow end, near the jets.  This should be low enough to avoid surface temperature fluctuation, yet high enough to avoid getting eatten by the vaccum stingray.
![sensor](https://github.com/h00die/poolmonitor/blob/master/docs/raspberrypi2.png)

## InitialState
Originally I developed a Django powered website to handle the data, and show graphs.  Then I learned of Initialstate.com which did all of what I wanted, and much more in an easier fashion.
Since then, I've contacted support on a Saturday at 3pm EST.  The Founder/CEO of the company responded in ~15min with lots of good helpful (technical) answers.  What better do you want from a company?
One thing to keep in mind, is that the InitialState log sender queues 10 at a time, so don't expect your data to show up immediately!