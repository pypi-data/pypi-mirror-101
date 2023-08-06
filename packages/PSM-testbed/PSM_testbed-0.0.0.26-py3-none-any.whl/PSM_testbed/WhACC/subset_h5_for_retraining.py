
import copy 
import h5py
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt



class subset_H5_generator():
  def __init__():
    pass
  def save_subset_h5_file(file_save, h5_IMG, LABELS, all_inds, retrain_H5_info):
    try:
      os.remove(file_save)
    except:
      pass
    with h5py.File(h5_IMG, 'r') as F:
      images = np.asarray([F['images'][k] for k in all_inds])
      labels = np.asarray([LABELS[k] for k in all_inds.astype('int')])
      in_range = np.asarray([F['in_range'][k] for k in all_inds])
      with h5py.File(file_save, 'w') as hf: # auto close in case of failure 
        hf.create_dataset('images', data=images)
        hf.create_dataset('labels', data=labels)
        hf.create_dataset('in_range', data = in_range)
        hf.create_dataset('all_inds', data = all_inds)
        hf.create_dataset('retrain_H5_info', data = [str(retrain_H5_info).encode("ascii", "ignore")])
        hf.close()
        print('finished with '+ file_save)
  def plot_pole_grab(im_stack, retrain_H5_info = None, height_stack_to_plot = 1):
    # retrain_H5_info will just resize the figure to be easy to see if you use 
    #a number that is very different from 20 samples per chunk 
    if retrain_H5_info is None:
      plt.figure(figsize=[40, 5*height_stack_to_plot])
      _ = plt.imshow(im_stack)
    else:
      width_plt = retrain_H5_info['num_high_prob_past_max_y']+retrain_H5_info['seg_len_look_dist']*2
      plt.figure(figsize=[width_plt, 5*height_stack_to_plot])
      _ = plt.imshow(im_stack)
  def get_example_segments(L2,
                          seg_len_look_dist = 10, 
                          min_y = .2,
                          max_y = .8,
                          num_to_sample = 40,
                          num_high_prob_past_max_y = 10,
                          add_frames_from_x1_to_x2 = [0, 50]):
    segs = np.where(L2>min_y)[0]
    chunks, chunk_inds = group_consecutives(segs, step=1)   
    good_up_segs = []
    good_down_segs = []
    for k in chunks:
      try:
        up = L2[k[0]-seg_len_look_dist:k[0]]
        down = L2[k[-1]-1:k[-1]+seg_len_look_dist-1]
        assert(len(up) == seg_len_look_dist)
        assert(len(down) == seg_len_look_dist)
        good_up_segs.append(np.min(up)<=min_y)
        good_down_segs.append(np.min(down)<=min_y)
      except: # if we are on the edges just toss these 
        good_up_segs.append(False)
        good_down_segs.append(False)
    good_up_segs = np.where(good_up_segs)[0]    
    good_down_segs = np.where(good_down_segs)[0]    
    a = np.random.choice(good_up_segs, size = num_to_sample, replace = False)
    up_start = [chunks[k][0]+1 for k in a] 

    a = np.random.choice(good_down_segs, size = num_to_sample, replace = False)
    down_start = [chunks[k][-1]+1 for k in a]

    all_inds = np.asarray([])
    onset_list = []
    offset_list = []
    for k1, k2 in zip(up_start, down_start):
      onset_list.append(np.asarray(range(k1-seg_len_look_dist,k1+num_high_prob_past_max_y)))
      all_inds = np.concatenate((all_inds, onset_list[-1]))
      offset_list.append(np.asarray(range(k2-1-num_high_prob_past_max_y, k2-1+seg_len_look_dist)))
      all_inds = np.concatenate((all_inds, offset_list[-1]))
    retrain_H5_info = {'seg_len_look_dist': seg_len_look_dist , 
                        'min_y': min_y , 
                        'max_y':max_y  , 
                        'num_to_sample': num_to_sample , 
                        'num_high_prob_past_max_y':  num_high_prob_past_max_y}
    inds_2_add = np.linspace(0, 50-1, ).astype(int)
    all_inds = np.concatenate((np.float64(inds_2_add), all_inds))

    return all_inds, onset_list, offset_list, retrain_H5_info

  def get_img_stack(h5_IMG, inds, h5_IMG_key = 'images'):
    im_stack = None
    for k in inds:
      with h5py.File(h5_IMG, 'r') as h:
        x = np.asarray(h[h5_IMG_key][k])
        if im_stack is None:
          im_stack = x
        else:
          im_stack = np.hstack((im_stack, x))
    return im_stack


  def plot_all_onset_or_offset(up_or_down_list, retrain_H5_info = None):
    for i, k in enumerate(up_or_down_list):
      if i == 0:
        im_stack = get_img_stack(h5_IMG, k)
      else:
        im_stack = np.vstack((im_stack, get_img_stack(h5_IMG, k)))
    plot_pole_grab(im_stack, retrain_H5_info, len(up_or_down_list))
