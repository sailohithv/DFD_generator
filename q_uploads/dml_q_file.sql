INSERT INTO final (
F1,
F2,
F3,
F4,
F5,
F6,
F7,
F8,
F9,
F10
)

SELECT

A_als.A1,
A_als.A2,
A_als.A3,
A_als.A4,
A_als.A5,
A_als.A6,
A_als.A7,
B_als.B1,
B_als.B2,
B_als.B3

FROM A as A_als
LEFT JOIN B as B_als
ON A_als.A1=B_als.B1;

INSERT INTO  A (

A1,
A2,
A3,
A4,
A5,
A6,
A7
)

SELECT

aa_als.aa1,
aa_als.aa2,
aa_als.aa3,
aa_als.aa4,
bb_als.bb1,
bb_als.bb2,
bb_als.bb3

FROM aa as aa_als
RIGHT JOIN bb as bb_als
ON aa_als.aa1=bb_als.bb2;

INSERT INTO aa (

aa1,
aa2,
aa3,
aa4,
aa5,
aa6,
aa7
)

SELECT

o_als.O1,
o_als.O2,
o_als.O3,
p_als.P1,
p_als.P2,
p_als.P3,
p_als.P4

FROM o as o_als
FULL OUTER JOIN p as p_als
ON o_als.O1=p_als.P1;


INSERT INTO p (

P1,
P2,
P3,
P4,

)

SELECT

hi_als.hi1,
hi_als.hi2,
h_als.h1
h_als.h2


FROM hi as hi_als
FULL OUTER JOIN h as h_als
ON hi_als.hi1=h_als.h2;




INSERT INTO bb (

bb1,
bb2,
bb3

)

SELECT

k_als.k1,
k_als.k2,
l_als.l1


FROM k as k_als
FULL JOIN l as l_als
ON k_als.k1=l_als.l1;


INSERT INTO h (
h1,
h2
)

SELECT

hey.hey1,
hey.hey2

FROM hey WHERE hey.hey1 >10 AND hey.hey2 is NULL;


CREATE TABLE o
(
o1 int(14),
o2 varchar(20),
o3 DATE DEFAULT '9999-01-01',
PRIMARY KEY ( o1 )
);

CREATE TABLE hi
(
h1 VARCHAR(255) NOT NULL,
h2 INT AUTO_INCREMENT,
h3 varchar(16) not null,
PRIMARY KEY ( h2 )
);

CREATE TABLE hey
(
hey1 int auto_increment not null,
hey2 varchar(32) not null,
hey3 varchar(16) not null,
PRIMARY KEY ( hey1 )
);

CREATE TABLE k
(
k1 varchar(4) not null,
k2 int(14),
k3 varchar(16) not null,
k4 DATE,
PRIMARY KEY ( k2 )
);

CREATE TABLE l
(
l1 varchar(4) not null,
l2 DATE,
l3 varchar(16) not null,
l4 int auto_increment not null,
PRIMARY KEY ( l4 )
);

INSERT INTO B (

c1,
c2,
d1
)

SELECT
c.c1,
c.c2,
d.d1

FROM c
JOIN d
ON c.k1=d.l1;


CREATE TABLE c
(
c1 int auto_increment not null,
c2 varchar(32),
c3 DATE DEFAULT '0000-01-01',
PRIMARY KEY ( c1 )
);

CREATE TABLE d
(
d1 int auto_increment not null,
d2 int(55),
d3 varchar(34),
PRIMARY KEY ( d1 )
);

