<div id="top"></div>

# NASDAQ-Python-Script
### Technologies Used
* Python 3.10
* Aiohttp 3.8.3
* Amazon S3
* Amazon QuickSight
* Black 

Script written in Python, takes BigMac index data from NASDAQ of all countries and sends to the Amazon S3 and visualise by Amazon QuickSight.
The script takes a set of data from https://data.nasdaq.com/data/ECONOMIST-the-economist-big-mac-index/usage/quickstart/api and saves it to Amazon S3.
#### Example of Big Mac Index - Romania - https://data.nasdaq.com/data/ECONOMIST/BIGMAC_ROU-big-mac-index-romania
<p align="left">
  <img src="https://i.imgur.com/MNl0XKI.png" width="80%" height="80%">
</p>

<br/><br/>
#### Next, the script sends email notification to the specified email address that the data was uploaded on S3 bucket.<br/>
<p align="left">
  <img src="https://i.imgur.com/snjPBB3.png" width="50%" height="50%">
</p>
</br>

### Script creates a data visualization based on the TOP countries with the highest Big Mac index in July 2021 using Amazon QuickSight.
Official link to visualised data: <br/>
https://eu-central-1.quicksight.aws.amazon.com/sn/embed/share/accounts/646507693275/dashboards/2ab4aa4c-c6d9-4e2a-adcb-cd8b19567d76/sheets/2ab4aa4c-c6d9-4e2a-adcb-cd8b19567d76_b3e238ab-67cc-4332-816c-c9da64ca3cd3/visuals/2ab4aa4c-c6d9-4e2a-adcb-cd8b19567d76_3433c8b9-c115-4324-a2ba-5353ea1f5097?directory_alias=tutorialdan
### *You may need to be logged in into Amazon account to see visualised data in the given link above.*
Otherwise check the picture below how it looks.

<p align="center">
  <img src="https://i.imgur.com/bhPl4xW.png" width="80%" height="80%">
</p>

## Setup
- _To run this project, you need to install [Python](https://www.python.org/downloads/) then create and active virtual environment_
```
$ python3 -m venv env
```
- _Clone repo and install packages in requirements.txt_ 
```
$ git clone https://github.com/fortyfortyy/NASDAQ-python-script.git
$ cd ../NASDAQ-python-script
$ pip install requirements.txt
```
- _Run script_
```
$ python main.py
```
<p align="right">(<a href="#top">back to top</a>)</p>
