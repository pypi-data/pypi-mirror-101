DROP TABLE IF EXISTS project_threat_assigned_awarenessmeasure;
DROP TABLE IF EXISTS project_threat_awarenessmeasure;
DROP TABLE IF EXISTS project_threat_assigned_countermeasure;
DROP TABLE IF EXISTS project_threat_countermeasure;
DROP TABLE IF EXISTS project_threat_affected_employee_group;
DROP TABLE IF EXISTS employee_group;
DROP TABLE IF EXISTS project_threat;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE project (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  end_date TIMESTAMP
);

CREATE TABLE employee_group (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  project_id INTEGER NOT NULL,
  description TEXT,
  FOREIGN KEY (project_id) REFERENCES project (id)
);

CREATE TABLE project_threat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  priority INTEGER NOT NULL DEFAULT 10,
  description TEXT,
  project_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_date TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES project (id)
);

CREATE TABLE project_threat_affected_employee_group (
  threat_id INTEGER NOT NULL,
  employee_group_id INTEGER NOT NULL,
  FOREIGN KEY (threat_id) REFERENCES project_threat (id),
  FOREIGN KEY (employee_group_id) REFERENCES employee_group (id)
);

CREATE TABLE project_countermeasure (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  percentage_executed INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  project_id INTEGER NOT NULL,
  FOREIGN KEY (project_id) REFERENCES project (id)
);

CREATE TABLE project_threat_countermeasure (
  threat_id INTEGER NOT NULL,
  countermeasure_id INTEGER NOT NULL,
  FOREIGN KEY (threat_id) REFERENCES project_threat (id),
  FOREIGN KEY (countermeasure_id) REFERENCES project_countermeasure (id)
);

CREATE TABLE project_awarenessmeasure (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  percentage_executed INTEGER NOT NULL DEFAULT 0,
  needs_legal_attention INTEGER NOT NULL DEFAULT 0,
  legal_description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_date TIMESTAMP,
  project_id INTEGER NOT NULL,
  FOREIGN KEY (project_id) REFERENCES project (id)
);

CREATE TABLE project_threat_awarenessmeasure (
  threat_id INTEGER NOT NULL,
  awarenessmeasure_id INTEGER NOT NULL,
  FOREIGN KEY (threat_id) REFERENCES project_threat (id),
  FOREIGN KEY (awarenessmeasure_id) REFERENCES project_awarenessmeasure (id)
);

-- Default user admin:hackattack
INSERT INTO user (id, username, password) VALUES (1, 'admin', 'pbkdf2:sha256:150000$3mu9J5Qp$d9d22a4d16a1009ef749f584fcbf89b73cc5b24572d6c5cee4fd18a1afb360f4');