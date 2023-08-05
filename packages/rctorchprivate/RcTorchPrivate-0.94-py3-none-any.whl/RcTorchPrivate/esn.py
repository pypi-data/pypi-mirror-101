#Imports
import math
from dataclasses import dataclass

#botorch
from botorch.acquisition import qExpectedImprovement
from botorch.fit import fit_gpytorch_model
from botorch.generation import MaxPosteriorSampling
from botorch.models import FixedNoiseGP, SingleTaskGP
from botorch.optim import optimize_acqf
#from botorch.test_functions import Ackley
from botorch.utils.transforms import unnormalize

#gpytorch
import gpytorch
from gpytorch.constraints import Interval
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.mlls import ExactMarginalLogLikelihood
from gpytorch.priors import HorseshoePrior

#torch (we import functions from modules for small speed ups in performance)
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
import torch.optim as optim
from torch import nn, optim
from torch.autograd import Variable
from torch.autograd import grad
from torch.autograd import Function as Function
from torch.quasirandom import SobolEngine
from torch import matmul, pinverse, hstack, eye, ones, zeros, cuda, Generator, rand, randperm, no_grad, normal, tensor, vstack, cat, dot
from torch import clamp, prod, where, randint, stack
from torch import device as torch_device
from torch.cuda import is_available as cuda_is_available
from torch.nn import Linear, MSELoss, Tanh, NLLLoss, Parameter

#other packages
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns
import time

from sklearn.linear_model import ElasticNet

from .custom_loss import *



#pytorch elastic net regularization:
#https://github.com/jayanthkoushik/torch-gel

#TODO: unit test setting interactive to False.

#TODO: repair esn documentation (go strait to reinier's, copy and make adjustments)

#TODO: rename some pyesn variables.

#TODO: improve documentation.

class Recurrence(Function):
    """
    def __init__(self,):
        self.states = states
        self.LinIn = LinIn
        self.LinOut = LinOut
        self.LinRes = LinRes
        self.bias = bias
        self.n_nodes = n_nodes
        self.activation_function = activation_function
        self.leaking_rate = leaking_rate
        self.noise = noise
        self.LinFeedback = LinFeedback
    """

    @staticmethod
    def forward(ctx, input_t,  state_t, LinIn, LinOut, LinRes, bias_, n_nodes, activation_function, leaking_rate, noise, feedback, y,  tensor_args, dh_dx, LinFeedback = None):
        #for t in range(1, input.shape[0]):
        #input_t, state = input[t, :].T, states[t-1,:]
        #state_t, output = self.train_state(t, X = input_t,
        #                          state = self.states[t-1,:], 
        #                          y = y[t-1], output = True)
        #assert False, f'Lin {LinIn.weight.shape} input {input.shape}'
        input_vector = LinIn(input_t)
        recurrent_vec = LinRes(state_t)

        preactivation = input_vector.view(*recurrent_vec.shape) + bias_ + recurrent_vec

        #if self.feedback:
        #    feedback_vec = self.LinFeedback(y)
        #    preactivation = preactivation.clone() + feedback_vec
        
        #if noise != None:
        #    noise_vec = rand(n_nodes, **tensor_args)*2 -1
        update = activation_function(preactivation) #+  noise_vec*noise) 
        next_state = leaking_rate[0] * update + leaking_rate[1] * state_t

        #if output:
        #    return next_state, self.LinOut(cat([X, next_state]))
        #else:
        #    return next_state
        #states = cat([states, next_state.view(-1, n_nodes)], axis = 0)
        #####################################################3
        #extended_states = hstack((input, states))
    
        #assert False, f'input.shape {input.shape}, states {states.shape} preactivation {preactivation.shape} next state {next_state.shape}'

        #yfit = LinOut(extended_states)
        #dy_dx_orig = dfx(input, yfit) 

        ctx.dh_dx = dh_dx

        return next_state #extended_states


    @staticmethod
    def backward(ctx, grad_output):
        if grad_output is None:
            return None, None
        #dh_dx = ctx.saved_tensors
        
        #dh_dx = dy_dx_orig / (LinOut_weight * LinOut_weight.shape[1])
        #dy_dx = self.dh_dx @ LinOut_weight.T
        return ctx.dh_dx, None, None, None, None, None, None, None, None, None, None, None, None, None, None

def dfx(x,f, retain_graph = True, create_graph = True, requires_grad = True, grad_outputs = None):
    try:
        assert not grad_outputs
        return grad([f],[x], grad_outputs=torch.ones_like(f), 
                    create_graph = create_graph, retain_graph = retain_graph)[0]
    except:
        return grad([f],[x], grad_outputs=torch.ones_like(f), create_graph = create_graph, 
                             retain_graph = retain_graph)[0]

def check_x(X, y, tensor_args = {}):
    if X is None:
        #X = ones(*y.shape, device = device, requires_grad = requires_grad)
        X = torch.linspace(0, 1, steps = y.shape[0], **tensor_args)
    try:
        if X is None:
            X = ones(*y.shape, **tensor_args)
            #print("1a")
    except:
        print("first try-catch failed")
        pass
    try:
        if type(X) == np.ndarray:
            X = torch.tensor(X,  **tensor_args)
            #print("2a")
    except:
        pass
    try:
        if len(X.shape) == 1:
            X = X.view(-1, 1)
            #print("3a")
    except:
        pass
    #assert X.requires_grad == tensor_args["requires_grad"]
    return X


def printn(param: torch.nn.parameter):
    """TODO"""
    print(param._name_ + "\t \t", param.shape)

def NRMSELoss(yhat,y):
    """TODO"""
    return torch.sqrt(torch.mean((yhat-y)**2)/y**2)

def sinsq(x):
    """TODO"""
    return torch.square(torch.sin(x))

def printc(string_, color_, end = '\n') :
    """TODO"""
    colorz = {
          "header" : '\033[95m',
          "blue" : '\033[94m',
          'cyan' : '\033[96m',
          'green' : '\033[92m',
          'warning' : '\033[93m',
          'fail' : '\033[91m',
          'endc' : '\033[0m',
           'bold' :'\033[1m',
           "underline" : '\033[4m'
        }
    print(colorz[color_] + string_ + colorz["endc"] , end = end)


