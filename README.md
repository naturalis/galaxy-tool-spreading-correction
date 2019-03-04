# galaxy-tool-spreading-correction
galaxy wrapper for spreading-correction
## Getting Started
### Installing
Installing the tool for use in Galaxy
```
cd /home/galaxy/Tools
```
```
sudo git clone https://github.com/naturalis/galaxy-tool-spreading-correction
```
```
sudo chmod 777 galaxy-tool-spreading-correction/unspread.py
sudo chmod 777 galaxy-tool-spreading-correction/unspread_manual.py
sudo chmod 777 galaxy-tool-spreading-correction/create_input.py
```
```
sudo ln -s /home/galaxy/Tools/galaxy-tool-spreading-correction/unspread.py /usr/local/bin/unspread.py
sudo ln -s /home/galaxy/Tools/galaxy-tool-spreading-correction/unspread_manual.py /usr/local/bin/unspread_manual.py
sudo ln -s /home/galaxy/Tools/galaxy-tool-spreading-correction/create_input.py /usr/local/bin/create_input.py

sudo ln -s /home/galaxy/Tools/galaxy-tool-spreading-correction/spreading_correction.sh /home/galaxy/galaxy/tools/identify/spreading_correction.sh
sudo ln -s /home/galaxy/Tools/galaxy-tool-spreading-correction/spreading_correction.xml /home/galaxy/galaxy/tools/identify/spreading_correction.xml
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="identify/spreading_correction.xml" />
```
Restart Galaxy to see the tool in the menu

## Source
https://www.nature.com/articles/nmeth.4666 <br />
https://github.com/sandberg-lab/spreading-correction/
