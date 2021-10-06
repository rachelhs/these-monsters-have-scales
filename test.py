import os

directory = r'/Users/rachel/Documents/These_Monsters_Have_Scales/tmhs-raspberrypi/sounds'
for filename in os.listdir(directory):
        print(os.path.join(directory, filename))