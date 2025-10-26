questions = {
    1: "Gosto de apresentar a verdade de Deus numa forma interessante e entusiasta.",
    2: "Estou sempre pronto para colocar em posição secundária meu conforto pessoal a fim de que as necessidades alheias sejam satisfeitas.",
    3: "Tenho facilidade para explorar a verdade de um texto dentro do seu contexto.",
    4: "Procuro incentivar individualmente os que vacilam e tem problemas espirituais.",
    5: "Administro meu dinheiro, mesmo quando pouco, de modo a separar uma quantia generosa para o trabalho de Deus.",
    6: "Acho fácil delegar responsabilidades e preparar outras pessoas para realizações no campo espiritual.",
    7: "Sou muito sensível às necessidades dos outros.",
    8: "Acho fácil falar de Jesus para não crentes.",
    9: "Gosto de acompanhar cristãos para ajudá-los no seu crescimento espiritual.",
    10: "Quando tento persuadir pessoas a respeito de suas reais motivações, faço-o de modo muito convincente.",
    11: "Consigo levar pessoas a se sentirem à vontade na minha presença.",
    12: "Sinto grande impulso para descobrir conceitos bíblicos e repassá-los a outros.",
    13: "Sempre estou interessado e procuro ajudar o crescimento espiritual das pessoas e levá-las a serem ativas na obra de Deus.",
    14: "Alegro-me em dar recursos materiais, de sorte que a obra do Senhor possa ser promovida.",
    15: "Sou eficiente em supervisionar as atividades dos outros.",
    16: "Gosto de visitar pessoas hospitalizadas ou que não podem sair de casa.",
    17: "Já tive experiências de levar outros à fé em Jesus.",
    18: "Tenho experiência de levar cristãos a permanecerem firmes na fé devido ao meu acompanhamento.",
    19: "Posso apresentar a Palavra de Deus a uma congregação de pessoas com clareza a ponto de serem trazidas à luz verdades escondidas.",
    20: "Sinto-me feliz quando solicitado a dar assistência a outros na obra do Senhor sem necessariamente ser indicado para um posto de liderança.",
    21: "Sou muito interessado em apresentar conceitos bíblicos de modo bem claro, dando especial atenção a definição de palavras importantes no texto.",
    22: "Sinto-me feliz por poder tratar as pessoas feridas espiritualmente.",
    23: "Não tenho nenhum problema em confiar os meus recursos a outros para a obra do ministério.",
    24: "Posso planejar as ações de outras pessoas, com calma, e dar-lhes os detalhes que as capacitem a trabalhar com eficiência.",
    25: "Tenho grande interesse pelos que se acham envolvidos em dificuldades.",
    26: "Considero um grande problema o fato de muitos cristãos não falarem aos outros da sua fé em Jesus.",
    27: "Preocupo-me com o fato de que muitos cristãos não receberem um acompanhamento na sua vida pessoal e espiritual.",
    28: "Esforço-me grandemente para obter resultados, sempre que apresento as verdades da Palavra de Deus.",
    29: "Sinto-me bem quando proporciono um agradável acolhimento aos hóspedes.",
    30: "Sou diligente em meu estudo da Bíblia e dispenso cuidadosa atenção à necessária pesquisa, não apenas para mostrar sabedoria, mas porque eu gosto.",
    31: "Julgo poder ajudar os que têm necessidades de aconselhamento sobre problemas pessoais.",
    32: "Preocupo-me em saber que o trabalho de assistência social está sendo suprido de recursos.",
    33: "Procuro estar ciente dos recursos disponíveis para a execução das tarefas que tenho que realizar.",
    34: "Sinto-me feliz quando consigo atingir pessoas geralmente esquecidas pelos outros.",
    35: "Para mim é fácil perceber quando uma pessoa está aberta a aceitar o evangelho.",
    36: "É fácil, para mim, acompanhar pessoalmente um grupo de cristãos e me empenhar pela sua unidade.",
    37: "Verifico que minha pregação leve pessoas a um ponto de decisão definido.",
    38: "Gosto de aliviar a carga das pessoas que ocupam uma posição-chave, de sorte que possam esforçar-se mais em tarefas a elas concernentes.",
    39: "Posso explicar bem como a Bíblia mantém sua unidade.",
    40: "Sou agudamente consciente das coisas que impedem as pessoas em seu desenvolvimento espiritual e anseio por ajudá-las a vencer seus problemas.",
    41: "Sou cuidadoso com a questão de dinheiro e oro continuamente acerca de sua distribuição adequada na obra do Senhor.",
    42: "Tenho objetivos bem definidos e consigo levar outros a assumirem meus objetivos.",
    43: "Posso relacionar-me com outras pessoas emocionalmente e me disponho a ajudá-las quando for necessário.",
    44: "Estou disposto a frequentar um curso preparatório para o evangelismo.",
    45: "Estou disposto a assumir a responsabilidade por um grupo de irmãos.",
}

