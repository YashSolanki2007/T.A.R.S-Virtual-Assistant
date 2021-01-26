# Making the imports
import math
import webbrowser
import pickle
import datetime
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Making the calculator function
def inbuilt_calculator():
    print("Welcome To Calculator, you can add, multiply, divide and subtract")
    num_1 = float(input("Enter The First Number: "))
    op = input("Enter the Operator: ")
    num_2 = float(input("Enter The Second Number: "))
    if op == "+":
        print(num_1 + num_2)

    elif op == "-":
        print(num_1 - num_2)

    elif op == "*":
        print(num_1 * num_2)

    elif op == "/":
        print(num_1 / num_2)

    else:
        print("Invalid Operator or Data Type...")


# Making the song generator loading in function
def generate_rap_song():
    import tensorflow as tf

    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.optimizers import Adam
    import numpy as np

    tokenizer = Tokenizer()

    data = open('dataset.rtf').read()

    corpus = data.lower().split("\n")

    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1

    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            input_sequences.append(n_gram_sequence)

    # pad sequences
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(
        pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    # create predictors and label
    xs, labels = input_sequences[:, :-1], input_sequences[:, -1]

    ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

    print("Generating Rap And training the model....\n\n")

    model = Sequential()
    model.add(Embedding(total_words, 100, input_length=max_sequence_len - 1))
    model.add(Bidirectional(LSTM(150)))
    model.add(Dense(total_words, activation='softmax'))
    adam = Adam(lr=0.01)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])
    #earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
    history = model.fit(xs, ys, epochs=15, verbose=4)
    #print model.summary()

    seed_text = input("Enter the text to start with: ")
    next_words = 100

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list],
                                   maxlen=max_sequence_len - 1,
                                   padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    print(seed_text)


# Making the function to name the assistant
def remember_assistant():
    assistant_name = input("Enter the name I should be Called: ")
    # Dumping the file
    pickle.dump(assistant_name, open("Assistant name.dat", "wb"))
    print("Name Remembered")


# Making the function to get the name
def get_assistant_name():
    asistant_name = pickle.load(open("Assistant name.dat", "rb"))
    print(
        f"Hi I am {asistant_name} your virtual assitant. Type -h for help. If you do not get any response that means the command is invalid."
    )


# Making the function to write to a text file
def make_and_write_in_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
        f.close()


# Making the reading file functionality
def open_file(filename):
    print("The File should be in the same dir")
    with open(filename, 'r') as f:
        lines = f.read()
        print(lines)
        f.close()


# Making the function for the graph gen
def hist_gen():
    print("This will generate a Histogram for you.")

    graph_title = input("What should be the title of the graph: ")
    graph_xlabel = input("What should be the X label for the graph: ")
    graph_ylabel = input("What should be the Y label for the graph: ")
    graph_lines = input(
        "Enter the values to be plotted seperated by a space as digits: ")

    # Plotting the graph based on the given params
    plt.title(graph_title)
    plt.xlabel(graph_xlabel)
    plt.ylabel(graph_ylabel)
    plot = []
    for i in range(len(graph_lines)):
        plot.append(i)
        plt.hist(i)

    plt.show()


# Making the function for the area finding calculator
def area_finder():
    choice = input(
        "Press (S) to find the area of a square, (T) for triangle, (R) for rectangle and (C) for circle."
    )

    # For square
    if choice.lower() == "s":
        len_of_side = float(input("Enter the length of the side: "))
        result = math.pow(len_of_side, 2)
        print(result)

    # For triangle
    elif choice.lower() == "t":
        len_of_base = float(
            input("Enter the length of the base of the triangle: "))
        len_of_height = float(input("Enter the height of the triangle: "))

        result = 1 / 2 * len_of_base * len_of_height
        print(result)

    # For rectange
    elif choice.lower() == "r":
        len_of_length = float(input("Enter the length of the triangle: "))
        len_of_breadth = float(input("Enter the width of the rectangle"))
        # I know my choice of variables is V bad 🤣

        result = len_of_length * len_of_breadth
        print(result)

    elif choice.lower() == "c":
        radius_of_circle = float(input("Enter the radius of the circle: "))

        result = 22 / 7 * math.pow(radius_of_circle, 2)
        print(result)

    else:
        print("Invalid Command")


# Gretting
try:
    get_assistant_name()

except Exception as e:
    print(
        "Hi I am T.A.R.S your virtual assitant. Type -h for help. If you do not get any response that means the command is invalid."
    )

# Making the choices variable
while True:
    # Making the prompt command
    user_command = input("Enter A Command: ")

    # Making the help condition
    if user_command.lower() == "-h":
        print(
            "Type cal to open the calculator \n quit to exit \n open_site to open a external website \n write_and_make_file to make a file and write some text to it \n get_time to get the current time \n read_file to read a file from the same dir \n area_cal to open the area calculator \n make_hist to make a histogram \n change_assistant_name to change the name of the assistant \n gen_rap to generate a rap \n remeber_me to remember your name \n get_name to get your name."
        )

    # Making the calculator conditions
    elif user_command.lower() == "cal":
        inbuilt_calculator()

    # Command for opening the website
    elif user_command.lower() == "open_site":
        try:
            # Making the url var
            url = input(
                "Enter the complete url of the website you want to open: ")

            webbrowser.open(url)

        except:
            print("Incorrect URL.")

    # Command for getting the time
    elif user_command.lower() == "get_time":
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Sir, the time is {strTime}")

    # Remebering Command
    elif user_command.lower() == "remember_me":
        name = input("Enter your name: ")

        # Making the file
        pickle.dump(name, open("name.dat", "wb"))

        print("Name Saved Type get_name to for me to call your name.")

    # Getting the name Command
    elif user_command.lower() == "get_name":
        try:
            remember_name = pickle.load(open("name.dat", 'rb'))

            print(f"You are {remember_name}")

        except:
            print("No name saved...")

    # Making the writing in file command:
    if user_command.lower() == "write_and_make_file":
        file_name = input("Write the name of the file you want to make: ")
        text = input("Write the content that you want to fill in this file: ")
        make_and_write_in_file(file_name, text)
        print("File Made And Filled Succesfully!")

    # Making the reading file cdommand
    if user_command.lower() == "read_file":
        file_to_open = input("Enter the name of the file to open: ")
        open_file(file_to_open)

    # Area calculator
    elif user_command.lower() == "area_cal":
        area_finder()

    # Check to see that the entry is blank
    elif user_command.strip() == "":
        print("Please Type A Command Do not leave the field blanck")

    # Check make hist condition
    elif user_command.lower() == "make_hist":
        hist_gen()

    # Check to see that the assistant remmeber commad
    elif user_command.lower() == "change_assistant_name":
        remember_assistant()

    elif user_command.lower() == "gen_rap":
        generate_rap_song()

    # Quit Command
    elif user_command.lower() == "quit":
        print("Bye Will Miss You 😃")
        break
