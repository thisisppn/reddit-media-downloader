# Reddit Media Downloader
A small python script that taken in the id of the subreddit as input and downloads all the images and video from it.
Currently the script supports imgur and gyfcat outside of reddit. 

#### Usage
`python3 reddi.py pics`

#### Dependencies
You might want to install requests using the command `pip3 install requests` if you don't already have it.

#### Sample logs
```
Namespace(subreddit='pics')
??? downloads/pics ????????

Downloading imgur http://i.imgur.com/GJYYNle.jpg
...100%, 0 MB, 253 KB/s, 1 seconds passed
Downloading imgur https://i.imgur.com/Fo7a18f.jpg
...101%, 0 MB, 118 KB/s, 1 seconds passed
Downloading imgur https://i.redd.it/pmmnq62lpiz01.jpg
...100%, 0 MB, 1194 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/ayj2cr2cuhlz.jpg
...106%, 0 MB, 659 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/mlfo0b3rec611.jpg
...106%, 0 MB, 703 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/fq3e8q25rnvz.jpg
...103%, 0 MB, 846 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/xyn2xxgal3601.jpg
...100%, 3 MB, 2848 KB/s, 1 seconds passed
Downloading imgur https://i.redd.it/gultof51thpz.jpg
...110%, 0 MB, 434 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/jouzymhjwtpy.jpg
...113%, 0 MB, 443 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/syycygxj3du01.jpg
...103%, 0 MB, 584 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/dn0ayymwsfpz.jpg
...116%, 0 MB, 458 KB/s, 0 seconds passedd
Downloading imgur https://i.imgur.com/O2vfxdf.jpg
...100%, 0 MB, 336 KB/s, 1 seconds passed
Downloading imgur https://i.imgur.com/q19s09w.jpg
...100%, 0 MB, 173 KB/s, 1 seconds passed
Downloading imgur https://i.redd.it/ny3ag1opjldz.jpg
...101%, 0 MB, 1558 KB/s, 0 seconds passed
Downloading imgur https://i.redd.it/etxh1zby4m8z.jpg
...102%, 0 MB, 937 KB/s, 0 seconds passed
Downloading imgur http://i.imgur.com/OX4ELwD.jpg
...100%, 0 MB, 312 KB/s, 1 seconds passed
Downloading imgur https://i.redd.it/xrgxdy9bzdn01.jpg
...100%, 0 MB, 400 KB/s, 0 seconds passed
Heading over to next page ... 
```

You'll see the downloaded media in a subfolder with the same name as the subreddit inside a folder called downloads.

## Enjoy!