gifts = {
    "A": [1, 10, 19, 28, 37],
    "B": [2, 11, 20, 29, 38],
    "C": [3, 12, 21, 30, 39],
    "D": [4, 13, 22, 31, 40],
    "E": [5, 14, 23, 32, 41],
    "F": [6, 15, 24, 33, 42],
    "G": [7, 16, 25, 34, 43],
    "H": [8, 17, 26, 35, 44],
    "I": [9, 18, 27, 36, 45],
}

# Gift names/descriptions (optional)
gift_names = {
    "A": "Profecia",
    "B": "Serviço",
    "C": "Ensino",
    "D": "Exortação",
    "E": "Contribuição",
    "F": "Liderança",
    "G": "Misericórdia",
    "H": "Evangelista",
    "I": "Pastor",
}


class QuizScorer:
    """
    Efficient quiz scorer for spiritual gifts assessment.

    Time Complexity: O(1) per answer update
    Space Complexity: O(g + q) where g=gifts, q=questions
    """

    def __init__(self, gifts_config):
        self.gifts_config = gifts_config
        self.answers = {}  # question_num -> score (0-3)
        self.scores = {gift: 0 for gift in gifts_config.keys()}

        # Build inverted index: question -> [gifts]
        # This allows O(1) updates when answering questions
        self.question_to_gifts = {}
        for gift, question_list in gifts_config.items():
            for q in question_list:
                if q not in self.question_to_gifts:
                    self.question_to_gifts[q] = []
                self.question_to_gifts[q].append(gift)

    def answer_question(self, question_num, value):
        """
        Answer a question with a value from 0-3.
        Updates affected gift scores incrementally.

        Args:
            question_num: int (1-45)
            value: int (0-3)
        """
        if not (1 <= question_num <= 45):
            raise ValueError(f"Question number must be 1-45, got {question_num}")
        if not (0 <= value <= 3):
            raise ValueError(f"Answer value must be 0-3, got {value}")

        # Get previous value (if answered before)
        old_value = self.answers.get(question_num, 0)
        self.answers[question_num] = value

        # Update only affected gifts (O(1) - typically 1 gift per question)
        delta = value - old_value
        for gift in self.question_to_gifts[question_num]:
            self.scores[gift] += delta

    def batch_answer(self, answers_dict):
        """
        Answer multiple questions at once.

        Args:
            answers_dict: dict {question_num: value}
        """
        for q_num, value in answers_dict.items():
            self.answer_question(q_num, value)

    def get_scores(self):
        """Get all gift scores as dictionary."""
        return self.scores.copy()

    def get_ranked_results(self):
        """
        Get gifts ranked by score (highest first).

        Returns:
            list of tuples: [(gift, score), ...]
        """
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)

    def get_top_gift(self):
        """
        Get the highest scoring gift.

        Returns:
            tuple: (gift, score)
        """
        return max(self.scores.items(), key=lambda x: x[1])

    def get_top_n_gifts(self, n=3):
        """
        Get top N gifts by score.

        Args:
            n: number of top gifts to return

        Returns:
            list of tuples: [(gift, score), ...]
        """
        return self.get_ranked_results()[:n]

    def get_progress(self):
        """
        Get quiz completion progress.

        Returns:
            dict: {
                'answered': int,
                'total': int,
                'percentage': float
            }
        """
        answered = len(self.answers)
        total = 45
        return {
            "answered": answered,
            "total": total,
            "percentage": (answered / total) * 100,
        }

    def reset(self):
        """Reset all answers and scores."""
        self.answers = {}
        self.scores = {gift: 0 for gift in self.gifts_config.keys()}

    def validate_config(self):
        """
        Validate that gift configuration covers all 45 questions exactly once.

        Returns:
            dict: validation results
        """
        all_questions = []
        for questions_list in self.gifts_config.values():
            all_questions.extend(questions_list)

        all_questions_set = set(all_questions)
        expected_questions = set(range(1, 46))

        return {
            "valid": all_questions_set == expected_questions,
            "total_mappings": len(all_questions),
            "unique_questions": len(all_questions_set),
            "missing": expected_questions - all_questions_set,
            "duplicates": len(all_questions) - len(all_questions_set),
        }


