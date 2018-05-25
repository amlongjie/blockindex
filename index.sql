create table bindex (
		id bigint(14) NOT NULL AUTO_INCREMENT,
		createtime datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
		idx bigint(14),
		PRIMARY KEY (id)
);

INSERT INTO bindex (createtime,idx) VALUES('2017-12-09 00:00:00',1000);


CREATE TABLE `otc_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `otc_buy` int(11) NOT NULL DEFAULT '0',
  `otc_sell` int(11) NOT NULL DEFAULT '0',
  `real_price` int(11) NOT NULL DEFAULT '0',
  `minute_money_in` int(11) NOT NULL DEFAULT '0',
  `hour_money_in` int(11) NOT NULL DEFAULT '0',
  `day_money_in` int(11) NOT NULL DEFAULT '0',
  `week_money_in` int(11) NOT NULL DEFAULT '0',
  `token` char(3) NOT NULL DEFAULT '',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=889 DEFAULT CHARSET=utf8