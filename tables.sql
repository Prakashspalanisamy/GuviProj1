create table Categories (category_id VARCHAR(50), category_name VARCHAR(100) not null, primary key (category_id) );


create table Competitions (competition_id VARCHAR(50), competition_name VARCHAR(100) not null, parent_id VARCHAR(50), type VARCHAR(20) not null, gender VARCHAR(10) not null, category_id VARCHAR(50), PRIMARY KEY (competition_id), FOREIGN KEY (category_id) REFERENCES Categories(category_id));



create table Complexes (complex_id VARCHAR(50), complex_name VARCHAR(100) not null, primary key (complex_id) );


create table Venues  (venue_id VARCHAR(50), venue_name VARCHAR(100) not null, city_name VARCHAR(100) not null, country_name VARCHAR(100) not null, country_code VARCHAR(3) not null, timezone VARCHAR(100) not null, complex_id VARCHAR(50), PRIMARY KEY (venue_id), FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id));



create table Competitors (competitor_id VARCHAR(50), name VARCHAR(100) not null, country VARCHAR(100) not null, country_code VARCHAR(3) not null, abbreviation VARCHAR(10) not null, primary key (competitor_id) );



create table Competitor_Rankings  (rank_id int AUTO_INCREMENT, rank int not null, movement int not null, points int not null, competitions_played int not null, gender VARCHAR(10), year int, week int, competitor_id VARCHAR(50), PRIMARY KEY (rank_id), FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id));

