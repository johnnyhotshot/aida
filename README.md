# AIDA: Artificial Intelligent Digital Assistant

I didn't come up with the acronym, but I liked the origin source enough to want to use the name for my own project.

### [ Short Description ]

Aida is a script that manages my fantasy football team, so that I don't have to. It reads the projected points for each player on my team, shuffles around my player roster accordingly, and then checks the free agents board to see if any of those players are higher scoring than my current team.

### [ History ]

My family, along with some neighbors and family friends, has a fantasy football league that we all host every football season. Although I don't know the first thing about football, I have to have a team so that the league has the right amount of players. In the past, I've just autodrafted my team and then left it be - usually ending up with my team losing horrifically due to zero management. Personally, I didn't care, but my brother and dad loved to bring up how they'd beaten me again. For the 2017-2018 football season, I finally did what I said I was going to do for a few years - write a computer program to play my team for me. Aida 1.0 wasn't written very elegantly, as I was learning both Python and all of the libraries I used as I wrote it, but it worked. It worked well enough to win me first place in the league. Now, Aida 2.0 will win me the 2018-2019 league, and hopefully result in my expulsion from the league for winning too much (which would be both hilarious and amazing).

### [ Functionality ]

Aida uses Python, BeautifulSoup4, and Selenium to read my team roster, check if the players projected to score the most points that week are playing, and make any necessary adjustments if not. Then, it looks at the available free agent players, sees if the top free agents are any better than my worst players, and makes trades if so. Pretty sure it doesn't classify as "Artificial Intelligence", but saying that I wrote an AI to win fantasy football sounds cooler than saying I wrote a sorting program to win fantasy football.
