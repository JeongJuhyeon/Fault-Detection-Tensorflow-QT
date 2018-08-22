selected_rois = []


def f():
    return


selected_rois.append(f)

line = "530_194_33_34_side1_screw10_4"
selected_rois.append(line.split('_')[:4])
selected_rois[-1].append('True')
selected_rois[-1].append('side1')
print(selected_rois)

l = []
sr = []
for roi in l:
    sr.append(roi)
if len(selected_rois[0]) == 0:
    selected_rois.pop()
