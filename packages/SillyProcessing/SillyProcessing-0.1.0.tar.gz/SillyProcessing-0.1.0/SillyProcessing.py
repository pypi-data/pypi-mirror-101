"""
SillyProcessing库：一个傻瓜式数据处理的库
依赖matplotlib,codecs等库
EnjoyXD
"""
import matplotlib.pyplot as plt
import codecs
x = []
y = []
slope = []
intercept_list = []
class position:
    def __init__(self):
        global intercept
    def output(filename,output):
        file = open(filename,"w")
        file.write(output)
        file.close()
    def get_position(self,textname):
        for i in range(2):
            file_position = codecs.open(textname, mode='r', encoding='utf-8')
            line = file_position.readline() # 以行的形式进行读取文件
            while line:
                a = line.split()
                b = a[i:i+1] # 这是选取需要读取的位数
                if i == 0:
                    x_num = b[0]
                    x_num=str(x_num)
                    x.append(x_num) # 将其添加在列表之中
                else:
                    y_num = b[0]
                    y_num=str(y_num)
                    y.append(y_num)
                line = file_position.readline()
        file_position.close()
    def draw_position(self):
        plt.plot(x,y,linewidth=3,marker='o',mec='r')
        plt.xlabel("x",fontsize=14)
        plt.ylabel("y",fontsize=14)
        plt.show()
    def write_slope(self,slopename):
        for j in range(len(x) - 1):
            if 0 != float(x[j+1]) - float(x[j]):
                deltax = float(x[j+1]) - float(x[j])
                deltay = float(y[j+1]) - float(y[j])
                slope.append(float(deltay/deltax))
            else:
                slope.append("(infinite slope)")
        slope_output = ""
        for k in range(len(slope)):
            slope_output = slope_output + str(slope[k]) + "\n"
        position.output(slopename,slope_output)
    def write_intercept(self,interceptname):
        file_intercept = open(interceptname,"w")
        last_x = float(x[len(x) - 1])
        last_y = float(y[len(y) - 1])
        for i in range(len(x) - 1):
            intercept = last_y - last_x  * slope[i]
            intercept_list.append((str(intercept)))
        intercept_output = ""
        for k in range(len(slope)):
            intercept_output = intercept_output + str(intercept_list[k]) + "\n"
        position.output(interceptname,intercept_output)
class process:
    def __init__(self):
        pass
    def averaging(self,list_n,mode="t"):
        time = 0
        number = 0
        for i in list_n:
            number_test = float(i)
            if mode != "t":
                if number_test == 0:
                    pass
                else:
                    number = number + float(i)
                    time = time+1
            else:
                number = number + float(i)
                time = time+1
        edition = number / time
        return edition
class figure:
    def __init__(self):
        pass
    def square(self,mode,side=4,area=16):
        if mode == "s":
            return area ** 0.5
        elif mode == "a":
            return side*side
    def rectangle(self,length,wide):
        return length*wide
    def triangle(self,mode,bottom=4,high=4,area=8):
        if mode == "a":
            return bottom*high/2
        elif mode == "b":
            return area*2/high
        elif mode == "h":
            return area*2/bottom
    def circle(self,mode,radius=1,perimeter=6.28,area=3.14):
        if mode == "p":
            return radius*2*3.14
        elif mode == "a":
            return radius*radius*3.14
        elif mode == "rp":
            return perimeter/3.14/2
        elif mode == "ra":
            return (area/3.14)**0.5
def main():
    pass
if __name__ == '__main__':
    main()
