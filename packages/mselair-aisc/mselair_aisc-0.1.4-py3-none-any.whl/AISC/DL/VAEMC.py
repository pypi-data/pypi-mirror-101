# Copyright 2020-present, Mayo Clinic Department of Neurology - Laboratory of Bioelectronics Neurophysiology and Engineering
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import pickle
import matplotlib.pyplot as plt

#import AISC
from AISC import DELIMITER
import numpy as np
from tqdm import tqdm
from copy import deepcopy
from dateutil import tz
#from umap import UMAP
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics import cohen_kappa_score, average_precision_score, f1_score
from scipy.stats import multivariate_normal, gaussian_kde
from sklearn.feature_selection import RFE, RFECV
from sklearn.svm import SVR
from sklearn import preprocessing

from hypnogram.io import load_CyberPSG
from hypnogram.utils import create_day_indexes, time_to_timezone, time_to_timestamp, tile_annotations, create_duration, filter_by_duration
#from cloud_tools.db import SessionFinder, SleepClassificationModelDBHandler, SystemStateLoader
#from cloud_tools.mef import MefClient

from datetime import datetime

from AISC.utils.feature import augment_features, print_classification_scores, get_classification_scores, replace_annotations
from AISC.utils.signal import unify_sampling_frequency, get_datarate, buffer
from AISC.modules.feature import ZScoreModule, LogModule, FeatureAugmentorModule, Log10Module
from AISC.FeatureExtractor.FeatureExtractor import SleepSpectralFeatureExtractor
from AISC.models import KDEBayesianModel, KDEBayesianCausalModel, MVGaussBayesianModel, MVGaussBayesianCausalModel
from AISC.utils.stats import kl_divergence_nonparametric


from AISC.models import SleepStageProbabilityMarkovChainFilter
from itertools import permutations
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score


from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
#from umap import UMAP
import scipy.signal as signal
from AISC.utils.feature import zscore
from mef_tools.io import MefReader

import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
#from umap import UMAP
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes, zscore
import scipy.signal as signal
#from umap import UMAP
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes
from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
#from umap import UMAP
import scipy.signal as signal
from AISC.utils.feature import zscore

import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes, zscore
import scipy.signal as signal

from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes
from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
import scipy.signal as signal
from AISC.utils.feature import zscore
from tqdm import tqdm
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics import cohen_kappa_score, average_precision_score, f1_score
from scipy.stats import multivariate_normal, gaussian_kde
from sklearn.feature_selection import RFE, RFECV
from sklearn.svm import SVR
from sklearn import preprocessing
from AISC.utils.files import get_files
from scipy.io import loadmat
import tifffile
from AISC.utils.files import get_folders
import torch.nn.functional as F
import os


import pickle
import matplotlib.pyplot as plt

#import AISC
from AISC import DELIMITER
import numpy as np
from tqdm import tqdm
from copy import deepcopy
from dateutil import tz
#from umap import UMAP
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics import cohen_kappa_score, average_precision_score, f1_score
from scipy.stats import multivariate_normal, gaussian_kde
from sklearn.feature_selection import RFE, RFECV
from sklearn.svm import SVR
from sklearn import preprocessing

from hypnogram.io import load_CyberPSG
from hypnogram.utils import create_day_indexes, time_to_timezone, time_to_timestamp, tile_annotations, create_duration, filter_by_duration
#from cloud_tools.db import SessionFinder, SleepClassificationModelDBHandler, SystemStateLoader
#from cloud_tools.mef import MefClient

from datetime import datetime

from AISC.utils.feature import augment_features, print_classification_scores, get_classification_scores, replace_annotations
from AISC.utils.signal import unify_sampling_frequency, get_datarate, buffer
from AISC.modules.feature import ZScoreModule, LogModule, FeatureAugmentorModule, Log10Module
from AISC.FeatureExtractor.FeatureExtractor import SleepSpectralFeatureExtractor
from AISC.models import KDEBayesianModel, KDEBayesianCausalModel, MVGaussBayesianModel, MVGaussBayesianCausalModel
from AISC.utils.stats import kl_divergence_nonparametric


from AISC.models import SleepStageProbabilityMarkovChainFilter
from itertools import permutations
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score


from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
#from umap import UMAP
import scipy.signal as signal
from AISC.utils.feature import zscore
from mef_tools.io import MefReader

import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
#from umap import UMAP
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes, zscore
import scipy.signal as signal
#from umap import UMAP
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes
from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
#from umap import UMAP
import scipy.signal as signal
from AISC.utils.feature import zscore

