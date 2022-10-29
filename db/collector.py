from models import Word

f = open('base.txt', 'r', encoding='utf-8')
lines = f.readlines()
print(len(lines))
type = None
r = []
for line in lines:
    line = line.replace('\n','')
    if line.startswith('['):
        type = line
        continue

    s = line.split(',')
    r.append(
        dict(
            word=s[0],
            description=s[1],
            interpretation=s[2],
            type=type[1:][:-1]
        )
    )

Word.insert_many(r).execute()