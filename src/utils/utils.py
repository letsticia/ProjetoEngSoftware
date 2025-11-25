from src.db.supabase_class import SupabaseClient

sb_client = SupabaseClient()

def questao_sequencial(indice):
    data = sb_client.client.table("questoes").select("*").eq("tipo", "sequencial").execute()

    data.data.sort(key=lambda x: x['id_questao'])
    
    questao_dados = data.data[indice]

    opcoes = []
    for i in range(1, 5):
        opcoes.append(questao_dados[f'resposta{i}'])

    resposta_correta = []
    for numero in str(questao_dados['resposta_correta']):
        resposta_correta.append(questao_dados[f'resposta{numero}'])
    from src.telas.questoes.sequencial import Sequencial
    questao = Sequencial(
        enunciado=questao_dados['enunciado'],
        opcoes=opcoes,
        resposta_correta=resposta_correta
    )
    return questao

def questao_quiz(indice):
    data = sb_client.client.table("questoes").select("*").eq("tipo", "quiz").execute()
    questao_dados = data.data[indice]

    opcoes = []
    for i in range(1, 5):
        opcoes.append(questao_dados[f'resposta{i}'])

    index_resposta_correta = questao_dados['resposta_correta']
    resposta_correta = questao_dados[f'resposta{index_resposta_correta}']
    from src.telas.questoes.quiz import Quiz
    questao = Quiz(
        enunciado=questao_dados['enunciado'],
        opcoes=opcoes,
        resposta_correta=resposta_correta
    )
    return questao