import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes, zscore
import scipy.signal as signal

from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from AISC.utils.feature import balance_classes
from AISC.utils.signal import PSD, LowFrequencyFilter
from AISC.utils.feature import remove_samples
import scipy.signal as signal
from AISC.utils.feature import zscore
from tqdm import tqdm
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics import cohen_kappa_score, average_precision_score, f1_score
from scipy.stats import multivariate_normal, gaussian_kde
from sklearn.feature_selection import RFE, RFECV
from sklearn.svm import SVR
from sklearn import preprocessing
from AISC.utils.files import get_files, create_folder
from scipy.io import loadmat
import tifffile
from AISC.utils.files import get_folders
import torch.nn.functional as F
import shutil
import time

import os

import yaml
from AISC.utils.types import ObjDict, DicToObj, DictToObjDict


def config(path_config):
    with open(path_config, 'r') as stream:
        Cfg = yaml.safe_load(stream)
    return DictToObjDict(Cfg)

class PSGDataset(Dataset):
    def __init__(self, path, channels_to_use=None):
        self.channels_to_use = channels_to_use
        self.states = ['AWAKE', 'N1', 'N2', 'N3', 'REM']
        DATA = {}
        for subj in get_folders(path):
            pth_pat = os.path.join(path, subj)
            path_signals = os.path.join(pth_pat, 'signals')
            #path_noise = os.path.join(pth_pat, 'noise')
            path_metadata = os.path.join(pth_pat, 'meta.mat')
            if os.path.isfile(path_metadata):
                metadata = loadmat(path_metadata)

                signal_files = get_files(path_signals)
                #noise_files = get_files(path_noise)
                metadata['signal'] = dict([(pth.split(DELIMITER)[-1][:-4], pth) for pth in signal_files])

                #metadata['noise'] = noise_files
                if signal_files.__len__() > 0:
                    DATA[subj] = metadata

        self.DATA = DATA
        self.keys = list(self.DATA.keys())

        self._unique_channels = np.unique([list(subj['signal']) for k, subj in self.DATA.items()])
        self._channels = [np.array(list(subj['signal'])) for k, subj in self.DATA.items()]

        if self.channels_to_use is None:
            self.channels_to_use = self._unique_channels

        self.max_length = []
        print('Determining max len of the dataset')
        for k in tqdm(range(self.__len__())):
            x = self.get_sample(k)
            self.max_length += [x['ySxx'].__len__()]
        self.max_length = np.max(self.max_length)



    @property
    def channels(self):
        return np.unique(np.concatenate(self._channels))
        #return #np.array(list(self._signal_channels.keys()))

    def __len__(self):
        return self.DATA.__len__()

    def __getitem__(self, index):
        x = self.get_sample(index)
        len_ = x['ySxx'].__len__()

        Sxx = np.zeros((x['Sxx'].shape[0], self.max_length))
        Sxx[:, :len_] = x['Sxx']

        ySxx = np.zeros(self.max_length) - 1
        ySxx[:len_] = x['ySxx']

        x['Sxx'] = Sxx
        x['ySxx'] = ySxx
        x['len'] = len_
        return x


    def get_sample(self, index):
        dat = self.DATA[self.keys[index]]
        channels = np.array([ch for ch in self._channels[index] if ch in self.channels_to_use])
        ch = np.random.choice(channels)
        pth = dat['signal'][ch]

        Sxx = tifffile.imread(pth).astype(np.float) / 1e3
        ySxx = dat['ySxx']

        t = dat['t'].squeeze()
        f = dat['f'].squeeze()
        ySxx = np.array([y.replace(' ', '') for y in ySxx])
        ySxx[ySxx == 'WAKE'] = 'AWAKE'
        ySxx = self.encode_labels(ySxx)

        return {
            'Sxx': Sxx,
            'ySxx': ySxx,
            'f': f,
            't': t,
            'channel': ch
        }

    def len_validation(self):
        l = 0
        for k, item in self.DATA.items():
            l += item['signal'].__len__()
        return l


    def getitem_validation(self, index):
        offset = 0
        for k, item in self.DATA.items():
            l = item['signal'].__len__()
            e = offset + l
            if index >= offset and index < e:
                files = item['signal']
                file = files[index-offset]
                Sxx = tifffile.imread(file).astype(np.float) / 1e3
                ySxx = item['ySxx']
                ySxx = np.array([y.replace(' ', '') for y in ySxx])
                return Sxx, ySxx
            offset = e
        raise AssertionError('Index higher than dataset sequence length')

    def encode_labels(self, y):
        y = np.array(y)
        yy = np.zeros(y.__len__()) - 1
        for idx, s in enumerate(self.states):
            yy[y==s] = idx
        return yy

    def decode_labels(self, y):
        y = np.array(y)
        yy = np.array(['']*y.shape[0], dtype='<U10')
        for idx, s in enumerate(self.states):
            yy[y==idx] = s
        return yy

