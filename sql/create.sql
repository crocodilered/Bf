

CREATE TABLE IF NOT EXISTS `calculation` (
  `calculation_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `params_template` text,
  `updated` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT 'Копия graph.updated',
  PRIMARY KEY (`calculation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='Тип рассчета';


CREATE TABLE `graph` (
	`graph_id` INT(11) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NULL DEFAULT NULL,
	`calculation_id` INT(11) NOT NULL,
	`params` TEXT NOT NULL,
	`finished` TINYINT(4) NULL DEFAULT '0',
	`created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`updated` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`graph_id`)
)
COMMENT='Список графиков'
COLLATE='utf8mb4_unicode_520_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

CREATE TABLE `data` (
	`data_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`graph_id` INT(11) NOT NULL,
	`point_x` DOUBLE NULL DEFAULT NULL,
	`point_y` DOUBLE NULL DEFAULT NULL,
	`image_mode` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`image_width` SMALLINT(5) UNSIGNED NULL DEFAULT NULL,
	`image_height` SMALLINT(5) UNSIGNED NULL DEFAULT NULL,
	`image_data` LONGBLOB NULL,
	`created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`data_id`),
	INDEX `data_graph_id` (`graph_id`)
)
COMMENT='Данные для графиков.'
COLLATE='utf8mb4_unicode_520_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;
