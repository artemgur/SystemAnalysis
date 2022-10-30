# import load_data
# import neural_network
# import prepare_nn_results
#
#
# x, y = load_data.load_data('test_data_100.csv')
# #print(y)
# loss, parameters = neural_network.calculate_loss_for_weights(x, y)
# print(loss, parameters)
# #send_nn_results.send(loss, parameters)

import rsa

for i in range(200):
    print(len(rsa.public_key_hex(i)))
