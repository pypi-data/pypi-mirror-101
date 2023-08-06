# Optimizers with better performance than Adam in CIFAR-10.
## 1.Optimizers:
### a.Adam_tanh
### b.Adam_tanh2
### c.Adam_tanh3
### d.Adam_tanh_w
### e.Adam_tanh2_w
### f.Adam_tanh3_w
### g.diffGradw
## 2.use_methods:
```
pip install Adam_tanhx
```

```python
import Adam_tanhx
#Adam_tanh can be replaced by any optimizer above
optimizer = Adam_tanhx.Adam_tanh(net.parameters())
```