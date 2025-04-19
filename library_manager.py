import streamlit as st
import pandas as pd
import json
import os
import datetime  # Correctly importing the datetime module
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lotiest import st_lottie
import requests

# Set page config
st.set_page_config(
    page_title="Personal Library Manager", 
    page_icon="📚",                 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        font-size: 3rem !important;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }

    .subheader {
        font-size: 1.8rem !important;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }

    .success-message {
        padding: 1rem;
        background-color: #ECFDF5;
        border-left: 5px solid #10b981;
        border-radius: 0.375rem;
    }

    .warning-message {
        padding: 1rem;
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
    }

    .book-card {
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3b82f6;
        transition: transform 0.3s;
    }

    .book-card-hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .read-badge {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .unread-badge {
        background-color: #F87171;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .action-button {
        margin-right: 0.5rem;
    }

    .stButton {
        border-radius: 0.375rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to load lottie animation from URL
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize session state for library if not present
if 'library' not in st.session_state:
    st.session_state['library'] = []
if 'search_results' not in st.session_state:
    st.session_state.book_added = False
    if 'book_removed' not in st.session_state:
        st.session_state.book_removed = False
        if 'current_view' not in st.session_state:
            st.session_state.current_view = "library"

        def load_library():
                    try:
                        if os.path.exists('library.json'):
                            with open('library.json', 'r') as file:
                                st.session_state.library = json.load(file)
                            return True
                        return False
                    except Exception as e:
                        st.error(f"Error loading library: {e}")
                        return False
        
        # Save library function
        def save_library():
            try:
                with open('library.json', 'w') as file:
                    json.dump(st.session_state.library, file)
            except Exception as e:
                st.error(f"Error saving library: {e}")
                return False
                
    # Add a book to the library
    def add_book(title, author, publication_year, genre, read_status):
        book = {
            'title': title,
            'author': author,
            'publication_year': publication_year,
            'genre': genre,
            'read_status': read_status,
            'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.library.append(book)
        save_library()
        st.session_state.book_added = True
        time.sleep(0.5)  # Animation delay
   
    #remove book from the library
    def remove_book(index):
        if 0 <= index < len(st.session_state.library):
            del st.session_state.library[index]
            save_library()
            st.session_state.book_removed = True
            return True
        # search for a book in the library
                    
    def search_book(search_term,search_by):
                    saerch_term = search_term.lower()
                    search_results = []

                    for book in st.session_state.library:
                        if search_by == "title" and saerch_term in book['title'].lower():
                            search_results.append(book)
                        elif search_by == "author" and saerch_term in book['author'].lower():
                            search_results.append(book)
                        elif search_by == "Genre" and saerch_term in str(book['genre']).lower():
                            search_results.append(book)
                    st.session_state.search_results = search_results

                    #calculate the percentage of libarary stats
                    def get_library_stats():
                        total_books = len(st.session_state.library)
                        read_books = sum(1 for book in st.session_state.library if book['read_status'] == 'read')
                        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

                        generes = {}
                        authors = {}
                        decades = {}
                        for book in st.session_state.library:
                            if [book ['genre']] in generes:                          
                                generes[book['genre']] +=1
                            else:

                                generes[book['genre']] = 1

                                # count authors

                                if book['author'] in authors:
                                    authors[book['author']] += 1
                                else:
                                    authors[book['author']] = 1

                                    #count dedcades
                                    decades =(book['publication_year'] // 10) * 10
                                    if decades in decades:
                                        decades[decades] += 1
                                    else:
                                        decades[decades] = 1
                                        #sort by count
                                        generes = dict(sorted(generes.items(), key=lambda x:x[1], reverse=True))
                                        authors = dict(sorted(authors.items(), key=lambda x:x[1], reverse=True))
                                        decades = dict(sorted(decades.items(), key=lambda x:x[0], reverse=True))
                                        return {
                                            'total_books': total_books,
                                            read_books: read_books,
                                            'percentage_read': percentage_read,
                                            'generes': generes,
                                            'authors': authors,
                                            'decades': decades
                                        }
                                    def create_visualizations(stats):
                                        if stats ['total_book'] >0:
                                            fig_read_status= go.Figure(data=[go.Pie(labels=['Read', 'Unread'], values=[stats['read_books'], stats['total_books'] - stats['read_books']],
                                                                                   hole=0.4,
                                                                                   marker=dict(colors=['#10b981', '#F87171']))])
                                        hole=0.4
                                        markers_color = ['#10b981', '#F87171']
                                        fig_read_status.update_layout(
                                                title_text='Read vs Unread Books',
                                                showlegend=True,
                                                height=400
                                        )
                                        st.plotly_chart(fig_read_status, use_container_width=True)

                                            # Genre bar chart
                                        if stats['generes']:
                                             generes_df = pd.DataFrame(list(stats['generes'].keys()), 
                                             counts=list(stats['generes'].values()))
                                        fig_genres = px.bar(
                                                    generes_df,
                                                      x='Genre', 
                                                      y='Counts', 
                                                      color='Counts',
                                                      color_container_scale=px.colors.sequential.blue,
                                                      )
                                        fig_genres.update_layou(
                                                title_text='Book by Publication decade',
                                                xaxis_title='Decade',
                                                yaxis_title='Number of Books',
                                                height=400,
                                            )
                                        st.plotly_chart(fig_genres, use_container_width=True)
                                        if stats['decades']:
                                                decades_df = pd.DataFrame({'Decades':[f"{decade}s" for decade in stats['decades'].keys()],
                                                'Counts': list(stats['decades'].values())
                                                })
                                                fig_decades = px.bar(
                                                    decades_df,
                                                    x='Decade',
                                                    y='Counts',
                                                    markers=True,
                                                    line_shape="spline"
                                                )
                                                fig_decades.update_layout(
                                                    title_text='Books by publication decade',
                                                    xaxis_title='Decade',
                                                    yaxis_title='Number of Books',
                                                    height=400,
                                                )
                                                st.plotly_chart(fig_decades, use_container_width=True)

                                                #load libary

                                                load_library()
                                                st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
                                                lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/1f20_aKAfind.json")
                                                if lottie_book:
                                                    with st.sidebar:
                                                        st_lottie(lottie_book, width=300, height=300, key="book animation")
                                                        nav_options =st.sidebar.radio(
                                                            "choose and option:",
                                                            ["View Library", "Add Book", "Search Book,Library Statistics"]
                                                        )
                                                        if nav_options == "View Library":
                                                            st.session_state.current_view = "library"
                                                        elif nav_options == "Add Book":
                                                            st.session_state.current_view = "add_book"
                                                        elif nav_options == "Search Book":
                                                            st.session_state.current_view = "search"
                                                        elif nav_options == "Library Statistics":
                                                            st.session_state.current_view = "statistics"

                                                            st.markdown("<h1 class='main-header'>Personal Library Manager </h1>",unsafe_allow_html=True)
                                                            if st.session_state.current_view=="add":
                                                                st.markdown("<h2 class='subheader'>Add a Book</h2>", unsafe_allow_html=True)

                                                                #adding a book to the library

                                                                with st.form(key='add_book_form'):
                                                                    col, col2, = st.columns(2)

                                                                    with col:
                                                                        title = st.text_input("Title")
                                                                        author = st.text_input("Author",max_chars=100)
                                                                        publication_year = st.number_input("Publication Year", min_value=1900, max_value=datetime.now().year, step=1,value=2023)
                                                                        with col2:
                                                                            genre = st.selection("Genre", options=["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Biography", "History", "Romance"])
                                                                            read_status = st.radio("Read Status", options=["Read", "Unread"], horizontal=True)
                                                                            read_boolean = read_status == "Read" 
                                                                            summit_button = st.form_submit_button("Add Book")
                                                                            summit_button = st.button(label="Add Book")

                                                                            if summit_button:
                                                                                if title and author and publication_year and genre:
                                                                                    add_book(title, author, publication_year, genre, read_boolean)

                                                                                    if st.session_state.book_added:
                                                                                        st.markdown("<div class='success-message'>Book added successfully!</div>", unsafe_allow_html=True)
                                                                                        st.balloons()
                                                                                        st.session_state.book_added = False

                                                                                    else:
                                                                                        st.session_state.current_view = "library"
                                                                                        st.markdown("<h2 class='subheader'>Your Library</h2>", unsafe_allow_html=True)
                                                                                        if not st.session_state.library:
                                                                                            st.markdown("<div class='warning-message'>Your library is empty. Please add books.</div>", unsafe_allow_html=True)
                                                                                        else:
                                                                                            cols=st.columns(2)
                                                                                            for i, book in enumerate(st.session_state.library):
                                                                                                with cols[i % 2]:
                                                                                                    st.markdown(f"""<div class='book-card'>
                                                                                                    <h3>{book['title']}</h3>"
                                                                                                                <p><strong>Author:</strong> {book['author']}</p>
                                                                                                                <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                                                                                                                <p><strong>Genre:</strong> {book['genre']}</p>
                                                                                                                <p><span class='{'read-badge' if book['read_status'] == 'read' else 'unread-badge'}'>
                                                                                                                {"Read" if book['read_status'] == 'read' else "Unread"}
                                                                                                                </span></p>
                                                                                                                </div>


                                                                                                                """,unsafe_allow_html=True)
                                                                                                    col1, col2 = st.columns(2)             
                                                                                                    with col1:
                                                                                                        remove_button = st.button("Remove Book", key=f"remove_{i}",use_container_width=True):
                                                                                                       
                                                                                                    if remove_book(i):
                                                                                                        st.reurn()
                                                                                                    with col2:
                                                                                                        new_status = not book['read_status']
                                                                                                        status_label = "Mark as Unread" if not book['read_status'] else "Mark as Read"
                                                                                                        if st.button(status_label, key=f"status_{i}", use_container_width=True):
                                                                                                            st.session_state.library[i]['read_status'] = new_status
                                                                                                            save_library()
                                                                                                            st.rerun()
                                                                                                            if st.session_state.book_removed:
                                                                                                                st.markdown("<div class='success-message'>Book removed successfully!</div>", unsafe_allow_html=True)
                                                                                                                st.session_state.book_removed = False
                                                                                                            elif st.session_state.current_view == "search":
                                                                                                                st.markdown("<h2 class='subheader'>Search Book</h2>", unsafe_allow_html=True)

                                                                                                                search_by = st.selectbox("Search by", options=["title", "author", "genre"])
                                                                                                                search_term = st.text_input("Enter search term")
                                                                                                                if st.spinner("Searching..."):
                                                                                                                    time.sleep(0.5)
                                                                                                                    search_book(search_term, search_by)
                                                                                                                    if hasattr(st.session_state, 'search_results'):
                                                                                                                        if st.session_state.search_results:
                                                                                                                            st.markdown(f"<h3> Found{len(st.session_state.search_results)} results:</h3>", unsafe_allow_html=True)
                                                                                                                            for i, book in enumerate(st.session_state.search_results):
                                                                                                                                st.markdown(f"""<div class='book-card'>
                                                                                                                                  <h3>{book['title']}</h3>"
                                                                                                                <p><strong>Author:</strong> {book['author']}</p>
                                                                                                                <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                                                                                                                <p><strong>Genre:</strong> {book['genre']}</p>
                                                                                                                <p><span class='{'read-badge' if book['read_status'] == 'read' else 'unread-badge'}'>
                                                                                                                {"Read" if book['read_status'] == 'read' else "Unread"}
                                                                                                                </span></p>
                                                                                                                </div>


                                                                                                                """, unsafe_allow_html=True)
                                                                                                                        elif search_term:
                                                                                                                            st.markdown("<div class='warning-message'>No results found.</div>", unsafe_allow_html=True)
                                                                                                                        elif st.session_state.current_view == "stats":
                                                                                                                                st.markdown("<h2 class='subheader'>Library Statistics</h2>", unsafe_allow_html=True)
                                                                                                                                if not st.session_state.library:
                                                                                                                                    st.markdown("<div class='warning-message'>Your library is empty. Please add books.</div>", unsafe_allow_html=True)
                                                                                                                                else:
                                                                                                                                    stats = get_library_stats()
                                                                                                                                    col1, col2 ,col3 = st.columns(3)
                                                                                                                                    with col1:
                                                                                                                                        st.metric("Total Books", stats['total_books'])
                                                                                                                                        with col2:
                                                                                                                                            st.metric("Read Books", stats['read_books'])
                                                                                                                                            with col3:
                                                                                                                                                st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")
                                                                                                                                                create_visualizations()
                                                                                                                                                
                                                                                                                                                if stats['author']:
                                                                                                                                                    st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
                                                                                                                                    top_authors = dict(list(stats['authors'].items())[:5])
                                                                                                                                    st.markdown(f"**{author}**: {count} books{'s' if count > 1 else ''}")
                                                                                                                                    
                                                                                                                                st.markdown("---")
                                                                                                                                st.markdown("copyright 2025 Zeba Khan. All rights reserved.", unsafe_allow_html=True)
                                                                                                                        
                                                                                        
                                                                                                                            
                                                                                                                                                                         
                            


                                
