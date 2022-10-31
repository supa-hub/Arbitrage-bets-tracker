# Arbitrage-bets-tracker
A script that tracks multiple european sports betting sites and looks for arbitrages<br />

The file betting_tracker.py contains the code that gets the bets data from the multiple sports betting sites.<br />
The code utilises slenium webdriver on some websites, and on others the normal requests python library.<br />
Selenium is used on some sites because these sites use more complicated get requests to get the data for the bets.<br />
<br />
The arbitrage_calculator.py is the file that gets all the data from the betting_tracker.py and calculates, if there is any arbitrage between the different websites.
The names.json file is used to store different name variations if the sports teams. This is because different betting websites have different name variations for the same teams.<br />
<br />
Currently the code is under development, but the file that needs to be updated is mostly the names.json, as the betting_tracker.py and arbitrage_calculator.py are mostly finished.<br />
<br />
As I am currently studying for my high school finals exams. Coding is mostly on hold for this reason, but development will resume after the finals.<br />
