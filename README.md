# ESPNFantasy
Playing around with python scraping + fantasy bball

Uses python 3, selenium for help in logging into the iframe / basic navigation and soup for some of the parsing.
Current sample output for a player so far:

{'Assists': '88',
 'Blocks': '9',
 'Field Goal Percentage': '.4502',
 'Free Throw Percentage': '.6837',
 'Id': '7',
 'Points': '305',
 'Rebounds': '104',
 'Steals': '25',
 'Three Pointers Made': '12',
 'Turnovers': '46',
 'teamMembers': ['Russell Westbrook, OKC PG',
                 'Jimmy Butler, Chi SG, SF',
                 'Jeff Green, Mem SF, PF',
                 'Carmelo Anthony, NY SF, PF',
                 'Bismack Biyombo, Tor C',
                 'Kyrie Irving, Cle PG, SG',
                 'Enes Kanter, OKC C, PF',
                 'Elfrid Payton, Orl PG',
                 'Jeremy Lin, Cha PG, SG',
                 'Clint Capela, Hou C, PF',
                 'LaMarcus Aldridge, SA PF, C',
                 'Khris Middleton, Mil SF, SG',
                 'C.J. Miles, Ind SF, SG']}

To run:
Replace the driver.get() part with your espn basketball league url. 
python3 espnFantasy.py login password
