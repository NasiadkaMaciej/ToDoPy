# Python Task Manager

Manage your tasks with this simple command-line task manager written in Python. Keep track of both global and local tasks with different priorities. It's based on my older program, written in C, [ToDo](https://github.com/NasiadkaMaciej/ToDo)

![App screenshot](https://nasiadka.pl/projects/ToDoPy/ToDoPy.png)

## Features

- Add global or local tasks
- Set task priorities
- Remove tasks by task ID
- Search for tasks by keyword
- View all tasks or specific task lists

## Getting Started

### Prerequisites

- Linux
- Python 3.x

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/NasiadkaMaciej/ToDoPy
    ```

2. Navigate to the project directory:

    ```bash
    cd ToDoPy
    ```

3. Run the task manager:

    ```bash
    python ToDo.py
    ```

## Usage

### Add a Global Task

```bash
python task_manager.py -ag "Complete project report" -p 2
```

### Add a Local Task

```bash
python task_manager.py -al "Prepare presentation slides" -p 1
```

### Remove a Global Task

```bash
python task_manager.py -rg 1
```

### Remove a Local Task

```bash
python task_manager.py -rl 2
```

### Search for a Task

```bash
python task_manager.py -s "presentation"
```

### View All Tasks

```bash
python task_manager.py -l
```

### View Local Tasks Only

```bash
python task_manager.py -ll
```