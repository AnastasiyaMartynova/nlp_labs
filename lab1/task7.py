import re
import random

class ElizaProductivityCoach:
    def __init__(self):
        self.rules = [
            # Правила для работы с эмоциональным состоянием
            {
                'pattern': r'.*\b(i am|i\'m)\s+(depressed|sad|tired|exhausted|overwhelmed).*',
                'responses': [
                    r"I'M SORRY TO HEAR YOU ARE \2. LET'S DISCUSS WHAT'S CAUSING THIS FEELING.",
                    r"WHY DO YOU THINK YOU ARE \2? THIS COULD BE RELATED TO YOUR PRODUCTIVITY.",
                    r"BEING \2 CAN AFFECT YOUR FOCUS. HOW CAN WE ADDRESS THIS TOGETHER?"
                ]
            },
            {
                'pattern': r'.*\b(i am|i\'m)\s+(stressed|anxious|worried|nervous).*',
                'responses': [
                    r"STRESS AND ANXIETY OFTEN HINDER PRODUCTIVITY. LET'S FIND WAYS TO MANAGE YOUR \2 FEELINGS.",
                    r"WHEN YOU FEEL \2, IT'S IMPORTANT TO IDENTIFY THE SOURCE. WHAT'S MAKING YOU FEEL THIS WAY?",
                    r"MANAGING \2 FEELINGS IS KEY TO MAINTAINING FOCUS. CAN YOU TELL ME MORE?"
                ]
            },
            
            # С целями и потребностями
            {
                'pattern': r'.*\b(i need)\s+(.*)',
                'responses': [
                    r"WHY DO YOU NEED \2? UNDERSTANDING THIS CAN HELP WITH PRIORITIZATION.",
                    r"LET'S EXPLORE WHY \2 IS IMPORTANT FOR YOUR PRODUCTIVITY.",
                    r"HAVING A CLEAR NEED FOR \2 CAN GUIDE YOUR PLANNING. WHAT'S THE URGENCY?"
                ]
            },
            {
                'pattern': r'.*\b(i want)\s+(.*)',
                'responses': [
                    r"WHY DO YOU WANT \2? UNDERSTANDING YOUR MOTIVATION CAN IMPROVE FOCUS.",
                    r"DESIRING \2 IS A START. WHAT STEPS ARE YOU TAKING TO ACHIEVE THIS?",
                    r"WANTING \2 CAN BE A GOOD MOTIVATOR. HOW DOES THIS ALIGN WITH YOUR GOALS?"
                ]
            },
            
            #С временными аспектами
            {
                'pattern': r'.*\b(always|never|constantly)\s+.*',
                'responses': [
                    r"USING WORDS LIKE '\1' CAN INDICATE ALL-OR-NOTHING THINKING. CAN YOU BE MORE SPECIFIC?",
                    r"EXTREME LANGUAGE LIKE '\1' OFTEN DISTORTS REALITY. WHAT'S A MORE NUANCED PERSPECTIVE?",
                    r"WHEN YOU SAY '\1', WHAT SPECIFIC EXAMPLES COME TO MIND?"
                ]
            },
            {
                'pattern': r'.*\b(procrastinat|delay|postpone|put off).*',
                'responses': [
                    r"PROCRASTINATION IS A COMMON PRODUCTIVITY CHALLENGE. WHAT'S CAUSING YOU TO DELAY?",
                    r"DELAYING TASKS OFTEN HAS UNDERLYING REASONS. WHAT FEELINGS COME UP WHEN YOU THINK ABOUT STARTING?",
                    r"LET'S BREAK DOWN WHAT YOU'RE PUTTING OFF INTO SMALLER, MANAGEABLE STEPS."
                ]
            },
            
            # С причинами и объяснениями
            {
                'pattern': r'.*\b(because)\s+(.*)',
                'responses': [
                    r"IS '\2' THE PRIMARY REASON, OR ARE THERE OTHER FACTORS?",
                    r"UNDERSTANDING YOUR REASONING HELPS WITH PROBLEM-SOLVING. TELL ME MORE ABOUT '\2'.",
                    r"THAT EXPLANATION GIVES US CLUES. HOW DOES '\2' AFFECT YOUR PRODUCTIVITY?"
                ]
            },
            
            # С отношениями и окружением
            {
                'pattern': r'.*\b(my)\s+(manager|boss|supervisor|team|colleague)\s+(.*)',
                'responses': [
                    r"WORK RELATIONSHIPS SIGNIFICANTLY IMPACT PRODUCTIVITY. HOW DOES YOUR \2 AFFECT YOUR WORK?",
                    r"YOUR \2 SEEMS TO INFLUENCE YOUR WORKFLOW. WHAT SPECIFIC CHALLENGES ARE YOU FACING?",
                    r"LET'S DISCUSS STRATEGIES FOR WORKING EFFECTIVELY WITH YOUR \2."
                ]
            },
            {
                'pattern': r'.*\b(family|mother|father|parents|spouse|partner)\s+(.*)',
                'responses': [
                    r"FAMILY DYNAMICS CAN AFFECT WORK-LIFE BALANCE. HOW IS THIS IMPACTING YOUR PRODUCTIVITY?",
                    r"TELL ME MORE ABOUT HOW YOUR \1 RELATIONSHIPS INFLUENCE YOUR DAILY ROUTINE.",
                    r"BALANCING \1 AND WORK RESPONSIBILITIES IS CHALLENGING. WHAT SUPPORT DO YOU NEED?"
                ]
            },
            
            # С конкретными задачами
            {
                'pattern': r'.*\b(can\'t|cannot)\s+(.*)',
                'responses': [
                    r"WHEN YOU SAY YOU CAN'T \2, WHAT SPECIFIC OBSTACLES ARE YOU FACING?",
                    r"LET'S REFRAME 'CAN'T \2' INTO 'HAVEN'T YET FOUND A WAY TO \2'.",
                    r"WHAT RESOURCES OR SUPPORT WOULD HELP YOU \2?"
                ]
            },
            {
                'pattern': r'.*\b(too much|overwhelming|impossible)\s+.*',
                'responses': [
                    r"WHEN THINGS FEEL OVERWHELMING, BREAKING THEM DOWN HELPS. WHAT'S THE FIRST SMALL STEP?",
                    r"LET'S PRIORITIZE. WHAT'S THE MOST IMPORTANT THING TO FOCUS ON RIGHT NOW?",
                    r"OVERWHELM OFTEN COMES FROM UNCLEAR PRIORITIES. WHAT CAN YOU DELEGATE OR POSTPONE?"
                ]
            }
        ]
        
        # Нейтральные ответы для фолбэка
        self.fallback_responses = [
            "PLEASE, GO ON. TELL ME MORE ABOUT YOUR PRODUCTIVITY CHALLENGES.",
            "I SEE. HOW DOES THIS RELATE TO YOUR DAILY PRODUCTIVITY?",
            "THAT'S INTERESTING. WHAT IMPACT DOES THIS HAVE ON YOUR WORK?",
            "LET'S FOCUS ON HOW THIS AFFECTS YOUR PRODUCTIVITY. CAN YOU ELABORATE?",
            "UNDERSTOOD. WHAT WOULD YOU LIKE TO ACHIEVE IN TERMS OF PRODUCTIVITY?"
        ]
    
    def reflect_pronouns(self, text):
        #Отражает местоимения для создания эхо-ответов
        reflections = {
            'i': 'YOU', 'me': 'YOU', 'my': 'YOUR', 'mine': 'YOURS',
            'you': 'I', 'your': 'MY', 'yours': 'MINE',
            'am': 'ARE', 'are': 'AM', 'was': 'WERE', 'were': 'WAS'
        }
        
        words = text.lower().split()
        reflected_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in reflections:
                reflected = reflections[clean_word]
                if word[0].isupper():
                    reflected = reflected.capitalize()
                reflected_words.append(reflected)
            else:
                reflected_words.append(word)
        
        return ' '.join(reflected_words)
    
    def process_input(self, user_input):
        #Обрабатывает пользовательский ввод и генерирует ответ
        # Нормализация входа
        normalized_input = user_input.upper().strip()
        
        # Поиск подходящего правила
        for rule in self.rules:
            match = re.match(rule['pattern'], normalized_input, re.IGNORECASE)
            if match:
                # Выбрать случайный ответ из доступных для этого правила
                response_template = random.choice(rule['responses'])
                
                # Заменить группы захвата
                response = response_template
                for i, group in enumerate(match.groups(), 1):
                    response = response.replace(f'\\{i}', group.upper())
                
                return response
        
        # Если ни одно правило не сработало, то фолбэк с отражением местоимений
        if len(user_input.split()) > 3:  # Если ввод достаточно длинный
            reflected = self.reflect_pronouns(user_input)
            return f"SO, {reflected.upper()}. HOW DOES THIS AFFECT YOUR PRODUCTIVITY?"
        else:
            return random.choice(self.fallback_responses)
    
    def chat(self):
        #Запускает интерактивный чат
        print("=" * 60)
        print("ELIZA PRODUCTIVITY COACH: HELLO! I'M YOUR PRODUCTIVITY COACH.")
        print("TELL ME ABOUT YOUR PRODUCTIVITY CHALLENGES OR TYPE 'QUIT' TO EXIT.")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\nYOU: ").strip()
                
                if user_input.upper() == 'QUIT':
                    print("\nELIZA: THANK YOU FOR OUR SESSION. REMEMBER: SMALL, CONSISTENT STEPS LEAD TO BIG CHANGES!")
                    break
                
                if not user_input:
                    print("ELIZA: PLEASE TELL ME MORE ABOUT WHAT'S ON YOUR MIND.")
                    continue
                
                response = self.process_input(user_input)
                print(f"ELIZA: {response}")
                
            except KeyboardInterrupt:
                print("\n\nELIZA: SESSION ENDED. TAKE CARE OF YOUR PRODUCTIVITY!")
                break
            except Exception as e:
                print(f"ELIZA: I ENCOUNTERED AN ISSUE. PLEASE REPHRASE: {str(e)}")

# Демонстрация работы бота на примерах
def demonstrate_eliza():
    eliza = ElizaProductivityCoach()
    
    test_cases = [
        "I am depressed about my work",
        "I need more time to finish this project",
        "I always procrastinate on important tasks",
        "I can't focus because there's too much noise",
        "My manager gives me too much work",
        "I want to be more productive but I don't know how",
        "I'm stressed about deadlines",
        "My family doesn't understand my work pressure",
        "The weather is nice today",
        "I put off everything until the last minute"
    ]
    
    print("DEMONSTRATION OF ELIZA PRODUCTIVITY COACH:")
    print("=" * 50)
    
    for case in test_cases:
        response = eliza.process_input(case)
        print(f"YOU: {case}")
        print(f"ELIZA: {response}")
        print("-" * 50)

if __name__ == "__main__":
    # Демонстрация работы
    demonstrate_eliza()
    
    print("\n" + "="*60)
    # Интерактивный чат
    eliza = ElizaProductivityCoach()
    eliza.chat()