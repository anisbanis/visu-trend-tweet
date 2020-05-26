# VTT - Visualisation of Trending Tweets

VTT is a small webapp enabling users to visualize their tweets in a nice and fun way. It is written in pure Python and pure JavaScript by Anis Bouaziz and Jean-Marc Fares (@al-one-zero).

## Installation

1. Clone the repo  
2. `cd visu-trend-tweet`
3. `python vtt.py` (`python` should designate a python3 interpreter)
4. Navigate to http://localhost:8080/frontend/src

## With Docker

1. Clone the repo
2. `docker build -t vtt:latest .`
3. `docker run -d -t 8080:8080 vtt`
4. Navigate to http://localhost:8080/frontend/src
