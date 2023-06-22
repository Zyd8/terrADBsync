import subprocess
import datetime

def get_second_to_last_word(path):
    slash_list = []
    for index, slash in enumerate(path):
        if slash == "\\" or slash == "/":
            slash_list.append(index)
    second_last_slash_index = slash_list[-2] if len(slash_list) >= 2 else -1
    return print(path[second_last_slash_index+1:max(slash_list)])

file_path = "sdcard/Android/data/com.and.games505.TerrariaPaid"  
get_second_to_last_word(file_path)

