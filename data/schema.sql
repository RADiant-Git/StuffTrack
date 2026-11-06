PRAGMA foreign_keys = ON;

-- Удаление таблиц
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS departments;

-- Справочник должностей
CREATE TABLE positions (
    position_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL UNIQUE,
    base_salary   INTEGER NOT NULL CHECK (base_salary >= 0),
    requirements  TEXT
);

-- Справочник отделов
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

-- Учётные записи
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
    email               TEXT NOT NULL UNIQUE,
    status              TEXT NOT NULL DEFAULT 'активен' CHECK (status IN ('активен', 'в отпуске', 'уволен')),
    hire_date           TEXT NOT NULL DEFAULT (datetime('now')),
    department_id       INTEGER,
    current_position_id INTEGER NOT NULL,
    user_id             INTEGER UNIQUE,
    FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE SET NULL,
    FOREIGN KEY (current_position_id) REFERENCES positions (position_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL
);

-- История назначений
CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id   INTEGER NOT NULL,
    position_id   INTEGER NOT NULL,
    start_date    TEXT NOT NULL DEFAULT (datetime('now')),
    end_date      TEXT,
    notes         TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions (position_id) ON DELETE RESTRICT
);

-- Индексы связей
CREATE INDEX idx_users_role_id ON users (role_id);
CREATE INDEX idx_employees_department_id ON employees (department_id);
CREATE INDEX idx_employees_position_id ON employees (current_position_id);
CREATE INDEX idx_assignments_employee_id ON assignments (employee_id);
CREATE INDEX idx_assignments_position_id ON assignments (position_id);

-- Начальные данные: роли
INSERT INTO roles (role_id, name, description) VALUES
(1, 'Администратор', 'Полный доступ к системе'),
(2, 'Сотрудник', 'Просмотр контактов и справочников');

-- Начальные данные: должности
INSERT INTO positions (position_id, title, base_salary, requirements) VALUES
(1, 'Младший разработчик', 65000, 'Python, базовый SQL, Git'),
(2, 'Ведущий разработчик', 160000, 'Опыт от 3 лет, архитектура БД'),
(3, 'HR-менеджер', 55000, 'Кадровое делопроизводство, ТК РФ');

-- Начальные данные: отделы
INSERT INTO departments (department_id, name, description) VALUES
(1, 'Отдел разработки', 'Разработка IT-продуктов компании'),
(2, 'Отдел кадров', 'Подбор и оформление персонала');

-- Начальные данные: пользователи
INSERT INTO users (user_id, username, password_hash, is_active, role_id) VALUES
(1, 'admin_varya', 'plain:admin123', 1, 1),
(2, 'dev_anatolii', 'plain:dev123', 1, 2);

-- Начальные данные: сотрудники
INSERT INTO employees (employee_id, full_name, phone, email, status, hire_date, department_id, current_position_id, user_id) VALUES
(1, 'Смирнова Елена Сергеевна', '79101112233', 'smirnova@company.local', 'активен', '2023-03-01 09:00:00', 2, 3, 1),
(2, 'Иванов Алексей Павлович',  '79202223344', 'ivanov@company.local',   'активен', '2024-01-15 10:00:00', 1, 2, 2);

-- Начальные данные: назначения
INSERT INTO assignments (start_date, end_date, notes, employee_id, position_id) VALUES
('2023-03-01 09:00:00', NULL, 'Приказ о приёме на работу', 1, 3),
('2024-01-15 10:00:00', '2024-06-01 10:00:00', 'Принят на должность', 2, 1),
('2024-06-01 10:00:00', NULL, 'Перевод на должность ведущего разработчика', 2, 2);