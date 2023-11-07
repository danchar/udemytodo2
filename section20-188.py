# from functions import get_todos, wirte_todos
import functions
import time
import PySimpleGUI as sg

sg.theme("LightBrown6")

clock = sg.Text('', key='clock')
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=[45,10])
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")
exit_button = sg.Button("Exit")

window = sg.Window('My To Do App',
                   layout=[[label],
                           [clock],
                            [input_box, add_button],
                            [list_box, edit_button, complete_button],
                            [exit_button]],
                   font=('Helvetica', 20))

while True:
    event, values = window.read(timeout=10)
    window['clock'].update(value=time.strftime("%b %d, %y %H:%M:%S"))
    print(event)
    print(values)
    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            functions.wirte_todos(todos)
            window['todos'].update(values=todos)

        case "Edit":
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo'] + "\n"

                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.wirte_todos(todos)
                window['todos'].update(values=todos)
            except IndexError:
                sg.Popup("Please select an item first", font=("Helvetica", 20))
        case 'Complete':
            try:
                todo_to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.wirte_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value=" ")
            except IndexError:
                sg.Popup("Please select an item first", font=("Helvetica", 20))
        case "Exit":
            break
        case 'todos':
            window['todo'].update(value=values['todos'][0])
        case sg.WIN_CLOSED:
            break

window.close()


timenow = time.strftime("%b %d, %y %H:%M")
print("Today's time",timenow)
while True:
    user_action = input("Type, edit, add, complete or show: ")
    user_action = user_action.strip()

    if user_action.startswith('add'):
        todo = user_action[4:]

        todos = functions.get_todos(filepath="todos.txt")

        todos.append(todo + '\n')

        functions.wirte_todos(todos)

    elif user_action.startswith('show'):

        todos = functions.get_todos(filepath="todos.txt")

        new_todos = []

        for item in todos:
            new_item = item.strip('\n')
            new_todos.append(new_item)
        print(todos)

        new_todos = [item.strip('\n') for item in todos]

        for index, item in enumerate(new_todos):
            item  = item.title()
            row = f"{index + 1}'-'{item}"
            print(row)

    elif user_action.startswith('edit'):
        try:
            number = int(user_action[5:])
            print(number)

            number = number - 1

            todos = functions.get_todos(filepath="todos.txt")

            new_todo = input("New todo: ")
            todos[number] = new_todo + '\n'

            with open('todos.txt', 'w') as file:
                file.writelines(todos)

            print('Here is how it will be', todos)

        except ValueError:
            print("Your command is not valid")
            continue


    elif user_action.startswith('complete'):
        try:
            number = int(user_action[9:])

            todos = get_todos(filepath="todos.txt")
            index = number - 1
            todo_to_remove = todos[index].strip('\n')
            todos.pop(index)

            functions.wirte_todos(todos)

            message = f"Todo {todo_to_remove} was removed"
            print(message)
        except IndexError:
            print("There is no item with that item")
            continue

    elif 'exit'  in user_action:
        break
    else:
        print("Command is not valid")

print("See ya!")