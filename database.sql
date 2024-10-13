DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name varchar(255) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id bigint REFERENCES urls(id) NOT NULL,
    status_code varchar(255),
    h1 varchar(255),
    title varchar(255),
    description text,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);