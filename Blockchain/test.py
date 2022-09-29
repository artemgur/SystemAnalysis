# import jsonpickle
#
# with open('blockchain.json', 'r') as file:
#     for line in file.readlines():
#         print(jsonpickle.decode(line.rstrip()).data)

from Blockchain import Blockchain
import jsonpickle

#jsonpickle.set_preferred_backend('json')
#jsonpickle.set_encoder_options('json', ensure_ascii=False)


blockchain = Blockchain.load_from_file("blockchain.json")
print(blockchain[1].data.decode('utf-8'))
1