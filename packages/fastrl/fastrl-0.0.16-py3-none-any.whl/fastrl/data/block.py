# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_data.block.ipynb (unless otherwise specified).

__all__ = ['source_events', 'Src', 'SrcCallback', 'GymSrc']

# Cell
# Python native modules
import os
from collections import deque
from time import sleep
# Third party libs
from fastcore.all import *
from fastai.torch_basics import *
from fastai.data.all import *
from fastai.basics import *
from torch.utils.data import Dataset
from torch import nn
import torch
import gym
import numpy as np
# Local modules
from ..core import *
from ..callback.core import *
from ..agent import *

# Cell
_events=L.split('create reset do_action do_step render history episodes initialize')
_events= _events.map(lambda s:'before_'+s) + _events.map(lambda s:'after_'+s)+_events.map(lambda s:'after_cancel_'+s)
_events+=L.split('reset do_step render initialize history do_action')

mk_class('source_events', **_events.map_dict(),
         doc="All possible events as attributes to get tab-completion and typo-proofing")

#nbdev_comment _all_=['source_events']

_loop=L(['Start Setup','before_initialize','initialize','after_initialize','End Setup',
             'before_episodes',
             'Start Episodes','before_reset','reset','after_reset',
                 'before_do_action','do_action','after_do_action',
                 'before_do_step','do_step','after_do_step',
                 'before_render','render','after_render',
                 'before_history','history','after_history',
             'End Episodes',
             'after_episodes'
             ])
_default_shapes={'done':(1,1),'step':(1,1),'env_id':(1,1)}

# Cell
class Src(Loop):
    _loop=_loop
    _events=source_events
    _default='source'
    end_event='after_episodes'
    initial_experience_flds='done step state next_state env_id'

    @delegates(Loop)
    def __init__(self,env:object,agent=None,n_envs:int=1,steps_count:int=1,steps_delta:int=1,
                 seed:int=None,mode=None,num_workers=0,but='',cbs=None,shape_map=None,**kwargs):
        super().__init__(cbs=cbs,**kwargs)
        store_attr(but='cbs,shape_map')
        self.env_kwargs=kwargs
        self.pool=L()
        self.histories=L()
        self.current_history=L()
        self.shape_map=merge(_default_shapes,ifnone(shape_map,{}))
        self.all_exp:BD=None
        self.imask=torch.zeros((1,))
        if self.mode is None: self.but+=',image'
        # Fields
        self.done=None
        self.step=None
        self.env_id=None

    def _init_state(self):     self('initialize')
    def _do_reset(self):       self('reset')
    def _do_action(self):      self('do_action')
    def _do_step(self):        self('do_step')
    def _do_render(self):      self('render')
    def process_history(self,history):
        self.current_history=history
        self('history')
        return self.current_history

    def yield_histories(self):
        self('before_history')
        for i,idx in enumerate(self.imask.nonzero().reshape(-1,)):
            self.histories[idx].append(self.active_exp()[i])
            if len(self.histories[idx])==self.steps_count and int(self.step[i])%self.steps_delta==0:
                yield self.process_history(sum(self.histories[idx]))
            if bool(self.done.reshape(-1,)[i]):
                if 0<len(self.histories[idx])<self.steps_count:
                    yield self.process_history(sum(self.histories[idx]))
                while len(self.histories[idx])>1:
                    self.histories[idx].popleft()
                    yield self.process_history(sum(self.histories[idx]))
        self('after_history')

    def active_exp(self,bs=None):
        return BD({k:TensorBatch(getattr(self,k),bs=ifnone(bs,self.imask.sum()))
                   for k in self.shape_map})

    def __iter__(self):
        "Iterates through a list of environments."
        if not self.pool:self._with_events(self._init_state,'initialize',Exception)
        self('before_episodes')
        while True:
            self._with_events(self._do_reset,'reset',Exception)
            self._with_events(self._do_action,'do_action',Exception)
            self._with_events(self._do_step,'do_step',Exception)
            if self.mode is not None: self._with_events(self._do_render,'render',Exception)
            yield from self.yield_histories()
        self('after_episodes')

# Cell
class SrcCallback(LoopCallback):
    _default='source'
    _methods=_events

    def after_cancel_initialize(self):raise
    def after_cancel_step(self):      raise
    def after_cancel_do_action(self):    raise
    def after_cancel_do_step(self):      raise
    def after_cancel_episodes(self):  raise
    def after_cancel_episode(self):   raise
    def after_cancel_history(self):   raise
    def after_cancel_render(self):    raise
    def after_cancel_create(self):    raise
    def after_cancel_reset(self):     raise

