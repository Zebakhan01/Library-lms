# Assignment: Personal Library Manager

## Objective

Create a **command-line Personal Library Manager** that allows users to manage their book collection. The program should let users add, remove, and search for books. Each book will be stored as a dictionary with details like title, author, publication year, genre, and read status. The program should also include a menu system, basic statistics, and optional file handling for saving and loading the library.

----------

## Requirements

### Core Features

1.  **Book Details**: Each book should have the following attributes:
    
    -   Title (string)
    -   Author (string)
    -   Publication Year (integer)
    -   Genre (string)
    -   Read Status (boolean: `True` if read, `False` if unread)
2.  **Menu System**: Implement a menu with the following options:
    
    -   Add a book
    -   Remove a book
    -   Search for a book
    -   Display all books
    -   Display statistics (total books, percentage read)
    -   Exit
3.  **Add a Book**: Prompt the user to enter the book's details and add it to the library.
    
4.  **Remove a Book**: Prompt the user to enter the title of the book to remove it from the library.
    
5.  **Search for a Book**: Allow the user to search for a book by title or author. Display all matching books.
    
6.  **Display All Books**: Show all books in the library in a formatted way.
    
7.  **Display Statistics**:
    
    -   Total number of books in the library.
    -   Percentage of books that have been read.
8.  **Exit**: Exit the program.
    

----------

### Optional Challenge (File Handling)

1.  **Save Library to a File**: Save the library data to a file (e.g., `library.txt`) when the program exits.
2.  **Load Library from a File**: Load the library data from the file when the program starts.

----------

## Sample Output

### Menu

```
Welcome to your Personal Library Manager!  
1. Add a book  
2. Remove a book  
3. Search for a book  
4. Display all books  
5. Display statistics  
6. Exit  
Enter your choice:  

```

### Add a Book

```
Enter the book title: The Great Gatsby  
Enter the author: F. Scott Fitzgerald  
Enter the publication year: 1925  
Enter the genre: Fiction  
Have you read this book? (yes/no): yes  
Book added successfully!  

```

### Remove a Book

```
Enter the title of the book to remove: The Great Gatsby  
Book removed successfully!  

```

### Search for a Book

```
Search by:  
1. Title  
2. Author  
Enter your choice: 1  
Enter the title: The Great Gatsby  
Matching Books:  
1. The Great Gatsby by F. Scott Fitzgerald (1925) - Fiction - Read  

```

### Display All Books

```
Your Library:  
1. The Great Gatsby by F. Scott Fitzgerald (1925) - Fiction - Read  
2. 1984 by George Orwell (1949) - Dystopian - Unread  

```

### Display Statistics

```
Total books: 2  
Percentage read: 50.0%  

```

### Exit

```
Library saved to file. Goodbye!  

```

----------

## Instructions

1.  Use a list of dictionaries to store the books.
2.  Use loops and conditionals to implement the menu system.
3.  Use string manipulation to format the output.
4.  Use type casting to convert user input to appropriate data types.
5.  (Optional) Use file handling to save and load the library.

----------

## Submission

1.  Write your code in a Python file named `library_manager.py`.
2.  Test your program thoroughly to ensure all features work as expected.
3.  (Optional) Include a text file (`library.txt`) to demonstrate file handling.

----------

## Tips

1.  Start by implementing the core features first.
2.  Test each feature individually before moving to the next.
3.  Use comments to explain your code.
4.  Have fun and be creative!

Once you are done submit this form ASAP:

https://forms.gle/tS7C3sr55tUZ36GY8 

Good luck! 🚀
