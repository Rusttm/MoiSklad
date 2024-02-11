
# import re
# text_line = "https://api.moysklad.ru/api/remap/1.2/entity/factureout?offset=0&filter=moment%3C=2021-05-25"
# text_line = "?offset=0&filter=moment%3C=2021-05-25"
# print(text_line.split("?"))
# print(text_line[1:].split("&"))
# print(text_line.find("offset="))
# print(text_line.find("&"))

# if param line already with data ?offset=2000=filter=moment<=2022-02-22...
old_param_line = "?offset=0&filter=moment%3C=2021-05-25"
# old_param_line = "?filter=moment%3C=2021-05-25&offset=1000"
add_param_line = "offset=2000"
finder = add_param_line.find("ffset=")
if finder:
    first_splitter = old_param_line[1:].split("&") #
    for line in first_splitter:
        res = line.find("ffset=")
        if res>0:
            first_splitter.remove(line)
            break
    old_param_line = "?" + "&".join(first_splitter) + "&" + add_param_line

print(old_param_line)