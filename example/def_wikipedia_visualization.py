
# coding: utf-8

# ## Topic visualizations of a Poisson-Gamma DEF (size 50-25-10) trained on 1,000 wikipedia articles

# In[17]:


get_ipython().magic(u'pylab inline')
get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')

import pandas
import sys


# In[18]:


# specific imports
sys.path += ['../scripts/']
from utils import *
from pyx import *
from wand.image import Image as WImage
from def_visualization import *


# In[19]:


word_list = read_words('./vocab.dat')
experiment_dir = '../experiments/def_wikipedia_1434725288667'


# In[20]:


t = map(softrect, load_bin_model(experiment_dir + '/train_iter01000.model.bin'))


# In[21]:


W0_shape, W0_scale, z0_shape, z0_scale = t[:4]    
z1_shape, z1_scale, z2_shape, z2_scale = t[4:8]        
W1_shape, W1_scale, W2_shape, W2_scale = t[8:]
W0_mean = W0_shape * W0_scale
W1_mean = W1_shape * W1_scale
W2_mean = W2_shape * W2_scale


# #### First layer topics

# In[22]:


g = top_words(W0_mean, word_list, k=10, W_shape=W0_shape, show_weight=True)


# #### Second layer groups

# In[23]:


#For each group we show: 
# 1) Most probable words
# 2) Top topics per group including their probability
# 3) The top word per topic
g = top_groups(W1_mean, W0_mean, word_list, k1=3, k=10, show_weight=True)


# #### Third layer super groups

# In[24]:


g = top_supers(W2_mean, W1_mean, W0_mean, word_list, k2=5, k1=5, k=6, show_weight=True)

