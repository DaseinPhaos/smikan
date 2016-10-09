import smikan
import copy

hp = smikan.get_homepage()
ohp = copy.deepcopy(hp)

print(ohp.fri)
lp = ohp.periods[1]
print(lp)

hp.change_period(lp)
print(hp.fri)

jojo = ohp.fri[0]
jojo.get()
print(jojo.subtitles)

