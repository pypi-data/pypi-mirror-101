from keras.optimizers import Optimizer
import keras.backend as K
from keras.legacy import interfaces


class SGD(Optimizer):

    def __init__(self, learning_rate=0.01, momention=0., nesterov=False, **kwargs):
        learning_rate = kwargs.pop('lr', learning_rate)
        self.initial_decay = kwargs.pop('decay', 0.0)
        super(SGD, self).__init__(**kwargs)
        with K.name_scope(self.__class__.__name__):
            self.interations = K.variable(0, dtype='int64', name='iterations')
            self.learning_rate = K.variable(learning_rate, name='learning_rate')
            self.momentum = K.variable(momention, name='momentum')
            self.decay = K.variable(self.initial_decay, name='decay')
        self.nesterov = nesterov

    @interfaces.legacy_get_updates_support
    @K.symbolic
    def get_updates(self, loss, params):
        grads = K.gradients(loss, params)
        self.updates = [K.update_add(self.interations, 1)]

        lr = self.learning_rate
        if self.initial_decay > 0:
            lr = lr * (1. / (1. + self.decay * K.cast(self.interations, K.dtype(self.decay))))
        # momention
        shapes = [K.int_shape(p) for p in params]
        momentums = [K.zeros(shape, name='moment_' + str(i)) for (i, shape) in enumerate(shapes)]
        self.weights = [self.interations] + momentums
        for p, g, m in zip(params, grads, momentums):
            v = self.momentum * m - lr * g
            self.updates.append(K.update(m, v))

            if self.nesterov:
                new_p = p + self.momentum * v - lr * g
            else:
                new_p = p + v
            if getattr(p, 'constraint', None) is not None:
                new_p = p.constraint(new_p)

            self.updates.append(K.update(p, new_p))

    def get_config(self):
        config = {
            'learning_rate': float(K.get_value(self.learning_rate)),
            'momentum': float(K.get_value(self.momentum)),
            'decay': float(K.get_value(self.decay)),
            'nestrov': float(K.get_value(self.nesterov))
        }
        base_config = super(SGD, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class Adam(Optimizer):

    def __init__(self, learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False, **kwargs):
        self.initial_decay = kwargs.pop('decay', 0.0)
        self.epsilon = kwargs.pop('epsilon', K.epsilon())
        learning_rate = kwargs.pop('lr', learning_rate)
        super(Adam, self).__init__(**kwargs)
        with K.name_scope(self.__class__.__name__):
            self.iterations = K.variable(0, dtype='int64', name='iterations')
            self.learning_rate = K.variable(learning_rate, name='learning_rate')
            self.beta_1 = K.variable(beta_1, name=beta_1)
            self.beta_2 = K.variable(beta_2, name=beta_2)
            self.decay = K.variable(self.initial_decay, name='decay')
        self.asmgrad = amsgrad

    @interfaces.legacy_get_updates_support
    @K.symbolic
    def get_updates(self, loss, params):
        grads = K.gradients(loss, params)
        self.updates = [K.update(self.iterations, 1)]

        lr = self.learning_rate
        if self.initial_decay > 0:
            lr = lr * (1. / (1. + self.decay * K.cast(self.iterations, K.dtype(self.decay))))
        t = K.cast(self.iterations, K.floatx()) + 1
        lr_t = lr * (K.sqrt(1. - K.pow(self.beta_2, t)) / (1. - K.pow(self.beta_1, t)))

        ms = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='m_' + str(i)) for (i, p) in enumerate(params)]
        vs = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='n_' + str(i)) for (i, p) in enumerate(params)]

        if self.asmgrad:
            vhats = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='vhat_' + str(i)) for (i, p) in enumerate(params)]
        else:
            vhats = [K.zeros(1, name='vhat_' + str(i)) for (i, p) in enumerate(params)]
        self.weights = [self.iterations] + ms + vs + vhats

        for p, g, m, v, vhat in zip(params, grads, ms, vs, vhats):
            m_t = (self.beta_1 * m) + (1 - self.beta_1) * g
            v_t = (self.beta_2 * v) + (1 - self.beta_2) * K.square(g)

            if self.asmgrad:
                vhat_t = K.maximum(vhat, v_t)
                p_t = p - lr_t * m_t / (K.sqrt(vhat_t) + self.epsilon)
                self.updates.append(K.update(vhat,vhat_t))
            else:
                p_t = p - lr_t * m_t /(K.sqrt(v_t) + self.epsilon)

            self.updates.append(K.update(m,m_t))
            self.updates.append(K.update(v,v_t))

            if getattr(p, 'contraint',None) is not None:
                new_p = p.contraint(new_p)
            self.updates.append(K.update(p,new_p))

        return self.updates

    def get_config(self):
        config = {
            'learning_rate':float(K.get_value(self.learning_rate)),
            'beta_1': float(K.get_value(self.beta_1)),
            'beta_2': float(K.get_value(self.beta_2)),
            'decay': float(K.get_value(self.decay)),
            'epsilon': self.epsilon,
            'amsgrad': self.asmgrad
        }
        base_config = super(Adam, self).get_config()
        return dict(list(base_config.items())+list(config.items()))