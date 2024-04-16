import random
import os
playerlist=[]
class Game1:
    def play(self):
        import xlrd
        workbook = xlrd.open_workbook('name.xls')
        sheet = workbook.sheet_by_index(0)
        playerlist = [sheet.cell_value(i, 1) for i in range(1, sheet.nrows)]
        Ghost = []
        for _ in range(2):
            startgost = random.choice(playerlist)
            self.getgost(startgost, playerlist, Ghost)
        end = 'C'
        i = 0
        while end != 'P' or end != 'G':
            if len(playerlist) <= 2:
                end = 'G'
                break
            else:
                attachghost = random.choice(Ghost)
                attachplayerlist = random.choice(playerlist)
                if random.randint(0, 1) == 0:
                    self.getgost(attachplayerlist, playerlist, Ghost)
                    if random.randint(0, 1) == 1:
                        Ghost.remove(attachghost)
                        playerlist.append(attachghost)
            print('Ghost', Ghost)
            print('playerlist', playerlist)
            print(
                '----------------------------------------------------------------------------------------------------------------------------')
            i += 1

        if end == 'G':
            print('Gost!')
        elif end == 'P':
            print('playerlist!')
        print('Ghost', Ghost)
        print('playerlist', playerlist)
        print('最终轮数', i)

    def getgost(self, name, playerlist, Ghost):
        playerlist.remove(name)
        Ghost.append(name)
class Game2:
    def play(self):
        import xlrd
        workbook = xlrd.open_workbook('name.xls')
        sheet = workbook.sheet_by_index(0)
        playerlist = [sheet.cell_value(i, 1) for i in range(1, sheet.nrows)]
        hunter = random.choice(playerlist)
        rounds = int(input("轮数："))

        for _ in range(rounds):
            print(f"当前hunter是: {hunter}")
            like = random.choice([True, False])

            if like:
                print(f"{hunter} 被选中")
                index = playerlist.index(hunter)
                next_hunter = random.choice([playerlist[index - 1], playerlist[(index + 1) % 20]])
                hunter = next_hunter
            else:
                n = random.randint(1, len(playerlist) - 1)
                next_hunters = random.sample(playerlist, n)
                next_hunter = random.choice(next_hunters)
                hunter = next_hunter

        print(f"最终的hunter是: {hunter}")
class Game3:
    def play(self):
        import xlrd
        workbook = xlrd.open_workbook('name.xls')
        sheet = workbook.sheet_by_index(0)
        playerlist = [sheet.cell_value(i, 1) for i in range(1, sheet.nrows)]
        while (len(playerlist) > 1):
            i = random.choice(playerlist)
            k = random.randint(0, 1)
            if len(playerlist) != 2:
                if (k):
                    tmpp = playerlist[playerlist.index(i) - 1]
                    playerlist.remove(playerlist[playerlist.index(i) - 1])
                else:
                    if (playerlist.index(i) + 1) < len(playerlist):
                        tmpp = playerlist[playerlist.index(i) + 1]
                        playerlist.remove(playerlist[playerlist.index(i) + 1])
                    else:
                        tmpp = playerlist[0]
                        playerlist.remove(playerlist[0])
                print(f"警长射中了:", tmpp)
                print(f"现在活着的人是:", playerlist)
            else:
                lasthit = random.choice(playerlist)
                playerlist.remove(lasthit)
                print(playerlist, f'击中了', lasthit)
                print(f'winer:', playerlist)
class Game4:
    def play(self):
        import xlrd
        workbook = xlrd.open_workbook('name.xls')
        sheet = workbook.sheet_by_index(0)
        playerlist = [sheet.cell_value(i, 1) for i in range(1, sheet.nrows)]
        random.shuffle(playerlist)
        def next_player(curr_index, direction, length):
            if direction == 'cw':
                return (curr_index + 1) % length
            else:
                return (curr_index - 1) % length

        def count_off(players, start_index, step):
            current_index = start_index
            player_count = len(players)
            direction = 'cw'
            count = 1
            while player_count > 1:
                print(f"玩家 {players[current_index]} 报数 {count}")
                if random.random() < 0.3:
                    direction = random.choice(['cw', 'ccw'])
                    print(
                        f"玩家 {players[current_index]} 换方向，下一个方向是{'顺时针' if direction == 'cw' else '逆时针'}")
                if random.random() < 0.1:
                    print(f"玩家 {players[current_index]} 被淘汰！")
                    players.pop(current_index)
                    player_count -= 1
                    current_index %= player_count
                    print(f"当前未淘汰玩家数量: {player_count}")
                else:
                    current_index = next_player(current_index, direction, player_count)
                count = (count % step) + 1
            print(f"最后留下的玩家是 {players[current_index]}")

        while True:
            count_off(playerlist, 0, 7)
            if len(playerlist) == 1:
                break
def info():
    print('***************************************************')
    print('*[*] A python file made by phtcloud 2024          *')
    print('*[!] AI is not a good practice                    *')
    print('***************************************************')
    print('*[*] Last updated date: 2024.04.16                *')
    print('*[*] This project follows an open source protocol *')
    print('*[*] GNU General Public License v3.0              *')
    print('*[*] You can found my GitHub repository           *')
    print('*[-] https://github.com/phtcloud-dev              *')
    print('***************************************************')

# 主函数
def main():
    games = {
        '1': Game1(),
        '2': Game2(),
        '3': Game3(),
        '4': Game4()
    }

    while True:
        print('----------games----------')
        print('1.                    鬼魂')
        print('2.                    邻居')
        print('3.                    警长')
        print('4.                    报数')
        print('----------tools----------')
        print('idp              安装依赖包')
        print('clear                 清屏')
        print('----------other----------')
        print('exit                  退出')
        print('info                 彩蛋?')
        game_num = input("请输入游戏编号（1, 2, 3, 4）或输入其他编号: ")

        if game_num in games:
            games[game_num].play()
        elif game_num.lower() == 'idp':
            os.system('pip install xlrd')
        elif game_num.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif game_num.lower() == 'info':
            info()
        elif game_num.lower() == 'exit':
            print("退出游戏。")
            break
        else:
            print("请输入有效的游戏编号。")


if __name__ == "__main__":
    info()
    main()
