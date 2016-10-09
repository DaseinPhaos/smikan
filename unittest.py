import smikan
import copy

homepage = smikan.get_homepage()

# Finding bangumis by broadcasting date
print(hp.fri)

# Grabing details from a particular bangumi
bangumi = hp.fri[0]
bangumi.get()
print(bangumi.subtitles)
    
# Check which season the homepage is currently in
print(homepage.period)

# Navigate to another season
homepage.change_period(homepage.periods[1])
print(homepage.fri)