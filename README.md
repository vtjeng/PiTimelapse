# PiTimelapse

Timelapse photography with the Raspberry Pi camera.

## Summary

A long-term time lapse is an effective and fun way to communicate changes over time. However, most cameras which are custom-built to capture time lapse videos are very costly. While DSLRs are able to capture photos at set intervals, the images captured cannot be accessed (without purchasing additional equipment) until the entire set of photos. Our project captures the individual frames of a timelapse video with cheap, reliable, off-the-shelf components, with the added benefit of allowing one to review and work with the images as they are being captured by uploading the images to Dropbox.

## Installation

Clone this repository to your Raspberry Pi and run the `run_timelapse` script. By default, the script will take images to the `images` directory once every minute, and _not_ upload it to Dropbox.

### Dropbox Upload

If you would like to upload the images to Dropbox, either ensure that the `images` folder exists on your Dropbox, or run

```sh
./Dropbox-Uploader/dropbox_uploader.sh mkdir images
```

### Auto-Start on Reboot

If you would like the script to run on reboot, add the following line to your crontab via `crontab -e`

```crontab
# runs script once on reboot
@reboot /PATH/TO/REPO/run_timelapse &
```

## Other Work

Plenty of work has already been done in the field of time-lapse photography, including an [Instructables Site](http://www.instructables.com/id/How-to-make-a-long-term-time-lapse/), an amazing [Vimeo video](http://www.photographyblogger.net/a-year-long-time-lapse-study-of-the-sky/), and a [project by David Hunt](http://www.davidhunt.ie/raspberry-pi-in-a-dslr-camera/) using a Raspberry Pi to control a DSLR camera

## Additional Resources

[Testing Multiple Pi Camera Options](https://www.raspberrypi-spy.co.uk/2013/06/testing-multiple-pi-camera-options-with-python/)
