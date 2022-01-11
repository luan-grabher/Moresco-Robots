DROP TABLE "calls";
CREATE TABLE "calls" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"robot" INTEGER,"user" varchar(255),"created_at" datetime,"started_at" datetime,"ended_at" datetime,"json_parameters" text,"json_return" text,"status" varchar(255));

DROP TABLE "robots";
CREATE TABLE "robots" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" varchar(255),
	"path" varchar(255),
	"description" text, 
	"enterprise" varchar(255), 
	"department" varchar(255), 
	"with_parameters_file" INTEGER
);

DROP TABLE "robots_parameters";
CREATE TABLE "robots_parameters" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"name" varchar(255),"type" varchar(255),"parameter_name" varchar(255),"robot" INTEGER,"default_value" varchar(255),"help" varchar(255));


INSERT INTO "robots" ("id", "name", "path", "description", "enterprise", "department", "with_parameters_file") VALUES
('1', 'Teste Py', 'C:/Users/Administrador/Documents/Projetos/Moresco/Moresco-Robots/test.py', 'haloooo', 'Nenhuma', 'Nenhum', NULL);

INSERT INTO "robots_parameters" ("id", "name", "type", "parameter_name", "robot", "default_value", "help") VALUES
(1, 'mes', 'int', NULL, 1, '6', NULL),
(2, 'ano', 'int', NULL, 1, '2022', NULL),
(3, 'ini', 'string', NULL, 1, 'ini.ini', NULL),
(4, 'outro', 'boolean', 'bool', 1, '1', NULL);
