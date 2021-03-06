#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''compute confusion matrix
labels.txt: contain labels name.
predict.txt: img predict_label true_label
'''
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
reload(sys)
sys.setdefaultencoding('utf-8')
#all data must tmp.txt
parser = argparse.ArgumentParser(description='confusion matrix')
parser.add_argument('label_name', help='label_name.txt: each line is name')
parser.add_argument('predict_file', help='predict result file: img predict_label true_label')
parser.add_argument('save_jpg', help='save jpg')
parser.add_argument('--norm', dest='norm to [0-1]', action='store_true')
parser.add_argument('--noNorm', dest='no norm', action='store_false')
parser.add_argument('font', help='font size, 5-20', type=int)
parser.set_defaults(norm=True)
args = parser.parse_args()

#load labels.
labels = []
file = open(args.label_name, 'r')
lines = file.readlines()
for line in lines:
	labels.append(line.strip())
file.close()

y_true = []
y_pred = []
#load true and predict labels.
file = open(args.predict_file, 'r')
lines = file.readlines()
for line in lines:
	y_true.append(int(line.split(" ")[2].strip()))
	y_pred.append(int(line.split(" ")[1].strip()))
file.close()
tick_marks = np.array(range(len(labels))) + 0.5
def plot_confusion_matrix(cm, title='Confusion Matrix', cmap = plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(y_true, y_pred)
#for i in range(0, len(cm)):
#	for j in range(0, len(cm[0])):
#		if(i == j):
#			print cm[i][j]
#			cm[i][j] -= 1
#print cm
np.set_printoptions(precision=2)
if(args.norm):
	cm = cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]
plt.figure(figsize=(12,8), dpi=600)
#set the fontsize of label.
for label in plt.gca().xaxis.get_ticklabels():
    label.set_fontsize(8)
for label in plt.gca().yaxis.get_ticklabels():
    label.set_fontsize(8)
#text portion
ind_array = np.arange(len(labels))
x, y = np.meshgrid(ind_array, ind_array)
print len(x), len(y)
for x_val, y_val in zip(x.flatten(), y.flatten()):
    c = cm[y_val][x_val]
   # if(y_val == x_val):
   # 	c = c - 1
    if(c >= 1):
    	plt.text(x_val, y_val, "%d" %(c,), color='red', fontsize=args.font, va='center', ha='center')
    elif(c >= 0.009):
       plt.text(x_val, y_val, "%0.2f" %(c,), color='red', fontsize=args.font, va='center', ha='center')
#offset the tick
plt.gca().set_xticks(tick_marks, minor=True)
plt.gca().set_yticks(tick_marks, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(True, which='minor', linestyle='-')
plt.gcf().subplots_adjust(bottom=0.15)

plot_confusion_matrix(cm, title='confusion matrix')
#show confusion matrix
#plt.show()
#save jpg
plt.savefig(args.save_jpg, dpi=600)
