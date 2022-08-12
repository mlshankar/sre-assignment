create database test;

use test;

DROP TABLE IF EXISTS `city_population`;
CREATE TABLE `city_population`
(
    `id`                bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `city_name`         varchar(128) COLLATE utf8_unicode_ci NOT NULL,
    `population`        bigint(20) unsigned NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_unicode_ci;