class EchoStateNetwork(nn.Module):
    """Class with all functionality to train Echo State Nets.
    Builds and echo state network with the specified parameters.
    In training, testing and predicting, x is a matrix consisting of column-wise time series features.
    Y is a zero-dimensional target vector.
    Parameters
    ----------
    n_nodes : int
        Number of nodes that together make up the reservoir
    input_scaling : float
        The scaling of input values into the network
    feedback_scaling : float
        The scaling of feedback values back into the reservoir
    spectral_radius : float
        Sets the magnitude of the largest eigenvalue of the transition matrix (weight matrix)
    leaking_rate : float
        Specifies how much of the state update 'leaks' into the new state
    connectivity : float
        The probability that two nodes will be connected
    regularization : float
        The L2-regularization parameter used in Ridge regression for model inference
    feedback : bool
        Sets feedback of the last value back into the network on or off
    random_seed : int
        Seed used to initialize RandomState in reservoir generation and weight initialization
    
    
    BACKPROP ARGUMENTS (not needed for the homework)
    backprop: bool
        if true the network initiates backpropogation.
    classification: bool
        if true the network assumes a categorical response, initiates backprop. Not yet working.
    criterion: torch.nn.Loss function
        loss function for backprogation training
    epochs: int
        the number of epochs to train the network for.
    l2_prop: float (between 0 and 1)
        this is the proportion of the l2 norm. if 1, ridge regression. if 0, lasso. in between it's elastic net regularization.
        **Please note that a significant slowdown will occur with values other than 0**



    Methods
    -------
    train(y, x=None, burn_in=100)
        Train an Echo State Network
    test(y, x=None, y_start=None, scoring_method='mse', alpha=1.)
        Tests and scores against known output
    predict(n_steps, x=None, y_start=None)
        Predicts n values in advance
    predict_stepwise(y, x=None, steps_ahead=1, y_start=None)
        Predicts a specified number of steps into the future for every time point in y-values array (NOT IMPLIMENTED)

    Arguments to be implimented later:
        obs_idx = None, resp_idx = None, input_weight_type = None, model_type = "uniform", PyESNnoise=0.001, 
        regularization lr: reg_lr = 10**-4, 
        change bias back to "uniform"
    """
    def __init__(self, n_nodes = 1000, bias = 0, connectivity = 0.1, leaking_rate = 0.99, spectral_radius=0.9, #<-- important hyper-parameters
                 regularization = None, activation_f = Tanh(), feedback = True,                              #<-- activation, feedback
                 input_scaling = 0.5, feedback_scaling = 0.5, noise = 0.0,                                     #<-- hyper-params not needed for the hw
                 approximate_reservoir = False, device = None, id_ = None, random_state = 123, reservoir = None, #<-- process args
                 backprop = False, classification = False, l2_prop = 1,
                 track_in_grad = False, dtype = torch.float32): #<-- this line is backprop arguments
        super().__init__()
        
        #activation function
        self.track_in_grad = track_in_grad
        self.activation_function = activation_f

        #cuda (gpu)
        if not device:
            self.device = torch_device("cuda" if cuda_is_available() else "cpu")
        else:
            self.device = device
        self.dtype = dtype

        # random state and default tensor arguments
        self.random_state = Generator(device=self.device).manual_seed(random_state)
        self.no_grad_ = {"requires_grad" : False}
        self.tensor_args = {"device": self.device, "generator" : self.random_state, **self.no_grad_}

        # hyper-parameters:
        self.bias = bias
        self.connectivity = connectivity
        self.feedback_scaling = feedback_scaling
        self.input_scaling = input_scaling
        self.leaking_rate = [leaking_rate, 1 - leaking_rate]
        self.n_nodes = n_nodes
        self.noise = noise
        self.regularization = regularization
        self.spectral_radius = spectral_radius

        #Feedback
        self.feedback = feedback

        #For speed up: approximate implimentation and preloaded reservoir matrices.
        self.approximate_reservoir, self.reservoir = approximate_reservoir, reservoir
        
        #backpropogation attributes:
        self.backprop= backprop

        #elastic net attributes: (default is 1, which is ridge regression for speed)
        self.l2_prop = l2_prop

        self.id_ = id_
        
        #Reservoir layer
        self.LinRes = Linear(self.n_nodes, self.n_nodes, bias = False)

        #https://towardsdatascience.com/logistic-regression-on-mnist-with-pytorch-b048327f8d19
        self.classification = classification

        """
        if self.classification:
            self.log_reg = Linear(self.n_nodes, 2)
            #self.criterion = criterion #torch.nn.CrossEntropyLoss()
        else:
            #self.criterion = MSELoss()
        """
            
        with no_grad():
            self.gen_reservoir()

        self.dev = {"device" : self.device, "dtype" : self.dtype, "requires_grad": self.track_in_grad}
        
        #scaler = "standardize"
        #if scaler == "standardize":
        #    self.scale   = self.stardardize
        #    self.descale = self.destandardize

        """TODO: additional hyper-parameters
        noise from pyesn — unlike my implimentation it happens outside the activation function. 
        TBD if this actually can improve the RC.
        self.PyESNnoise = 0.001
        self.external_noise = rand(self.n_nodes, device = self.device)
        colorz = {
          "header" : '\033[95m',
          "blue" : '\033[94m',
          'cyan' : '\033[96m',
          'green' : '\033[92m',
          'warning' : '\033[93m',
          'fail' : '\033[91m',
          'endc' : '\033[0m',
           'bold' :'\033[1m',
           "underline" : '\033[4m'
        }"""

    def plot_reservoir(self):
        """Plot the network weights"""
        sns.histplot(self.weights.cpu().numpy().view(-1,))

    def train_state(self, t, X, state, y, output = False):
        """
        Arguments:
            t: the current timestep
            input_: the input vector for timestep t
            current_state: the current state at timestep t
            output_pattern: the output pattern at timestep t.
        """
        # generator = self.random_state, device = self.device)  
        #assert 3 == 0, f'LinRes {self.LinRes(current_state).shape},'

        input_vector = self.LinIn(X)
        recurrent_vec = self.LinRes(state)

        preactivation = input_vector + self.bias_ + recurrent_vec

        if self.feedback:
            #avoiding inplace operations:
            feedback_vec = self.LinFeedback(y)
            preactivation = preactivation.clone() + feedback_vec
        
        if self.noise != None:
            noise_vec = rand(self.n_nodes, **self.tensor_args)*2 -1
        update = self.activation_function(preactivation +  noise_vec*self.noise) 
        next_state = self.leaking_rate[0] * update + self.leaking_rate[1] * state

        if output:
            return next_state, self.LinOut(cat([X, next_state], axis = 0).view(self.n_outputs,-1))
        else:
            return next_state

    def forward(self, extended_states):
        #if fit_states:
        #    self.train_states(**kwargs)
        return self.LinOut(extended_states)



    def gen_reservoir(self, obs_idx = None, targ_idx = None, load_failed = None):
        """Generates random reservoir from parameters set at initialization."""
        # Initialize new random state

        #random_state = np.random.RandomState(self.random_state)

        max_tries = 1000  # Will usually finish on the first iteration
        n = self.n_nodes

        #if the size of the reservoir has changed, reload it.
        if self.reservoir:
            if self.reservoir.n_nodes_ != self.n_nodes:
                load_failed = 1

        already_warned = False
        book_index = 0
        for i in range(max_tries):
            if i > 0:
                printc(str(i), 'fail', end = ' ')

            #only initialize the reservoir and connectivity matrix if we have to for speed in esn_cv.
            if not self.reservoir or not self.approximate_reservoir or load_failed == 1:

                self.accept = rand(self.n_nodes, self.n_nodes, **self.tensor_args) < self.connectivity
                self.weights = rand(self.n_nodes, self.n_nodes, **self.tensor_args) * 2 - 1
                self.weights *= self.accept
                #self.weights = csc_matrix(self.weights)
            else:
                #print("LOADING MATRIX", load_failed)
                try:
                    if self.approximate_reservoir:
                        self.weights = self.reservoir.get_approx_preRes(self.connectivity, i).to(self.device)
                    else:
                        self.weights = self.reservoir.reservoir_pre_weights < self.connectivity
                        self.weights *= self.reservoir.accept
                        self.weights = self.weights

                        del self.accept; del self.reservoir.reservoir_pre_weights;

                    #printc("reservoir successfully loaded (" + str(self.weights.shape) , 'green') 
                except:
                    assert 1 == 0
                    if not i:
                        printc("approx reservoir " + str(i) + " failed to load ...regenerating...", 'fail')
                    #skip to the next iteration of the loop
                    if i > self.reservoir.number_of_preloaded_sparse_sets:
                        load_failed = 1
                        printc("All preloaded reservoirs Nilpotent, generating random reservoirs, connectivity =" + str(round(self.connectivity,8)) + '...regenerating', 'fail')
                    continue
                else:
                    assert 1 == 0, "TODO, case not yet handled."
             
            max_eigenvalue = self.weights.eig(eigenvectors = False)[0].abs().max()
            
            if max_eigenvalue > 0:
                break
            else: 
                if not already_warned:
                    printc("Loaded Reservoir is Nilpotent (max_eigenvalue ={}), connectivity ={}.. .regenerating".format(max_eigenvalue, round(self.connectivity,8)), 'fail')
                already_warned = True
                #if we have run out of pre-loaded reservoirs to draw from :
                if i == max_tries - 1:
                    raise ValueError('Nilpotent reservoirs are not allowed. Increase connectivity and/or number of nodes.')

        # Set spectral radius of weight matrix
        self.weights = self.weights * self.spectral_radius / max_eigenvalue
        self.weights = Parameter(self.weights, requires_grad = False)

        self.LinRes.weight = self.weights
        
        if load_failed == 1 or not self.reservoir:
            self.state = zeros(1, self.n_nodes, device=torch_device(self.device), **self.no_grad_)
        else:
            self.state = self.reservoir.state

        # Set output weights to none to indicate untrained ESN
        self.out_weights = None
             

    def set_Win(self): #inputs
        """
        Build the input weights.
        Currently only uniform implimented.

        Arguments:
            inputs:
        """
        with no_grad():
            n, m = self.n_nodes, self.n_inputs
            #weight
            if not self.reservoir or 'in_weights' not in dir(self.reservoir): 
                
                #print("GENERATING IN WEIGHTS")

                in_weights = rand(n, m, generator = self.random_state, device = self.device, requires_grad = False)
                in_weights =  in_weights * 2 - 1
                
            else:
                
                in_weights = self.reservoir.in_weights #+ self.noise * self.reservoir.noise_z One possibility is to add noise here, another is after activation.
                
                ##### Later for speed re-add the feedback weights here.

                #if self.feedback:
                #    feedback_weights = self.feedback_scaling * self.reservoir.feedback_weights
                #    in_weights = hstack((in_weights, feedback_weights)).view(self.n_nodes, -1)

            in_weights *= self.input_scaling

            #if there is white noise add it in (this will be much more useful later with the exponential model)
            #populate this bias matrix based on the noise

            #bias
            #uniform bias can be seen as means of normal random variables.
            if self.bias == "uniform":
                #random uniform distributed bias
                bias = bias * 2 - 1
            elif type(self.bias) in [type(1), type(1.5)]:
                bias = bias = zeros(n, 1, device = self.device, **self.no_grad_)
                bias = bias + self.bias

                #you could also add self.noise here.
            
            self.bias_ = bias
            if self.bias_.shape[1] == 1:
                self.bias_ = self.bias_.squeeze()

            if self.feedback:
                feedback_weights = rand(self.n_nodes, self.n_outputs, device = self.device, requires_grad = False, generator = self.random_state) * 2 - 1
                feedback_weights *= self.feedback_scaling
                feedback_weights = feedback_weights.view(self.n_nodes, -1)
                feedback_weights = Parameter(feedback_weights, requires_grad = False) 
            else:
                feedback_weights = None
   
        in_weights = Parameter(in_weights, requires_grad = False)
        #in_weights._name_ = "in_weights"

        return (in_weights, feedback_weights)
    
    def check_device_cpu(self):
        """TODO: make a function that checks if a function is on the cpu and moves it there if not"""
        pass

    def display_in_weights(self):
        """TODO"""
        sns.heatmap(self.in_weights)

    def display_out_weights(self):
        """TODO"""
        sns.heatmap(self.out_weights)

    def display_res_weights(self):
        """TODO"""
        sns.heatmap(self.weights)

    def plot_states(self, n= 10):
        """TODO"""
        for i in range(n):
            plt.plot(list(range(len(self.state[:,i]))), RC.state[:,i], alpha = 0.8)

    def freeze_weights(self):
        names = []
        for name, param in zip(self.state_dict().keys(), self.parameters()):
            names.append(name)
            if name != "LinOut.weight":
                param.requires_grad_(False)
            else:
                self.LinOut.weight.requires_grad_(True)
                self.LinOut.bias.requires_grad_(True)
                assert self.LinOut.weight.requires_grad
            #print('param:', name,  params.requires_grad)

    def train_states(self, X, y, states):
        for t in range(1, X.shape[0]):
            state_t, output = self.train_state(t, X = X[t, :].T,
                                      state = states[t-1,:], 
                                      y = y[t-1], output = True)
            states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)
        return states

    def train(self, y, X=None, burn_in=0, input_weight=None, verbose = False , 
        learning_rate = 0.005, return_states = False, epochs = None, patience = 20, criterion =  MSELoss(), optimizer = None,
        out_weights = None, save_after_n_epochs = None, ODE = True, scale_x = True):
        """
        NLLLoss(),
        Train the network.
        
        Arguments: TODO
            y: response matrix
            x: observer matrix
            burn in: obvious
            input_weight : ???
            learning_rate: 
            verbose:
        """
        self.ODE = ODE
        self.epochs = epochs
        self.burn_in = burn_in

        self.patience = patience
        self.criterion = criterion

        if save_after_n_epochs  == None and self.epochs:
            save_after_n_epochs = int(self.epochs * 0.7)
        

        #if self.id_ is None:
        #    assert y.is_leaf == True, "y must be a leaf variable"
        
        #ensure that y is a 2-dimensional tensor with pre-specified arguments.
        if type(y) == np.ndarray:
             y = torch.tensor(y, **self.dev)
        y = y.clone()
        if y.device != self.device:
            y = y.to(self.device)
        if len(y.shape) == 1:
            y = y.view(-1, 1)

            #y = y.detach()
        
        #ensure that X is a two dimensional tensor, or if X is None declare a tensor.
        X = check_x(X , y, self.dev).to(self.device)
        
        self.unscaled_X = Parameter(X, requires_grad = self.track_in_grad)

        if self.unscaled_X.device != self.device:
            self.unscaled_X.data = self.unscaled_X.data.to(self.device)

        assert self.unscaled_X.requires_grad == self.track_in_grad
        
        #protect against input that is a vector of ones. (otherwise we divide by infinity)
        # Normalize inputs and outputs
        y = self.scale(outputs=y, keep=True)
        if self.unscaled_X.std() != 0:
            self.X = self.unscaled_X.clone()
            if scale_x:
                self.X.data = self.scale(inputs=self.unscaled_X, keep=True).clone()
        else:
            self._input_stds = None
            self._input_means = None

        #assert self.X.requires_grad == self.track_in_grad, "X.requires_grad not enabled"

        start_index = 1 if self.feedback else 0 
        rows = y.shape[0] - start_index
        
        self.n_outputs = y.shape[1]
        self.n_inputs = self.X.shape[1]
        
        self.lastoutput = y[-1, :]
        self.lastinput = self.X[-1, :]

        self.n_outputs  = y.shape[1]
        
        start_index = 1 if self.feedback else 0 
        rows = y.shape[0] - start_index

        self.LinIn = Linear(self.n_inputs, self.n_nodes,  bias = False)
        self.LinFeedback = Linear(self.n_inputs, self.n_nodes, bias = False)
        self.LinIn.weight, self.LinFeedback.weight = self.set_Win()
        self.LinOut = Linear(self.n_nodes + 1, self.n_outputs)

        #self.freeze_weights()

        if self.track_in_grad:
            #X.requires_grad_(True)
            self.LinIn.weight.requires_grad_(True)
            self.LinOut.weight.requires_grad_(True)#.requires_grad_(True)
            if self.feedback:
                self.LinFeedback.weight.requires_grad_(True)#.requires_grad_(True)
        else:
            self.LinIn.weight.requires_grad_(False)
            self.LinOut.weight.requires_grad_(False)
            if self.feedback:
                self.LinFeedback.weight.requires_grad_(False)

        # if we are doing backprop the only tensor that can have requires_grad True is the output weight.
        if False:
            assert not self.X.requires_grad, "we only want to train the output layer, set X.requires_grad to False."
            assert not y.requires_grad, "we only want to train the output layer, set y.requires_grad to False."
            self.LinIn.requires_grad_(False)
            self.LinOut.requires_grad_(True)
            self.LinFeedback.requires_grad_(False)
            self.track_in_grad = False

        if not self.classification:
            self.out_activation = self.LinOut
        
        #build the state matrix:
        self.state = zeros((1, self.n_nodes), **self.dev)

        if not self.track_in_grad or not self.backprop:
            self.state = self.state.clone().detach()

        self.state._name_ = "state"

        current_state = self.state[-1] 

        try:
            assert self.LinOut.weight.device == self.device
        except:
            self.LinOut.weight = Parameter(self.LinOut.weight.to(self.device))
            self.LinOut.bias = Parameter(self.LinOut.bias.to(self.device))


        ################################################################################################
        #+++++++++++++++++++++++++++         FORWARD PASS AND SOLVE             ++++++++++++++++++++++++
        ################################################################################################
        #fast exact solution ie we don't want to run backpropogation:
        if not self.backprop:
            with torch.set_grad_enabled(self.track_in_grad):

                #run through the states.
                for t in range(1, self.X.shape[0]):
                    #this following was the old method, which is in-place which will fail to carry the grads.
                    #_______________________________________________________________________
                    #self.state[t, :] = self.forward(t, input_ = X[t, :].T,
                    #                                   current_state = self.state[t-1,:], 
                    #                                   output_pattern = y[t-1]).squeeze()
                    #_______________________________________________________________________
                    state_t = self.train_state(t, X = self.X[t, :].T,
                                              state = self.state[t-1,:], 
                                              y = y[t-1]).squeeze()
                    self.state = cat([self.state, state_t.view(-1, self.n_nodes)], axis = 0)


                extended_states = hstack((self.X, self.state))
                extended_states._name_ = "complete_data"

                #include everything after burn_in
                train_x = extended_states[burn_in:, :]
                train_y = y[burn_in:] #if not self.feedback else y[burn_in + 1:] <-- in Reiniers code
                bias = None
                if not self.regularization:
                    print("no regularization")
                    pinv = pinverse(train_x)
                    weight = matmul(pinv, train_y)
                elif self.l2_prop == 1:

                    #print("ridge regularizing")
                    with torch.set_grad_enabled(self.track_in_grad):
                        
                        ones_row = ones(train_x.shape[0],1, **self.dev)
                        train_x = cat((ones_row, train_x), axis = 1)
                        ridge_x = matmul(train_x.T, train_x) + \
                                           self.regularization * eye(train_x.shape[1], **self.dev)
                        ridge_y = matmul(train_x.T, train_y)
                        ridge_x_inv = pinverse(ridge_x)
                        weight = ridge_x_inv @ ridge_y

                        bias = weight[0]
                        weight = weight[1:]
                        #assert weight.requires_grad, "weight doesn't req grad"

                    #torch.solve solves AX = B. Here X is beta_hat, A is ridge_x, and B is ridge_y
                    #weight = torch.solve(ridge_y, ridge_x).solution

                else: #+++++++++++++++++++++++         This section is elastic net         +++++++++++++++++++++++++++++++

                    gram_matrix = matmul(train_x.T, train_x) 

                    regr = ElasticNet(random_state=0, 
                                          alpha = self.regularization, 
                                          l1_ratio = 1-self.l2_prop,
                                          selection = "random",
                                          max_iter = 3000,
                                          tol = 1e-3,
                                          #precompute = gram_matrix.numpy(),
                                          fit_intercept = True
                                          )
                    print("train_x", train_x.shape, "_____________ train_y", train_y.shape)
                    regr.fit(train_x.numpy(), train_y.numpy())

                    weight = tensor(regr.coef_, device = self.device, **self.dev)
                    bias = tensor(regr.intercept_, device =self.device, **self.dev)

                req_grad_dict = {'requires_grad' : self.track_in_grad or self.backprop}#self.track_in_grad or self.backprop}
                
                self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                if type(bias) != type(None):
                    self.LinOut.bias = Parameter(bias.view(self.n_outputs, -1))
                if self.track_in_grad:
                    self.LinOut.weight.requires_grad = True

        else:
            #+++++++++++++++++++++++++++++++         backprop          +++++++++++++++++++++++++++++++
            trainable_parameters = []
            trainable_parameters = []

            for p in self.parameters():
                if p.requires_grad:
                    trainable_parameters.append(p)

            for i, p in enumerate(trainable_parameters):
                print(f'Trainable parameter {i} {p.name} {p.data.shape}')


            running_loss = 0
            train_losses = []
            if not optimizer:
                optimizer = optim.Adam(self.parameters(), lr=learning_rate)

            min_loss = float("Inf")
            epochs_not_improved = False

            bias_buffer = torch.ones((y.shape[0],1),**self.dev)

            
            if self.epochs == None:
                endless = True
            else:
                endless = False

            self.freeze_weights()
            assert self.LinOut.weight.requires_grad

            states = self.state.clone()
            states = states.to(self.device)


            ######.  TRAIN STATES ################### SEPARATELY FROM THE OTHER FORWARD PASS
            #X_detached = self.X.detach()
            #X_detached.requires_grad_(True)

            
                #self.dh_dx = torch.zeros(0,**self.dev)
            X_detached = self.unscaled_X.clone().detach().requires_grad_(True)
            if scale_x:
                X_detached = (X_detached- self._input_means) / self._input_stds
            if out_weights:
                self.LinOut.weight.data = out_weights["weight"]
                self.LinOut.bias.data = out_weights["bias"]
                #self.LinOut.weight.requires_grad_(False)
                #self.LinOut.bias.requires_grad_(False)
            state_list = []

            if self.feedback:
                assert False, "not implimented"

            for t in range(0, X_detached.shape[0]):
                input_t = X_detached[t, :].T
                state_t, output_t = self.train_state(t, X = input_t,
                                          state = states[t,:], 
                                          y = None, output = True)
                state_list.append(state_t)
                with no_grad():
                    dht_dt = dfx(X_detached, state_t)
                    dht_dy = dfx(state_t, output_t)
                    dyt_dx = dfx(X_detached, output_t) #<-- calculating the derivative at each timestep.
                if t == 0:
                    self.dh_dts = []
                    self.dh_dys = []
                    self.dy_dxs = []
                    self.outputs = []
                    self.outputs = []
                    self.dh_dt = dht_dt
                    #self.dy_dh = 
                    #elif t > 1:
                    self.dh_dt = torch.cat((self.dh_dt, dht_dt))
                    #self.dy_dh = torch.cat((self.dh_dx, dht_dx))
                
                self.dh_dys.append(dht_dy)
                self.dh_dts.append(dht_dt)
                self.outputs.append(output_t)
                self.dy_dxs.append(dyt_dx)

                states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)
            #####################################################
            self.dy_dx = dfx(X_detached, torch.vstack(self.outputs)) #one time derivative doesn't work very well.
            #####################################################################
            
            del states

            self.dy_dx_matrix = torch.hstack(self.dy_dxs)
            #del self.dy_dxs
            #proper scaling:
            self.dy_dx = self.dy_dx_matrix.sum(axis = 0 )# / self._input_stds)*self._output_stds
            #undo the output layer:
            self.dh_dx =  self.dy_dx / (self.LinOut.weight.view(-1,self.n_outputs) * (self.n_nodes + 1))

            #self.dh_dx_for_backwards_pass = self.dh_dx.mean(axis = 0).view(-1,1).clone().detach()
            #assert False

            #extended_states = hstack((X_detached, states[1:]))

            self.loss_history, reassign = [], False
            base_derivative_calculated = False   

            
            
            # The recurrence class will do the forward pass for backprop. We will give it the derivative after doing another forward pass
            
            #order: ctx, input,  states, LinIn, LinOut, LinRes, bias_, n_nodes, activation_function, leaking_rate, noise, feedback, y,  tensor_args, LinFeedback = None
            
            

            if 1 == 0:
                pass
            else:
                for e in range(self.epochs):
                    self.states = self.state.clone()
                    self.states = self.states.to(self.device)

                    optimizer.zero_grad()
                    for t in range(0, X_detached.shape[0]):
                        input_t = self.X[t, :].T
                        train_states_class = Recurrence()
                        state_t = train_states_class.apply(input_t, 
                                                           self.states[t,:],
                                                           self.LinIn, 
                                                           self.LinOut, 
                                                           self.LinRes, 
                                                           self.bias, 
                                                           self.n_nodes, 
                                                           self.activation_function, 
                                                           self.leaking_rate, 
                                                           self.noise, 
                                                           self.feedback, 
                                                           y, 
                                                           self.tensor_args,
                                                           self.dh_dts[t].detach(),
                                                           None)

                        self.states = cat([self.states, state_t.view(-1, self.n_nodes)], axis = 0)

                    extended_states = hstack((self.X, self.states[1:]))
                    self.yfit = self.forward(extended_states)

                    
                    
                    #self.dy_dh = dfx(states, self.yfit)
                    #with torch.no_grad():
                    #    if self.track_in_grad or ODE:
                    #        self.dy_dx_orig = dfx(self.X, self.yfit) 
                    #        self.dh_dx = self.dy_dx_orig / (self.LinOut.weight * self.LinOut.weight.shape[1])
                    if ODE:
                        #assert self.yfit.shape == self.dh_dx.shape, f'{self.yfit.shape} != {self.dh_dx.shape}'
                        if scale_x:
                            yfit = self.yfit  / self._input_stds
                        with torch.no_grad():
                            self.dy_dx = dfx(self.X, self.yfit)
                        loss = self.criterion(self.X, self.yfit, self.dy_dx)
                    else:
                        #self.yfit = self.yfit * self._output_stds + self._output_means
                        loss = self.criterion(self.yfit, y)

                    assert loss.requires_grad
                    #assert False, loss
                    loss.backward(retain_graph = True)
                    assert type(self.X.grad != None)

                    #save best weights
                    if e > save_after_n_epochs:
                        
                        if float(loss) < min(self.loss_history):
                            best_bias, best_weight = self.LinOut.bias.clone(), self.LinOut.weight.clone()
                            self.LinOut.bias.data, self.LinOut.weight.data = best_bias, best_weight.view(*self.LinOut.weight.shape)

                    self.loss_history.append(float(loss))

                    optimizer.step()
                    if e % 100 == 0:
                        print("Epoch: {}/{}.. ".format(e+1, self.epochs),
                              "Training  Loss: {:.3f}.. ".format(torch.log(loss)))

                    #early stopping
                    if self.patience:
                        if e > 10:
                            if loss < min_loss:
                                epochs_not_improved = 0
                                min_loss = loss
                            else:
                                epochs_not_improved += 1

                        if e > 10 and epochs_not_improved >= self.patience:
                            print('Early stopping at epoch' ,  e, 'loss', loss)
                            early_stop = True
                            
                            break
                            
                        else:
                            continue
                    e=e+1

                    #to avoid unstable solutions consider an additional convergence parameter


                #early stopping code from the following article:
                #https://www.kaggle.com/akhileshrai/tutorial-early-stopping-vanilla-rnn-pytorch
            
            #for the final state we want to save that in self.state
            self.out_weights = self.LinOut.weight
            self.out_weights._name_ = "out_weights"
            #extended_states = hstack((self.X, self.state))
        
        # Store last y value as starting value for predictions
        self.y_last = y[-1, :]
        self.laststate = self.state[-1, :]

        self.yfit = self.LinOut(extended_states)
        #self.yfit = self._output_stds * self.yfit + self._output_means

        self.yfit = self.yfit.view(-1, self.n_outputs)

        
        # Return all data for computation or visualization purposes (Note: these are normalized)
        if return_states:
            return extended_states, (y[1:,:] if self.feedback else y), burn_in
        else:
            self.yfit = self._output_stds * self.yfit + self._output_means
            #if not self.track_in_grad:

            #    self.yfit = self.yfit.cpu().detach().numpy()
            return self.yfit


    def calculate_n_grads(self, X, y,  n = 2, scale = False):
        self.grads = []

        #X = X.reshape(-1, self.n_inputs)

        assert y.requires_grad, "entended doesn't require grad, but you want to track_in_grad"
        for i in range(n):
            print('calculating derivative', i+1)
            if not i:
                grad = dfx(X, y)
            else:
                grad = dfx(X, self.grads[i-1])

            self.grads.append(grad)

            if scale:
                self.grads[i] = self.grads[i]/(self._input_stds)
        with no_grad():
            self.grads = [self.grads[i][self.burn_in:] for i in range(n)]
                
            #self.yfit = self.yfit[self.burn_in:]
        #assert extended_states.requires_grad, "entended doesn't require grad, but you want to track_in_grad"
    
    def scale(self, inputs=None, outputs=None, keep=False):
        """Normalizes array by column (along rows) and stores mean and standard devation.

        Set `store` to True if you want to retain means and stds for denormalization later.

        Parameters
        ----------
        inputs : array or None
            Input matrix that is to be normalized
        outputs : array or No ne 
        no_grads            Output column vector that is to be normalized
        keep : bool
            Stores the normalization transformation in the object to denormalize later

        Returns
        -------
        transformed : tuple or array
            Returns tuple of every normalized array. In case only one object is to be returned the tuple will be
            unpacked before returning

        """
        # Checks
        if inputs is None and outputs is None:
            raise ValueError('Inputs and outputs cannot both be None')

        # Storage for transformed variables
        transformed = []
        if not inputs is None:

            if keep:
                # Store for denormalization
                self._input_means = inputs.mean(axis=0)
                self._input_stds = inputs.std(dim = 0)

            # Transform
            transformed.append((inputs - self._input_means) / self._input_stds)

        if not outputs is None:
            if keep:
                # Store for denormalization
                self._output_means = outputs.mean(axis=0)
                self._output_stds = outputs.std(dim = 0)#, ddof=1)

            # Transform
            transformed.append((outputs - self._output_means) / self._output_stds)
            
            self._output_means = self._output_means
            self._output_stds = self._output_stds
        # Syntactic sugar
        return tuple(transformed) if len(transformed) > 1 else transformed[0]

    def error(self, predicted, target, method='nmse', alpha=1.):
        """Evaluates the error between predictions and target values.

        Parameters
        ----------
        predicted : array
            Predicted value
        target : array
            Target values
        method : {'mse', 'tanh', 'rmse', 'nmse', 'nrmse', 'tanh-nmse', 'log-tanh', 'log'}
            Evaluation metric. 'tanh' takes the hyperbolic tangent of mse to bound its domain to [0, 1] to ensure
            continuity for unstable models. 'log' takes the logged mse, and 'log-tanh' takes the log of the squeezed
            normalized mse. The log ensures that any variance in the GP stays within bounds as errors go toward 0.
        alpha : float
            Alpha coefficient to scale the tanh error transformation: alpha * tanh{(1 / alpha) * error}.
            This squeezes errors onto the interval [0, alpha].
            Default is 1. Suggestions for squeezing errors > n * stddev of the original series
            (for tanh-nrmse, this is the point after which difference with y = x is larger than 50%,
             and squeezing kicks in):
             n  |  alpha
            ------------
             1      1.6
             2      2.8
             3      4.0
             4      5.2
             5      6.4
             6      7.6

        Returns
        -------
        error : float
            The error as evaluated with the metric chosen above

        """
        errors = predicted - target

        # Adjust for NaN and np.inf in predictions (unstable solution)
        #if not torch.all(torch.isfinite(predicted)):
        #    # print("Warning: some predicted values are not finite")
        #    errors = torch.inf
        
        def nmse(y, yhat):
            """
            normalized mean square error
            """
            return ((torch.sum(torch.square(y - yhat)) / torch.sum(torch.square(y)))) / len(y.squeeze())
            
        #### attempt at loss function when steps ahead > 2 

        def step_ahead_loss(y, yhat, plot = False, decay = 0.9):
            loss = zeros(1,1, device = self.device)
            losses = []
            total_length = len(y)
            for i in range(1, total_length - self.steps_ahead):
                #step ahead == i subsequences
                #columnwise
                #   yhat_sub = yhat[:(total_length - i), i - 1]
                #   y_sub = y[i:(total_length),0]
                #row-wise
                yhat_sub = yhat[i-1, :]
                y_sub = y[i:(self.steps_ahead + i),0]
                assert(len(yhat_sub) == len(y_sub)), "yhat: {}, y: {}".format(yhat_sub.shape, y_sub.shape)

                loss_ = nmse(y_sub.squeeze(), yhat_sub.squeeze())

                if decay:
                    loss_ *= (decay ** i)

                #if i > self.burn_in:
                loss += loss_
                losses.append(loss_)

            if plot:
                plt.plot(range(1, len(losses) + 1), losses)
                plt.title("loss vs step ahead")
                plt.xlabel("steps ahead")
                plt.ylabel("avg loss")
            return loss.squeeze()

        if predicted.shape[1] != 1:
            return step_ahead_loss(y = target, yhat = predicted) 

        # Compute mean error
        if type(method) != type("custom"):
            #assert self.custom_criterion, "You need to input the argument `custom criterion` with a proper torch loss function that takes `predicted` and `target` as input"
            try:
                error = method(self.X_test, target, predicted)
            except:
                error = method(target = target, predicted = predicted)

            """
            try:
                error = 
            except:
                if type(method) == type("custom"):
                    pass
                else:
                assert False, "bad scoring method, please enter a string or input a valid custom loss function"
            """
        elif method == 'mse':
            error = torch.mean(torch.square(errors))
        elif method == "combined":
            nmse = torch.mean(torch.square(errors)) / torch.square(target.squeeze().std())

            kl = torch.sigmoid(torch.exp(torch.nn.KLDivLoss(reduction= 'sum')(
                torch.softmax(predicted, dim = -1), 
                torch.softmax(target, dim = -1))))
            error = nmse + kl
            print('score', 'nmse', nmse, 'kl', kl, 'combined', error)
        elif method == "trivial_penalty":
            mse = torch.mean(torch.square(errors))
            penalty = torch.square((1/predicted).mean())
            error = mse + penalty
            print('score', 'mse', mse.data, 'penalty', penalty.data, 'combined', error.data)
        elif method == "smoothing_penalty":
            mse = torch.mean(torch.square(errors))
            penalty = torch.square(self.dydx2).mean()
            error = mse + 0.1 * penalty
            print('score', 'mse', nmse, 'penalty', penalty, 'combined', error)
        elif method == "combined_penalties":
            mse = torch.mean(torch.square(errors))
            #we should include hyper-parameters here.
            dxpenalty = torch.log(torch.abs(self.dydx2))
            dxpenalty_is_positive = (dxpenalty > 0)*1
            dxpenalty = dxpenalty * dxpenalty_is_positive
            dxpenalty = dxpenalty.mean()
            nullpenalty = torch.square((1/predicted).mean())
            error = mse + dxpenalty + nullpenalty
            print('score', 'mse', mse.data, 'dydx^2_penalty', dxpenalty.data, "penalty2", nullpenalty.data, 'combined', error.data)
        elif method == 'tanh':
            error = alpha * torch.tanh(torch.mean(torch.square(errors)) / alpha)  # To 'squeeze' errors onto the interval (0, 1)
        elif method == 'rmse':
            error = torch.sqrt(torch.mean(torch.square(errors)))
        elif method == 'nmse':
            error = torch.mean(torch.square(errors)) / torch.square(target.squeeze().std())#ddof=1))
        elif method == 'nrmse':
            error = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std()#ddof=1)
        elif method == 'tanh-nrmse':
            nrmse = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std(ddof=1)
            error = alpha * torch.tanh(nrmse / alpha)
        elif method == 'log':
            mse = torch.mean(torch.square(errors))
            error = torch.log(mse)
        elif method == 'log-tanh':
            nrmse = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std(ddof=1)
            error = torch.log(alpha * torch.tanh((1. / alpha) * nrmse))
        else:
            raise ValueError('Scoring method not recognized')
        return error.type(self.dtype)
    

    def back(self, tensor_spec, retain_graph = True):
        return tensor_spec.backward(torch.ones(*tensor_spec.shape, device = tensor_spec.device), retain_graph = retain_graph)

    def test(self, y, X=None, y_start=None, steps_ahead=None, scoring_method='nmse', alpha=1.):
        """Tests and scores against known output.

        Parameters
        ----------
        y : array
            Column vector of known outputs
        x : array or None
            Any inputs if required
        y_start : float or None
            Starting value from which to start testing. If None, last stored value from trainging will be used
        steps_ahead : int or None
            Computes average error on n steps ahead prediction. If `None` all steps in y will be used.
        scoring_method : {'mse', 'rmse', 'nrmse', 'tanh'}
            Evaluation metric used to calculate error
        alpha : float
            Alpha coefficient to scale the tanh error transformation: alpha * tanh{(1 / alpha) * error}

        Returns
        -------
        error : float
            Error between prediction and knwon outputs

        """ 

        self.steps_ahead = steps_ahead

        if type(y) == np.ndarray:
             y = torch.tensor(y, **self.dev)
        if len(y.shape) == 1:
            y = y.view(-1, 1)
        if y.device != self.device:
            y = y.to(self.device)

        X = check_x(X , y, self.dev).detach().clone().to(self.device).requires_grad_(True)
        
        #X = Parameter(X, requires_grad = self.track_in_grad)

        #if X.device != self.device:
        #    X = X.to(self.device)

        assert X.requires_grad == self.track_in_grad
        
        # Run prediction
        final_t =y.shape[0]
        if steps_ahead is None:
            y_predicted = self.predict(n_steps = y.shape[0], x=X, y_start=y_start)
            #printc("predicting "  + str(y.shape[0]) + "steps", 'blue')
        else:
            y_predicted = self.predict_stepwise(y, X, steps_ahead=steps_ahead, y_start=y_start)[:final_t,:]

        #if self.track_in_grad:
        #    self.back(y_predicted, retain_graph = True)
        

        y = y[self.burn_in:]
        if self.ODE:
            dy_dx_val = dfx(self.X_val, y_predicted)
            score = self.criterion(self.X_val, y_predicted, dy_dx_val)
        else:
            score = self.error(predicted = y_predicted, target = y, method = scoring_method, alpha=alpha)

        #score.backward() #consider "my backward"
        
        # Return error
        if self.id_ == None:
            #user friendly
            return score, {"yhat": y_predicted.deta, "ytest": y}, x[self.burn_in:]
        else:
            #internal to esn_cv
            return score.detach(), y_predicted.detach(), self.id_


    def predict(self, n_steps, x=None, y_start=None, continuation = True):
        """Predicts n values in advance.

        Prediction starts from the last state generated in training.

        Parameters
        ----------
        n_steps : int
            The number of steps to predict into the future (internally done in one step increments)
        x : numpy array or None
            If prediciton requires inputs, provide them here
        y_start : float or None
            Starting value from which to start prediction. If None, last stored value from training will be used

        Returns
        -------
        y_predicted : numpy array
            Array of n_step predictions

        """
        # Check if ESN has been trained
        if self.y_last is None: 
            raise ValueError('Error: ESN not trained yet')  
        # Normalize the inputs (like was done in train)
        if not x is None and type(self._input_means) != type(None):
            self.X_val = Parameter(self.scale(inputs=x))

        dev = {"device" : self.device, "dtype" : self.dtype, "requires_grad": False}

        n_samples = self.X_val.shape[0]

        if not y_start is None: #if not x is None:
            previous_y = self.scale(outputs=y_start)[0]

        if continuation:
            laststate = self.laststate
            lastinput = self.lastinput
            lastoutput = self.lastoutput
        else:
            laststate = zeros(self.n_nodes, **dev)
            lastinput = zeros(self.n_inputs, **dev)
            lastoutput = zeros(self.n_outputs, **dev)

        inputs = vstack([lastinput, self.X_val]).view(-1, self.X_val.shape[1])
        states = zeros((1, self.n_nodes), **dev)
        states[0,:] = laststate

        outputs = lastoutput.view(self.n_outputs, -1 )

        for t in range(n_samples):

            state_t = self.train_state(t, X = inputs[t+1, :],
                                      state = states[t,:], 
                                    y = outputs[t, :]).squeeze()
            states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)
            
            extended_state_spec = cat([inputs[t+1, :], states[t+1, :]]).view(-1,self.n_outputs)
            
            #bias_tensor = ones(*self.LinOut.weight.shape, **dev).squeeze()*self.LinOut.bias.item()
            #err_msg = "Linout " + str(self.LinOut.weight.shape) + ", extended_state_spec: " + str(extended_state_spec.shape)
            #err_msg = err_msg + " output:, " + str(self.LinOut(extended_state_spec).shape)
            #assert False, err_msg
            output_t = self.LinOut(extended_state_spec.T)
                
            outputs = cat([outputs, output_t.view(-1, self.n_outputs)], axis = 0)

        try:
            yhat = self.descale(outputs = outputs[1 + self.burn_in:]).view(-1, self.n_outputs) 
        except:
            yhat = outputs[1 + self.burn_in:]

        return yhat
        #https://towardsdatascience.com/in-place-operations-in-pytorch-f91d493e970e



    def predict_stepwise(self, y, x=None, steps_ahead=1, y_start=None):
        """Predicts a specified number of steps into the future for every time point in y-values array.
        E.g. if `steps_ahead` is 1 this produces a 1-step ahead prediction at every point in time.
        Parameters
        ----------
        y : numpy array
            Array with y-values. At every time point a prediction is made (excluding the current y)
        x : numpy array or None
            If prediciton requires inputs, provide them here
        steps_ahead : int (default 1)
            The number of steps to predict into the future at every time point
        y_start : float or None
            Starting value from which to start prediction. If None, last stored value from training will be used
        Returns
        -------
        y_predicted : numpy array
            Array of predictions at every time step of shape (times, steps_ahead)
        """

        # Check if ESN has been trained
        if self.out_weights is None or self.y_last is None:
            raise ValueError('Error: ESN not trained yet')

        # Normalize the arguments (like was done in train)
        y = self.scale(outputs=y)
        if not x is None:
            x = self.scale(inputs=x)

        # Timesteps in y
        t_steps = y.shape[0]

        # Check input
        if not x is None and not x.shape[0] == t_steps:
            raise ValueError('x has the wrong size for prediction: x.shape[0] = {}, while y.shape[0] = {}'.format(
                x.shape[0], t_steps))

        # Choose correct input
        if x is None and not self.feedback:
            #pass #raise ValueError("Error: cannot run without feedback and without x. Enable feedback or supply x")
            inputs = ones((t_steps + steps_ahead, 2), **dev) 
        elif not x is None:
            # Initialize input
            inputs = ones((t_steps, 1), **dev)  # Add bias term
            inputs = hstack((inputs, x))  # Add x inputs
        else:
            # x is None
            inputs = ones((t_steps + steps_ahead, 1), **dev)  # Add bias term
        
        # Run until we have no further inputs
        time_length = t_steps if x is None else t_steps - steps_ahead + 1

        # Set parameters
        y_predicted = zeros((time_length, steps_ahead), dtype=self.dtype, device=self.device)

        # Get last states
        previous_y = self.y_last
        if not y_start is None:
            previous_y = self.scale(outputs=y_start)[0]

        # Initialize state from last availble in train
        current_state = self.state[-1]

        # Predict iteratively
        with no_grad():
            
            for t in range(time_length):

                # State_buffer for steps ahead prediction
                prediction_state = current_state.clone().detach()
                
                # Y buffer for step ahead prediction
                prediction_y = previous_y.clone().detach()
            
                # Predict stepwise at from current time step
                for n in range(steps_ahead):
                    
                    # Get correct input based on feedback setting
                    prediction_input = inputs[t + n] if not self.feedback else hstack((inputs[t + n], prediction_y))
                    
                    # Update
                    prediction_update = self.activation_function(matmul(self.in_weights, prediction_input.T) + 
                                                   matmul(self.weights, prediction_state))
                    
                    prediction_state = self.leaking_rate * prediction_update + (1 - self.leaking_rate) * prediction_state
                    
                    # Store for next iteration of t (evolves true state)
                    if n == 0:
                        current_state = prediction_state.clone().detach()
                    
                    # Prediction. Order of concatenation is [1, inputs, y(n-1), state]
                    prediction_row = hstack((prediction_input, prediction_state))
                    if not self.backprop:
                        y_predicted[t, n] = matmul(prediction_row, self.out_weights)
                    else:
                        y_predicted[t, n] = self.LinOut.weight.T @ prediction_row[1:]
                    prediction_y = y_predicted[t, n]

                # Evolve true state
                previous_y = y[t]

        # Denormalize predictions
        y_predicted = self.descale(outputs=y_predicted)
        
        # Return predictions
        return y_predicted
    
    

    def descale(self, inputs=None, outputs=None):
        """Denormalizes array by column (along rows) using stored mean and standard deviation.

        Parameters
        ----------
        inputs : array or None
            Any inputs that need to be transformed back to their original scales
        outputs : array or None
            Any output that need to be transformed back to their original scales

        Returns
        -------
        transformed : tuple or array
            Returns tuple of every denormalized array. In case only one object is to be returned the tuple will be
            unpacked before returning

        """
        if inputs is None and outputs is None:
            raise ValueError('Inputs and outputs cannot both be None')

        # Storage for transformed variables
        transformed = []
        
        #for tensor in [train_x, train_y]:
        #     print('device',tensor.get_device())
        
        if not inputs is None:
            transformed.append((inputs * self._input_stds) + self._input_means)

        if not outputs is None:
            transformed.append((outputs * self._output_stds) + self._output_means)

        # Syntactic sugar
        return tuple(transformed) if len(transformed) > 1 else transformed[0]