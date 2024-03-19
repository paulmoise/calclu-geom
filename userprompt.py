import re
import argparse

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import completion_is_selected

from carre import Carre
from cercle import Cercle
from point import Point
from rectangle import Rectangle
from triangle import Triangle

keywords = ['Carre', 'Triangle', 'Cercle', 'Rectangle', 'Point', 'Distance', 'Surface', 'Perimetre', 'Quitter',
            "Centre", "Export", "export"]

bindings = KeyBindings()


@bindings.add('enter')
def handle_enter(event: KeyPressEvent):
    """
    Custom enter key behavior: select completion if menu is visible,
    otherwise, submit the text.
    """
    buffer = event.app.current_buffer
    # Check if the completion menu is visible
    if buffer.complete_state:
        # If visible, select the current completion
        buffer.complete_state.current_completion.complete(event)
    else:
        # Otherwise, submit the text
        buffer.validate_and_handle()


@bindings.add("c-space")
def _(event):
    """
    Initialize autocompletion at cursor.

    If the autocompletion menu is not showing, display it with the
    appropriate completions for the context.

    If the menu is showing, select the next completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


@bindings.add("enter", filter=completion_is_selected)
def _(event):
    """Makes the enter key work as the tab key only when showing the menu.

    In other words, don't execute query when enter is pressed in
    the completion dropdown menu, instead close the dropdown menu
    (accept current selection).

    """

    event.current_buffer.complete_state = None
    b = event.app.current_buffer
    b.complete_state = None


class CustomLexer(Lexer):
    def lex_document(self, document: Document):
        def get_line(lineno):
            line_text = document.lines[lineno]
            tokens = []
            word = ''
            for char in line_text:
                if char.isalpha():  # Accumulate letters to form words
                    word += char
                else:
                    # Style accumulated word if it's a keyword
                    if word:
                        color = 'class:keyword' if word in keywords else 'class:text'
                        tokens.append((color, word))
                        word = ''  # Reset word accumulator
                    # Style non-letter characters individually
                    if char in '()':  # Color parentheses in yellow
                        tokens.append(('class:parentheses', char))
                    else:  # Style other non-letter characters as regular text
                        tokens.append(('class:text', char))
            # Catch any trailing word after the loop
            if word:  # Style if it's a keyword
                color = 'class:keyword' if word in keywords else 'class:text'
                tokens.append((color, word))
            return tokens

        return get_line


# Define your custom style for highlighting keywords in the auto-completion menu
# style = Style.from_dict({
#     'completion-menu.completion': 'bg:#008888 #ffffff',  # Background and foreground colors for completion items
#     'completion-menu.completion.current': 'bg:#00aaaa #000000',
#     # Background and foreground colors for the selected completion item
#     'scrollbar.background': 'bg:#88aaaa',
#     'scrollbar.button': 'bg:#222222',
#     'keyword': 'ansigreen bold italic',  # Keyword style
# })

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
    'keyword': 'ansigreen bold italic',  # Updated keyword style
    'parentheses': 'ansiyellow',  # New style for parentheses
    'text': ''  # Default text style (optional, for clarity)
})

welcome_text = """
Bienvenue dans le programme de calcul géométrique.

Vous pouvez effectuer diverses opérations géométriques et exporter vos commandes. Voici comment procéder :

Points:
Exemples :
- P1 = Point(2;4) # Crée un point P1 aux coordonnées (2, 4).
- P2 = Point(5;7) # Crée un point P2 aux coordonnées (5, 7).

Formes géométriques :
Vous pouvez créer différentes formes géométriques telles que le Cercle, le Rectangle, le Carré et le Triangle.
Exemples :
- C1 = Cercle(P1; 4) # Crée un cercle nommé C1 avec le centre en P1 et un rayon de 4.
- R1 = Rectangle(P1; 10; 5) # Crée un rectangle avec le coin supérieur gauche en P1, une largeur de 10 et une hauteur de 5.
- Ca1 = Carre(P2; 6) # Crée un carré nommé Ca1 avec le coin supérieur gauche en P2 et un côté de longueur 6.
- T1 = Triangle(4;4;8) # Crée un triangle avec les sommets en P1, P2 et un troisième point aux coordonnées (2, 8).

Opérateurs :
Utilisez ces opérateurs pour calculer la distance entre deux points, la surface ou le centre d'une forme.
Exemples :
- d1 = Distance(P1, P2) # Calcule la distance entre les points P1 et P2.
- sC1 = Surface(C1) # Calcule la surface du cercle C1.
- sR1 = Surface(R1) # Calcule la surface du rectangle R1.
- cC1 = Centre(C1) # Retourne le centre du cercle C1.
- sCa1 = Surface(Ca1) # Calcule la surface du carré Ca1.
- sT1 = Surface(T1) # Calcule la surface du triangle T1.

Exportation de vos commandes :
- Tapez "Export" ou "export" pour sauvegarder toutes les commandes entrées dans un fichier. 
Cela peut être utile pour documenter votre travail ou pour recharger les commandes lors d'une future session.

