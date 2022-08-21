with open("C:\\Users\\spos\\Downloads\\radiokp.ru.har", 'r') as text:
    counter = 0
    new_list = list()
    for row in text:
        if "mavecloud.s3mts.ru" in row and "episodes" in row and".mp3" in row:
            counter +=1
            print(row.split('"')[3])
            new_list.append(row.split('"')[3])

    print(len)
    print(counter)

# "url" in row