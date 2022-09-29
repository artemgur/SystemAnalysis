from Blockchain import Blockchain
import load_keys
import jsonpickle


#jsonpickle.set_preferred_backend('json')
#jsonpickle.set_encoder_options('json', ensure_ascii=False)


private_key = load_keys.load_private_key('private_key.pem')
blockchain = Blockchain.create("blockchain.json")
blockchain.add_block('Block 0', private_key)
blockchain.add_block('Блок 1 some text', private_key)
blockchain.add_block('2 text', private_key)
print(blockchain[1].data)
import evil

evil.change_block_data(blockchain[1], 'Данные изменены злоумышленником')
blockchain.verify(public_key=load_keys.load_public_key('public_key.pem'))