class ResLayer_K3_EncDec(nn.Module):
    def __init__(self, n=16):
        super(ResLayer_K3_EncDec, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=n, out_channels=n, kernel_size=3, stride=1, dilation=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=n, out_channels=n, kernel_size=3, stride=1, dilation=1, padding=1)


        self.conv1_up = nn.ConvTranspose2d(in_channels=n, out_channels=n, kernel_size=3, stride=1, dilation=1, padding=1)
        self.conv2_up = nn.ConvTranspose2d(in_channels=n, out_channels=n, kernel_size=3, stride=1, dilation=1, padding=1)


    def encode(self, x):
        xe = self.conv1(x)
        xe = F.relu(xe)
        xe = self.conv2(xe)
        xe = F.relu(xe + x)
        return xe

    def decode(self, x):
        xe = self.conv1_up(x)
        xe = F.relu(xe)
        xe = self.conv2_up(xe)
        xe = F.relu(xe + x)
        return xe

class GRUVariantialSleepEncoder(nn.Module):
    def __init__(self, cfg):
        super(GRUVariantialSleepEncoder, self).__init__()
        self.dropout_rate = cfg.MODEL.TRAIN.DROPOUT
        filters_n = cfg.MODEL.ARCHITECTURE.N_FILTERS
        gru_n = cfg.MODEL.ARCHITECTURE.GRU_NEURONS_N
        embedded_n = cfg.MODEL.ARCHITECTURE.EMBEDDED_FEATURES_N
        clf_lin_n = cfg.MODEL.ARCHITECTURE.CLF_LINEAR_N

        #self.dropout = nn.Dropout(dropout_rate)
        self.lrelu = nn.LeakyReLU(0.1)
        self.softmax = nn.Softmax()

        self.conv1 = nn.Conv2d(in_channels=2, out_channels=filters_n, kernel_size=(6, 3), stride=(3, 1), padding=(2, 1)) # 67

        self.Res1 = ResLayer_K3_EncDec(filters_n)
        self.Res2 = ResLayer_K3_EncDec(filters_n)

        self.gru = nn.GRU(int(67*filters_n), hidden_size=gru_n, num_layers=1, bidirectional=False)

        self.fc1_mu = nn.Linear(gru_n, embedded_n)
        self.fc1_var = nn.Linear(gru_n, embedded_n)

        self.fc2 = nn.Linear(embedded_n, clf_lin_n)
        self.fc3 = nn.Linear(clf_lin_n, 5)

        self.fc2_1 = nn.Linear(embedded_n, clf_lin_n)
        self.fc3_1 = nn.Linear(clf_lin_n, 5)

        self.fc2_2 = nn.Linear(embedded_n, clf_lin_n)
        self.fc3_2 = nn.Linear(clf_lin_n, 5)

        self.fc2_3 = nn.Linear(embedded_n, clf_lin_n)
        self.fc3_3 = nn.Linear(clf_lin_n, 5)

        self.up_fc1 = nn.Linear(embedded_n, gru_n)
        self.up_gru = nn.GRU(gru_n, hidden_size=gru_n, num_layers=1, bidirectional=False)
        self.up_fc_c = nn.Linear(gru_n, int(67*filters_n))

        self.uconv1 = nn.ConvTranspose2d(in_channels=filters_n, out_channels=2, kernel_size=(6, 3), stride=(3, 1), padding=(2, 1))

    def encode(self, x):
        #device = self.state_dict()[list(self.state_dict().keys())[0]].device
        ### THIS IS WHAT SHOULD BE FIXED. LET'S MAKE THE CONVERSION BEFORE BECAUSE OF THIS AND CROPPING THE DATA IN COLLATE_FN
        #print(x_dict)
        #x = x_dict['Sxx']
        #x = x.to(device)
        #x_dict['Sxx'] = x

        #x = self.dropout(x)
        x = self.conv1(x)
        x = self.lrelu(x)

        x = self.Res1.encode(x)
        x = self.Res2.encode(x)

        x = x.view(x.shape[0], -1, x.shape[-1])
        x = torch.transpose(x, 0, 1)
        x = torch.transpose(x, 0, 2)

        h0 = torch.zeros(1, x.shape[1], 32).float().to(x.device)
        self.gru.flatten_parameters()
        xe1, hn = self.gru(x, h0)

        mu = self.fc1_mu(xe1)
        logvar = self.fc1_var(xe1)

        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        x_ = mu + eps * std



        #outp = {
            #'mu': mu.transpose(0, 1),
            #'logvar': logvar.transpose(0, 1),
            #'x': x_.transpose(0, 1),
            #'hn': hn
        #}
        #x_dict.update(outp)
        #return x_dict
        return mu.transpose(0, 1), logvar.transpose(0, 1), x_.transpose(0, 1), hn

    def decode(self, x, hn):
        #x_ = x['x']
        #hn = x['hn']
        nbatch = x.shape[0]

        xe1u = self.up_fc1(x)
        xe1u = self.lrelu(xe1u)
        xe1u = torch.transpose(xe1u, 0, 1)

        self.up_gru.flatten_parameters()
        xgu, hnu = self.up_gru(xe1u, hn)
        xgu = self.up_fc_c(xgu)
        xgu = torch.transpose(xgu, 0, 1)
        xgu = torch.transpose(xgu, 1, 2)
        xgu = xgu.view(nbatch, 32, 67, xgu.shape[-1])

        xgu = self.Res2.decode(xgu)
        xgu = self.Res1.decode(xgu)

        xoutp = self.uconv1(xgu)
        xoutp = F.relu(xoutp)
        #x['rSxx'] = xoutp
        return xoutp

    def classify(self, x):
        #x_ = x['x']
        x1 = self.fc2_1(x)
        x1 = self.lrelu(x1)
        x1 = self.fc3_1(x1)

        x2 = self.fc2_2(x)
        x2 = self.lrelu(x2)
        x2 = self.fc3_2(x2)

        x3 = self.fc2_3(x)
        x3 = self.lrelu(x3)
        x3 = self.fc3_3(x3)
        #x['scores'] = x
        return x1, x2, x3

    def forward(self, x):
        #x =
        mu, logvar, x_, hn = self.encode(x)
        x = self.classify(x_)
        xrec = self.decode(x_, hn)
        return mu, logvar, x_, x, xrec

    #def inference(self, x):
        #x = self.encode(x)
        #x = self.classify(x)
        #return x

    def _format(self, x):
        x[x==0] = np.nan
        x2 = self.normalize(x, 2)
        x3 = self.normalize(x, 3)

        #x2[xbl] = 0
        #x3[xbl] = 0
        x = torch.cat((x2, x3), dim=1)
        x = torch.nan_to_num(x, nan=0)
        return x

    def format_single(self, x):
        sd = self.state_dict()
        k = list(sd.keys())[0]
        device = sd[k].device
        Sxx = x['Sxx']
        ySxx = x['ySxx']

        Sxx = torch.tensor(Sxx).reshape(1, 1, *Sxx.shape).float().to(device)
        Sxx = self._format(Sxx)

        ySxx = torch.tensor(ySxx).reshape(1, *ySxx.shape).long().to(device)
        x['Sxx'] = Sxx
        x['ySxx'] = ySxx
        x['channel'] = np.array([x['channel']])
        return x

    def normalize(self, x, ax):
        q99 = torch.nanquantile(x, 0.99, axis=ax, keepdims=True)
        q01 = torch.nanquantile(x, 0.01, axis=ax, keepdims=True)
        den = (q99-q01)
        den[den == 0] = 1
        x = (x - q01) / den
        x[x<0] = 0
        return x

    def get_losses(self, x):
        loss_KL = self.loss_KL_Divergence(x)
        loss_rec = self.loss_reconstruction(x)
        loss_crossentropy = self.loss_crossentropy(x)

        return {
            'loss_KL_Div': loss_KL,
            'loss_crossentropy': loss_crossentropy,
            'loss_reconstruction': loss_rec
        }

    def loss_KL_Divergence(self, x):
        return -0.5 * torch.mean(1 + x['logvar'] - x['mu'].pow(2) - x['logvar'].exp())

    def loss_crossentropy(self, x):
        x1, x2, x3 = x['scores']
        y = x['ySxx'].to(x1.device)

        loss = []
        for x1_, x2_, x3_, y_, ch in zip(x1, x2, x3, y, x['channel']):
            x1_ = x1_[y_ >= 0].squeeze()
            x2_ = x2_[y_ >= 0].squeeze()
            x3_ = x3_[y_ >= 0].squeeze()
            y_ = y_[y_ >= 0].squeeze()

            if ch in ['c3m2', 'c4m1']:
                x__ = x1_
            if ch in ['f3m2', 'f4m1']:
                x__ = x2_
            if ch in ['o1m2', 'o2m1']:
                x__ = x3_

            loss1 = F.cross_entropy(x__, y_) / 2
            #loss += [loss1]

            x__ = x__[y_ != 1]
            y_ = y_[y_ != 1]
            y_[y_ == 0] = 0
            y_[y_ > 1] -= 1

            loss2 = F.cross_entropy(x__[:, [0, 2, 3, 4]], y_) / 2

            loss += [loss1 + loss2]
        return torch.stack(loss).mean()

    def loss_reconstruction(self, x):
        if 'Sxx_orig' in x.keys():
            Sxx = x['Sxx_orig']
        else:
            Sxx = x['Sxx']
        rSxx = x['rSxx']
        return F.mse_loss(rSxx[Sxx != 0], Sxx[Sxx != 0])

    @staticmethod
    def classification_scores(x):
        y = x['ySxx']#.squeeze().detach().cpu().numpy()
        #yy = x['scores'].argmax(axis=2).squeeze().detach().cpu().numpy()
        x1, x2, x3 = x['scores']



        scores = {
            'kappa': [],
            'f1_0': [],
            'f1_1': [],
            'f1_2': [],
            'f1_3': [],
            'f1_4': [],
        }
        for x1_, x2_, x3_, y_, ch in zip(x1, x2, x3, y, x['channel']):
            x1_ = x1_[y_ >= 0].squeeze()
            x2_ = x2_[y_ >= 0].squeeze()
            x3_ = x3_[y_ >= 0].squeeze()
            y_ = y_[y_ >= 0].squeeze().squeeze().detach().cpu().numpy()

            if ch in ['c3m2', 'c4m1']:
                try:
                    yy1 = x1_.argmax(axis=-1).squeeze().detach().cpu().numpy()
                    scores['kappa'] += [cohen_kappa_score(y_, yy1)]
                    for k in range(5):
                        scores['f1_' + str(k)] += [f1_score(y_==k, yy1==k)]
                except: pass

            if ch in ['f3m2', 'f4m1']:
                try:
                    yy2 = x2_.argmax(axis=-1).squeeze().detach().cpu().numpy()
                    scores['kappa'] += [cohen_kappa_score(y_, yy2)]
                    for k in range(5):
                        scores['f1_' + str(k)] += [f1_score(y_==k, yy2==k)]
                except: pass

            if ch in ['o1m2', 'o2m1']:
                try:
                    yy3 = x3_.argmax(axis=-1).squeeze().detach().cpu().numpy()
                    scores['kappa'] += [cohen_kappa_score(y_, yy3)]
                    for k in range(5):
                        scores['f1_' + str(k)] += [f1_score(y_==k, yy3==k)]
                except: pass

        for k in scores.keys():
            scores[k] = np.nanmean(scores[k])

        #for k in range(5):
            #scores['f1_' + str(k)] = f1_score(y==k, yy==k)
        return scores