# Cell
def _add_batch(t):
    if len(t)==1: return (1,t[0])
    elif t[0]!=1: return (1,*t)
    return t

def _fix_shape_map(t:Tensor,expected_shape,bs=None):
    if not hasattr(t,'shape'): t=Tensor([t])
    if bs is not None: expected_shape=(bs,*expected_shape[1:])
    if expected_shape!=tuple(t.shape):
        if isinstance(t,np.ndarray): t=Tensor(t)
        t=t.unsqueeze(0)
        test_eq(expected_shape,t.shape)
    return t

def _env_seed(o,seed): return o.seed(seed)

def _env_reset(o,shape_map=None):
    state=o.reset()
    return _fix_shape_map(state,shape_map['state'])

def _env_render(o,mode='rgb_array',shape_map=None):
    image=o.render(mode=mode).copy()
    if shape_map is None: return image
    return _fix_shape_map(image,shape_map['image'])

def _env_step(o,*args,shape_map=None,**kwargs):
    s,r,d,info=o.step(*args,**kwargs)
    s=_fix_shape_map(s,shape_map['state'])
    r=_fix_shape_map(r,shape_map['reward'])
    d=_fix_shape_map(d,shape_map['done'])
    return (s,r,d,info)

def _batchwise_zero(shape,bs): return torch.zeros((bs,*shape[1:]))


class GymSrc(SrcCallback):
    def initialize(self):
        self.source.histories,self.source.pool=L((deque(maxlen=self.steps_count),
                          gym.make(self.env,**self.env_kwargs))
                          for _ in range(self.n_envs)).zip().map(L)
        self.source.pool.map(_env_seed,seed=self.seed)
        if self.source.agent is None:
            test_cb=TstCallback(action_space=self.pool[0].action_space)
            self.source.agent=Agent(cbs=test_cb)
       # Extra fields
        self.source.next_state=None
        self.source.state=None
        self.source.image=None
        self.source.action=None

        self.init_shapes()

        self('reset')
        if self.mode is not None: self.init_render_shapes()
        self.source.imask=torch.zeros((self.n_envs,)).bool()

    def init_render_shapes(self):
        "Set the image shapes with a batch dim."
        image_shape=_env_render(self.pool[0],self.mode).shape
        self.shape_map['image']=_add_batch(image_shape)

    def init_shapes(self):
        "Set the reward shape, state shapes."
        self.shape_map['reward']=(1,1)
        obs_shape=_add_batch(self.pool[0].observation_space.shape)
        for k in ('state','next_state'): self.shape_map[k]=obs_shape

    def reset(self):
        if self.imask.sum()==0:
            reset_exps=D(self.shape_map).mapv(_batchwise_zero,bs=self.n_envs)
            for k,v in reset_exps.items(): setattr(self.source,k,v)
            self.source.state=self.pool.map(_env_reset,shape_map=self.shape_map)
            self.source.state=TensorBatch.vstack(tuple(self.state))
            self.source.done=self.source.done.bool()
            self.source.env_id=self.source.env_id.long()

    def after_reset(self):
        if self.imask.sum()==0:
            self.source.all_exp=deepcopy(self.active_exp(self.n_envs))
            self.source.imask=torch.ones((self.n_envs,)).bool()

    def do_action(self):
        self.source.action,exp=self.agent.do_action(**self.active_exp())
        for k in exp: setattr(self.source,k,exp[k])

    def do_step(self):
        step_res=self.pool[self.imask].zipwith(self.action).starmap(_env_step,shape_map=self.shape_map)
        next_states,rewards,dones=step_res.zip()[:3]
        self.source.next_state=TensorBatch.vstack(next_states)
        self.source.reward=TensorBatch.vstack(rewards)
        self.source.done=TensorBatch.vstack(dones).bool()
        self.source.env_id=TensorBatch(self.imask.nonzero().reshape(-1,1),bs=self.imask.sum()).long()

    def after_history(self):
        self.source.step+=1
        active_exp=self.active_exp()
        for k in self.all_exp: self.all_exp[k][self.imask]=active_exp[k]
        self.source.imask=~self.all_exp['done'].reshape(-1,)
        for k in self.all_exp:setattr(self.source,k,self.all_exp[k][self.imask])