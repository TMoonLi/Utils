import argparse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

test_interval = 100
display = 20
jump = 5

def print_loss():
		files = os.listdir('./')
		for afile in files:
			#print(os.path.splitext(afile)[1])
			if os.path.splitext(afile)[1] == '.log':
				f = open(afile, 'r')
				test_loss = []
				test_loss2 = []
				window = []
				count = 0
				for line in f:
					begin = line.find('Test loss')
					if begin >= 0:
						if count < jump:
							count += 1
							continue
						test_loss2.append(float(line[begin + 11:-1]))
						if len(window) < 10:
							test_loss.append(float(line[begin + 11:-1]))
							window.append(float(line[begin + 11:-1]))
						else:
							del window[0]
							window.append(float(line[begin + 11:-1]))
							# print(window)
							loss = 0
							for num in window:
								loss += num
							test_loss.append(loss/10)
				xold = range(jump*test_interval,(len(test_loss) + jump)*test_interval,test_interval)
				# print(xold)

				# print(len(xold))
				# print(len(test_loss))
				plt.plot(np.array(xold),np.array(test_loss), 'b', lw=1.5, label = 'test_smooth')
				plt.plot(np.array(xold),np.array(test_loss2), 'g', lw=0.5, label = 'test')
				# plt.grid(True)
				# plt.minorticks_on()
				# plt.savefig('loss_pic/test_'+os.path.splitext(afile)[0]+'.png')
				# plt.clf()

				f.close()
				f = open(afile, 'r')
				train_loss = []
				time = 0
				count = 0
				b_lr = ''
				for line in f:
					begin = line.find('smoothed_loss')
					if begin >= 0:
						if count < jump*test_interval/display:
							count += 1
							continue
						train_loss.append(float(line[begin + 16:-1]))

					begin = line.find('Speed:')
					if begin >= 0:
						time += float(line[begin+7 : begin+9])

					if b_lr == '':
						begin = line.find('lr = ')
						if begin >= 0:
							b_lr = line[begin + 5:-1]
				xold = range(jump*test_interval,(len(train_loss) + jump*test_interval/display)*display,display)
				plt.plot(np.array(xold),np.array(train_loss), 'r', lw=1.5, label = 'train')
				plt.grid(True)
				plt.minorticks_on()
				plt.legend()
				if train_loss[-1] != train_loss[-1]:
					plt.text(xold[len(xold)/4], 0, "base_lr: " + b_lr + "  time: " + str(time*20/3600) + ' hour', size = 15, color = "r", style = "italic", weight = "light")
					# plt.text(xold[len(xold)/2], 0, "time: " + str(time*20/3600) + ' hour', size = 15, color = "r", style = "italic", weight = "light")
				else:
					plt.text(xold[len(xold)/4], train_loss[10], "base_lr: " + b_lr + "  time: " + str(time*20/3600) + ' hour', size = 15, color = "r", style = "italic", weight = "light")
					# plt.text(xold[len(xold)/2], train_loss[10], "time: " + str(time*20/3600) + ' hour', size  = 15, color = "r", style = "italic", weight = "light")
				plt.savefig('loss_pic/'+os.path.splitext(afile)[0]+'.png')
				plt.clf()
				

def main():
   # description = ('Parse a Caffe training log into .jpg '
   #                'containing testing information')
   # parser = argparse.ArgumentParser(description=description)

   # parser.add_argument('logfile_path',
   #                     help='Path to log file')

   # parser.add_argument('output_dir',
   #                     help='Directory in which to place output CSV files')

   # args = parser.parse_args()

   # print_loss(args.logfile_path,args.output_dir)
	 print_loss()


if __name__ == '__main__':
    main()

