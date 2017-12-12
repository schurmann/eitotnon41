from matplotlib import pyplot as plt
import sys

def plot(data, name):
    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    plt.plot(xs, ys, marker='o', label=name) 
    plt.xticks([1, 5, 10, 15, 20])

def annotate(data):
    index = 4
    plt.annotate(data[index][2], xy=(data[index][0], data[index][1]), xytext=(data[index][0] - 3, data[index][1] + 50), arrowprops=dict(facecolor='black', shrink=0.05),)
    index = 9
    plt.annotate(data[index][2], xy=(data[index][0], data[index][1]), xytext=(data[index][0], data[index][1] - 100), arrowprops=dict(facecolor='black', shrink=0.05),)
    index = 14
    plt.annotate(data[index][2], xy=(data[index][0], data[index][1]), xytext=(data[index][0], data[index][1] - 100), arrowprops=dict(facecolor='black', shrink=0.05),)
    index = 19
    plt.annotate(data[index][2], xy=(data[index][0], data[index][1]), xytext=(data[index][0] - 5, data[index][1] + 70), arrowprops=dict(facecolor='black', shrink=0.05),)

if __name__ == '__main__':
    plots = sys.argv[1:-1]
    pdf_name = sys.argv[-1]
    for i, name in enumerate(plots):
        with open(name, 'r') as f:
            lines = [line.strip().split(':') for line in f]
            data = [(int(line[0]) + 1, float(line[1])*1000, line[2]) for line in lines]
            plot(data, 'chrcmp execution time')
    annotate(data)
    plt.xlabel('Iteration')
    plt.ylabel('Average time (ms)')
    plt.legend()
    plt.savefig(f'{pdf_name}.png')
