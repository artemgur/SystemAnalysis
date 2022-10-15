import rsa


def format_float(number):
    return f'{number:.12f}'.rstrip('0')


def __append_number(str_builder, number):
    str_builder.append(f'"{format_float(number)}",')


def nn_results_to_string(loss, parameters):
    str_builder = ['{']
    for source_neuron in range(2):
        for layer_neuron in range(2):
            str_builder.append(f'"w{source_neuron + 1}{layer_neuron + 1}":')
            __append_number(str_builder, parameters[0][layer_neuron, source_neuron])

    for source_neuron in range(2):
        for layer_neuron in range(3):
            str_builder.append(f'"v{source_neuron + 1}{layer_neuron + 1}":')
            __append_number(str_builder, parameters[1][layer_neuron, source_neuron])

    for source_neuron in range(3):
        str_builder.append(f'"w{source_neuron + 1}":')
        __append_number(str_builder, parameters[2][0, source_neuron])

    str_builder.append('"e":')
    __append_number(str_builder, loss)

    str_builder.append('"publickey":"')
    str_builder.append(rsa.public_key_hex())
    str_builder.append('"}')

    result = ''.join(str_builder)

    return result
