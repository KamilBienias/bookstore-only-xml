import xml.etree.cElementTree as ET
import datetime as dt


class UserInterface:

    def __init__(self):
        pass

    def menu(self):
        quit_program = False
        while not quit_program:
            print("\nChoose number from menu:")
            print("1. Add new customer")
            print("2. Add new book")
            print("3. Show all customers")
            print("4. Show all books")
            print("5. Order the book on the customer's account")
            print("6. Delete customer")
            print("7. Delete book")
            print("0. Quit bookstore")

            is_number_error = True
            while is_number_error:
                try:
                    chosen_number = input("Pass number (0 - 7): ")
                    chosen_number_int = int(chosen_number)
                    if chosen_number_int not in range(0, 8):  # or [0, 1, 2, 3, 4, 5, 6, 7]
                        raise NameError()
                    is_number_error = False
                except ValueError as e:
                    print(chosen_number + " is not an integer")
                except NameError as e:
                    print(chosen_number + " is out of menu")

            if chosen_number_int == 1:
                self.add_customer()
            if chosen_number_int == 2:
                self.add_book()
            if chosen_number_int == 3:
                self.all_customers()
            if chosen_number_int == 4:
                self.all_books()
            if chosen_number_int == 5:
                self.order_book()
            if chosen_number_int == 6:
                self.delete_customer()
            if chosen_number_int == 7:
                self.delete_book()
            if chosen_number_int == 0:
                print("Bye bye")
                quit_program = True

    # 1
    def add_customer(self):

        passed_first_name = input("Pass new customer's first name: ")
        passed_last_name = input("Pass new customer's last name: ")

        is_pesel_error = True
        while is_pesel_error:
            try:
                passed_pesel = input("Pass new customer's pesel: ")
                int(passed_pesel)  # check if pesel contains only numbers
                if len(passed_pesel) != 11:
                    raise Exception()
                is_pesel_error = False
            except ValueError as e:
                print(passed_pesel + " does not consist of integers")
            except Exception as e:
                print("Pesel should consist of 11 digits")

        tree_of_clients = ET.parse("clients.xml")
        clients = tree_of_clients.getroot()

        client = ET.Element("client")

        firstName = ET.Element("firstName")
        client.append(firstName)
        firstName.text = passed_first_name

        lastName = ET.Element("lastName")
        client.append(lastName)
        lastName.text = passed_last_name

        pesel = ET.Element("pesel")
        client.append(pesel)
        pesel.text = passed_pesel

        boughtBooks = ET.Element("boughtBooks")
        client.append(boughtBooks)
        boughtBooks.text = "Id of purchased books:"

        createdAt = ET.Element("createdAt")
        client.append(createdAt)
        createdAt.text = str(dt.datetime.now())

        clients.append(client)

        # saves changes to clients.xml
        tree_of_clients.write("clients.xml")  # relative path
        print("New customer saved to clients.xml: ")
        print(passed_first_name, passed_last_name, passed_pesel)

    # 2
    def add_book(self):

        passed_title = input("Pass new book's title: ")
        passed_author_name = input("Pass new book's author's name: ")
        passed_author_surname = input("Pass new book's author's surname: ")

        is_price_error = True
        while is_price_error:
            try:
                passed_price_string = input("Pass new book's price (use a dot instead of a comma): ")
                passed_price = float(passed_price_string)
                passed_price_rounded = str(round(passed_price, 2))
                is_price_error = False
            except ValueError as e:
                print(passed_price_string + " is not a float number")

        tree_of_books = ET.parse("books.xml")
        books = tree_of_books.getroot()

        # looks for max_id from all books
        max_id = 0
        if len(books) > 0:  # if there are no books in books.xml
            max_id = int(books[-1].attrib["id"])  # takes last book's attribute id

        book = ET.Element("book")
        book.set("id", str(max_id + 1))  # sets attribute id with a number 1 greater than the max_id
        book.set("status", "available")  # sets attribute status with "available"
        title = ET.Element("title")
        book.append(title)
        title.text = passed_title

        authorName = ET.Element("authorName")
        book.append(authorName)
        authorName.text = passed_author_name

        authorSurname = ET.Element("authorSurname")
        book.append(authorSurname)
        authorSurname.text = passed_author_surname

        price = ET.Element("price")
        book.append(price)
        price.text = passed_price_rounded

        createdAt = ET.Element("createdAt")
        book.append(createdAt)
        createdAt.text = str(dt.datetime.now())

        books.append(book)

        # saves changes to books.xml
        tree_of_books.write("books.xml")  # relative path
        print("\nNew book saved to books.xml: ")
        print(passed_title, passed_author_name, passed_author_surname, passed_price_rounded)

    # 3
    def all_customers(self):

        print("\nCustomers details from clients.xml:\n")
        tree = ET.parse("clients.xml")
        clients = tree.getroot()

        for client in clients:
            i = 0
            for client_data in client:

                print(client_data.tag + ": " + client_data.text)

                if str(client_data.tag) == "boughtBooks":
                    for boughtBook in client_data:
                        print(boughtBook.tag + " id: " + boughtBook.text)

                i = i + 1
                if i % 5 == 0:  # if a multiple of 5 iterations, then space between clients
                    print("")

    # 4
    def all_books(self):

        print("\nBooks details from books.xml:\n")
        tree = ET.parse("books.xml")
        books = tree.getroot()

        for book in books:
            print(book.attrib)  # prints dictionary of book attributes
            i = 0

            for book_data in book:  # for each element in book
                # prints one by one book_data's tag and text. For example firstName: James
                print(book_data.tag + ": " + book_data.text)
                i = i + 1
                # if a multiple of 5 iterations, then space between books
                if i % 5 == 0:
                    print("")

    # 5
    def order_book(self):

        # saves available id's of books to list_of_available_books_id
        tree_of_books = ET.parse("books.xml")
        books = tree_of_books.getroot()
        list_of_available_books_id = list()
        for book in books:
            if book.attrib["status"] == "available":
                # book.attrib is dictionary so book.attrib["id"] takes value of key "id"
                list_of_available_books_id += str(book.attrib["id"])

        # if list_of_available_books_id is empty then exit ordering book
        if len(list_of_available_books_id) == 0:
            print("\nThere is no available books")
            # self.menu()
            return  # if there are no available books then leave this method

        self.all_customers()  # show all clients

        # user passes customer's pesel
        is_pesel_error = True
        while is_pesel_error:
            try:
                passed_pesel = input("Pass customer's pesel: ")
                int(passed_pesel)  # check if pesel contains only numbers
                if len(passed_pesel) != 11:
                    raise Exception()
                is_pesel_error = False
            except ValueError as e:
                print(passed_pesel + " does not consist of integers")
            except Exception as e:
                print("Pesel should consist of 11 digits")

        self.all_books()  # show all books

        # user passes id. Then id is checked, if it belongs to list_of_books_id or if it is an available book
        is_id_error = True
        while is_id_error:
            try:
                passed_id = input("Pass available book's id: ")
                int(passed_id)  # check if id contains only numbers
                if passed_id not in list_of_available_books_id:
                    raise IndexError()
                # If book status is "available", changes it to "bought". Printed are only "available" books
                for book in books:
                    if str(book.attrib["id"]) == passed_id:
                        if str(book.attrib["status"]) == "available":
                            book.set("status", "bought")
                is_id_error = False
            except ValueError as e:
                print(passed_id + " doesn't consist of integers")
            except IndexError as e:
                print("Id " + passed_id + " is out of available books list: " + str(list_of_available_books_id))

        tree_of_books.write("books.xml")

        # adds the id of the purchased book to the client's tag boughtBooks
        tree_of_clients = ET.parse("clients.xml")
        clients = tree_of_clients.getroot()
        for client in clients:
            if str(client[2].text) == passed_pesel:  # client[2] is element with tag pesel
                boughtBook = ET.Element("boughtBook")  # creates new tag boughtBook
                boughtBook.text = passed_id  # text of that tag is id number of bought book
                client[3].append(boughtBook)  # client[3] is element with tag boughtBooks

        # saves changes to clients.xml
        tree_of_clients.write("clients.xml")

        print("Client with pesel " + passed_pesel + " bought book with id " + passed_id)

    # 6
    def delete_customer(self):

        self.all_customers()  # show all clients

        # user passes customer's pesel
        is_pesel_error = True
        while is_pesel_error:
            try:
                passed_pesel = input("Pass customer's pesel: ")
                int(passed_pesel)  # check if pesel contains only numbers
                if len(passed_pesel) != 11:
                    raise Exception()
                is_pesel_error = False
            except ValueError as e:
                print(passed_pesel + " does not consist of integers")
            except Exception as e:
                print("Pesel should consist of 11 digits")

        # removes selected customer
        tree_of_clients = ET.parse("clients.xml")
        clients = tree_of_clients.getroot()
        for client in clients:
            if str(client[2].text) == passed_pesel:
                clients.remove(client)

        # saves changes to clients.xml
        tree_of_clients.write("clients.xml")
        print("Customer with pesel " + passed_pesel + " has been removed")

    # 7
    def delete_book(self):

        self.all_books()  # show all books

        # saves id's of all books to list_of_books_id
        tree_of_books = ET.parse("books.xml")
        books = tree_of_books.getroot()
        list_of_books_id = list()
        for book in books:
            # book.attrib is dictionary so book.attrib["id"] takes value of key "id"
            list_of_books_id += str(book.attrib["id"])

        # user passes id. Then id is checked, if it belongs to list_of_books_id
        is_id_error = True
        while is_id_error:
            try:
                passed_id = input("Pass book's id: ")
                int(passed_id)  # check if id contains only numbers
                if passed_id not in list_of_books_id:
                    raise IndexError()
                is_id_error = False
            except ValueError as e:
                print(passed_id + " doesn't consist of integers")
            except Exception as e:
                print("Id " + passed_id + " is out of all books list " + str(list_of_books_id))

        # removes selected book
        for book in books:
            if str(book.attrib["id"]) == passed_id:
                books.remove(book)

        # saves changes to books.xml
        tree_of_books.write("books.xml")

        # removes the tag boughtBook of the removed book from the client's tag boughtBooks
        tree_of_clients = ET.parse("clients.xml")
        clients = tree_of_clients.getroot()
        for client in clients:
            for client_data in client:  # client_data are firstName, lastName, pesel, boughtBooks, createdAt
                if client_data.tag == "boughtBooks":
                    for boughtBook in client_data:  # tu client_data to boughtBooks
                        if boughtBook.text == passed_id:  # if text in boughtBook tag is the same as given id
                            pesel_of_client_who_had_removed_book = str(client[2].text)  # take pesel of that client
                            client_data.remove(boughtBook)  # and remove whole tag boughtBook z boughtBook

        # saves changes to clients.xml
        tree_of_clients.write("clients.xml")

        print("Book with id " + passed_id + " has been removed from books.xml and from client with pesel " + pesel_of_client_who_had_removed_book + " from clients.xml")


def main():
    try:
        ET.parse("clients.xml")
    except FileNotFoundError:
        print("clients.xml doesn't exist. Creates a new one")
        clients_base = open("clients.xml", "w")
        root = ET.Element("clients")
        new_tree = ET.ElementTree(root)
        new_tree.write("clients.xml")
        clients_base.close()
        ET.parse("clients.xml")

    try:
        ET.parse("books.xml")
    except FileNotFoundError:
        print("books.xml doesn't exist. Creates a new one")
        new_base = open("books.xml", "w")
        root = ET.Element("books")
        new_tree = ET.ElementTree(root)
        new_tree.write("books.xml")
        new_base.close()
        ET.parse("books.xml")

    user_interface = UserInterface()
    user_interface.menu()


if __name__ == "__main__":
    main()
