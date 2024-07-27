stock_list = []

with open("D:\\Code\\Python\\pachong\\list.html", 'r', encoding='utf-8') as file:
    for line in file:
        if ">US</span> " in line:
            part = line.split(">US</span> ", 1)
            result = part[1].strip()
            stock_list.append(result)
            print(result)

print(stock_list)