def my_collate(batch):
    #data = []

    Sxx = []
    ySxx = []
    len_ = []
    channels = []

    for item in batch:
        Sxx += [
            torch.tensor(item['Sxx']).float().view(1, 1, *item['Sxx'].shape)
        ]
        ySxx += [
            torch.tensor(item['ySxx']).float().view(1, *item['ySxx'].shape)
        ]
        len_ += [item['len']]
        channels += [item['channel']]

    Sxx = torch.cat(Sxx, dim=0)
    ySxx = torch.cat(ySxx, dim=0)
    len_ = torch.tensor(len_)
    channels = np.array(channels)
    return {
        'Sxx': Sxx,
        'ySxx': ySxx,
        'len': len_,
        'channel': channels
    }

        # print(item.keys())
        #data += [{
        #    'Sxx': torch.tensor(item['Sxx']).float(),
        #    'ySxx': torch.tensor(item['ySxx']).long()
        #}]
    #return data


class Trainer:
    def __init__(self, path_config, model_path=None):
        self.cfg = config(path_config)
        self.DatasetTrain = PSGDataset(self.cfg.PATH_TRAIN)
        self.DatasetValidation = PSGDataset(self.cfg.PATH_VALIDATION)
        self.DatasetTest = PSGDataset(self.cfg.PATH_TEST)

        self.min_training_length = int(self.cfg.MODEL.TRAIN.MIN_MAX_DATA_LENGTH.split(',')[0])
        self.max_training_length = int(self.cfg.MODEL.TRAIN.MIN_MAX_DATA_LENGTH.split(',')[1])


        self.path_report = os.path.join(self.cfg.MODEL.TRAIN.PATH_REPORT, datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        self.path_report_models = os.path.join(self.path_report, 'Models')
        self.path_report_images = os.path.join(self.path_report, 'Images')
        self.path_report_config = os.path.join(self.path_report, 'config.yaml')
        self.path_report_losses = os.path.join(self.path_report, 'losses.csv')
        self.path_report_losses_validation = os.path.join(self.path_report, 'losses_val.csv')


        create_folder(self.path_report)
        create_folder(self.path_report_models)
        create_folder(self.path_report_images)
        shutil.copyfile(path_config, self.path_report_config)

        with open(self.path_report_losses, 'w') as f:
            f.write('Epoch, lr, loss_KL, loss_CE, loss_REC, loss, Kappa, F1_0, F1_1, F1_2, F1_3, F1_4\n')

        with open(self.path_report_losses_validation, 'w') as f:
            f.write('Epoch, lr, loss_KL, loss_CE, loss_REC, loss, Kappa, F1_0, F1_1, F1_2, F1_3, F1_4\n')

        self.save_model_freq = self.cfg.MODEL.TRAIN.SAVE_MODEL_EPOCH
        self.save_report_freq = self.cfg.MODEL.TRAIN.SAVE_REPORT_EPOCH

        self.GPUs = self.cfg.MODEL.TRAIN.GPU
        self.num_gpus = self.GPUs.__len__()
        self.minibatchsize = int(self.cfg.MODEL.TRAIN.BATCH_SIZE)

        self.lr = self.cfg.MODEL.TRAIN.BASE_LR
        self.gamma = self.cfg.MODEL.TRAIN.LR_DECAY
        self.lr_decay = self.cfg.MODEL.TRAIN.LR_DECAY_STEPS

        self.epochs = self.cfg.MODEL.TRAIN.MAX_EPOCHS

        self.lossKL_weight = self.cfg.MODEL.TRAIN.LOSS_KL_DIVERGENCE_WEIGHT
        self.lossMSE_weight = self.cfg.MODEL.TRAIN.LOSS_RECONSTRUCTION_WEIGHT
        self.lossCE_weight = self.cfg.MODEL.TRAIN.LOSS_CROSSENTROPY_WEIGHT

        self.current_epoch = 0
        self.epoch_list = []
        self.lossKL_list = []
        self.lossMSE_list = []
        self.loss_list = []
        self.device = self.GPUs[0]


        self.model = GRUVariantialSleepEncoder(self.cfg)

        def init_weights(x):
            pass
            #if type(x) == torch.nn.Conv2d:
                #torch.nn.init.xavier_uniform(x.weight)
                #torch.nn.init.orthogonal_(x.weight)
                #x.bias.data.fill_(0.00)

        self.model.apply(init_weights)


        if type(model_path) != type(None):
            self.model.cuda(self.device)
            self.model.load_state_dict(torch.load(model_path))
            self.model.train()
            self.current_epoch = int(model_path.split(DELIMITER)[-1].split('_')[-1]) + 1





        #self.DLoaderTrain = DataLoader(self.DatasetTrain, batch_size=self.minibatchsize, shuffle=True, num_workers=self.cfg.DATASET.CPU_COUNT_LOADER, drop_last=False, collate_fn=my_collate)
        self.DLoaderTrain = DataLoader(self.DatasetTrain, batch_size=self.minibatchsize, shuffle=True, drop_last=False,
                                       collate_fn=my_collate)
        # self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.alpha)

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(self.optimizer, milestones=self.lr_decay, gamma=self.gamma)

        self.model.cuda(self.device)

        if self.GPUs.__len__() > 1:
            self.model_parallel = torch.nn.DataParallel(self.model, device_ids=self.GPUs)
        else:
            self.model_parallel = None

    def forward(self, x):
        self.optimizer.zero_grad()
        return self.model(x)

    def forward_parallel(self, x):
        self.optimizer.zero_grad()
        return self.model_parallel(x)



    def do_epoch(self):
        t = time.time()
        e_losses = []


        print('----------------------------------')
        print('VAE Epoch ' + str(self.current_epoch))


        self.model.train()
        for k, X in enumerate(tqdm(self.DLoaderTrain)):
            min_ = self.min_training_length
            max_ = self.max_training_length
            len_ = X['len']

            if max_ > len_.min():
                max_ = len_.min()

            segment = np.random.randint(min_, max_)
            temp_sxx = torch.zeros_like(X['Sxx'])[:, :, :, :segment]
            temp_ysxx = torch.zeros_like( X['ySxx'])[:, :segment]

            for idx_ in range(len_.__len__()):
                start = np.random.randint(len_[idx_] - segment)
                #X['Sxx'] = X['Sxx'][idx_, :, :, start:start + segment]
                #X['ySxx'] = X['ySxx'][idx_, start:start + segment]
                #X['Sxx'][idx_, :, :, :segment] = X['Sxx'][idx_, :, :, start:start + segment].clone()
                #X['ySxx'][idx_, :segment] = X['ySxx'][idx_, start:start + segment].clone()
                temp_sxx[idx_, :, :, :] = X['Sxx'][idx_, :, :, start:start + segment]
                temp_sxx_orig = temp_sxx.clone()
                dp = self.model.dropout_rate * np.random.rand()
                drop_band = 5
                min_d = drop_band
                max_d = temp_sxx.shape[-2] - drop_band
                for c in np.random.randint(min_d, max_d, int(np.round(temp_sxx.shape[-2]/10*dp))):
                    to_erase = np.arange(c-drop_band, c+drop_band)
                    temp_sxx[idx_, :, to_erase, :] = 0
                temp_ysxx[idx_, :] = X['ySxx'][idx_, start:start + segment]



                #X['Sxx'] = X['Sxx'][:, :, :, start:start + segment]
                #X['ySxx'] = X['ySxx'][:, start:start + segment]
            #X['Sxx'] = X['Sxx'][:, :, :, :segment]
            #X['ySxx'] = X['ySxx'][:, :segment]
            #temp_sxx = torch.tensor(temp_sxx).cuda(self.device).float()
            #temp_ysxx = torch.tensor(temp_ysxx).cuda(self.device).long()

            X['Sxx'] = temp_sxx
            X['Sxx_orig'] = temp_sxx_orig
            X['ySxx'] = temp_ysxx
            X['Sxx'] = self.model._format(X['Sxx'])
            X['Sxx_orig'] = self.model._format(X['Sxx_orig'])

            X['Sxx'] = X['Sxx'].cuda(self.device).float()
            X['Sxx_orig'] = X['Sxx_orig'].cuda(self.device).float()
            X['ySxx'] = X['ySxx'].cuda(self.device).long()


            if self.model_parallel:
                X['mu'], X['logvar'], X['x_'], X['scores'], X['rSxx'] = self.forward_parallel(X['Sxx'])
            else:
                X['mu'], X['logvar'], X['x_'], X['scores'], X['rSxx'] = self.forward(X['Sxx'])

            losses = self.model.get_losses(X)
            losses['loss_crossentropy'] = losses['loss_crossentropy'] * self.lossCE_weight
            losses['loss_reconstruction'] = losses['loss_reconstruction'] * self.lossMSE_weight
            losses['loss_KL_Div'] = losses['loss_KL_Div'] * self.lossKL_weight
            losses['loss'] = losses['loss_reconstruction'] + losses['loss_KL_Div'] + losses['loss_crossentropy']

            losses['loss'].backward()
            #losses['loss_crossentropy'].backward()
            #torch.nn.utils.clip_grad_norm_(self.model.parameters(), 0.3)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 0.5, norm_type=2.0)
            self.optimizer.step()

            scores = self.model.classification_scores(X)

            losses['loss_crossentropy'] = float(losses['loss_crossentropy'].detach().cpu().numpy())
            losses['loss_reconstruction'] = float(losses['loss_reconstruction'].detach().cpu().numpy())
            losses['loss_KL_Div'] = float(losses['loss_KL_Div'].detach().cpu().numpy())
            losses['loss'] = float(losses['loss'].detach().cpu().numpy())

            losses.update(scores)
            e_losses += [losses]
            #if k == 2:
                #break
            if k == 10:
                self.plot_to_file(X)


        #print(pd.DataFrame(e_losses).mean(axis=0))

        self.print_losses_to_file(pd.DataFrame(e_losses).mean(axis=0).to_dict())
        self.plot_to_file(X)

        #if self.current_epoch % self.save_report_freq == 0:

        if self.current_epoch % self.save_model_freq == 0:
            self.validate()
            self.save_model()


        print(pd.DataFrame(e_losses).mean(axis=0))
        print('Time elapsed per epoch: ' + str(time.time() - t) + ' s')
        self.current_epoch += 1
        self.lr_scheduler.step()




    def validate(self):
        #### VALIDATION
        self.model.eval()
        val_dict_PSG = []
        for ch in ['c3m2', 'f3m2', 'f4m1']:#self.DatasetValidation.channels:
            print('VALIDATING Channel: ', ch)
            self.DatasetValidation.channels_to_use = np.array([ch])
            for validx in tqdm(list(range(self.DatasetValidation.__len__()))):
                X = self.DatasetValidation.get_sample(validx)
                X['Sxx'] = torch.tensor  (X['Sxx']).cuda(self.device).float()
                X['ySxx'] = torch.tensor(X['ySxx']).cuda(self.device).long()

                X = self.model.format_single(X)
                X['mu'], X['logvar'], X['x_'], X['scores'], X['rSxx'] = self.forward(X['Sxx'])
                losses = self.model.get_losses(X)
                scores = self.model.classification_scores(X)

                losses['loss_crossentropy'] = losses['loss_crossentropy'] * self.lossCE_weight
                losses['loss_reconstruction'] = losses['loss_reconstruction'] * self.lossMSE_weight
                losses['loss_KL_Div'] = losses['loss_KL_Div'] * self.lossKL_weight
                losses['loss'] = losses['loss_crossentropy'] + losses['loss_reconstruction'] + losses['loss_KL_Div']

                losses['loss_crossentropy'] = float(losses['loss_crossentropy'].detach().cpu().numpy())
                losses['loss_reconstruction'] = float(losses['loss_reconstruction'].detach().cpu().numpy())
                losses['loss_KL_Div'] = float(losses['loss_KL_Div'].detach().cpu().numpy())
                losses['loss'] = float(losses['loss'].detach().cpu().numpy())

                losses.update(scores)
                val_dict_PSG += [losses]

        print('##### VALIDATION PSG ####')
        print(pd.DataFrame(val_dict_PSG).mean(axis=0))
        self.print_losses_to_file(pd.DataFrame(val_dict_PSG).mean(axis=0).to_dict(), validation=True)



    def print_losses_to_file(self, losses, validation=False):
        if validation: path = self.path_report_losses_validation
        else: path = self.path_report_losses

        lr = self.optimizer.param_groups[0]['lr']
        #f.write('Epoch, lr, loss_KL, loss_CE, loss_REC, Kappa, F1_0, F1_1, F1_2, F1_3, F1_4\n')
        printStr = f'{self.current_epoch}, {lr}, ' + ', '.join([f'{i:.8f}' for k, i in losses.items()]) + '\n'

        with open(path, 'a') as f:
            f.write(printStr)


    def plot_to_file(self, X):
        y = X['ySxx'][-1].detach().cpu().squeeze().numpy()
        oX = X['Sxx'][-1].detach().cpu().squeeze().numpy()
        rX = X['rSxx'][-1].detach().cpu().squeeze().numpy()
        img_path = os.path.join(self.path_report_images, "Epoch_" + f"{self.current_epoch:06d}" + ".png")

        plt.figure(figsize=(12, 12))
        ax0 = plt.subplot(5, 1, 1)
        plt.plot(y)
        plt.subplot(5, 1, 2, sharex=ax0)
        plt.imshow(oX[0], vmin=0, vmax=1.2)
        ax1 = plt.subplot(5, 1, 3, sharex=ax0)
        plt.imshow(rX[0], vmin=0, vmax=1.2)
        ax1 = plt.subplot(5, 1, 4, sharex=ax1)
        plt.imshow(oX[1], vmin=0, vmax=1.2)
        ax1 = plt.subplot(5, 1, 5, sharex=ax1)
        plt.imshow(rX[1], vmin=0, vmax=1.2)
        plt.savefig(img_path)
        plt.close()
        #plt.show()

    def save_model(self):
        PATH = os.path.join(self.path_report_models, 'epoch_' + f"{self.current_epoch:06d}")
        torch.save(self.model.state_dict(), PATH)

    def read_model(self, PATH):
        self.model = GRUVariantialSleepEncoder(self.cfg)
        self.model.load_state_dict(torch.load(PATH, map_location='cpu'), strict=False)
        self.model.to(self.device)
        if self.GPUs.__len__() > 1:
            self.model_parallel = torch.nn.DataParallel(self.model, device_ids=self.GPUs)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def train(self):
        for k in range(self.epochs):
            self.do_epoch()

