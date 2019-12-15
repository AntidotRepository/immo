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
	energyEfficiency	CHAR(1),
	builtInKitchen		BOOLEAN,
	balcony				BOOLEAN,
	garden				BOOLEAN,
	lift				BOOLEAN,
	guestToilet			BOOLEAN,
	cellar				BOOLEAN,
	isBarrierFree		BOOLEAN,
	stillAvailable		BOOLEAN		NOT NULL,	-- Does it still on the website
	lastTimeView		DATE		NOT NULL	-- Last time it has been seen on the website
);

CREATE TABLE addresses
(
	appartment_id		INTEGER		PRIMARY KEY,
	street				CHAR(150),
	houseNumber			CHAR(10),
	latitude			REAL,
	longitude			REAL,
	preciseHouseNumber	BOOLEAN		NOT NULL,
	postCode			INTEGER		NOT NULL,
	city				CHAR(50)	NOT NULL,
	quarter				CHAR(50)	NOT NULL
);
