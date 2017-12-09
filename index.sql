create table bindex (
		id bigint(14) NOT NULL AUTO_INCREMENT,
		createtime datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
		idx bigint(14),
		PRIMARY KEY (id)
)

INSERT INTO bindex (createtime,idx) VALUES('2017-12-09 00:00:00',1000)