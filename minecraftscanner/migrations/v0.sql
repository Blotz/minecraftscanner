CREATE TABLE IF NOT EXISTS `meta` (
    version INTEGER PRIMARY KEY
);
INSERT INTO `meta` VALUES (-1);

CREATE TABLE IF NOT EXISTS `servers` (
    `ip` TEXT PRIMARY KEY,
    `previewsChat` BOOLEAN NOT NULL,
    `enforcesSecureChat` BOOLEAN NOT NULL,
    `onlinePlayers` INTEGER NOT NULL,
    `maxPlayers` INTEGER NOT NULL,
    `version` TEXT NOT NULL,
    `protocol` INTEGER NOT NULL,
    `description` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `players` (
    `uuid` TEXT PRIMARY KEY,
    `name` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `server_players` (
    `server` TEXT NOT NULL,
    `player` TEXT NOT NULL,
    PRIMARY KEY (`server`, `player`),
    FOREIGN KEY (`server`) REFERENCES `servers`(`ip`),
    FOREIGN KEY (`player`) REFERENCES `players`(`uuid`)
);

CREATE TABLE IF NOT EXISTS `modpacks` (
    `projectID` INT PRIMARY KEY,
    `name` TEXT NOT NULL,
    `version` TEXT NOT NULL,
    `versionID` INT NOT NULL,
    `isMetadata` BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS `server_modpacks` (
    `server` TEXT NOT NULL,
    `modpack` INT NOT NULL,
    PRIMARY KEY (`server`, `modpack`),
    FOREIGN KEY (`server`) REFERENCES `servers`(`ip`),
    FOREIGN KEY (`modpack`) REFERENCES `modpacks`(`projectID`)
);

CREATE TABLE IF NOT EXISTS `mods` (
    `modid` TEXT NOT NULL,
    `version` TEXT NOT NULL,
    PRIMARY KEY (`modid`, `version`)
);

CREATE TABLE IF NOT EXISTS `server_mods` (
    `server` TEXT NOT NULL,
    `mod` TEXT NOT NULL,
    `version` TEXT NOT NULL,
    PRIMARY KEY (`server`, `mod`),
    FOREIGN KEY (`server`) REFERENCES `servers`(`ip`),
    FOREIGN KEY (`mod`, `version`) REFERENCES `mods`(`modid`, `version`)
);

DELETE FROM `meta`;
INSERT INTO `meta` VALUES (0);