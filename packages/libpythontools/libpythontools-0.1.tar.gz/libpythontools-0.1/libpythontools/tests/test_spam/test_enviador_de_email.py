from libpythontools.spam.enviador_de_email import Enviador


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


def test_remetente():
    enviador = Enviador()
    resultado = enviador.enviar(
        'deivisondamiao01@outlook.com',
        'deivison.ds1999@gmail.com',
        'Curso Python Pro',
        'Ultima turma liberada.'
    )
    assert 'deivisondamiao01@outlook.com' in resultado