Pour quitter le programme, tapez "Quitter".
"""

key_words_completer = WordCompleter(keywords, ignore_case=True)


def extract_command(text):
    # Splitting the text into variable name and the command
    name, command = [part.strip() for part in text.split('=')]
    # Extracting shape name and parameters
    shape_name, params = re.match(r"(\w+)\(([^)]+)\)", command).groups()
    # Splitting parameters by comma and stripping whitespace
    params = [param.strip() for param in params.split(';')]
    # print(f"Name: {name}, Shape: {shape_name}, Params: {params}")
    return name, {shape_name: params}


def execute_user_prompt(text: str, object_memory=None):
    if object_memory is None:
        object_memory = {}

    name, obj_details = extract_command(text)

    type_form = list(obj_details.keys())[0]

    params = obj_details[type_form]

    obj_str = None

    if type_form == 'Carre':
        if len(params) == 2:
            obj_str = Carre(name, float(params[1]), object_memory[params[0]])
        if len(params) == 1:
            obj_str = Carre(name, float(params[0]))

    elif type_form == 'Triangle':
        obj = Triangle(name, float(params[0]), float(params[1]), float(params[2]))
        obj_str = obj

    elif type_form == 'Point':
        obj = Point(name, float(params[0]), float(params[1]))
        obj_str = obj

    elif type_form == 'Cercle':
        if len(params) == 2:
            obj_str = Cercle(name, float(params[1]), object_memory[params[0]])
        if len(params) == 1:
            obj_str = Cercle(name, float(params[0]))

    elif type_form == 'Rectangle':
        if len(params) == 3:
            obj_str = Rectangle(name, float(params[1]), float(params[2]), object_memory[params[0]])
        if len(params) == 2:
            obj_str = Rectangle(name, float(params[0]), float(params[1]))

    elif type_form == 'Distance':
        p1 = object_memory[params[0]]
        p2 = object_memory[params[1]]
        d = p1.distance(p2)
        obj_str = f"Distance({p1.name}; {p2.name}) = {round(d, 2)}"

    elif type_form == 'Surface':
        obj = object_memory[params[0]]
        s = obj.surface()
        obj_str = f"Surface: Nom Forme Géométrique = {obj.name}; Type = {type(obj).__name__}; Valeur = {round(s, 2)}"

    elif type_form == 'Perimetre':
        obj = object_memory[params[0]]
        p = obj.perimetre()
        obj_str = f"Perimetre: Forme Géométrique = {obj.name};  Type = {type(obj).__name__}; Valeur = {round(p, 2)}"

    elif type_form == 'Centre':
        obj = object_memory[params[0]]
        x, y = obj.calculate_center()
        obj_str = f"Centre: Forme Géométrique = {obj.name};  Type = {type(obj).__name__}; Centre = Point({x}, {y})"
    return name, obj_str


def read_prompt_from_file(file_path: str, object_memory=None, commands_history=None):
    if object_memory is None:
        object_memory = {}

    if commands_history is None:
        commands_history = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            commands_history.append(line.strip())
            name, obj = execute_user_prompt(line.strip(), object_memory)
            object_memory[name] = obj
        file.close()

    return object_memory, commands_history


def export_to_file(file_path, command_list):
    with open(file_path, 'w') as f:
        for command in command_list:
            f.write(command + '\n')
        f.close()


def main(file_path=None):
    session = PromptSession(lexer=CustomLexer(), completer=key_words_completer, style=style, key_bindings=bindings,
                            complete_while_typing=False)
    #print(welcome_text)

    object_memory = {}
    commands_history = []

    if file_path is not None:
        object_memory, commands_history = read_prompt_from_file(file_path, object_memory, commands_history)

    if object_memory:
        print(f"___________________________________________________________")
        print(f"Liste des objets en memoire:")
        for idx, (key, value) in enumerate(object_memory.items()):
            print(f"{idx + 1}: {value}")

    while True:
        try:
            text = session.prompt('> ')

            if text in ['Export', 'export']:
                export_to_file("file/commands.txt", commands_history)
                print(f"Les commandes ont été exportées dans le fichier commands.txt")
                text = session.prompt('> ')

            commands_history.append(text)
            name, obj_str = execute_user_prompt(text, object_memory)

            object_memory[name] = obj_str

            print(f"___________________________________________________________")
            print(f"List des objets en memoire:")
            for idx, (key, value) in enumerate(object_memory.items()):
                print(f"{idx + 1}: {value}")

            # print(f"*" * 50)
            # print(f"List des commandes:")
            # for idx, cmd in enumerate(commands_history):
            #     print(f"{idx + 1}: {cmd}")

            #     elif type_form == 'Distance':
            #         object = Distance(name, params[0], params[1])
            #     elif type_form == 'Surface':
            #         object = Surface(name, params[0])
            #     elif type_form == 'Perimetre':
            #         object = Perimetre(name, params[0])
            # if name == 'Carre':
            #     break
            #
            # print(results)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            pass
            # print('You said: %s' % text)
    print('GoodBye!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='Le chemin du fichier à traiter.')
    args = parser.parse_args()
    if args.file is not None:
        file_path = "file/" + args.file
        main(file_path)
    else:
        main()
