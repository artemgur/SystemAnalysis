import load_data
import neural_network
import prepare_nn_results


x, y = load_data.load_data('test_data_100.csv')
#print(y)
loss, parameters = neural_network.train(x, y)
print(loss)
#send_nn_results.send(loss, parameters)
