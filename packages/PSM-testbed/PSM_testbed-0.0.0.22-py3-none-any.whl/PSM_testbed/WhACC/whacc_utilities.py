class whacc_utils():
  def __init__():
    pass
  def group_consecutives(vals, step=1):
      run = []
      run_ind = []
      result = run
      result_ind = run_ind
      expect = None
      for k, v in enumerate(vals):
          if (v == expect):
              if not(np.isnan(v)):
                # print(v)
                # print(expect)
                run.append(v)
                run_ind.append(k)
          else:
              if not(np.isnan(v)):
                
                run = [v]
                run_ind = [k]
                result.append(run)
                result_ind.append(run_ind)
          expect = v + step
      # print(result)
      if result == []:
        pass
      elif result[0]==[]:
        result = result[1:]
        result_ind = result_ind[1:]
      return result, result_ind
  def get_h5s(base_dir):
    H5_file_list = []
    for path in Path(base_dir + '/').rglob('*.h5'):
      H5_file_list.append(str(path.parent) + '/'+ path.name)
    H5_file_list.sort()
    return H5_file_list
  def check_if_file_lists_match(H5_list_LAB, H5_list_IMG):
    for h5_LAB, h5_IMG in zip(H5_list_LAB, H5_list_IMG):
      try:
        assert h5_IMG.split('/')[-1] in h5_LAB
      except: 
        print('DO NOT CONTINUE --- some files do not match on your lists try again')
        assert(1==0)
    print('yay they all match!')


def get_model_list(model_save_dir):
  print('These are all the models to choose from...')
  model_2_load_all = glob.glob(model_save_dir+ '/*.ckpt')
  # print(*model_2_load_all, sep = '\n')
  _ = [print(str(i) + ' ' + k.split('/')[-1]) for i, k in enumerate(model_2_load_all)]
  return model_2_load_all


        
