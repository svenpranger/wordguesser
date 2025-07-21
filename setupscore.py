header = "name|score|correctwords|totalguesses|totalmistakes|help|date"

for i in range (1,4):
    filename = f"score{i}.txt"
    with open (filename, "x") as f:
        f.write(header)
