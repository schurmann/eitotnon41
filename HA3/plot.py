from matplotlib import pyplot as plt
import sys

def plot(data):
    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    plt.plot(xs, ys) 

if __name__ == '__main__':
    plots = sys.argv[1:-1]
    pdf_name = sys.argv[-1]
    for i, name in enumerate(plots):
        with open(name, 'r') as f:
            lines = [line.strip().split(':') for line in f]
            data = list(map(lambda l: (float(l[0]), float(l[1])), lines))
            plot(data)
    plt.savefig(f'{pdf_name}.pdf')
