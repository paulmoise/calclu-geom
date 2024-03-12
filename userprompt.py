import re

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

keywords = ['Carre', 'Triangle', 'Cercle', 'Rectangle', 'Point', 'Distance', 'Surface', 'Perimetre', 'Quitter']

bindings = KeyBindings()


# @bindings.add('enter')
# def handle_enter(event: KeyPressEvent):
#     """
#     Custom enter key behavior: select completion if menu is visible,
#     otherwise, submit the text.
#     """
#     buffer = event.app.current_buffer
#     # Check if the completion menu is visible
#     if buffer.complete_state:
#         # If visible, select the current completion
#         buffer.complete_state.current_completion.complete(event)
#     else:
#         # Otherwise, submit the text
#         buffer.validate_and_handle()

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

welcome_text = 'Bienvenue dans le programme de calcul geometrique\n'
description = """
Pour saisir un point: nom_point = Point(x, y)
Pour saisir un carre: nom_carre = Carre(point, cote)
Pour saisir un triangle: nom_triangle = Triangle(point1, point2, point3)
Pour calculer la distance entre deux points : d = Distance(point1, point2)
Pour calculer la surface d'un carre : s = Surface(carre)
Pour calculer la surface d'un triangle : s = Surface(triangle)
Taper "Quitter" pour quitter le programme
"""

key_words_completer = WordCompleter(keywords, ignore_case=True)


def extract_command(text):
    pattern = r"(Carre|Triangle|Cercle|Point|Distance|Rectangle|Surface|Perimetre)\(([^)]+)\)"
    name = text.split('=')[0].strip()

    results = {}
    matches = re.findall(pattern, text)
    for match in matches:
        key, params = match
        if key not in results:
            results[key] = []

        if ';' in params:
            results[key] = params.split(';')
        if "," in params:
            results[key] = params.split(',')
    return name, results


def main():
    pattern = r"(Carre|Triangle|Cercle|Point|Distance|Surface|Rectangle|Perimetre)\(([^)]+)\)"

    session = PromptSession(lexer=CustomLexer(), completer=key_words_completer, style=style, key_bindings=bindings,
                            complete_while_typing=False)

    print(welcome_text)
    print(description)
    object_memory = {}

    while True:
        try:
            text = session.prompt('> ')
            name, obj_details = extract_command(text)
            # print(name, obj_details)
            type_form = list(obj_details.keys())[0]
            params = obj_details[type_form]

            obj = None
            if type_form == 'Carre':
                obj = Carre(name, float(params[0]))
                object_memory[name] = obj
            elif type_form == 'Triangle':
                obj = Triangle(name, float(params[0]), float(params[1]), float(params[2]))
                object_memory[name] = obj

            elif type_form == 'Point':
                obj = Point(name, float(params[0]), float(params[1]))
                object_memory[name] = obj

            elif type_form == 'Cercle':
                obj = Cercle(name, float(params[0]))
                object_memory[name] = obj

            elif type_form == 'Rectangle':
                obj = Rectangle(name, float(params[0]), float(params[1]))
                object_memory[name] = obj

            elif type_form == 'Distance':
                p1 = object_memory[params[0]]
                p2 = object_memory[params[1]]
                d = p1.distance(p2)
                str_distance = f"Distance({p1.name}; {p2.name}) = {round(d, 2)}"
                object_memory[name] = str_distance

                # print(f"Distance({p1.name}; {p2.name}) = {round(d, 2)}")
            elif type_form == 'Surface':
                obj = object_memory[params[0]]
                s = obj.surface()
                str_surface = f"Surface({obj.name}) = {round(s, 2)}"
                object_memory[name] = str_surface
                # print(f"Surface({obj.name}) = {round(s, 2)}")
            elif type_form == 'Perimetre':
                obj = object_memory[params[0]]
                p = obj.perimetre()
                str_perimetre = f"Perimetre({obj.name}) = {p}"
                # print(f"Perimetre({obj.name}) = {p}")
                object_memory[name] = str_perimetre
            print(f"___________________________________________________________")
            print(f"List des objets en memoire:")
            for idx, (key, value) in enumerate(object_memory.items()):
                print(f"{idx + 1}: {value}")

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
    main()
