path = "sdcard/Android/data/com.and.games505.TerrariaPaid/Worlds"
list = []
for index, element in enumerate(path):
    if element == "/":
        list.append(index)

print(max(list))

result = path[max(list)+1::]
print(result)