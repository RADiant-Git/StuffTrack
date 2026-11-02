-- Включение строгого контроля внешних ключей в SQLite
PRAGMA foreign_keys = ON;

-- ========================================================
-- 1. Удаление таблиц в обратном порядке связей
-- ========================================================
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS departments;

-- ========================================================
-- 2. Таблицы-справочники (не зависят от других таблиц)
-- ========================================================

-- Должности
CREATE TABLE positions (
    position_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL UNIQUE,
    base_salary   INTEGER NOT NULL CHECK (base_salary >= 0),
    requirements  TEXT
);

-- Подразделения / Отделы
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    description   TEXT
);

-- Роли пользователей
CREATE TABLE roles (
    role_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    description   TEXT
);

-- ========================================================
-- 3. Пользователи и Сотрудники
-- ========================================================

-- Учётные записи пользователей
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    role_id       INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE RESTRICT
);

-- Карточки сотрудников
CREATE TABLE employees (
    employee_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name           TEXT NOT NULL,
    phone               TEXT NOT NULL UNIQUE,
    email               TEXT UNIQUE,
    status              TEXT NOT NULL DEFAULT 'активен' CHECK (status IN ('активен', 'в отпуске', 'уволен')),
    hire_date           TEXT NOT NULL, -- В SQLite даты хранятся в формате YYYY-MM-DD (TEXT)
    department_id       INTEGER,
    current_position_id INTEGER,
    user_id             INTEGER UNIQUE, -- Ограничение UNIQUE обеспечивает связь 1:1
    FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE SET NULL,
    FOREIGN KEY (current_position_id) REFERENCES positions (position_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL
);

-- ========================================================
-- 4. Журнал назначений и перемещений (Связь M:N)
-- ========================================================

CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date    TEXT NOT NULL,
    end_date      TEXT,          -- NULL, если должность занимает сейчас
    notes         TEXT,
    employee_id   INTEGER NOT NULL,
    position_id   INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions (position_id) ON DELETE RESTRICT
);

-- ========================================================
-- 5. Начальные тестовые данные (для выполнения п. 2.3 лабы)
-- ========================================================

-- Роли
INSERT INTO roles (name, description) VALUES
('Администратор', 'Полный доступ к редактированию штата и пользователей (RW)'),
('Сотрудник', 'Просмотр контактов и справочника должностей (RO)');

-- Должности
INSERT INTO positions (title, base_salary, requirements) VALUES
('Младший разработчик', 65000, 'Python, базовый SQL, Git'),
('Ведущий разработчик', 160000, 'Опыт от 3 лет, архитектура БД, руководство командой'),
('HR-менеджер', 55000, 'Кадровое делопроизводство, ТК РФ');

-- Отделы
INSERT INTO departments (name, description) VALUES
('Отдел разработки', 'Создание и развитие IT-продуктов компании'),
('Отдел кадров', 'Рекрутинг и ведение кадровой документации');

-- Пользователи
INSERT INTO users (username, password_hash, is_active, role_id) VALUES
('admin_varya', '$2b$12$e8AdminHashExampleValueString123', 1, 1),
('dev_anatolii',   '$2b$12$e8UserHashExampleValueString456',  1, 2);

-- Сотрудники
INSERT INTO employees (full_name, phone, email, status, hire_date, department_id, current_position_id, user_id) VALUES
('Смирнова Елена Сергеевна', '+7-910-111-22-33', 'smirnova@company.local', 'активен', '2023-03-01 09:00:00', 2, 3, 1),
('Иванов Алексей Павлович',  '+7-920-222-33-44', 'ivanov@company.local',   'активен', '2024-01-15 10:00:00', 1, 2, 2);

-- История назначений (M:N)
INSERT INTO assignments (start_date, end_date, notes, employee_id, position_id) VALUES
('2023-03-01', NULL, 'Приказ о приёме на должность HR-менеджера', 1, 3),
('2024-01-15', '2024-06-01', 'Принят на должность Младшего разработчика', 2, 1),
('2024-06-01', NULL, 'Успешное прохождение испытательного срока, перевод на должность Ведущего разработчика', 2, 2);