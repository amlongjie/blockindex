CREATE TABLE bindex (
  id         BIGINT(14) NOT NULL AUTO_INCREMENT,
  createtime DATETIME   NOT NULL DEFAULT '1970-01-01 00:00:00',
  idx        BIGINT(14),
  PRIMARY KEY (id)
);

INSERT INTO bindex (createtime, idx) VALUES ('2017-12-09 00:00:00', 1000);


CREATE TABLE `otc_index` (
  `id`              INT(11)   NOT NULL AUTO_INCREMENT,
  `otc_buy`         INT(11)   NOT NULL DEFAULT '0',
  `otc_sell`        INT(11)   NOT NULL DEFAULT '0',
  `real_price`      INT(11)   NOT NULL DEFAULT '0',
  `minute_money_in` INT(11)   NOT NULL DEFAULT '0',
  `hour_money_in`   INT(11)   NOT NULL DEFAULT '0',
  `day_money_in`    INT(11)   NOT NULL DEFAULT '0',
  `week_money_in`   INT(11)   NOT NULL DEFAULT '0',
  `token`           CHAR(3)   NOT NULL DEFAULT '',
  `create_time`     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 889
  DEFAULT CHARSET = utf8;

CREATE TABLE `flag` (
  `id`          INT(11)   NOT NULL AUTO_INCREMENT,
  `flag`        INT       NOT NULL DEFAULT 0,
  `next`        INT       NOT NULL DEFAULT 0,
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 4857
  DEFAULT CHARSET = utf8