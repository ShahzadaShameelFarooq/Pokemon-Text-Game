f = open('test.txt', 'r')

for line in f:
    if line != '':
        if line.startswith('TRAINER:'):
            s = line.split(':')[-1].strip().lower()
            print(s)
            n = f.readline()
            print(n.split(':')[-1].strip())

        elif line.startswith('POKEMON:'):
            p = line.split(':')[-1].strip().lower()
            print(p)
            lvl = f.readline().split(':')[-1].strip()
            print(lvl)
            max_hp = f.readline().split(':')[-1].strip()
            print(max_hp)
            attk = f.readline().split(':')[-1].strip()
            print(attk)
            defense = f.readline().split(':')[-1].strip()
            print(defense)

f.close()
