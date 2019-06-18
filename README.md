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
Create the conda environment
```
conda env create -f make_otu_table_environment.yml
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="identify/spreading_correction.xml" />
```
Restart Galaxy to see the tool in the menu

## Source
https://www.nature.com/articles/nmeth.4666 <br />
https://github.com/sandberg-lab/spreading-correction/
