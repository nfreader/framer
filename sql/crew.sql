CREATE TABLE crew (
  id  INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname  TEXT NOT NULL,
  rank  TEXT NOT NULL DEFAULT 'Assistant',
  assignment  INTEGER,
  FOREIGN KEY (assignment) REFERENCES station (id)
)