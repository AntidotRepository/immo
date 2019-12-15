CREATE TABLE offers
(
	id					INTEGER		PRIMARY KEY,
	modification 		DATE,
	creation			DATE,
	title				CHAR(150)	NOT NULL,
	privateOffer		BOOLEAN		NOT NULL,
	price				REAL		NOT NULL,
	livingSpace			REAL		NOT NULL,
	numberOfRooms		INTEGER		NOT NULL,
	energyPerfCert		BOOLEAN		NOT NULL,
	energyEfficiency	CHAR(1)		NOT NULL,
	builtInKitchen		BOOLEAN		NOT NULL,
	balcony				BOOLEAN		NOT NULL,
	garden				BOOLEAN		NOT NULL,
	lift				BOOLEAN		NOT NULL,
	guestToilet			BOOLEAN		NOT NULL,
	cellar				BOOLEAN		NOT NULL,
	isBarrierFree		BOOLEAN		NOT NULL
);

CREATE TABLE addresses
(
	street				CHAR(150),
	houseNumber			CHAR(10),
	latitude			REAL,
	longitude			REAL,
	preciseHouseNumber	BOOLEAN		NOT NULL,
	postCode			INTEGER		NOT NULL,
	city				CHAR(50)	NOT NULL,
	quater				CHAR(50)	NOT NULL
);
