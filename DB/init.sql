CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    ranking INT UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    rating DECIMAL(2, 1) CHECK (rating >= 0 AND rating <= 10),
    age_rating INT CHECK (age_rating >= 1 AND age_rating <= 14),
    run_time INT CHECK (run_time > 0),
    tagline VARCHAR(255),
    budget BIGINT CHECK (budget >= 0),
    box_office BIGINT CHECK (box_office >= 0)
);

CREATE TABLE IF NOT EXISTS genres (
    movie_id INT NOT NULL,
    genre int CHECK (genre >= 1 AND genre <= 21) NOT NULL,
    PRIMARY KEY (movie_id, genre),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS staff (
    id SERIAL PRIMARY KEY,
    staff_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS movie_staff (
    movie_id INT NOT NULL,
    staff_id INT NOT NULL,
    staff_role INT NOT NULL CHECK (staff_role IN (1, 2, 3)),
    PRIMARY KEY (movie_id, staff_role, staff_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(id) 
);