# Helper function for batch calculation (if you have all answers)
def calculate_scores_batch(answers, gifts_config):
    """
    Calculate scores directly from complete answers.
    Use when you have all answers upfront (simpler but less flexible).

    Args:
        answers: dict {question_num: value}
        gifts_config: dict {gift: [question_numbers]}

    Returns:
        dict: {gift: score}

    Time Complexity: O(n) where n = total question mappings (45)
    """
    scores = {}
    for gift, question_list in gifts_config.items():
        scores[gift] = sum(answers.get(q, 0) for q in question_list)
    return scores


def save_progress(name, scorer, filename="quiz_progress.json"):
    """
    Save user progress to a JSON file.

    Args:
        name: User's name
        scorer: QuizScorer instance with current progress
        filename: File to save progress to
    """
    import json
    import os
    from datetime import datetime

    # Load existing data or create new
    data = {}
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

    # Save user's progress
    data[name] = {
        "answers": scorer.answers,
        "scores": scorer.scores,
        "last_updated": datetime.now().isoformat(),
        "completed": len(scorer.answers) == 45,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_progress(name, filename="quiz_progress.json"):
    """
    Load user progress from JSON file.

    Args:
        name: User's name
        filename: File to load progress from

    Returns:
        dict with 'answers' and 'scores', or None if not found
    """
    import json
    import os

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(name)
    except:
        return None


def run_interactive_quiz():
    """
    Run an interactive quiz session where user answers all 45 questions.
    Supports saving progress and resuming from where user left off.
    """
    print("=" * 80)
    print("BEM-VINDO AO TESTE DE DONS ESPIRITUAIS")
    print("=" * 80)

    # Ask for user's name
    print("\nPor favor, digite seu nome:")
    user_name = input("Nome: ").strip()

    if not user_name:
        print("❌ Nome não pode estar vazio.")
        return

    print(f"\nOlá, {user_name}! 👋\n")

    # Check for existing progress
    scorer = QuizScorer(gifts)
    start_question = 1

    saved_progress = load_progress(user_name)

    if saved_progress and not saved_progress.get("completed", False):
        num_answered = len(saved_progress["answers"])
        print(f"📋 Encontramos um questionário em andamento!")
        print(f"   Você respondeu {num_answered} de 45 perguntas.")
        print()

        while True:
            choice = input("Deseja continuar de onde parou? (s/n): ").strip().lower()
            if choice in ["s", "sim", "y", "yes"]:
                # Load previous answers
                scorer.answers = {
                    int(k): v for k, v in saved_progress["answers"].items()
                }
                scorer.scores = saved_progress["scores"]
                start_question = (
                    max(int(k) for k in saved_progress["answers"].keys()) + 1
                )
                print(f"\n✓ Continuando da pergunta {start_question}...\n")
                break
            elif choice in ["n", "não", "nao", "no"]:
                print("\n✓ Iniciando novo questionário...\n")
                break
            else:
                print("❌ Por favor, responda 's' para sim ou 'n' para não.")
    elif saved_progress and saved_progress.get("completed", False):
        print(f"✓ Você já completou este questionário anteriormente!")
        print()
        while True:
            choice = input("Deseja refazer o questionário? (s/n): ").strip().lower()
            if choice in ["s", "sim", "y", "yes"]:
                print("\n✓ Iniciando novo questionário...\n")
                break
            elif choice in ["n", "não", "nao", "no"]:
                print("\n✓ Até logo!")
                return
            else:
                print("❌ Por favor, responda 's' para sim ou 'n' para não.")

    print("\nResponda cada pergunta com um número de 0 a 3:")
    print("  3 = Descreve-me de forma correta")
    print("  2 = É uma tendência minha")
    print("  1 = Tenho pequena inclinação para isto")
    print("  0 = Não tem nada a ver comigo")
    print("\nComandos especiais:")
    print("  'voltar' ou 'v' = Voltar para a pergunta anterior")
    print("  'sair' ou 'q' = Salvar progresso e sair")
    print("\n" + "=" * 80 + "\n")

    # Ask all 45 questions
    question_num = start_question
    while question_num <= 45:
        while True:
            print(f"\nPergunta {question_num} de 45:")
            print(f"{questions[question_num]}")

            # Show previous answer if exists
            if question_num in scorer.answers:
                prev_answer = scorer.answers[question_num]
                print(f"(Resposta anterior: {prev_answer})")

            print()

            try:
                answer = input("Sua resposta (0-3): ").strip().lower()

                # Allow user to go back
                if answer in ["voltar", "v", "back"]:
                    if question_num > 1:
                        question_num -= 1
                        print(f"\n⬅️  Voltando para a pergunta {question_num}...")
                        break
                    else:
                        print("❌ Você já está na primeira pergunta.")
                        continue

                # Allow user to quit
                if answer in ["q", "quit", "sair"]:
                    print("\n💾 Salvando progresso...")
                    save_progress(user_name, scorer)
                    print("✓ Progresso salvo! Você pode continuar mais tarde.")
                    return

                answer_value = int(answer)

                if 0 <= answer_value <= 3:
                    scorer.answer_question(question_num, answer_value)
                    # Save progress after each answer
                    save_progress(user_name, scorer)
                    question_num += 1
                    break
                else:
                    print("❌ Por favor, digite um número entre 0 e 3.")
            except ValueError:
                print(
                    "❌ Entrada inválida. Digite um número (0-3), 'voltar' ou 'sair'."
                )

        # Show progress every 9 questions (each gift cycle)
        if question_num > 1 and (question_num - 1) % 9 == 0:
            progress = scorer.get_progress()
            print(f"\n{'─' * 60}")
            print(
                f"📊 Progresso: {progress['answered']}/45 ({progress['percentage']:.0f}%)"
            )
            print(f"{'─' * 60}")

    # Quiz completed - save final progress
    save_progress(user_name, scorer)

    # Show results
    print("\n" + "=" * 80)
    print("QUESTIONÁRIO COMPLETO!")
    print("=" * 80)

    print("\n📊 SEUS RESULTADOS:\n")
    print(f"Participante: {user_name}\n")

    # Show all scores ranked
    ranked_results = scorer.get_ranked_results()
    max_score = max(score for _, score in ranked_results) if ranked_results else 0

    for rank, (gift, score) in enumerate(ranked_results, 1):
        gift_name = gift_names.get(gift, gift)
        # Create a simple bar chart
        bar_length = int((score / 15) * 30) if max_score > 0 else 0  # Max is 15
        bar = "█" * bar_length
        print(f"{rank}. {gift} - {gift_name:15s}: {score:2d} pontos {bar}")

    # Highlight top 3
    print("\n" + "=" * 80)
    print("🏆 SEUS PRINCIPAIS DONS ESPIRITUAIS:")
    print("=" * 80)

    top_3 = scorer.get_top_n_gifts(3)
    for rank, (gift, score) in enumerate(top_3, 1):
        gift_name = gift_names.get(gift, gift)
        emoji = ["🥇", "🥈", "🥉"][rank - 1]
        print(f"{emoji} {rank}º lugar: {gift_name} ({gift}) - {score} pontos")

    print("\n" + "=" * 80)
    print(f"Obrigado por participar, {user_name}!")
    print("💾 Seus resultados foram salvos.")
    print("=" * 80 + "\n")

    return scorer


# Example usage
if __name__ == "__main__":
    # Run the interactive quiz
    run_interactive_quiz()
