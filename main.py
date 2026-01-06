import json
import random
import os

class Database:
    def __init__(self):
        self.db = None
        self.rand_list = []
        self.wrong = []
        self.point = 0
        self.sg=0
        self.mt=0
        self.data = {'done': [], 'wrong': []}
        self.type = 0
    def load(self):
        with open(f"db{self.type}.json", 'r',encoding='utf-8') as f:
            self.db = json.load(f)
            f.close()
        try:
            with open(f"index{self.type}.json", 'r') as f:
                self.data = json.load(f)
                f.close()
        except FileNotFoundError:
            print("没有错题记录，请先做题")
            with open(f"index{self.type}.json", 'w') as f:
                json.dump(self.data, f)
                f.close()
        except json.decoder.JSONDecodeError:
            print("错题记录错误,已重置")
            with open(f"index{self.type}.json", 'w') as f:
                json.dump(self.data, f)
                f.close()

    def save(self,option,index):
        if option==1 :
            if index+1 in self.data['wrong']:
                self.data['wrong'].remove(index+1)
                self.data['done'].append(index)
            elif index not in self.data['done']:
                self.data['done'].append(index)
        elif option==0 and index+1 not in self.data['wrong']:
            self.data['wrong'].append(index+1)
        with open(f"index{self.type}.json", 'w') as f:
            json.dump(self.data,f)
            f.close()
            
            



    def printf(self,index):
        print(self.db[index]['title'])
        print(f"A:{self.db[index]['a']}")
        print(f"B:{self.db[index]['b']}")
        print(f"C:{self.db[index]['c']}")
        print(f"D:{self.db[index]['d']}")

    def sequence(self):
        for i in range(0,len(self.db)-1):
            if self.db[i]['index']+1 not in self.data['done']:
                self.rand_list.append(i)

    @staticmethod
    def sort(i, word):
        match i:
            case 1:
                word.append('A')
            case 2:
                word.append('B')
            case 3:
                word.append('C')
            case 4:
                word.append('D')
        return word

    def false_handler(self,index):
        word = []
        if self.db[index]['type'] == 2:
            for i in self.db[index]['answer']:
                self.sort(i, word)
        else:
            self.sort(self.db[index]['answer'], word)
        print(f"\033[1;31m答案{word}\033[0m")
        self.save(0,index)
        input("按任意键继续")
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def rand_gen(self,mode):
        l1=20 if mode==0 else 35
        l2=30 if mode==0 else 50
        done_list = self.data['done']
        while True:
            num = random.randint(0, len(self.db)-1)
            test = self.db[num]
            print(f"{len(self.db)},{len(done_list)}")
            if len(self.db)-len(done_list) <= l1:
                for i in range(0,len(self.db)-1):
                    if i not in done_list:
                        self.rand_list.append(i)
                break
            if num not in self.rand_list and test['type'] == 1 and num not in done_list:
                self.rand_list.append(num)
            if len(self.rand_list) >= l1:
                break
        while self.type==0:
            num = random.randint(0, len(self.db)-1)
            test = self.db[num]
            if len(self.db)-len(done_list) <= l2:
                for i in range(0,len(self.db)-1):
                    if i not in done_list:
                        self.rand_list.append(i)
                break
            if num not in self.rand_list and test['type'] == 2 and num not in self.data['done']:
                self.rand_list.append(num)
            if len(self.rand_list) >= l2:
                break
        print("题目已生成")

    def wrong_sequence(self):
        wrong_data = self.data['wrong']
        for data in wrong_data:
            self.rand_list.append(int(data)-1)

    @staticmethod
    def judge(ans):
        if ans == 'A' or ans == '1':
            par = 1
        elif ans == 'B' or ans == '2':
            par = 2
        elif ans == 'C' or ans == '3':
            par = 3
        elif ans == 'D' or ans == '4':
            par = 4
        else:
            par = 0
        return par

    def do(self,arg):
        j = 0
        try:
            for index in self.rand_list:
                j += 1
                print(f"{j}/{len(self.rand_list)}")
                print("[单选题]", end='') if self.db[index]['type'] == 1 else print("[\033[1;6;33m多选题\033[0m]", end='')
                self.printf(index)
                ans = input()
                ans = ans.upper()
                if self.db[index]['type'] == 1:
                    par = self.judge(ans)
                    if par != self.db[index]['answer']:
                        self.false_handler(index)
                        self.sg += 1
                    else:
                        self.point += 1 if arg==0 else 2
                        print("\033[1;32m正确\033[0m")
                        self.save(1,index)
                else:
                    if len(ans) != len(self.db[index]['answer']):
                        self.false_handler(index)
                        self.mt += 1
                        continue
                    flag = 0
                    for i in ans:
                        par = self.judge(i)
                        if par not in self.db[index]['answer']:
                            self.false_handler(index)
                            self.mt += 1
                            flag = 1
                            break
                    if flag != 1:
                        self.point += 2
                        print("\033[1;32m正确\033[0m")
                        self.save(1,index)
                os.system('cls') if os.name == 'nt' else os.system('clear')
        except KeyboardInterrupt:
            return j-2
        return -10

    def result(self, arg1):
        print()
        if arg1=='2':
            print("\033[1;31m很遗憾，考试不合格\033[0m") if self.point<35 else print("\033[1;32m恭喜您，考试合格\033[0m")
        elif arg1=='4':
            print("\033[1;31m很遗憾，考试不合格\033[0m") if self.point<90 else print(
                "\033[1;32m恭喜您，考试合格\033[0m")
        print(f"您的最终得分：{self.point},其中错{self.sg}道单选，{self.mt}道多选")

    def clear(self):
        self.data['done'].clear()
        with open(f"index{self.type}.json",'w') as f:
            json.dump(self.data,f)
            f.close()
        print("已清除")



if __name__ == "__main__":
    root=Database()
    print("------复习不------")
    print("0.习概")
    print("1.计算机网络")
    print("2.马原(ai题目)")
    temp=int(input())
    root.type=temp if 0<=temp<=2 else exit(1)
    root.load()
    print("1.顺序刷题")
    print("2.模拟考试")
    print("3.错题集")
    print("4.整活模式")
    print("5.清除数据")
    a = input()
    match a:
        case '1':
            root.sequence()
        case '2':
            root.rand_gen(0)
        case '3':
            root.wrong_sequence()
        case '4':
            root.rand_gen(1)
        case '5':
            root.clear()
        case _:
            exit(1)
    b=root.do(0 if a=='2' else 1)
    root.result(a)
