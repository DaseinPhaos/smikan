import mikanapi

hp = mikanapi.get_homepage()
print(hp.fri)
jojo = hp.fri[0]
jojo.get_content()
print(jojo.subtitles)