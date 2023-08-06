# AnimeHoursFinder
Find the amount of hours you took to watch the anime you love.  

Uses [unoffical mal api by Daren Liang](https://github.com/darenliang/mal-api) to get the data from [MyAnimeList](https://myanimelist.net/).  

#### Install  
`pip install animeHours==0.1.1`  

### Usage   
To import the package do this  
```
from animeHours import animeHours as ah
```  

To search with an XML file exported from MyAnimeList create a `Finder` class with the `file` arg pointing to the file  
```
file = "anime-list.xml"
finder = ah.Finder(file=file)

hours = brain.find("open")
print("You've watched {} hours of anime\n".format(hours)
```  
  
To search with a string of anime titles, create a `Finder` class with the `animelist` arg pointing to the string
```
animeList = "Dr Stone, My Hero Academia Season 1"
brain = ah.Finder(animelist=animeList)

hours = brain.find()
print("You've watched {} hours of anime\n".format(hours))
```  
  
