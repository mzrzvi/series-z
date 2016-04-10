CREATE TABLE cities (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	investor_followers INTEGER NOT NULL, 
	popularity INTEGER NOT NULL, 
	num_companies INTEGER NOT NULL, 
	num_people INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE founders (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	angel_id INTEGER NOT NULL, 
	popularity INTEGER, 
	image_url VARCHAR, 
	bio VARCHAR, 
	rank INTEGER, 
	num_startups INTEGER, 
	city_name VARCHAR, 
	city_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(city_id) REFERENCES cities (id)
);
CREATE TABLE startups (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	location VARCHAR NOT NULL, 
	popularity INTEGER NOT NULL, 
	market VARCHAR NOT NULL, 
	num_founders INTEGER NOT NULL, 
	product_desc VARCHAR, 
	company_url VARCHAR, 
	logo_url VARCHAR, 
	city_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(city_id) REFERENCES cities (id)
);
CREATE TABLE startup_to_founder (
	startup_id INTEGER NOT NULL, 
	founder_id INTEGER NOT NULL, 
	PRIMARY KEY (startup_id, founder_id), 
	FOREIGN KEY(startup_id) REFERENCES startups (id), 
	FOREIGN KEY(founder_id) REFERENCES founders (id)
);
