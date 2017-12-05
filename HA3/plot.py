from matplotlib import pyplot as plt
import sys

def plot(data, name):
    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    plt.plot(xs, ys, label=name) 

if __name__ == '__main__':
    plots = sys.argv[1:-1]
    pdf_name = sys.argv[-1]
    for i, name in enumerate(plots):
        with open(name, 'r') as f:
            lines = [line.strip().split(':') for line in f]
            data = list(map(lambda l: (float(l[0]), 1-float(l[1])), lines))[15:30]
            plot(data, name)
    plt.xlabel('X size')
    plt.ylabel('Breaking probability')
    plt.annotate('Meeting point', xy=(18, 0.5), xytext=(20, 0.51),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    plt.legend()
    plt.savefig(f'{pdf_name}.png')
