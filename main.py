import json, os, hashlib, time
from getpass import getpass
from statistics import mean, median, mode, StatisticsError
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MATERIAIS_PDF = {
    
    "pensamento_computacional": os.path.join(BASE_DIR, "materiais", "pensamento_computacional.pdf"),
    "seguranca_digital": os.path.join(BASE_DIR, "materiais", "seguranca_digital.pdf"),
    "programacao_python": os.path.join(BASE_DIR, "materiais", "programacao_python.pdf")
}

def hash_password(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def load_data(file):
    caminho = os.path.join(BASE_DIR, file)
    return json.load(open(caminho, encoding="utf-8")) if os.path.exists(caminho) else {}

def save_data(file, data):
    caminho = os.path.join(BASE_DIR, file)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def cadastrar_usuario():
    users = load_data('users.json')
    usuario = input("Usuário: ").lower()
    if usuario in users:
        print("Usuário já existe.")
        return
    nome = input("Nome completo: ")
    idade = input("Idade: ")
    email = input("Email: ").lower()
    senha = getpass("Senha: ")
    users[usuario] = {"nome": nome, "idade": idade, "email": email, "senha": hash_password(senha)}
    save_data('users.json', users)
    print("Cadastro realizado com sucesso!")

def aplicar_quiz(quizzes):
    pontuacao = 0
    total_perguntas = 0
    inicio = time.time()
    for materia, perguntas in quizzes.items():
        print(f"\n--- Quiz de {materia.replace('_', ' ').title()} ---")
        for q in perguntas:
            print(f"\n{q['pergunta']}")
            for i, op in enumerate(q['opcoes']):
                print(f"{i+1}) {op}")
            escolha = int(input("Escolha (1-4): ")) - 1
            if escolha == q['resposta']:
                print("✅ Resposta correta!")
                pontuacao += 1
            else:
                print("❌ Resposta incorreta!")
            total_perguntas += 1
    fim = time.time()
    duracao = round(fim - inicio, 2)
    return pontuacao, duracao

def quiz_feedback():
    print("\n===== FEEDBACK SOBRE A PLATAFORMA =====")
    perguntas = [
        "O que você achou da navegação na plataforma?",
        "O conteúdo foi útil e fácil de entender?",
        "Você recomendaria a plataforma CodeComVoce para outras pessoas?",
        "Como você avalia a experiência geral até agora?",
    ]
    opcoes = ["(1) Péssima", "(2) Ruim", "(3) Regular", "(4) Boa", "(5) Excelente"]
    respostas = {}
    for p in perguntas:
        print(f"\n{p}")
        for op in opcoes:
            print(op)
        while True:
            try:
                escolha = int(input("Sua avaliação (1 a 5): "))
                if escolha in range(1, 6):
                    respostas[p] = escolha
                    break
                else:
                    print("Escolha um número entre 1 e 5.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    print("\nObrigado pelo seu feedback! 😊")
    return respostas

def mostrar_graficos(perf, users):
    nomes = []
    medias = []
    tempos_quiz = []
    tempos_pdf = []

    for user, resultados in perf.items():
        notas = []
        tempos = []
        pdfs = []
        for r in resultados:
            for materia, dados in r.items():
                if isinstance(dados, dict):
                    notas.append(dados.get('nota', 0))
                    tempos.append(dados.get('tempo', 0))
                    pdfs.append(dados.get('tempo_pdf', 0))
        if notas:
            nomes.append(users.get(user, {}).get("nome", user))
            medias.append(mean(notas))
            tempos_quiz.append(mean(tempos))
            tempos_pdf.append(mean(pdfs))

    if not nomes:
        print("\nNenhum dado suficiente para gerar gráficos.")
        return

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.bar(nomes, medias, color='skyblue')
    plt.title('Média de Notas')
    plt.xticks(rotation=45, ha='right')

    plt.subplot(1, 3, 2)
    plt.bar(nomes, tempos_quiz, color='orange')
    plt.title('Tempo Médio nos Quizzes (s)')
    plt.xticks(rotation=45, ha='right')

    plt.subplot(1, 3, 3)
    plt.bar(nomes, tempos_pdf, color='green')
    plt.title('Tempo Médio Leitura PDF (s)')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def gerar_relatorio():
    perf = load_data('performance.json')
    users = load_data('users.json')
    print("\n===== RELATÓRIO DE DESEMPENHO =====")
    for user, resultados in perf.items():
        notas = []
        tempos = []
        leitura_pdfs = []
        for r in resultados:
            for materia, dados in r.items():
                if isinstance(dados, dict):
                    notas.append(dados.get('nota', 0))
                    tempos.append(dados.get('tempo', 0))
                    leitura_pdfs.append(dados.get('tempo_pdf', 0))
                else:
                    notas.append(dados)
        try:
            moda_nota = mode(notas)
        except StatisticsError:
            moda_nota = "Não definida"
        media_nota = mean(notas) if notas else 0
        mediana_nota = median(notas) if notas else 0
        tempo_medio = mean(tempos) if tempos else 0
        tempo_leitura_medio = mean(leitura_pdfs) if leitura_pdfs else 0
        nome = users.get(user, {}).get("nome", "Desconhecido")
        print(f"\n--------------------------------------")
        print(f"Usuário: {nome} ({user})")
        print(f"Média: {media_nota:.2f}")
        print(f"Moda: {moda_nota}")
        print(f"Mediana: {mediana_nota}")
        print(f"Tempo médio no quiz: {tempo_medio:.2f}s")
        print(f"Tempo médio lendo PDF: {tempo_leitura_medio:.2f}s")
        print(f"--------------------------------------")

    ver_graficos = input("\nDeseja ver a performance dos alunos baseada em gráficos? (s/n): ").lower()
    if ver_graficos == 's':
        mostrar_graficos(perf, users)

def menu_conteudo(usuario):
    contents = load_data('contents.json')
    quizzes = load_data('quizzes.json')
    performance = load_data('performance.json')
    while True:
        print("\n[1] Estudar Conteúdo + Fazer Quiz\n[2] Relatório Geral\n[3] Avaliação da Plataforma\n[4] Voltar")
        opcao = input("Escolha: ")
        if opcao == '1':
            for materia, info in contents.items():
                print(f"\n--- {info['titulo']} ---")
                print(info['conteudo'])
                caminho_pdf = MATERIAIS_PDF.get(materia)
                tempo_pdf = 0
                if caminho_pdf and os.path.exists(caminho_pdf):
                    abrir = input(f"Deseja abrir o PDF de {info['titulo']}? (s/n): ").lower()
                    if abrir == 's':
                        inicio_leitura = time.time()
                        comando = f'start "" "{caminho_pdf}"' if os.name == 'nt' else f'xdg-open "{caminho_pdf}"'
                        os.system(comando)
                        input("Pressione Enter quando terminar de ler o PDF...")
                        fim_leitura = time.time()
                        tempo_pdf = round(fim_leitura - inicio_leitura, 2)
                pronto = input(f"Você está apto(a) para fazer o quiz de {info['titulo']}? (s/n): ").lower()
                if pronto == 's':
                    if materia in quizzes:
                        nota, tempo = aplicar_quiz({materia: quizzes[materia]})
                        perf = load_data('performance.json')
                        if usuario not in perf:
                            perf[usuario] = []
                        perf[usuario].append({materia: {"nota": nota, "tempo": tempo, "tempo_pdf": tempo_pdf}})
                        save_data('performance.json', perf)
                        print(f"Sua nota em {info['titulo']} foi: {nota} ponto(s) em {tempo:.2f}s (leitura PDF: {tempo_pdf:.2f}s)")
        elif opcao == '2':
            gerar_relatorio()
        elif opcao == '3':
            quiz_feedback()
        elif opcao == '4':
            break

def login():
    users = load_data('users.json')
    usuario = input("Usuário: ").lower()
    senha = getpass("Senha: ")
    if usuario in users and users[usuario]["senha"] == hash_password(senha):
        print(f"\nBem-vindo, {users[usuario]['nome']}!")
        menu_conteudo(usuario)
    else:
        print("Login ou senha incorretos.")

def menu():
    while True:
        print("\n[1] Cadastrar\n[2] Login\n[3] Sair")
        opcao = input("Escolha: ")
        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            login()
        elif opcao == '3':
            break

if __name__ == "__main__":

     menu()