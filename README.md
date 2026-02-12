# English Mastery Vocabulary App

A comprehensive English vocabulary learning application built with Python and Flet.

## Features

- **Level-Based Learning**: Structured learning path with multiple difficulty levels (1-6).
- **Interactive Learning**: View English words, reveal translations, and track your progress.
- **Progress Tracking**: 
  - Save progress per level.
  - Resume from where you left off.
  - Reset progress to start over.
- **Difficult Words Review**: Automatically tracks words you struggle with and provides a dedicated review section.
- **Word Management**: 
  - Add, edit, and delete words.
  - Bulk delete functionality.
  - Import words from XLSX files.
- **User System**: Simple username-based login to track individual progress.
- **Dark Mode UI**: tailored for comfortable viewing.

## Prerequisites

- Python 3.7+

## Installation

1. Clone or download the repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

## Application Structure

- `main.py`: Entry point of the application. Handles routing and app initialization.
- `database.py`: Database management (SQLite) and data access layer.
- `views/`: Contains the UI logic for different screens:
  - `landing_view.py`: Login screen.
  - `dashboard_view.py`: Main dashboard with level selection.
  - `learning_view.py`: Flashcard interface for learning words.
  - `words_view.py`: Word management interface.
  - `difficult_words_view.py`: Interface for reviewing difficult words.
- `seed_data.py`: Script to populate the database with initial data.

## key Controls

- **Enter**: Reveal translation / Next word.
- **Backslash (\)**: Play audio pronunciation (if available).

