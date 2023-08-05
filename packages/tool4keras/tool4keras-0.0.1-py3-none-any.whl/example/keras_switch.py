import keras.backend as K

pred = K.placeholder([], dtype='bool')
count = K.variable(0)
x = K.switch(condition=pred, then_expression=lambda: K.update_add(count, 0),
             else_expression=lambda: K.update_add(count, 1))
f = K.function(inputs=[pred], outputs=[x])

print(f([True]))
print(f([False]))