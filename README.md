# NCAA_ML

ncaa_ml is a fun project that uses KenPom data to generate March Madness brackets using GNB, RF models.

- the main `ncaa_ml.py` runs a specified number of simulations.
- choose one to fill out your bracket with.
- can visualize the end of simulation by who won the most.
### Installation / Running
1.  Install requirements.txt with conda / favorite env manager.
2.  gets all kenpom data and updates config `python get_data.py`
3.  if necessary change ncaa_config.yml for # simulations, risk
4.  in config replace all State -> St. to match names, and fix names that might be wrong like UConn -> Conneticut
5.  in kenpom_current DELETE the teams that aren't in from first 4, only should have 64 teams
5.  python ncaa_ml.py --data data/kenpom_data.csv --plot False   
### Other Notes
The data is scraped from [KenPom](https://www.kenpom.com) from 2002-Current Year.
Out of respect for KenPom, I prefer not to supply the scraping script (however it is pretty easy), and the formatted data.
It looks something like this:
![data](https://imgur.com/koWksdN.png)

