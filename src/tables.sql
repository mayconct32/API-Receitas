CREATE TABLE chef (
    chef_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    chef_name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash CHAR(97) NOT NULL,
    create_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE recipe (
    recipe_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    chef_id INTEGER NOT NULL,
    recipe_name VARCHAR(100) NOT NULL,
    description TEXT,
    prep_time time,
    posted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_url CHAR(130),
    FOREIGN KEY(chef_id)
    REFERENCES chef(chef_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE instruction (
    instruction_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY(recipe_id)
    REFERENCES recipe(recipe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE ingredient (
    ingredient_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    ingredient_name VARCHAR(100),
    quantity VARCHAR(30),
    FOREIGN KEY(recipe_id)
    REFERENCES recipe(recipe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


